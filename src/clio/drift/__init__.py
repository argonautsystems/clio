# Copyright 2026 clio Contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0

"""clio.drift — semantic drift detection over tracked fingerprints.

Designed Phase 1.5b (cleanroom-claude); implemented in 1.5b/c.

Planned subsystems:

    detect    Diff fingerprints across time, classify drift events
              (column added/removed/renamed/dtype-changed/value-range-shifted).

    remap     When drift fits a known shape, invoke clio.extract.schema_map
              to auto-re-extract.

    alarm     When drift doesn't fit a known shape, surface for human review.
"""
