# Compatibility and installation evidence

## Current verified status

The repository packages are structurally validated. At immutable public commit `33a67ee942f02780981c8d526f4251ccc1967078`, `assess-agent-autonomy` was anonymously downloaded, extracted as a standalone package, and validated. The identical runtime bytes passed one positive activation and one near-miss routing check with Codex CLI `0.163.0-alpha.10.2` on macOS 15.7.7 (x86_64).

The verified public-source installation procedure was:

```sh
mkdir -p .agents/skills
curl -fsS -o source.tar.gz \
  https://codeload.github.com/carlocaprini/product-ai-skills/tar.gz/33a67ee942f02780981c8d526f4251ccc1967078
tar -xzf source.tar.gz -C .agents/skills --strip-components=2 \
  product-ai-skills-33a67ee942f02780981c8d526f4251ccc1967078/skills/assess-agent-autonomy
```

This is evidence for that package revision and named client version only. It is not a release, a promise about later revisions, or a cross-client compatibility claim. The complete procedure, hashes, routing observations, and limitations are recorded in [`skills/assess-agent-autonomy/tests/evals.md`](../skills/assess-agent-autonomy/tests/evals.md).

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
