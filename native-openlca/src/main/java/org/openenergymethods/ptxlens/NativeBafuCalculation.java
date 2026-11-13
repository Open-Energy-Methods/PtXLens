package org.openenergymethods.ptxlens;

import java.io.File;
import java.nio.file.Path;
import java.util.Locale;

import org.openlca.core.database.Derby;
import org.openlca.core.math.SystemCalculator;
import org.openlca.core.matrix.ProductSystemBuilder;
import org.openlca.core.matrix.linking.LinkingConfig;
import org.openlca.core.model.CalculationSetup;
import org.openlca.core.model.FlowType;
import org.openlca.core.model.ImpactMethod;
import org.openlca.core.model.Process;

/** Native GreenDelta BAFU:2026 LCIA using the user's PRIVATE restored database.
 *
 * Unlike an API precomputed factor, this executes the actual BAFU 1.1 unit
 * process matrix and IPCC 2021 GWP100 method. Does not alter original flows.
 *
 * Usage: <existing BAFU private DERBY directory> [original reference UUID]
 * IMPORTANT: a reference Swiss 30bar PEM H2 result is not automatically a
 * complete or geographically representative Dutch 2023 PtXLens scenario.
 */
public final class NativeBafuCalculation {
    private static final String H2_30_BAR_CH = "99a1af16-58cd-3f11-a877-c43d3c8e5d78";
    private static final String METHOD_NAME = "IPCC 2021";
    private static final String GWP_CATEGORY = "GWP 100";

    public static void main(String[] args) throws Exception {
        if (args.length < 1 || args.length > 2)
            throw new IllegalArgumentException("usage: <existing-private-BAFU-Derby-directory> [actual BAFU process uuid]");
        File folder=Path.of(args[0]).toAbsolutePath().toFile();
        if (!Derby.isDerbyFolder(folder))
            throw new IllegalArgumentException("provided folder is not a restored native openLCA Derby database");
        String processUuid = args.length==2 ? args[1] : H2_30_BAR_CH;

        try (var db = new Derby(folder)) {
            if (db.getDescriptors(Process.class).size() < 11000)
                throw new IllegalStateException("not an original complete BAFU:2026 database");
            var source=db.get(Process.class, processUuid);
            if (source==null || source.quantitativeReference==null)
                throw new IllegalStateException("original source reference process absent: "+processUuid);
            ImpactMethod method=null;
            for (var descriptor:db.getDescriptors(ImpactMethod.class)) {
                if (METHOD_NAME.equals(descriptor.name)) {
                    if (method != null)
                        throw new IllegalStateException("ambiguous native IPCC 2021 method name");
                    method=db.get(ImpactMethod.class,descriptor.id);
                }
            }
            if (method == null)
                throw new IllegalStateException("native BAFU IPCC 2021 method absent");

            var linker=new LinkingConfig()
                .preferredType(LinkingConfig.PreferredType.UNIT_PROCESS);
            var productSystem=new ProductSystemBuilder(db,linker).build(source);
            if (productSystem==null || productSystem.referenceExchange==null)
                throw new IllegalStateException("unable to construct native original BAFU product system");
            var linked = new java.util.HashSet<Long>();
            for (var link:productSystem.processLinks)
                linked.add(link.exchangeId);
            int unlinkedProduct=0, unlinkedWaste=0;
            for (var id:productSystem.processes) {
                var process=db.get(Process.class,id);
                if(process==null)
                    throw new IllegalStateException("null linked source process");
                for(var e:process.exchanges) {
                    if(e.flow==null || Math.abs(e.amount)<1e-12)
                        continue;
                    if(e.isInput && e.flow.flowType==FlowType.PRODUCT_FLOW
                        && !linked.contains(e.id)) unlinkedProduct++;
                    if(!e.isInput && e.flow.flowType==FlowType.WASTE_FLOW
                        && !linked.contains(e.id)) unlinkedWaste++;
                }
            }
            System.out.println("PTXLENS_NATIVE_BAFU_ORIGINAL_PROCESS_ID\t"+processUuid);
            System.out.println("PTXLENS_NATIVE_BAFU_PROCESS_NAME\t"+source.name.replace('\t',' '));
            System.out.println("PTXLENS_NATIVE_BAFU_REFERENCE_AMOUNT\t"+source.quantitativeReference.amount);
            System.out.println("PTXLENS_NATIVE_BAFU_REFERENCE_UNIT\t"+source.quantitativeReference.unit.name);
            System.out.println("PTXLENS_NATIVE_BAFU_METHOD\t"+method.name);
            System.out.println("PTXLENS_NATIVE_BAFU_LINKED_PROCESSES\t"+productSystem.processes.size());
            System.out.println("PTXLENS_NATIVE_BAFU_LINKED_EXCHANGES\t"+productSystem.processLinks.size());
            System.out.println("PTXLENS_NATIVE_BAFU_UNLINKED_INPUTS\t"+unlinkedProduct);
            System.out.println("PTXLENS_NATIVE_BAFU_UNLINKED_WASTE\t"+unlinkedWaste);
            if(unlinkedProduct !=0 || unlinkedWaste !=0)
                throw new IllegalStateException("native supplier graph incomplete; do not calculate an apparent full footprint");

            var setup=CalculationSetup.of(productSystem)
                .withImpactMethod(method)
                .withAmount(1.0);
            var result=new SystemCalculator(db).calculate(setup);
            try {
                if(!result.hasImpacts())
                    throw new IllegalStateException("native engine did not produce impacts");
                boolean found=false;
                for(var impact:result.getTotalImpacts()) {
                    if(GWP_CATEGORY.equals(impact.impact().name)) {
                        double value=impact.value();
                        if (!Double.isFinite(value))
                            throw new IllegalStateException("nonfinite original native GWP100");
                        System.out.println("PTXLENS_NATIVE_BAFU_IPCC2021_GWP100_KGCO2E_PER_REFERENCE_UNIT\t"+
                           String.format(Locale.ROOT,"%.14g",value));
                        found=true;
                    }
                }
                if(!found)
                    throw new IllegalStateException("BAFU native IPCC 2021 method does not contain named GWP100 category");
            }finally{
                result.dispose();
            }
        }
        System.out.println("PTXLENS_NATIVE_BAFU_LCIA_STATUS\tEXECUTED_SOURCE_REFERENCE_LCIA");
        System.out.println("PTXLENS_NATIVE_BAFU_NL2023_E_ES_MODELLED\tfalse");
    }
}
