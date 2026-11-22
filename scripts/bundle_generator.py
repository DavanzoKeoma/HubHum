"""Curated Starter Bundles entrypoint delegating directly to cluster_orchestrator."""

from __future__ import annotations

import argparse
import sys

from cluster_orchestrator import generate_clusters


def main() -> int:
    parser = argparse.ArgumentParser(description="HubHum Curated Bundle Generator (delegates to cluster_orchestrator)")
    parser.parse_known_args()
    res = generate_clusters()
    bundles = res.get("bundles") or []
    print(f"[BUNDLE ORCHESTRATOR] Synced {len(bundles)} curated bundles and {res.get('total_guide_pages', 0)} guides.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
