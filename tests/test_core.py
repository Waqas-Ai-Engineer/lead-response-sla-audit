import sys, os, unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from leadsla.core import load, audit, bucket_of


class T(unittest.TestCase):
    def test_bucket(self):
        self.assertEqual(bucket_of(None), "never")
        self.assertEqual(bucket_of(2), "<5 min")
        self.assertEqual(bucket_of(5000), ">24 h")

    def test_audit(self):
        r = audit(load(os.path.join(os.path.dirname(__file__), "..", "examples", "sample_leads.csv")), 15, 5000)
        self.assertEqual(r["total"], 120)
        self.assertEqual(sum(r["buckets"].values()), 120)
        self.assertTrue(0 <= r["sla_pct"] <= 100)


if __name__ == "__main__":
    unittest.main()
