package org.openenergymethods.ptxlens;

import java.io.File;
import java.io.FileReader;
import java.nio.file.Path;
import java.util.HashSet;
import java.util.Locale;

import com.google.gson.JsonParser;
import org.openlca.core.database.Derby;
import org.openlca.core.database.ProcessDao;
import org.openlca.core.math.SystemCalculator;
import org.openlca.core.matrix.ProductSystemBuilder;
import org.openlca.core.matrix.linking.LinkingConfig;
import org.openlca.core.matrix.solvers.MatrixSolver;
import org.openlca.core.model.CalculationSetup;
import org.openlca.core.model.FlowType;
import org.openlca.core.model.ImpactMethod;
import org.openlca.core.model.Process;
import org.openlca.nativelib.Module;
import org.openlca.nativelib.NativeLib;

/**
 * Real GreenDelta openLCA native BAFU v1.1 calculation for E / E+S
 * electricity-substituted variants of the published Swiss 30-bar PEM H2
 * foreground. The v1.1 raw .zolca is always kept unaltered; input DB must be
 * an independent local scratch COPY of the original restored database.
 *
 * This scoped scenario includes the original 30bar PEM stack, BOP, water,
 * disposal and foreground emissions, but NOT the added E+S tank manufacturing,
 * storage compression and losses, physical Dutch H2 transport, modern turbine
 * vintage, nor measured plant validation. Therefore it must NOT be called the
 * complete E/E+S cradle-to-gate GWP.
 */
public final class NativeBafuDutchScenario {
    private static final String BASE_PROCESS="99a1af16-58cd-3f11-a877-c43d3c8e5d78";
    private static final String NL_GRID_LOW="53996c5d-bba0-3c62-a027-6624bf998d68";
    private static final String NL_DEIONIZED="64b93c35-a87c-33d3-8983-01a8c951d462";
    private static final String OFFSHORE_WIND_2MW="23f2cd16-32d3-3312-85c9-8095bfe6815c";
    private static final String NATIVE_GWP="IPCC 2021 GWP 100";

    private static void require(boolean ok,String why){
        if(!ok)throw new IllegalStateException(why);
    }

    private static Process exactSource(Derby db,String uuid,String name,String unit){
        Process p=db.get(Process.class,uuid);
        require(p!=null && p.quantitativeReference!=null && p.quantitativeReference.flow!=null,
                "source supplier unavailable "+uuid);
        require(name.equals(p.name), "source provider name mismatch "+uuid+" actual "+p.name);
        require(unit.equals(p.quantitativeReference.unit.name),
                "source provider unit mismatch "+uuid+" actual "+p.quantitativeReference.unit.name);
        return p;
    }

    private static ImpactMethod climateMethod(Derby db){
        ImpactMethod found=null;
        for(var d:db.getDescriptors(ImpactMethod.class)){
            if(!"IPCC 2021".equals(d.name))continue;
            require(found==null,"ambiguous named source impact methods");
            found=db.get(ImpactMethod.class,d.id);
        }
        require(found!=null,"named original source IPCC 2021 method missing");
        require(found.impactCategories.stream().anyMatch(c->NATIVE_GWP.equals(c.name)),
                "exact original native BAFU GWP100 category missing");
        return found;
    }

    private static void addInput(Process copy,Process supplier,double amount) {
        require(amount>0 && Double.isFinite(amount),"invalid original-source scenario amount");
        var e=copy.input(supplier.quantitativeReference.flow,amount);
        e.unit=supplier.quantitativeReference.unit;
        e.flowPropertyFactor=supplier.quantitativeReference.flowPropertyFactor;
        e.defaultProviderId=supplier.id;
    }

    private static void runCase(Derby db,ImpactMethod method,Process original,
                                Process grid,Process wind,Process water,
                                String caseId,String originalSha,double gridKwh,double windKwh,
                                double modeledH2Kg) {
        require(("E".equals(caseId) || "E_plus_S".equals(caseId)),
                "only original source E or E_plus_S allowed");
        require(originalSha.length()==64,"original source historical archive SHA missing");
        require(modeledH2Kg>0 && gridKwh>=0 && windKwh>=0,"unphysical source energy or denominator");
        var cloned=original.copy();
        require(cloned.id==0,"BAFU ProcessCopy was not a new process; do not mutate source");
        cloned.name="PtXLens 2023 NL original "+caseId+" -- modified BAFU 30bar PEM reference, scoped sensitivity";
        // Remove ONLY source grid-electricity and CH water technosphere inputs;
        // leave source stack manufacturing, original BOP and end of life intact.
        int changed=0;
        var it=cloned.exchanges.iterator();
        while(it.hasNext()){
            var e=it.next();
            if(!e.isInput || e.flow==null || e.flow.flowType!=FlowType.PRODUCT_FLOW)continue;
            if("Electricity, low voltage, at grid".equals(e.flow.name) &&
                Math.abs(e.amount-54)<1e-9){
                it.remove();changed++;continue;
            }
            if("Water, deionised, at plant".equals(e.flow.name) &&
                Math.abs(e.amount-14)<1e-9){
                it.remove();changed++;continue;
            }
        }
        require(changed==2,"BAFU source 54kWh grid / 14kg CH water exchanges not found exactly twice");
        addInput(cloned,grid,gridKwh);
        addInput(cloned,wind,windKwh);
        addInput(cloned,water,14.0);
        var dao=new ProcessDao(db);
        cloned=dao.insert(cloned);
        require(cloned!=null && cloned.id>0 && !cloned.refId.equals(original.refId),
                "native scenario did not create separate process UUID");

        var linker=new LinkingConfig()
              .preferredType(LinkingConfig.PreferredType.UNIT_PROCESS);
        var system=new ProductSystemBuilder(db,linker).build(cloned);
        require(system!=null && system.referenceProcess!=null && system.referenceExchange!=null,
                "native scenario product system missing");
        var refs=new HashSet<Long>();
        for(var p:system.processLinks) refs.add(p.exchangeId);
        int missingProduct=0,missingWaste=0;
        for(var id:system.processes){
            var p=db.get(Process.class,id);
            require(p!=null,"missing actual BAFU source process");
            for(var e:p.exchanges){
                if(e.flow==null || Math.abs(e.amount)<1e-12)continue;
                if(e.isInput && e.flow.flowType==FlowType.PRODUCT_FLOW && !refs.contains(e.id))
                    missingProduct++;
                if(!e.isInput && e.flow.flowType==FlowType.WASTE_FLOW && !refs.contains(e.id))
                    missingWaste++;
            }
        }
        System.out.println("PTXLENS_NATIVE_2023_CASE\t"+caseId);
        System.out.println("PTXLENS_NATIVE_2023_ORIGINAL_SOURCE_SHA\t"+originalSha);
        System.out.println("PTXLENS_NATIVE_2023_MODELLED_DELIVERED_H2_KG\t"+modeledH2Kg);
        System.out.println("PTXLENS_NATIVE_2023_INPUT_GRID_NL_LOW_KWH_PER_KG_H2\t"+gridKwh);
        System.out.println("PTXLENS_NATIVE_2023_INPUT_LEGACY_OFFSHORE_WIND_KWH_PER_KG_H2\t"+windKwh);
        System.out.println("PTXLENS_NATIVE_2023_LOCAL_SCENARIO_UUID\t"+cloned.refId);
        System.out.println("PTXLENS_NATIVE_2023_LINKED_PROCESSES\t"+system.processes.size());
        System.out.println("PTXLENS_NATIVE_2023_LINKED_EXCHANGES\t"+system.processLinks.size());
        System.out.println("PTXLENS_NATIVE_2023_UNLINKED_PRODUCT_INPUTS\t"+missingProduct);
        System.out.println("PTXLENS_NATIVE_2023_UNLINKED_WASTE_OUTPUTS\t"+missingWaste);
        require(missingProduct==0&&missingWaste==0,
               "actual BAFU NL-scenario native graph does not close");

        var setup=CalculationSetup.of(system).withImpactMethod(method).withAmount(1.0);
        var result=new SystemCalculator(db).withSolver(MatrixSolver.get()).calculate(setup);
        try{
            require(result.hasImpacts(),"actual native 2023 scenario method returned no impacts");
            boolean found=false;
            for(var item:result.getTotalImpacts()){
                if(!NATIVE_GWP.equals(item.impact().name))continue;
                require(!found,"multiple native GWP100 impacts with exact same method category");
                require(Double.isFinite(item.value()),"nonfinite native source GWP100");
                System.out.println("PTXLENS_NATIVE_2023_GWP100_KGCO2E_PER_KG_H2\t"+
                    String.format(Locale.ROOT,"%.14g",item.value()));
                found=true;
            }
            require(found,"exact native BAFU IPCC 2021 GWP 100 climate impact missing");
        }finally{
            result.dispose();
        }
        System.out.println("PTXLENS_NATIVE_2023_ADDITIONAL_E_PLUS_S_TANK_INCLUDED\tfalse");
        System.out.println("PTXLENS_NATIVE_2023_FULL_CRADLE_TO_GATE_CLAIM\tfalse");
    }

    public static void main(String[] args) throws Exception{
        if(args.length!=3 && args.length!=4)
            throw new IllegalArgumentException("usage: <scratch-copy-BAFU-v1.1-Derby-db> <source-verified-E-ES-config.json> <GPL-UMFPACK-root> [E|E_plus_S]");
        String requested=args.length==4?args[3]:"both";
        require("both".equals(requested)||"E".equals(requested)||"E_plus_S".equals(requested),
                "unsupported independently selected historical scenario");
        File folder=Path.of(args[0]).toAbsolutePath().toFile();
        require(Derby.isDerbyFolder(folder),"the scratch DB is not an actual native openLCA Derby database");
        NativeLib.loadFrom(Path.of(args[2]).toAbsolutePath().toFile());
        require(NativeLib.isLoaded(Module.UMFPACK),"sparse UMFPACK failed to load; refusing impractical dense solver");
        System.out.println("PTXLENS_NATIVE_UMFPACK_SPARSE_LOADED\ttrue");
        com.google.gson.JsonObject config;
        try(var f=new FileReader(args[1])){
            config=JsonParser.parseReader(f).getAsJsonObject();
        }
        require("ptxlens.native-bafu-2023-source-config-v0.1".equals(config.get("schema").getAsString()),
              "not source verified 2023 E/E+S config");
        var cases=config.getAsJsonArray("cases");
        require(cases!=null && cases.size()==2,"require original E and E+S cases only");
        try(var db=new Derby(folder)){
            require(db.getDescriptors(Process.class).size()>=11947,"original BAFU complete source database is missing processes");
            var original=exactSource(db,BASE_PROCESS,
               "Hydrogen production, gaseous, 30 bar, from PEM electrolysis, from grid electricity","kg");
            var grid=exactSource(db,NL_GRID_LOW,"Electricity, low voltage, at grid","kWh");
            var wind=exactSource(db,OFFSHORE_WIND_2MW,
                "xx Electricity, at wind power plant 2MW, offshore","kWh");
            var water=exactSource(db,NL_DEIONIZED,
                "Water, deionised, water balance according to MoeK 2013, at plant","kg");
            var method=climateMethod(db);
            int i=0,executed=0;
            for(var e:cases){
                var row=e.getAsJsonObject();
                String scenario=row.get("case").getAsString();
                require((i==0?"E":"E_plus_S").equals(scenario),
                    "expected registered original E followed by E_plus_S source model");
                require(!row.get("incremental_storage_equipment_included").getAsBoolean(),
                    "source config wrongly asserts independently validated extra storage");
                if("both".equals(requested)||scenario.equals(requested)) {
                    runCase(db,method,original,grid,wind,water,scenario,
                            row.get("original_sha256").getAsString(),
                            row.get("grid_input_kWh_per_kg_H2").getAsDouble(),
                            row.get("wind_input_kWh_per_kg_H2").getAsDouble(),
                            row.get("modelled_delivered_kg_2023").getAsDouble());
                    executed++;
                }
                i++;
            }
            System.out.println("PTXLENS_NATIVE_SCENARIOS_EXECUTED\t"+executed);
        }
        System.out.println("PTXLENS_NATIVE_BAFU_V11_SOURCE_REMAINS_UNALTERED\ttrue");
        System.out.println("PTXLENS_NATIVE_DUTCH_PTX_COMPLETE_STUDY\tfalse");
    }
}
