"""Generates SYNTHETIC demo data (seeded). Not real client data."""
import csv, random
from datetime import datetime, timedelta
random.seed(7)
src = ["Google Ads", "Website form", "Facebook", "Phone", "Referral"]
t0 = datetime(2026, 9, 1, 7, 0)
with open("examples/sample_leads.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["lead_id", "source", "created_at", "first_response_at", "won"])
    for i in range(120):
        c = t0 + timedelta(minutes=random.randint(0, 28 * 24 * 60))
        r = random.random()
        delay = None if r < .14 else random.choice([2, 3, 4, 8, 20, 45, 120, 300, 900, 2000]) + random.random() * 5
        win_p = .45 if delay is not None and delay < 5 else .25 if delay is not None and delay < 240 else .08
        resp = (c + timedelta(minutes=delay)).strftime("%Y-%m-%d %H:%M:%S") if delay is not None else ""
        w.writerow([f"L{i+1:03d}", random.choice(src), c.strftime("%Y-%m-%d %H:%M:%S"), resp, int(random.random() < win_p)])
