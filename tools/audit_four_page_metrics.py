"""Offline audit; preserves raw caches, reports, credentials and production jobs."""
import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path

TARGETS = {"1022527194267367": 9, "1442323328956326": 2,
           "1421270697727753": 2, "1407231352464711": 2}


def rate(numerator, denominator):
    if numerator is None or denominator is None or denominator <= 0:
        return None
    if numerator < 0:
        raise ValueError("Negative numerator")
    return round(100 * numerator / denominator, 2)


def classify_comments(comments, managed_page_ids, internal_actor_ids=()):
    """Classify explicit IDs only. Text/URLs/names never prove authorship or pinning.

    External actors are audience candidates, not proven buyers. Collect all pages
    and replies upstream; unknown IDs and missing records stay unknown.
    """
    managed = set(map(str, managed_page_ids))
    internal = set(map(str, internal_actor_ids))
    counts = {"page": 0, "internal": 0, "audience_candidate": 0,
              "unknown": 0, "duplicate": 0}
    seen = set()
    for comment in comments:
        cid = comment.get("id")
        if cid and cid in seen:
            counts["duplicate"] += 1
            continue
        if cid:
            seen.add(cid)
        actor = str((comment.get("from") or {}).get("id") or "")
        category = ("unknown" if not cid or not actor else
                    "page" if actor in managed else
                    "internal" if actor in internal else "audience_candidate")
        counts[category] += 1
    return counts


def audit(cache, source_hash):
    pages = cache["page_results"]
    ids = [str(p["id"]) for p in pages]
    if len(ids) != 4 or set(ids) != set(TARGETS):
        raise ValueError("Expected four unique configured pages")
    end = dt.datetime.fromtimestamp(cache["timestamp"], dt.timezone.utc)
    rows = []
    for page in pages:
        pid = str(page["id"])
        usable = page.get("connected") is True and not page.get("error")
        posted = page.get("posts_24h") if usable else None
        rows.append({
            "page_id": pid, "name": page["name"], "target_posts": TARGETS[pid],
            "reported_posts_24h": posted,
            "provisional_attainment_pct": rate(posted, TARGETS[pid]),
            "published_ids_and_full_pagination_verified": False,
            "reported_scheduled_sample_count": page.get("scheduled_count") if usable else None,
            "reported_lifetime_likes_on_sampled_posts": page.get("likes_total") if usable else None,
            "sampled_posts": page.get("posts_total_sampled") if usable else None,
            "legacy_customer_comment_claim": page.get("user_comments_count"),
            "verified_customer_comments": None, "verified_page_comments": None,
            "verified_pinned_posts": None,
            "video_starts": None, "video_3s_views": None, "hook_rate_pct": None,
            "outbound_link_clicks": None, "shopee_attributed_clicks": None,
            "valid_orders": None, "cancelled_returned_rejected_orders": None,
            "pending_commission_vnd": None, "approved_commission_vnd": None,
            "paid_commission_vnd": None, "ctr_pct": None, "cvr_pct": None,
            "epc_vnd": None, "decision": "ITERATE",
            "decision_scope": "measurement; creative KEEP/STOP not assessable",
        })
    total = (sum(r["reported_posts_24h"] for r in rows)
             if all(r["reported_posts_24h"] is not None for r in rows) else None)
    return {
        "status": "AUDITED_LOCAL_SNAPSHOT_CONVERSION_EVIDENCE_MISSING",
        "source_sha256": source_hash, "timezone": "Asia/Ho_Chi_Minh",
        "snapshot_end": end.isoformat(),
        "rolling_24h_start": (end - dt.timedelta(hours=24)).isoformat(),
        "target_posts_per_day": sum(TARGETS.values()),
        "reported_posts_24h": total,
        "provisional_attainment_pct": rate(total, sum(TARGETS.values())),
        "warning": "Snapshot aggregates are not raw API evidence; missing is null, not zero.",
        "pages": rows,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.cache.resolve() == args.output.resolve() or args.output.exists():
        parser.error("Use a NEW output path; source and existing artifacts are preserved")
    raw = args.cache.read_bytes()
    result = audit(json.loads(raw.decode("utf-8-sig")), hashlib.sha256(raw).hexdigest())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8") as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    print(f"{result['reported_posts_24h']}/{result['target_posts_per_day']} = "
          f"{result['provisional_attainment_pct']}%; conversion evidence missing")


if __name__ == "__main__":
    main()
