job_mapping = {
    "mappings": {
        "dynamic": "strict",
        "properties": {
            "avam": {"type": "integer"},  # formerly "string"
            "bfs": {"type": "integer"},
            "isco08": {"type": "integer"},
            "title": {"type": "text"},
            "isco_title": {"type": "text"},
        },
    }
}
