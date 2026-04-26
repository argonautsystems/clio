# Copyright 2026 clio Contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0

"""clio.extract — unstructured input to structured output via AI.

Subsystems:

    vision        PDF/image -> JSON via vision LLM, parameterized prompt + schema.
                  Lifted Phase 1.5a from ic-engine pdf_extraction_dual_mode.py;
                  domain-specific heuristics (broker formats, account-section
                  parsing) intentionally NOT lifted — those stay in domain
                  libraries.

    schema_map    CSV column drift remapping via sentence-transformer embeddings
                  with cosine threshold. (Phase 1.5b lift from cleanroom
                  LLM_Mapper.py.)

    normalize     Name + address normalization with rapidfuzz. (Phase 1.5b lift
                  from cleanroom T1_normalization_utils.py.)

    text          NER + relation extraction. Deferred to v0.2+ — no concrete
                  consumer yet; placeholder so the directory shape is stable.

    confidence    Common Protocol across subsystems; each subsystem keeps its
                  native scoring algorithm.
"""
