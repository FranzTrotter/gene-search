def deduplicate_hits(hits):
    best_hits = {}
    for hit in hits:
        fields = hit.get("fields", {})
        # extract base disease id
        disease_id = fields.get("disease_id", hit["_id"]) #fallback to _id
        score = hit.get("_score", 0)

        # keep the highest score for each disease
        if disease_id not in best_hits or score > best_hits[disease_id]["_score"]:
            best_hits[disease_id] = hit
    # return list of unique hits sorted by score
    return sorted(best_hits.values(), key=lambda x: x["_score"], reverse=True)
