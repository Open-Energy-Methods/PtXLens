"""RC2-C native Java/openLCA environment inventory, not a native calculation.

Records declared POM, actual JVM/Maven and resolved dependency JAR hashes.
Optional local BAFU archive comparison reads bytes only. Does not import,
calculate, upload an archive, grant data rights, or qualify a native LCIA.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
POM = ROOT / "native-openlca" / "pom.xml"
NAMESPACE = {"m": "http://maven.apache.org/POM/4.0.0"}
EXPECTED_BAFU = "e63b7e7ef5cde04bfe1176a783a55b5f72e2b73f42c36632b6150af39d348c4c"
EXPECTED_BAFU_SIZE = 135424513


def need(ok, msg):
    if not ok:
        raise ValueError("RC2-C native inventory: " + msg)


def fingerprint(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024**2), b""):
            h.update(chunk)
    return h.hexdigest()


def run_version(cmd, pattern):
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            text=True, encoding="utf-8", errors="replace", timeout=20,
                            check=True)
    cleaned = re.sub(r"\x1b\[[0-9;]*m", "", result.stdout)
    m = re.search(pattern, cleaned)
    need(m is not None, "runtime version unavailable")
    return m.group(1)


def declared():
    root = ET.parse(POM).getroot()
    compiler = root.findtext("m:properties/m:maven.compiler.release", namespaces=NAMESPACE)
    deps = [{k: x.findtext("m:" + k, namespaces=NAMESPACE)
             for k in ("groupId", "artifactId", "version")}
            for x in root.findall("m:dependencies/m:dependency", NAMESPACE)]
    plugins = [{k: x.findtext("m:" + k, namespaces=NAMESPACE)
                for k in ("groupId", "artifactId", "version")}
               for x in root.findall("m:build/m:plugins/m:plugin", NAMESPACE)]
    need(compiler == "25" and any(x == {
        "groupId": "org.openlca", "artifactId": "olca-core", "version": "2.7.0"
    } for x in deps), "native source POM changed; re-review qualification")
    return {"java_compiler_release": compiler, "declared_dependencies": deps,
            "declared_build_plugins": plugins, "pom_sha256": fingerprint(POM)}


def jars_from_classpath(path):
    items = path.read_text(encoding="utf-8").strip().split(os.pathsep)
    need(items and len(items) == len(set(items)), "duplicate or empty runtime classpath")
    rows = []
    for item in items:
        p = Path(item)
        need(p.is_file() and p.suffix.lower() == ".jar", "non-JAR or missing classpath member")
        rows.append({"jar": p.name, "sha256": fingerprint(p), "bytes": p.stat().st_size})
    names = [r["jar"] for r in rows]
    need(len(names) == len(set(names)) and "olca-core-2.7.0.jar" in names,
         "ambiguous runtime JARs or wrong openLCA core")
    return sorted(rows, key=lambda row: row["jar"])


def report(classpath=None, bafu=None):
    d = declared()
    d.update({
        "schema_version": "ptxlens.rc2c.native_environment_inventory.v1",
        "java_runtime_version": run_version(["java", "-version"], r'version "([^"]+)"'),
        "maven_runtime_version": run_version(["mvn", "-version"], r"Apache Maven ([^\s]+)"),
        "runtime_classpath_jar_hashes": jars_from_classpath(classpath) if classpath is not None else None,
        "expected_private_BAFU_2026_v11_archive_sha256": EXPECTED_BAFU,
        "expected_private_BAFU_2026_v11_archive_bytes": EXPECTED_BAFU_SIZE,
        "private_BAFU_archive_checked": False,
        "native_database_import_or_LCIA_run": False,
        "all_maven_plugins_transitively_hash_locked": False,
        "native_optional_UMFPACK_binary_checked": False,
        "full_native_environment_certified": False,
        "scientific_v1_approved": False,
    })
    need(d["java_runtime_version"].split(".")[0] == "25", "Java 25 runtime required")
    if bafu is not None:
        need(bafu.is_file() and not bafu.is_symlink() and bafu.suffix.lower() == ".zolca",
             "expected private ordinary BAFU .zolca")
        need(bafu.stat().st_size == EXPECTED_BAFU_SIZE and fingerprint(bafu) == EXPECTED_BAFU,
             "private BAFU archive differs from original v1.1 source")
        d["private_BAFU_archive_checked"] = True
    return d


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--classpath", type=Path, help="Maven runtime dependency build-classpath file")
    p.add_argument("--bafu", type=Path, help="Optional original PRIVATE local BAFU v1.1 .zolca")
    p.add_argument("--baseline", type=Path, help="Compare resolved runtime inventory with reviewed baseline")
    p.add_argument("--output", type=Path)
    a = p.parse_args(argv)
    r = report(a.classpath, a.bafu)
    if a.baseline is not None:
        prior = json.loads(a.baseline.read_text(encoding="utf-8"))
        keys = ("pom_sha256", "java_runtime_version", "maven_runtime_version",
                "declared_dependencies", "declared_build_plugins", "runtime_classpath_jar_hashes")
        differences = [k for k in keys if r[k] != prior[k]]
        if differences:
            print("RC2C_NATIVE_RUNTIME_BASELINE_DRIFT " + json.dumps(differences))
            print("RC2C_NATIVE_ENVIRONMENT_INVENTORY " + json.dumps(r, sort_keys=True))
        need(a.classpath is not None and not differences,
             "native resolved runtime differs from recorded baseline; review required: " + ", ".join(differences))
        print("RC2C_NATIVE_RUNTIME_BASELINE_MATCH")
    if a.output:
        with a.output.open("x", encoding="utf-8", newline="\n") as f:
            json.dump(r, f, indent=2, sort_keys=True, allow_nan=False)
            f.write("\n")
    print("RC2C_NATIVE_ENVIRONMENT_INVENTORY " + json.dumps(r, sort_keys=True))
    print("RC2C_NATIVE_ENVIRONMENT_INVENTORY_ONLY_NO_NATIVE_LCIA_OR_SCIENTIFIC_V1")


if __name__ == "__main__":
    main()
