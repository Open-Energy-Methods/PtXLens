"""Live, attributed Dutch day-ahead prices from Fraunhofer Energy-Charts API.

No credentials, invented defaults, forward-fill, interpolation or synthetic fallback.
2023 NL prices from the API are an **independent source check** against
the original ENTSO-E A44-priced *frozen* PyNEXUS dispatch, not a retroactive
modification of that registered experiment.
"""
from __future__ import annotations
import csv
import hashlib
import io
import json
import math
from datetime import datetime, timedelta, timezone
from pathlib import Path
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

BASE = "https://api.energy-charts.info/price"
ATTRIBUTION = "Fraunhofer ISE Energy-Charts.info; NL prices sourced from Bundesnetzagentur/SMARD; CC BY 4.0"
LICENSE = "CC BY 4.0"


def build_url(year, bzn="NL"):
    if bzn != "NL":
        raise ValueError("only Netherlands NL is licensed/validated in this pipeline")
    if not isinstance(year, int) or year < 2005 or year > datetime.now(timezone.utc).year:
        raise ValueError("unexpected market year")
    args = {"bzn":bzn, "start":f"{year}-01-01T00:00Z",
            "end":f"{year+1}-01-01T00:00Z"}
    return BASE + "?" + urlencode(args)


def parse_price_response(payload, year, raw_sha256="", request_url=""):
    if not isinstance(payload, dict):
        raise ValueError("API returned no JSON object")
    instants, prices = payload.get("unix_seconds"), payload.get("price")
    if not isinstance(instants, list) or not isinstance(prices, list) or len(instants) != len(prices):
        raise ValueError("invalid time-price array lengths")
    start = datetime(year, 1, 1, tzinfo=timezone.utc)
    end = datetime(year+1, 1, 1, tzinfo=timezone.utc)
    data = {}
    for ts, p in zip(instants, prices):
        if isinstance(ts, bool) or not isinstance(ts, (int, float)):
            raise ValueError("bad Unix timestamp")
        dt = datetime.fromtimestamp(ts, tz=timezone.utc)
        if not start <= dt < end:
            continue
        if dt.minute or dt.second or dt.microsecond:
            raise ValueError("not hourly data; refuse 15-minute market aggregation")
        if isinstance(p, bool) or not isinstance(p, (float, int)) or not math.isfinite(p):
            raise ValueError("missing/nonfinite prices; no interpolation permitted")
        if dt in data:
            raise ValueError("repeated UTC hour; no DST ambiguity allowed")
        data[dt] = float(p)
    expected = int((end - start).total_seconds()/3600)
    if len(data) != expected:
        raise ValueError(f"price coverage {len(data)}/{expected}; missing historical hours")
    ordered = sorted(data.items())
    if any(t != start+timedelta(hours=i) for i,(t,_) in enumerate(ordered)):
        raise ValueError("UTC hourly gaps or order mismatch")
    if payload.get("unit", "").replace(" ", "") not in ("EUR/MWh", "€/MWh"):
        raise ValueError("unexpected monetary unit from price API")
    info = payload.get("license_info", "")
    if not isinstance(info,str) or not info:
        raise ValueError("license_info absent; cannot publish dataset without attribution")
    return {
        "schema_version":"ptxlens.energy_charts_nl_hourly.v0.1",
        "source_url":request_url, "provider":ATTRIBUTION,
        "source_license_note":info, "license_classification":LICENSE,
        "source_raw_json_sha256":raw_sha256,
        "market_zone":"NL", "year":year, "timezone":"UTC",
        "unit":"EUR/MWh", "row_count":expected,
        "series":[{"timestamp_utc":t.strftime("%Y-%m-%dT%H:%M:%SZ"),
                   "price_eur_mwh":p} for t,p in ordered]
    }


def fetch_prices(year, *, opener=urlopen):
    url = build_url(year)
    req = Request(url, headers={"User-Agent":"PtXLens/0.2 academic-reproducibility (+https://github.com/Open-Energy-Methods/PtXLens)", "Accept":"application/json"})
    for attempt in range(3):
        try:
            with opener(req, timeout=60) as resp:
                raw = resp.read(4_000_001)
            if len(raw) > 4_000_000:
                raise ValueError("API response unexpectedly large")
            obj = json.loads(raw)
            return parse_price_response(obj, year, hashlib.sha256(raw).hexdigest(),url)
        except HTTPError as e:
            if e.code != 429 or attempt == 2:
                raise
            try:
                backoff = min(max(float(e.headers.get("Retry-After","5")),1),30)
            except ValueError:
                backoff = 5
            time.sleep(backoff)
        except (URLError, TimeoutError):
            if attempt == 2:
                raise
            time.sleep(2 * (attempt+1))
    raise RuntimeError("price API unsuccessful")


def write_prices(dataset, csv_path, manifest_path):
    """Output source-attributed CSV + reproducibility manifest; refuse overwrite."""
    csv_path, manifest_path = Path(csv_path), Path(manifest_path)
    for p in (csv_path,manifest_path):
        if p.exists():
            raise FileExistsError(f"existing output must not be overwritten: {p}")
    with io.StringIO(newline="") as s:
        writer = csv.writer(s, lineterminator="\n")
        writer.writerow(["timestamp_utc","price_eur_mwh"])
        writer.writerows((r["timestamp_utc"],format(r["price_eur_mwh"],".12g")) for r in dataset["series"])
        csvbytes = s.getvalue().encode()
    manifest = {k:v for k,v in dataset.items() if k!="series"}
    manifest["csv_sha256"] = hashlib.sha256(csvbytes).hexdigest()
    csv_path.write_bytes(csvbytes)
    manifest_path.write_text(json.dumps(manifest,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    return manifest
