package org.openenergymethods.ptxlens;

import java.io.File;
import java.nio.file.Path;
import java.util.Locale;
import java.util.HashSet;
import java.util.ArrayList;
import org.openlca.core.model.FlowType;

import org.openlca.core.database.Derby;
import org.openlca.core.math.SystemCalculator;
import org.openlca.core.matrix.ProductSystemBuilder;
import org.openlca.core.matrix.linking.LinkingConfig;
import org.openlca.core.model.CalculationSetup;
import org.openlca.core.model.ImpactMethod;
import org.openlca.core.model.Process;
import org.openlca.jsonld.ZipStore;
import org.openlca.jsonld.input.JsonImport;

/**
 * Executes the *real* openLCA 2.7.0 Java database importer and calculation
 * kernel on an unchanged, SHA-verified Federal LCA Commons 2026 archive.
 *
 * IMPORTANT: Missing upstream providers are a known blocker. This emits a
 * diagnostic NATIVE_ENGINE result, never asserts cradle-to-gate completeness.
 * The USLCI 2017 1kg H2 record is not the NL 2023 PtXFlex/PyNEXUS plant.
 */
public final class DiagnosticNativeCalculation {

    static final String PEM_PROCESS = "f00a298a-295f-4fbc-b463-45f8e96f018b";
    static final String IPCC_METHOD = "00feb6d9-9282-3bcf-9d18-7b040f516935";
    static final String AR6_CATEGORY = "AR6-100";

    public static void main(String[] args) throws Exception {
        if (args.length != 2)
            throw new IllegalArgumentException("usage: <original-jsonld-zip> <scratch-Derby-folder>");
        File zip = Path.of(args[0]).toAbsolutePath().toFile();
        File databaseFolder = Path.of(args[1]).toAbsolutePath().toFile();
        if (!zip.isFile())
            throw new IllegalArgumentException("Original Commons archive not found");
        if (databaseFolder.exists())
            throw new IllegalArgumentException("Refusing to modify existing openLCA database");

        System.out.println("PTXLENS_NATIVE_ENGINE_VERSION\topenLCA-core-2.7.0");
        System.out.println("PTXLENS_NATIVE_INPUT\toriginal unmodified 2026 Commons Merged JSON-LD");
        try (Derby db = new Derby(databaseFolder)) {
            try (ZipStore store = ZipStore.open(zip)) {
                System.out.println("PTXLENS_NATIVE_IMPORT_STARTED");
                new JsonImport(store, db).run();
            }
            var processCount = db.getDescriptors(Process.class).size();
            System.out.println("PTXLENS_NATIVE_IMPORTED_PROCESS_COUNT\t" + processCount);
            if (processCount < 2000)
                throw new IllegalStateException("Not a full real Commons source import");

            Process source = db.get(Process.class, PEM_PROCESS);
            ImpactMethod method = db.get(ImpactMethod.class, IPCC_METHOD);
            if (source == null || method == null)
                throw new IllegalStateException("Published USLCI hydrogen process or IPCC method missing");

            var linker = new LinkingConfig()
                .preferredType(LinkingConfig.PreferredType.UNIT_PROCESS);
            var system = new ProductSystemBuilder(db, linker).build(source);
            if (system == null || system.referenceProcess == null || system.referenceExchange == null)
                throw new IllegalStateException("Failed to construct native product system");
            System.out.println("PTXLENS_NATIVE_LINK_COUNT\t" + system.processLinks.size());
            System.out.println("PTXLENS_NATIVE_PROCESS_COUNT\t" + system.processes.size());

            // Evaluate the actual native auto-linked system, not only the
            // JSON-LD default-provider fields. Unlinked product-inputs are
            // an explicit research completeness blocker, not zero impacts.
            var actualLinks = new HashSet<Long>();
            for (var link : system.processLinks) {
                actualLinks.add(link.exchangeId);
            }
            var missingInputs = new ArrayList<String>();
            for (var processId : system.processes) {
                var participating = db.get(Process.class, processId);
                if (participating == null)
                    throw new IllegalStateException("Missing process inside native system");
                for (var exchange : participating.exchanges) {
                    if (!exchange.isInput || exchange.flow == null ||
                            exchange.flow.flowType != FlowType.PRODUCT_FLOW ||
                            Math.abs(exchange.amount) < 1e-12)
                        continue;
                    if (!actualLinks.contains(exchange.id)) {
                        missingInputs.add(participating.name + " / " +
                                exchange.flow.name + " [" + exchange.flow.refId + "]");
                    }
                }
            }
            System.out.println("PTXLENS_NATIVE_UNLINKED_PRODUCT_INPUT_COUNT\t" + missingInputs.size());
            for (var i = 0; i < Math.min(15, missingInputs.size()); i++)
                System.out.println("PTXLENS_NATIVE_MISSING_PRODUCT_INPUT\t" + missingInputs.get(i));


            CalculationSetup setup = CalculationSetup.of(system)
                .withImpactMethod(method)
                .withAmount(1.0);
            var result = new SystemCalculator(db).calculate(setup);
            try {
                if (!result.hasImpacts())
                    throw new IllegalStateException("Native engine returned no impacts");
                boolean found = false;
                for (var impact : result.getTotalImpacts()) {
                    if (AR6_CATEGORY.equals(impact.impact().name)) {
                        if (!Double.isFinite(impact.value()))
                            throw new IllegalStateException("Nonfinite native GWP");
                        System.out.println("PTXLENS_NATIVE_AR6_100_KG_CO2E_PER_KG_US_REFERENCE_H2\t"
                                + String.format(Locale.ROOT, "%.12g", impact.value()));
                        found = true;
                    }
                }
                if (!found)
                    throw new IllegalStateException("IPCC AR6-100 not returned by real native engine");
            } finally {
                result.dispose();
            }
        }
        System.out.println("PTXLENS_LCA_SCIENTIFIC_COMPLETENESS\tINCOMPLETE_UPSTREAM_PROVIDERS");
        System.out.println("PTXLENS_LCA_CLAIM\tDIAGNOSTIC_US_2017_ONLY_NOT_DUTCH_CRADLE_TO_GATE");
    }
}
