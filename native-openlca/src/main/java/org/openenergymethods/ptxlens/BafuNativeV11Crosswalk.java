package org.openenergymethods.ptxlens;

import java.io.File;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.security.MessageDigest;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.Locale;
import java.util.Set;
import java.util.zip.ZipFile;

import org.openlca.core.database.Derby;
import org.openlca.core.model.Process;
import org.openlca.core.model.FlowType;

/**
 * First-party native BAFU:2026 v1.1 QUANTITATIVE REFERENCE IDENTITY replay.
 *
 * Input database is the exact user-authorized ORIGINAL BAFU v1.1 .zolca;
 * never downloads Nexus files, publishes original manufacturing exchanges,
 * creates an LCIA result, or marks a process as an approved foreground
 * supplier. Separately generated v1 public OGD catalogue is only a lead.
 *
 * Run LOCALLY with allowed licence, original source, private new scratch db
 * directory, one UUID per line and private output TSV:
 *
 * mvn -ntp -f native-openlca/pom.xml compile exec:java \\
 *   -Dexec.mainClass=org.openenergymethods.ptxlens.BafuNativeV11Crosswalk \\
 *   -Dexec.args="/PRIVATE/BAFU-2026_v1.1_original.zolca /PRIVATE/EMPTY_new_DB \\
 *     /PRIVATE/bafu_v1_candidate_uuids.txt /PRIVATE/bafu_v11_native_reference_evidence.tsv"
 */
public final class BafuNativeV11Crosswalk {
    private static final String EXPECTED_SHA256 =
        "e63b7e7ef5cde04bfe1176a783a55b5f72e2b73f42c36632b6150af39d348c4c";
    private static final long EXPECTED_BYTES = 135424513L;
    private static final int EXPECTED_PROCESSES = 11947;
    private static final String FORMAT =
        "ptxlens.BAFU2026_original_v11_native_quantitative_reference_identity.v1";

    private static String sha(File original) throws Exception {
        MessageDigest digest=MessageDigest.getInstance("SHA-256");
        try(InputStream in=Files.newInputStream(original.toPath())) {
            byte[] chunk=new byte[1024*1024];
            int n;
            while((n=in.read(chunk))!=-1) digest.update(chunk,0,n);
        }
        return java.util.HexFormat.of().formatHex(digest.digest());
    }

    private static String clean(String value) {
        return value==null ? "NULL" :
            value.replace("\t"," ").replace("\n"," ").replace("\r"," ").strip();
    }

    private static Set<String> uuidList(Path file) throws Exception {
        if(!Files.isRegularFile(file) || Files.isSymbolicLink(file))
            throw new IllegalArgumentException("private candidate UUIDs file missing");
        var ids=new java.util.LinkedHashSet<String>();
        for(String line:Files.readAllLines(file,StandardCharsets.UTF_8)){
            String x=line.strip();
            if(x.isEmpty()) continue;
            if(!x.matches("[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"))
                throw new IllegalArgumentException("invalid process UUID in private candidate input");
            if(!ids.add(x))
                throw new IllegalArgumentException("duplicate public process candidate UUID");
            if(ids.size()>250) throw new IllegalArgumentException("unbounded candidate export");
        }
        if(ids.isEmpty())
            throw new IllegalArgumentException("cannot validate empty candidate set");
        return ids;
    }

    public static void main(String[] args) throws Exception {
        if(args.length!=4) throw new IllegalArgumentException(
            "usage: <ORIGINAL_v1.1.zolca> <NEW_PRIVATE_DB> <candidate_uuids.txt> <NEW_PRIVATE_TSV>");
        File source=Path.of(args[0]).toAbsolutePath().toFile();
        File dest=Path.of(args[1]).toAbsolutePath().toFile();
        Path candidates=Path.of(args[2]).toAbsolutePath();
        Path output=Path.of(args[3]).toAbsolutePath();

        if(!source.isFile() || !source.getName().toLowerCase(Locale.ROOT).endsWith(".zolca")
                || source.length()!=EXPECTED_BYTES)
            throw new IllegalArgumentException("the exact original BAFU:2026 v1.1 ZIP is required");
        if(dest.exists() || Files.exists(output) ||
                source.toPath().equals(output) || source.toPath().equals(candidates))
            throw new IllegalArgumentException("do not overwrite original BAFU or a research witness");
        String inputSHA=sha(source);
        if(!EXPECTED_SHA256.equals(inputSHA))
            throw new IllegalArgumentException("original BAFU:2026 v1.1 bytes changed");
        var ids=uuidList(candidates);
        try(ZipFile zip=new ZipFile(source)) {
            boolean service=false,log=false,segment=false;
            var en=zip.entries();
            while(en.hasMoreElements()){
                var item=en.nextElement();
                String p=item.getName().replace('\\','/');
                if(p.startsWith("/") || p.contains("../") || p.contains("\u0000"))
                    throw new IllegalArgumentException("unsafe original Derby archive");
                if(p.equals("service.properties")) service=true;
                if(p.startsWith("log/")) log=true;
                if(p.startsWith("seg0/")) segment=true;
            }
            if(!(service&&log&&segment)) throw new IllegalArgumentException(
                "expected ORIGINAL native Derby database, not an outer Nexus download ZIP");
        }

        Derby.unzip(dest,source);
        if(!Derby.isDerbyFolder(dest)) throw new IllegalStateException(
            "actual native original v1.1 Derby restore unsuccessful");
        StringBuilder lines=new StringBuilder();
        lines.append("schema_version\toriginal_zolca_SHA256\tprocess_UUID\tnative_process_found")
             .append("\tnative_process_name\tquantitative_flow_UUID\tquantitative_flow_name")
             .append("\tquantitative_ref_unit\tquantitative_ref_flow_type\n");
        int missing=0,verified=0;
        try(Derby db=new Derby(dest)) {
            int count=db.getDescriptors(Process.class).size();
            if(count!=EXPECTED_PROCESSES)
                throw new IllegalStateException("native BAFU process count not expected 11947");
            for(String id:ids) {
                var process=db.get(Process.class,id);
                if(process==null){
                    lines.append(FORMAT+"\t"+inputSHA+"\t"+id+"\tfalse\tNULL\tNULL\tNULL\tNULL\tNULL\n");
                    missing++;
                    continue;
                }
                var reference=process.quantitativeReference;
                if(reference==null || reference.flow==null || reference.unit==null ||
                   reference.flow.refId==null || reference.flow.name==null)
                    throw new IllegalStateException(
                        "native BAFU process missing quantitative reference identity: "+id);
                lines.append(FORMAT+"\t"+inputSHA+"\t"+id+"\ttrue\t")
                     .append(clean(process.name)).append("\t")
                     .append(reference.flow.refId).append("\t")
                     .append(clean(reference.flow.name)).append("\t")
                     .append(clean(reference.unit.name)).append("\t")
                     .append(reference.flow.flowType==null ? "UNKNOWN" : reference.flow.flowType.name()).append("\n");
                verified++;
            }
        }
        if(output.getParent()!=null)Files.createDirectories(output.getParent());
        Files.writeString(output,lines.toString(),StandardCharsets.UTF_8);
        System.out.println("PTXLENS_BAFU_V11_ORIGINAL_SHA_VERIFIED\t"+inputSHA);
        System.out.println("PTXLENS_BAFU_V11_NATIVE_PROCESSES\t"+EXPECTED_PROCESSES);
        System.out.println("PTXLENS_BAFU_V11_NATIVE_CANDIDATES_FOUND\t"+verified);
        System.out.println("PTXLENS_BAFU_V11_NATIVE_CANDIDATES_NOT_PRESENT\t"+missing);
        System.out.println("PTXLENS_BAFU_V11_NAMED_PROVIDERS_APPROVED\t0");
        System.out.println("PTXLENS_BAFU_V11_OEM_BOM_AND_SYSTEM_GWP_COMPLETE\tfalse");
    }
}
