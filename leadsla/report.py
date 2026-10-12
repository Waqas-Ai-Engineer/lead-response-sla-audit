from .core import fmt_min, BUCKETS
from html import escape


def to_markdown(a):
    L = ["# Speed-to-Lead Audit", "",
         f"- Leads analysed: **{a['total']}** | never answered: **{a['never']}**",
         f"- Answered within {a['sla_minutes']} min SLA: **{a['sla_pct']:.0f}%**",
         f"- Median response: **{fmt_min(a['median'])}** | P90: **{fmt_min(a['p90'])}**",
         f"- After-hours leads: {a['after_hours']} ({a['after_hours_unanswered']} waited >4 h or never heard back)", "",
         "| Response time | Leads | Win rate |", "|---|---:|---:|"]
    for name in [b for b, _ in BUCKETS] + ["never"]:
        w = a["win"][name]
        L.append(f"| {name} | {a['buckets'][name]} | {'-' if w is None else f'{w*100:.0f}%'} |")
    L += ["", "| Source | Leads | Never answered | Median |", "|---|---:|---:|---:|"]
    for s, v in sorted(a["by_source"].items(), key=lambda x: -x[1]["n"]):
        L.append(f"| {s} | {v['n']} | {v['never']} | {fmt_min(v['median'])} |")
    if a["leak"] is not None:
        L += ["", f"> Illustrative estimate: ~**${a['leak']:,.0f}** of work may be leaking if slow/unanswered leads "
              f"converted at your own observed <5 min win rate ({a['fast_win_rate']*100:.0f}%). "
              "This is a scenario from your data, not a guarantee."]
    return "\n".join(L) + "\n"


def to_html(a):
    names = [b for b, _ in BUCKETS] + ["never"]
    mx = max(a["buckets"].values()) or 1
    bars = ""
    for i, n in enumerate(names):
        h = a["buckets"][n] / mx * 140
        col = "#16a34a" if i < 2 else "#f59e0b" if i < 4 else "#dc2626"
        bars += (f'<rect x="{30+i*80}" y="{170-h:.0f}" width="56" height="{h:.0f}" fill="{col}" rx="4"/>'
                 f'<text x="{58+i*80}" y="{164-h:.0f}" text-anchor="middle" font-size="12">{a["buckets"][n]}</text>'
                 f'<text x="{58+i*80}" y="190" text-anchor="middle" font-size="11">{escape(n)}</text>')
    rows = "".join(f"<tr><td>{escape(s)}</td><td>{v['n']}</td><td>{v['never']}</td><td>{fmt_min(v['median'])}</td></tr>"
                   for s, v in sorted(a["by_source"].items(), key=lambda x: -x[1]["n"]))
    leak = (f"<p class='note'>Illustrative: ~${a['leak']:,.0f} may be leaking if slow leads converted at your own "
            f"&lt;5 min win rate. A scenario, not a guarantee.</p>") if a["leak"] is not None else ""
    return f"""<!doctype html><meta charset=utf-8><title>Speed-to-Lead Audit</title>
<style>body{{font-family:system-ui;max-width:720px;margin:2rem auto;padding:0 1rem;color:#111}}
.k{{display:flex;gap:12px;flex-wrap:wrap}}.k div{{flex:1;min-width:140px;background:#f3f4f6;border-radius:10px;padding:12px}}
.k b{{font-size:1.6rem;display:block}}table{{border-collapse:collapse;width:100%}}td,th{{border-bottom:1px solid #ddd;padding:6px;text-align:left}}
.note{{background:#fffbeb;padding:10px;border-radius:8px}}</style>
<h1>Speed-to-Lead Audit</h1><div class=k>
<div><b>{a['sla_pct']:.0f}%</b>answered within {a['sla_minutes']} min</div>
<div><b>{fmt_min(a['median'])}</b>median response</div>
<div><b>{a['never']}</b>never answered</div>
<div><b>{a['after_hours_unanswered']}</b>after-hours leads left waiting</div></div>
<h2>Response-time distribution</h2><svg viewBox="0 0 500 200" width="100%">{bars}</svg>
<h2>By lead source</h2><table><tr><th>Source<th>Leads<th>Never answered<th>Median</tr>{rows}</table>{leak}"""
