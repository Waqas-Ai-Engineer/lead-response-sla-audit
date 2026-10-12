import argparse, sys
from .core import load, audit
from .report import to_markdown, to_html


def main(argv=None):
    p = argparse.ArgumentParser(prog="leadsla", description="Audit how fast your business answers new leads.")
    p.add_argument("csv", help="CSV with lead_id,source,created_at,first_response_at,won")
    p.add_argument("--sla", type=int, default=15, help="SLA in minutes (default 15)")
    p.add_argument("--job-value", type=float, default=0, help="average job value, enables leak estimate")
    p.add_argument("--html", help="write HTML report to this path")
    a = p.parse_args(argv)
    res = audit(load(a.csv), a.sla, a.job_value)
    sys.stdout.write(to_markdown(res))
    if a.html:
        open(a.html, "w", encoding="utf-8").write(to_html(res))
        print(f"\nHTML report: {a.html}")
