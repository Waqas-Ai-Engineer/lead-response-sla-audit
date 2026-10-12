"""Speed-to-lead audit: pure stdlib, no network."""
import csv, statistics
from datetime import datetime, timedelta

FMT = ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%SZ")
BUCKETS = [("<5 min", 5), ("5-30 min", 30), ("30 min-4 h", 240), ("4-24 h", 1440), (">24 h", float("inf"))]


def parse_ts(s):
    s = (s or "").strip()
    if not s:
        return None
    for f in FMT:
        try:
            return datetime.strptime(s, f)
        except ValueError:
            pass
    raise ValueError(f"Unrecognised timestamp: {s!r}")


def is_business_hours(ts, start=8, end=18, weekdays=(0, 1, 2, 3, 4)):
    return ts.weekday() in weekdays and start <= ts.hour < end


def load(path):
    rows = []
    with open(path, newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            created = parse_ts(r["created_at"])
            first = parse_ts(r.get("first_response_at"))
            minutes = (first - created).total_seconds() / 60 if first else None
            rows.append({
                "id": r.get("lead_id", ""), "source": r.get("source", "unknown") or "unknown",
                "created": created, "minutes": minutes,
                "won": (r.get("won", "").strip().lower() in ("1", "true", "yes", "y")),
            })
    return rows


def bucket_of(minutes):
    if minutes is None:
        return "never"
    for name, lim in BUCKETS:
        if minutes < lim:
            return name
    return BUCKETS[-1][0]


def audit(rows, sla_minutes=15, avg_job_value=0.0, hours=(8, 18)):
    total = len(rows)
    answered = [r for r in rows if r["minutes"] is not None]
    never = total - len(answered)
    mins = [r["minutes"] for r in answered]
    within = sum(1 for m in mins if m <= sla_minutes)
    buckets = {n: 0 for n, _ in BUCKETS}
    buckets["never"] = 0
    win = {n: [0, 0] for n in buckets}
    for r in rows:
        b = bucket_of(r["minutes"])
        buckets[b] += 1
        win[b][0] += 1
        win[b][1] += r["won"]
    after = [r for r in rows if not is_business_hours(r["created"], *hours)]
    after_unanswered = sum(1 for r in after if r["minutes"] is None or r["minutes"] > 240)
    by_source = {}
    for r in rows:
        s = by_source.setdefault(r["source"], {"n": 0, "mins": [], "never": 0})
        s["n"] += 1
        if r["minutes"] is None:
            s["never"] += 1
        else:
            s["mins"].append(r["minutes"])
    fast_rate = (win["<5 min"][1] / win["<5 min"][0]) if win["<5 min"][0] else None
    slow = [r for r in rows if r["minutes"] is None or r["minutes"] > sla_minutes]
    slow_won = sum(r["won"] for r in slow)
    leak = None
    if fast_rate is not None and avg_job_value and slow:
        # Illustrative: if slow/never leads converted at the observed <5 min rate.
        leak = max(0.0, (fast_rate * len(slow) - slow_won) * avg_job_value)
    return {
        "total": total, "answered": len(answered), "never": never,
        "sla_minutes": sla_minutes, "sla_pct": (within / total * 100) if total else 0,
        "median": statistics.median(mins) if mins else None,
        "p90": (sorted(mins)[int(0.9 * (len(mins) - 1))] if mins else None),
        "buckets": buckets, "win": {k: (v[1] / v[0] if v[0] else None) for k, v in win.items()},
        "after_hours": len(after), "after_hours_unanswered": after_unanswered,
        "by_source": {k: {"n": v["n"], "never": v["never"],
                          "median": statistics.median(v["mins"]) if v["mins"] else None}
                      for k, v in by_source.items()},
        "fast_win_rate": fast_rate, "slow_leads": len(slow), "leak": leak,
    }


def fmt_min(m):
    if m is None:
        return "n/a"
    return f"{m:.0f} min" if m < 120 else f"{m/60:.1f} h"
