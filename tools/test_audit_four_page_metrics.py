import unittest
from audit_four_page_metrics import TARGETS, audit, classify_comments, rate


class AuditTests(unittest.TestCase):
    def test_null_and_zero_denominator(self):
        self.assertIsNone(rate(None, 10))
        self.assertIsNone(rate(0, 0))
        self.assertEqual(rate(0, 10), 0)

    def test_ids_override_text_and_page_can_comment_twice(self):
        comments = [
            {"id": "1", "from": {"id": "page"}, "message": "reply"},
            {"id": "2", "from": {"id": "page"}, "message": "second reply"},
            {"id": "3", "from": {"id": "other_page"}},
            {"id": "4", "from": {"id": "visitor"}, "message": "📌 https://example.com"},
            {"id": "5", "message": "unknown"},
            {"id": "6", "from": {"id": "staff"}},
            {"id": "4", "from": {"id": "visitor"}},
        ]
        self.assertEqual(classify_comments(comments, ["page", "other_page"], ["staff"]),
                         {"page": 3, "internal": 1, "audience_candidate": 1,
                          "unknown": 1, "duplicate": 1})

    def test_correct_quota_and_do_not_reuse_customer_claims(self):
        pages = [{"id": pid, "name": pid, "connected": True,
                  "posts_24h": 7 if i == 0 else 0, "user_comments_count": 2}
                 for i, pid in enumerate(TARGETS)]
        result = audit({"timestamp": 1793325627, "page_results": pages}, "test")
        self.assertEqual(result["target_posts_per_day"], 15)
        self.assertEqual(result["provisional_attainment_pct"], 46.67)
        self.assertEqual(result["pages"][0]["provisional_attainment_pct"], 77.78)
        self.assertTrue(all(p["verified_customer_comments"] is None for p in result["pages"]))
        self.assertTrue(all(p["valid_orders"] is None for p in result["pages"]))
        pages[1]["connected"] = False
        self.assertIsNone(audit({"timestamp": 1793325627, "page_results": pages}, "x")
                          ["provisional_attainment_pct"])

    def test_duplicate_pages_rejected(self):
        with self.assertRaises(ValueError):
            audit({"timestamp": 0, "page_results": [{"id": "x"}] * 4}, "x")


if __name__ == "__main__":
    unittest.main()
