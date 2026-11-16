"""F3-D Windows PowerShell 5.1 launcher source compatibility regression.

Windows PowerShell 5.1 may decode UTF-8 without BOM as the system ANSI code
page. A Unicode en dash inside a double-quoted string can consequently create
a bad quote-like byte sequence and a parser error before ANY scientific test
can run. Keep the launcher strictly ASCII and parse it through the installed
Windows PowerShell parser where supported. Source-only tests: no MILPs.
"""
from pathlib import Path
import shutil
import subprocess

import pytest


SCRIPT=Path(__file__).resolve().parents[1]/"scripts"/"F3D_Robustness_Local.ps1"


def test_f3d_launcher_strictly_ascii_for_windows_powershell_51():
    raw=SCRIPT.read_bytes()
    assert raw, "F3D runner file missing"
    assert all(c<128 for c in raw), (
        "PowerShell 5.1 interpreted a UTF-8 punctuation mark incorrectly; "
        "use ASCII for cross-system launcher literals and comments")
    assert b"\r" not in raw, "Keep Git source file canonical LF"


def test_f3d_launcher_has_2024_publication_gate_without_auto_publication():
    content=SCRIPT.read_text(encoding="ascii")
    assert '"AuditAndCompare2024"' in content
    assert 'if($Phase -eq "AuditAndCompare2024"){' in content
    assert 'f3d_2024_crossyear_publication' in content
    assert 'test_f3d_2024_crossyear_publication.py' in content
    assert "git add" not in content
    assert "git push" not in content


def test_f3d_launcher_parses_with_actual_windows_powershell_51_if_available():
    executable=shutil.which("powershell.exe") or shutil.which("powershell")
    if executable is None:
        pytest.skip("Windows PowerShell executable unavailable on this host")
    # ParseFile only: never invoke the research launcher or source-year MILPs.
    # PowerShell -File is NOT used and there is no code execution from the script.
    name=str(SCRIPT).replace("'","''")
    command=(
        "$tokens=$null; $errors=$null; "
        f"[System.Management.Automation.Language.Parser]::ParseFile('{name}',"
        "[ref]$tokens,[ref]$errors) | Out-Null; "
        'if($errors.Count -gt 0){ $errors | ForEach-Object '
        '{ Write-Output $_.ToString() }; exit 1 }; exit 0'
    )
    p=subprocess.run(
        [executable,"-NoProfile","-NonInteractive","-Command",command],
        stdout=subprocess.PIPE,stderr=subprocess.PIPE,
        text=True,timeout=20,check=False,
    )
    assert p.returncode==0, (
        "F3D Windows PowerShell parser errors:\n"+p.stdout+"\n"+p.stderr)
