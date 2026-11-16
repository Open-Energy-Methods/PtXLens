"""Actual openLCA 2 IPC calculation with documented product-system parameters.

Requires user-installed openLCA, running IPC server, an actual linked foreground
product system and a licensed/available background inventory. Not a mock.
This module NEVER fabricates LCIA results or injects guessed emission factors.
"""
from __future__ import annotations
import importlib.metadata
import json
import math
from pathlib import Path


def per_kg_electricity_from_verified_observed(summary):
    """Derive param inputs in kWh/kg **delivered** from audited PyNEXUS case.

    Uses electricity balance accounting convention: grid imports are assigned
    to electrolysis and onsite wind supplies the remainder. This is NOT
    evidence of renewable-hydrogen certification or physical electron origin.
    """
    if summary.get("schema_version") != "ptxlens.pynexus_wp5_observed.v0.1":
        raise ValueError("requires independently audited PyNEXUS observed 2023 summary")
    delivered = summary["annual_delivered_h2_kg"]
    grid = summary["annual_grid_import_mwh"]
    wind = summary["annual_wind_consumed_mwh"]
    electro = summary["annual_electrolyser_input_mwh"]
    if delivered <= 0 or grid < 0 or wind < 0:
        raise ValueError("invalid hydrogen denominator or source energy allocation")
    if not math.isclose(grid + wind, electro, abs_tol=1e-3):
        raise ValueError("electricity source allocation does not close")
    return {"electricity_grid_kwh_per_kg": 1000*grid/delivered,
            "electricity_wind_kwh_per_kg": 1000*wind/delivered}


def validate_openlca_contract(config):
    """Require user to identify an actual LCI dataset, LCIA method and models."""
    if not isinstance(config, dict):
        raise ValueError("openLCA config must be a JSON object")
    for k in ("product_system_id", "product_system_name",
              "impact_method_id", "impact_method_name",
              "database_name", "database_version", "database_license",
              "database_provider"):
        if not isinstance(config.get(k), str) or not config[k].strip():
            raise ValueError(f"openLCA contract requires {k}")
    if config.get("reference_flow_amount_kg_h2") != 1:
        raise ValueError("product system must use exactly 1 kg delivered gaseous H2")
    params = config.get("parameter_mapping")
    expected = {"electricity_grid_kwh_per_kg","electricity_wind_kwh_per_kg"}
    if not isinstance(params, dict) or set(params) != expected:
        raise ValueError("must map both grid and wind electricity parameters")
    if any(not isinstance(v,str) or not v.strip() for v in params.values()):
        raise ValueError("openLCA parameter names must be nonempty")
    if params["electricity_grid_kwh_per_kg"] == params["electricity_wind_kwh_per_kg"]:
        raise ValueError("grid/wind parameters must be separate")
    port = config.get("ipc_port",8080)
    if isinstance(port,bool) or not isinstance(port,int) or not 1 <= port <= 65535:
        raise ValueError("invalid IPC port")
    return config


def run_actual_openlca(summary, config):
    """Submit a real parameterized LCIA to an already running openLCA server.

    An empty database, unmatched product system, wrong parameter or no server
    produces an error, NEVER a placeholder footprint.
    """
    settings = validate_openlca_contract(config)
    intensities = per_kg_electricity_from_verified_observed(summary)
    try:
        import olca_ipc as ipc
        import olca_schema as o
    except ImportError as exc:
        raise RuntimeError("install Python 3.12+ and pip install 'olca-ipc==2.6.3'") from exc
    client = ipc.Client(port=settings.get("ipc_port",8080))
    systems = client.get_descriptors(o.ProductSystem)
    methods = client.get_descriptors(o.ImpactMethod)
    system = next((x for x in systems if x.id == settings["product_system_id"]),None)
    method = next((x for x in methods if x.id == settings["impact_method_id"]),None)
    if system is None or system.name != settings["product_system_name"]:
        raise ValueError("actual openLCA product system UUID/name mismatch")
    if method is None or method.name != settings["impact_method_name"]:
        raise ValueError("actual openLCA LCIA method UUID/name mismatch")
    # Global model-level redefinitions are accepted only if present in the
    # inspected product system. A missing param is a hard scientific stop.
    current = client.get_parameters(o.ProductSystem, system.id)
    available = {p.name:p for p in current}
    redirections = []
    for source_key, target_key in settings["parameter_mapping"].items():
        if target_key not in available:
            raise ValueError(f"openLCA model lacks parameter {target_key}; edit product system")
        current_parameter = available[target_key]
        redirections.append(o.ParameterRedef(
            name=target_key,
            value=intensities[source_key],
            context=current_parameter.context,
        ))
    setup = o.CalculationSetup(
        target=system,
        impact_method=method,
        parameters=redirections,
        amount=1.0,
    )
    result = client.calculate(setup)
    if result is None:
        raise RuntimeError("openLCA did not return a calculation result")
    try:
        result.wait_until_ready()
        impact_values = result.get_total_impacts()
        entries = []
        for impact in impact_values:
            category = impact.impact_category
            if not category or not category.name or not category.ref_unit:
                raise ValueError("openLCA returned undefined category name/unit")
            value = float(impact.amount)
            if not math.isfinite(value):
                raise ValueError("openLCA returned nonfinite impact")
            entries.append({"category":category.name, "unit":category.ref_unit,
                            "amount_per_kg_delivered_h2":value})
        if not entries:
            raise ValueError("no impacts returned; check method factors and providers")
    finally:
        result.dispose()
    return {
        "schema_version":"ptxlens.openlca_calculated.v0.1",
        "execution_status":"CALCULATED_BY_LIVE_OPENLCA_IPC",
        "claim_level":"openLCA IPC calculated but foreground provider completeness NOT automatically established",
        "is_full_cradle_to_gate_lca":False,
        "openlca_ipc_version":importlib.metadata.version("olca-ipc"),
        "source_observed_archive_sha256":summary["archive_sha256"],
        "scenario":summary["scenario"],
        "system":{"id":system.id,"name":system.name},
        "method":{"id":method.id,"name":method.name},
        "database":{"name":settings["database_name"],"version":settings["database_version"],
                    "license":settings["database_license"],"provider":settings["database_provider"]},
        "foreground_unit":"1 kg delivered gaseous H2",
        "source_energy_accounting_kwh_per_kg":intensities,
        "parameter_mapping":settings["parameter_mapping"],
        "category_results":entries,
        "limitations":"openLCA model/database not automatically independently verified; physical plant not validated; ISO 14044 conformance not claimed",
    }


def run_from_files(archive_path, configuration_path, output_path):
    from .observed import load_archive
    archive = load_archive(archive_path)
    config = json.loads(Path(configuration_path).read_text(encoding="utf-8"))
    result = run_actual_openlca(archive,config)
    out = Path(output_path)
    if out.exists():
        raise FileExistsError("refusing to overwrite existing LCIA result")
    out.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    return result
