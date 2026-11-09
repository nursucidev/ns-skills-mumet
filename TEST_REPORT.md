# ns-skills-mumet v11 — Test Report

**Date:** 2026-11-09  
**Scope:** static policy contracts + isolated local sandbox demonstrations, not live-agent compliance.  
**Package under test:** V11 after adaptive RED–GREEN–REFACTOR addition and CLI upgrade instructions.

## Summary

- **80/80 tests passed** with Python standard-library `unittest` (no extra dependencies).
- Tests include **40** existing policy contracts, **16** adaptive project fidelity contracts, **20** new adaptive RED–GREEN–REFACTOR/CLI update contracts, and **4** local disposable-sandbox demonstration tests.
- **RED baseline before V11 instructions:** 19/20 new TDD/upgrade tests failed against extracted V10; one structural package-invariance test already passed. This is an observed static-policy RED, **not** a live-model behavior baseline.
- **GREEN:** after V11 instructions and tests were integrated, all 80 passed.
- **REFACTOR/negative controls:** all three intentionally weakened disposable copies were detected by the test suite (exit nonzero). These copies were isolated and do not change the deliverable.

## Representative technology-neutral scenarios

1. Testable behavior has a real RED before implementation, GREEN after minimal compatible change.
2. The observed RED failure must reflect the expected behavior, not an unrelated setup failure.
3. LIGHT work avoids mandatory testing ceremony when a narrow safe check suffices.
4. STANDARD favors the RED/GREEN sequence only for meaningful testable behavior.
5. CRITICAL uses safe isolated and risk-proportionate evidence; no dangerous experiments for a red test.
6. REFACTOR is optional and reruns genuinely affected tests/contracts when used.
7. No manufactured RED failures, intentionally broken production code, or disabled tests.
8. Without safe executable RED, report accurate NOT_RUN/BLOCKED/INCONCLUSIVE and alternative checks.
9. No product modification for spec-only, plan-only, diagnosis-only, or read-only tasks.
10. Bug root-cause evidence and minimal reproduction precede the fix when feasible.
11. Read-only reviews check test-first evidence but never write in protected workspace.
12. Performance work compares real baseline/after metrics and retains correctness checks without fake RED.
13. No assumed language, framework, mandated testing library, test count, or added workers.
14. Parent/subagent boundaries and all five independent skills remain intact.
15. Existing CLI upgrades use discovered actual paths, backup, selective five-skill replacement, and careful global-guidance merge.

## Negative mutation tests (isolated copies)

- Removed the adaptive TDD gate from `RULES.md` → test failure detected.
- Replaced the feature RED correctness requirement → test failure detected.
- Removed the upgrade guide heading → test failure detected.

## Commands

```sh
# From the unpacked ns-skills-mumet directory
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py' -q
```

Observed: `Ran 80 tests ... OK`.

## Limits

- Tests inspect the **written policy**, not agent choices or actual adherence in a live CLI runtime.
- No real delegated agent, nested agent, CLI installation/upgrade, or language-specific application project was executed.
- Explicit tests for real agent decisions, plugin-discovery behavior and production regressions remain runtime-dependent.
- The test-first baseline was a **policy-contract baseline**, not proof that an LLM ignored V10 or complied with V11.
- Documentation-level instructions cannot technically enforce sandbox boundaries; the selected agent runtime must enforce real permissions.

**Verdict:** V11 static contract and local sandbox tests PASS. Live-agent and real CLI upgrade validation NOT RUN.
