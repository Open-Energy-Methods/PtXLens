package org.openenergymethods.ptxlens;

import java.io.File;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.Locale;
import java.util.Set;
import java.util.zip.ZipFile;

import org.openlca.core.database.Derby;
import org.openlca.core.matrix.ProductSystemBuilder;
import org.openlca.core.matrix.linking.LinkingConfig;
import org.openlca.core.model.FlowType;
import org.openlca.core.model.ImpactMethod;
import org.openlca.core.model.Process;

/**
 * Audit a legally obtained *original* BAFU:2026 v1 .zolca database.
 *
 * Never calls Nexus, accepts third-party terms, rewrites source inventories,
 * modifies an existing database, or claims that online process-level pre-
 * calculated GWP figures are the result of this native supplier graph.
 *
 * Usage (only after end user downloaded Nexus BAFU:2026 v1 under its terms):
 * mvn -f native-openlca/pom.xml -Dexec.mainClass=...BafuZolcaAudit
 *     -Dexec.args="/private/BAFU_2026_v1.zolca /tmp/ptxlens_bafu_clean" compile exec:java
 */
public final class BafuZolcaAudit {
    private static final String H2_PEM_30_BAR_CH = "99a1af16-58cd-3f11-a877-c43d3c8e5d78";
    private static final String NL_GRID = "437a439d-1994-3496-b51f-23868b6987aa";
    private static final String NL_DEIONISED_WATER = "64b93c35-a87c-33d3-8983-01a8c951d462";
    private static final String RER_STEEL_18_8 = "fc9385f8-fe2d-3399-b663-4b66e5062a3f";
    private static final String RER_ALUMINIUM_PRIMARY = "5cac9857-21f7-305d-b705-c83a02a94e6e";
    private static final String RER_COPPER = "3972eb0c-d60e-3537-9ad1-fd6b7bbafce8";
    private static final String GLO_IRIDIUM = "8a6c655d-b743-3945-a1a6-e070f70c48b2";
    private static final String RER_NAFION_MEMBRANE = "e8610445-cb47-3f69-8bd9-d2d580fd8e45";
    private static final String SOURCE_CITATION = "Database of the Swiss Federal Administration, BAFU:2026, Federal Office for the Environment, 2026";

    public static void main(String[] args) throws Exception {
        if (args.length != 2)
            throw new IllegalArgumentException("usage: <authorized-original-BAFU2026.zolca> <new-private-DB-folder>");
        File source = Path.of(args[0]).toAbsolutePath().toFile();
        File dest = Path.of(args[1]).toAbsolutePath().toFile();
        if (!source.isFile() || !source.getName().toLowerCase(Locale.ROOT).endsWith(".zolca"))
            throw new IllegalArgumentException("Must supply a locally obtained original BAFU .zolca");
        if (dest.exists())
            throw new IllegalArgumentException("Will not open, alter, or overwrite an existing database folder");
        try (ZipFile check = new ZipFile(source)) {
            if (check.size() < 50)
                throw new IllegalArgumentException("Suspiciously small BAFU backup");
            boolean hasService = false, hasLog = false, hasSegments = false;
            var entries = check.entries();
            while (entries.hasMoreElements()) {
                var zipEntry = entries.nextElement();
                String path = zipEntry.getName().replace('\\','/');
                if (path.startsWith("/") || path.contains("../") || path.equals("..") || path.contains("\u0000"))
                    throw new IllegalArgumentException("Unsafe BAFU backup path: " + path);
                if (path.equals("service.properties")) hasService = true;
                if (path.startsWith("log/")) hasLog = true;
                if (path.startsWith("seg0/")) hasSegments = true;
            }
            if (!(hasService && hasLog && hasSegments))
                throw new IllegalArgumentException("Not a direct native openLCA Derby .zolca: unpack outer Nexus ZIP first");
        }
        System.out.println("PTXLENS_NATIVE_BAFU_ORIGINAL_SOURCE\t" + SOURCE_CITATION);
        Derby.unzip(dest, source); // GreenDelta's real .zolca restore, no artificial data.
        if (!Derby.isDerbyFolder(dest))
            throw new IllegalStateException("Restored file is not a native openLCA Derby database");
        try (Derby db = new Derby(dest)) {
            var descs = db.getDescriptors(Process.class);
            System.out.println("PTXLENS_NATIVE_BAFU_PROCESS_COUNT\t" + descs.size());
            if (descs.size() < 11_000)
                throw new IllegalStateException("Too few actual BAFU processes; verify Nexus 2026 v1 edition");
            for (String uuid : new String[]{
                    H2_PEM_30_BAR_CH, NL_GRID, NL_DEIONISED_WATER,
                    RER_STEEL_18_8, RER_ALUMINIUM_PRIMARY, RER_COPPER,
                    GLO_IRIDIUM, RER_NAFION_MEMBRANE}) {
                var p = db.get(Process.class, uuid);
                if (p == null)
                    throw new IllegalStateException("Required real BAFU provider process UUID absent: " + uuid);
                if (p.quantitativeReference == null || p.quantitativeReference.flow == null)
                    throw new IllegalStateException("Source process quantitative reference absent: " + uuid);
                var ref = p.quantitativeReference;
                System.out.println("PTXLENS_REAL_BAFU_PROCESS\t" + uuid
                    + "\t" + p.name.replace('\t',' ')
                    + "\t" + ref.flow.name.replace('\t',' ')
                    + "\t" + (ref.unit == null ? "MISSING_UNIT" : ref.unit.name));
            }
            var methodDescriptors = db.getDescriptors(ImpactMethod.class);
            System.out.println("PTXLENS_NATIVE_BAFU_METHOD_COUNT\t" + methodDescriptors.size());
            for (var method : methodDescriptors)
                System.out.println("PTXLENS_REAL_BAFU_LCIA_METHOD\t" + method.name.replace('\t',' '));

            var foreground = db.get(Process.class,H2_PEM_30_BAR_CH);
            for (var input : foreground.exchanges) {
                if (!input.isInput || input.flow==null)
                    continue;
                var provider = input.defaultProviderId>0
                      ? db.get(Process.class,input.defaultProviderId):null;
                System.out.println("PTXLENS_REAL_PEM30_BAR_INPUT\t"
                    + input.flow.name.replace('\t',' ')
                    + "\t" + input.amount
                    + "\t" + (input.unit==null?"UNKNOWN":input.unit.name)
                    + "\t" + (provider==null?"NOT_EXPLICITLY_LINKED":provider.name.replace('\t',' ')));
            }

            var linker=new LinkingConfig().preferredType(LinkingConfig.PreferredType.UNIT_PROCESS);
            var system=new ProductSystemBuilder(db,linker).build(foreground);
            if (system==null || system.referenceExchange==null)
                throw new IllegalStateException("Cannot construct original BAFU 30bar PEM product system");
            var linkSet = new HashSet<Long>();
            for (var x : system.processLinks)
                linkSet.add(x.exchangeId);
            int unlinkedProduct=0;
            int unlinkedWaste=0;
            for (var id : system.processes) {
                var p=db.get(Process.class,id);
                if (p==null)throw new IllegalStateException("Native BAFU supplier process absent");
                for (var x : p.exchanges) {
                    if (x.flow==null || Math.abs(x.amount)<1e-12)continue;
                    if (x.isInput && x.flow.flowType==FlowType.PRODUCT_FLOW
                            && !linkSet.contains(x.id))unlinkedProduct++;
                    if (!x.isInput && x.flow.flowType==FlowType.WASTE_FLOW
                            && !linkSet.contains(x.id))unlinkedWaste++;
                }
            }
            System.out.println("PTXLENS_NATIVE_BAFU_AUTO_LINKED_PROCESSES\t" + system.processes.size());
            System.out.println("PTXLENS_NATIVE_BAFU_AUTO_LINKED_EXCHANGES\t" + system.processLinks.size());
            System.out.println("PTXLENS_NATIVE_BAFU_UNLINKED_PRODUCT_INPUTS\t" + unlinkedProduct);
            System.out.println("PTXLENS_NATIVE_BAFU_UNLINKED_WASTE_OUTPUTS\t" + unlinkedWaste);
            System.out.println("PTXLENS_NATIVE_BAFU_COMPLETE_UPSTREAM_CLOSURE\t"
                + (unlinkedProduct==0&&unlinkedWaste==0));
            System.out.println("PTXLENS_NL_2023_SCENARIO_ADAPTED\tfalse");
            System.out.println("PTXLENS_FULL_CRADLE_TO_GATE_CLAIM\tfalse");
        }
    }
}
