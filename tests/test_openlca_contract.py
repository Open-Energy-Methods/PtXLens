"""Real openLCA IPC client contract checks. No fake server or LCIA output."""
import pytest

from ptxlens.olca_real import validate_openlca_contract


def _cfg():
    return {
        "product_system_id":"11111111-1111-1111-1111-111111111111",
        "product_system_name":"PEM hydrogen",
        "impact_method_id":"22222222-2222-2222-2222-222222222222",
        "impact_method_name":"EF 3.1 climate change",
        "database_name":"actual user database",
        "database_version":"source-version",
        "database_provider":"actual institution",
        "database_license":"check",
        "reference_flow_amount_kg_h2":1,
        "parameter_mapping":{
            "electricity_grid_kwh_per_kg":"grid_kwh",
            "electricity_wind_kwh_per_kg":"wind_kwh"},
        "ipc_port":8080,
    }


def test_contract_requires_explicit_user_database_and_distinct_parameters():
    assert validate_openlca_contract(_cfg())["ipc_port"]==8080
    cfg=_cfg()
    cfg["parameter_mapping"]["electricity_wind_kwh_per_kg"]="grid_kwh"
    with pytest.raises(ValueError,match="separate"):
        validate_openlca_contract(cfg)
    cfg=_cfg()
    cfg["impact_method_id"]=None
    with pytest.raises(ValueError,match="requires impact_method_id"):
        validate_openlca_contract(cfg)


def test_client_package_2_6_api_exists():
    import olca_ipc
    import olca_schema as o
    assert hasattr(olca_ipc,"Client")
    assert hasattr(o,"CalculationSetup")
    assert hasattr(o,"ParameterRedef")
    assert hasattr(o,"ProductSystem")
    assert hasattr(o,"ImpactMethod")
