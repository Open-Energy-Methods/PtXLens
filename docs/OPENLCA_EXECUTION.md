# openLCA real LCIA — reproducibility gate

Status: a **live IPC calculation command exists**, but there is no completed LCA calculation in the current repo. No fake footprint or empty process system will be accepted as a valid cradle-to-gate result.

## Obtain actual real LCI resources

1. Install GreenDelta openLCA 2 locally: https://www.openlca.org/ . Start/create an openLCA database.
2. Obtain legally permitted unit-process LCI data and a matching named GWP100 LCIA method. Sources: https://www.lcacommons.gov/quick-start-guide and https://www.openlca.org/data/ .
3. Official USLCI openLCA 2 JSON-LD free LCI is available at https://www.lcacommons.gov/lca-collaboration/National_Renewable_Energy_Laboratory/USLCI_Database_Public . The US geographic scope is **not equivalent to NL**. Open background provider coverage is process-specific; audit every missing link.
4. Official Federal LCA Commons REST API supports licensed search/download and requires an api.data.gov key: https://www.lcacommons.gov/lca-commons-api-guide .
5. Build a true hydrogen foreground product system referenced to 1 kg delivered gaseous H2 at a *defined pressure/purity/gate*. Include water, electricity, stack/manufacturing replacements, compression/purification, physical BoP inventories and explicit provider links and a compatible GWP100 impact characterization method. The upstream PyNEXUS model provides energy and delivered amounts but does not validate compressor or quality controls.
6. In the product system, define two separate, operative parameters for grid/wind electricity in kWh per kg delivered hydrogen, with actual processes linked and no duplicate electricity GWP entry. Test that overriding these parameters changes actual provider requirements.
7. Enable openLCA IPC server (local port 8080 by default) on the exact database and record product-system UUID, product-system name, impact-method UUID and name, database name, version, provider, source year and licence.

## Headless server option (official openLCA IPC)

GreenDelta also supports headless stand-alone servers that connect to a previously imported workspace database; no graphical session is required for calculations. See https://greendelta.github.io/openLCA-ApiDoc/servers.html .

After importing the model into an actual openLCA database, stop the desktop's connection to that database and launch the openLCA installation's bin/ipc-server script with the real database name (the desktop and headless server cannot open that same database simultaneously). Headless server needs a valid openLCA workspace containing databases and any referenced libraries.

Optionally use the official gdt-server container with that workspace mounted and a read-only source database. The absence of a real linked database is still a hard stop: starting an empty server is NOT a completed LCA. Never commit restricted LCI files or database directories to GitHub.

## Run the real LCA

Copy configs/openlca.user.template.json to a private local file and replace all nulls and the placeholder parameter names with real verified values. Do not commit provider licence files or private API keys.

Commands:

~~~bash
python -m pip install -e .
python -m pip install "olca-ipc==2.6.3"
ptxlens openlca-run pynexus-wp5-e-2023.zip \
  --config /private/path/openlca_real_database.json \
  --output outputs/lca_real_E_result.json
~~~

The source ZIP is byte-checked against the original PyNEXUS frozen SHA256. Input source grid and wind energy is normalized by modeled delivered hydrogen. The script refuses missing product-system or impact-method UUID/name, missing dynamic parameters and absent server, and only writes an output after the actual engine reports impact-category results.

Parameter API: https://greendelta.github.io/openLCA-ApiDoc/examples/parameters.html

## Reject incomplete results

Reject any purported cradle-to-gate GWP if a background provider is missing, method elementary flow factors do not align, input production quality/gate is undefined, wind infrastructure is double counted, or US LCI factors are used unqualified as 2023 Netherlands electricity impacts. Inspect provider contributions, numerical perturbations, functional unit, allocation and LCIA method. This work is not ISO 14044-certified or third-party-reviewed.
