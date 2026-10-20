## Summary

Describe the public change and the problem it solves.

## Evidence

List the validation performed and, where relevant, distinguish expected evaluation behavior from observed results.

## Public-safety checklist

- [ ] The diff contains no credentials, private paths, customer data, sensitive transcripts, or internal planning material.
- [ ] Examples are synthetic and sources are attributable.
- [ ] Installation, compatibility, evaluation, and release claims are backed by evidence in this change.
- [ ] `python scripts/validate_repo.py .` passes.
- [ ] `python -m unittest discover -s tests -v` passes.
