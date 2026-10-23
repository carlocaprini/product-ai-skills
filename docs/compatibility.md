# Compatibility and installation evidence

## Current verified status

The repository packages are structurally validated. All four packages also have anonymous public-origin extraction and scoped Codex CLI routing evidence:

| Package | Immutable public commit | Client | Observed checks |
| --- | --- | --- | --- |
| `review-product-decision` | `5acb3900a7dab7c638b5a35dc0a71abdd2694761` | Codex CLI `0.163.0-alpha.11.1` | standalone validation; one positive activation and one near miss |
| `assess-agent-autonomy` | `33a67ee942f02780981c8d526f4251ccc1967078` | Codex CLI `0.163.0-alpha.10.2` | standalone validation; one positive activation and one near miss |
| `review-api-product-change` | `585a7fc59bbd21671ceb67be086938a6010c6df2` | Codex CLI `0.163.0-alpha.11.1` | standalone validation; one positive activation and one near miss |
| `evaluate-ai-feature` | `1693662a2f3bac4fad57c8b5d901f7e894946253` | Codex CLI `0.163.0-alpha.11.1` | standalone validation; one positive activation and one near miss |

All named-client checks ran on macOS 15.7.7 (x86_64). The `0.163.0-alpha.11.1` checks used fresh ephemeral workspaces, read-only sandboxes, disabled web search, disabled apps/plugins/memories and bundled skills, and explicit disable entries for detected personal skills. Command traces established target-skill reads and near-miss non-reads.

The verified public-source installation procedure was:

```sh
mkdir -p .agents/skills
curl -fsS -o source.tar.gz \
  https://codeload.github.com/carlocaprini/product-ai-skills/tar.gz/33a67ee942f02780981c8d526f4251ccc1967078
tar -xzf source.tar.gz -C .agents/skills --strip-components=2 \
  product-ai-skills-33a67ee942f02780981c8d526f4251ccc1967078/skills/assess-agent-autonomy
```

For the other verified packages, substitute the immutable commit and final package name in the URL and extraction path above. This is evidence only for each recorded package revision and named client version. It is not a release, a promise about later revisions, or a cross-client compatibility claim. Complete procedures, hashes, routing observations, captured outputs, and limitations are recorded in the evaluation evidence for [`review-product-decision`](../skills/review-product-decision/tests/evals.md), [`assess-agent-autonomy`](../skills/assess-agent-autonomy/tests/evals.md), [`review-api-product-change`](../skills/review-api-product-change/tests/evals.md), and [`evaluate-ai-feature`](../skills/evaluate-ai-feature/tests/evals.md).

## Evidence required for a claim

An installation or compatibility statement must be backed by a reproducible record that includes:

- the immutable repository commit tested;
- the exact package path;
- the client name and exact version;
- the operating environment relevant to the result;
- the command or manual installation steps used;
- the installed files and package boundary observed;
- a positive activation case and a negative or near-miss case;
- the verification date, outcome, reviewer, and limitations.

Claims are scoped to the recorded client and version. Conformance to the Agent Skills file format, successful installation, correct routing, behavioral quality, and cross-client compatibility are separate facts.

Commands, badges, support tables, and directory listings must not be published as working examples until they have been tested against the public repository state they reference.
