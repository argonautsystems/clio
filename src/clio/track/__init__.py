# Copyright 2026 clio Contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0

"""clio.track — persistent provenance and lineage.

Designed Phase 1.5b (cleanroom-claude); implemented in 1.5b/c.

Planned subsystems:

    fingerprint   Schema-shape hash + dtype map + null pct + value range +
                  source URI + extraction date. Content-hash based for stable
                  IDs across rebuilds.

    store         Parquet-backed lineage log. Append-only, immutable rows.

    lineage       Query API: "where did this row come from? what confidence?"

    audit         Per-extraction audit envelope. Composes with caller-side
                  envelopes (e.g. ic_result.clio_fingerprint_id) so the chain
                  runs end-to-end from agent output back to source URI.
"""
