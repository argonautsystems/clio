# clio

Foundation library for AI-driven semantic ETL: extraction, tracking, drift detection.

`clio` is the substrate layer in a three-layer fleet architecture:

| Layer            | Role                                                                | Examples                                                                            |
| ---------------- | ------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| Foundation       | AI-driven primitives — extract structure from unstructured input, track provenance, detect drift, auto-remap | **`clio`** (this library)                                                            |
| Domain substrate | Domain-specific models, providers, computation, routing, built on top of `clio` | `ic-engine` (portfolio), `etlantis` (public-records ETL)                            |
| Adapter          | Runtime-specific glue: install scripts, manifests, slash commands, marketplace metadata | `InvestorClaw` (claws-runtime), `InvestorClaude` (Claude Code), `RiskyEats`, `rvmaps` |

The split is deliberate: domain assumptions stay out of `clio` so successor domains adopt it without inheriting portfolio or hospitality conventions, and adapters can swap their domain substrate without re-implementing extraction, lineage, or drift handling.

## Status

**Alpha.** This is the `v0.0.1-rc1-bootstrap` snapshot. Phase 1.5a contributed:

- `clio.runtime.hardware` — CPU/GPU/memory probing across darwin + linux + WSL2 (lifted from ic-engine)
- `clio.extract.vision` — PDF/image → structured JSON via vision LLM (parameterized prompt + schema, litellm-backed for provider-agnostic routing)
- Package skeleton for `extract/`, `track/`, `drift/`, `runtime/`

Phase 1.5b will land schema mapping, normalization, tracking, and drift detection. Phase 1.5c stabilizes the v0.1.0 surface.

## Subsystems

```
clio/
├── extract/          unstructured input → structured output via AI
│   ├── vision.py         PDF/image → JSON via vision LLM (parameterized)
│   ├── schema_map.py     CSV column drift remapping (Phase 1.5b)
│   ├── normalize.py      name + address normalization (Phase 1.5b)
│   ├── text.py           NER + relation extraction (deferred to v0.2+)
│   └── confidence.py     common Protocol across subsystems (Phase 1.5b)
├── track/            persistent provenance + fingerprint store (Phase 1.5b)
│   ├── fingerprint.py    schema-shape hash + dtype map + value range
│   ├── store.py          parquet-backed lineage log
│   ├── lineage.py        query API: where did this row come from?
│   └── audit.py          per-extraction audit envelope
├── drift/            semantic drift detection over fingerprints (Phase 1.5b)
│   ├── detect.py         diff fingerprints, classify drift events
│   ├── remap.py          auto-re-extract via extract.schema_map
│   └── alarm.py          surface unfixable drift for human review
└── runtime/          AI-aware execution
    ├── hardware.py       CPU/GPU/memory detection
    ├── model_cache.py    sentence-transformers + vision-model cache
    └── gpu_memory.py     GPU memory budgeter
```

## Install

`clio` is published on the public GitLab mirror at <https://gitlab.com/perlowja/clio>. Install from source for now (PyPI publication will follow v0.1.0).

```bash
git clone https://gitlab.com/perlowja/clio.git
cd clio
uv sync
```

Or as a dependency in another project:

```toml
# pyproject.toml
dependencies = [
    "clio @ git+https://gitlab.com/perlowja/clio.git@v0.0.1-rc1-bootstrap",
]
```

## Quick start: vision extraction

```python
from clio.extract.vision import extract

result = extract(
    pdf_path="/path/to/document.pdf",
    prompt='''Extract all entities mentioned in this document.
              Return JSON of shape: {"entities": [{"name": str, "role": str}]}''',
    model="claude-sonnet-4-6",
    max_pages=5,
)

if result.succeeded:
    print(result.data["entities"])
    print(f"Confidence: {result.confidence.value} (method: {result.confidence.method})")
```

The prompt and schema are caller-supplied. `clio.extract.vision` is a foundation primitive that takes a document, sends pages to a vision-capable LLM via `litellm`, and parses JSON out of the response. Domain knowledge (broker statement formats, license filing schemas, restaurant menu structures) lives in the calling library, not here.

Provider routing is litellm-shaped. Pass any vision-capable model string:

- `claude-sonnet-4-6`
- `openai/gpt-4o`
- `vertex_ai/gemini-2.5-pro`

Set `CLIO_VISION_API_KEY` (or pass `api_key=` directly), or use the provider's native env var that litellm picks up (`ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, etc.).

## Hardware detection

```python
from clio.runtime.hardware import HardwareProfile

hw = HardwareProfile()
print(hw)  # human-readable summary

if hw.can_use_gpu(min_free_memory_gb=5.0):
    # use sentence-transformers / vision LLM with GPU
    ...
```

Detects NVIDIA, AMD ROCm, Intel Arc/iGPU, and Apple Metal with unified-memory awareness.

## Methodology

`clio` is the implementation of the AI-driven semantic-ETL methodology covered by the Tina agreement (Feb 2026 DocuSign F5124E6D-...): semantic validation, automated extraction, transformation, and loading. The library is the public face of that methodology — published Apache 2.0 so the substrate is a contributable open core, with domain libraries (`ic-engine`, `etlantis`) and adapters (`InvestorClaw`, `RiskyEats`) layered on top per the consumer's deployment posture.

## License

Apache 2.0. See [LICENSE](./LICENSE).

## Contributing

Source-of-truth bare repo: `root@argonas:/mnt/datapool/git/clio.git` (internal). Public mirror: <https://gitlab.com/perlowja/clio>. Pull requests via GitLab merge requests.

Commit author convention: `Jason Perlow <jperlow@gmail.com>`. Pre-commit: run `ruff check --fix && ruff format` before committing.
