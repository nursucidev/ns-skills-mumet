---
name: ns-risk-review
description: Assess realistic software change risks for security, privacy, durable data, APIs, concurrency, reliability, performance, and deployment. Use before high-impact changes or when a bug could cause serious loss or outages.
---
# NS Risk Review

## Agent role, STOP, and reporting (self-contained)
- **Role:** parent = main agent serving user; subagent = separately delegated worker, including nested workers. Loading this skill never changes role. A subagent **MUST NOT** ask/contact/notify the user, request approval, or invoke user-facing input tools. Report only to the calling agent, which relays upward.
- **Canonical STOP:** If delegated work cannot safely continue because proceeding risks credible major harm or unauthorized production/destructive/data/secrets/cost effects, or needs a consequential decision with no safe authorized default: **STOP the entire delegated task immediately**, including optional work; report evidence (redact secrets), impact, safe options, decision/permission needed and unfinished work **only to caller**; **END**. Never ask/wait for user. A severe finding during an authorized safely continuing read-only review is not automatically a task blocker; finish the review and use `review_verdict: BLOCK` if warranted. A CRITICAL risk rating alone is not a STOP trigger.
- **Report:** only subagents use compact `task_status`, `result`, `evidence/check_results`, `findings`, `decisions_needed`, `remaining`, plus `review_verdict` for reviews. `task_status` is work progress (`COMPLETED`, `PARTIAL`, `BLOCKED`), separate from check results (`PASS`, `FAIL`, `NOT_RUN`, `BLOCKED`, `INCONCLUSIVE`, `PRE_EXISTING_FAIL`) and review verdict (`BLOCK`, `FIX`, `NO_FINDINGS`). Parent follows the user's format.

## Ownership and read-only boundary
Risk assessment only, focusing on plausible high-impact scenarios. Do not edit code or duplicate a full dependency map/diff review. Inspect existing evidence.

**Read-only boundary:** preserve original workspace/Git state, user data, production and remote systems unchanged. Do not run tools **there** that may write files, caches, logs, databases, or remote state. A requested review permits **safe local disposable sandbox checks without extra approval** only within that request's scope: create the scratch copy **outside the original workspace**, isolate shared caches, symlinks, credentials, volumes, sockets and live network/services, and clean up only the scratch. No production/network writes, spending, destructive work, unknown installers or access beyond task scope is implied. Honor explicit no-execution/no-write restrictions. If effects or isolation are uncertain, do not execute; mark `NOT_RUN` or `BLOCKED` with evidence. Never claim unrun checks passed.

## Adaptive fidelity & minimal-complete-change gate (self-contained)
- Discover the real language(s), framework/toolchain **if any**, architecture, conventions, and affected contracts from the project; never assume a stack. No-framework projects use their established style and idiomatic platform/language mechanisms.
- Preserve established project structure, file roles, supported framework integration/lifecycle, behavior and contracts. Prefer existing project code/patterns, then compatible framework/platform facilities, then installed dependencies, then minimal readable custom code; omit unneeded scope and avoid speculative abstractions/dependencies. **Do not bypass a framework or replace project architecture with native/custom code only for brevity or assumed speed.**
- Native/low-level code remains valid when idiomatic, supported within the project mechanism, or justified by an authorized unmet need. A deliberate architecture/data-format deviation requires authorized scope and proportionate compatibility/regression checks. For performance work, confirm a bottleneck and compare results when practical; optimize within conventions first, preserve safety/correctness, and label unmeasured gains unverified. A delegated worker escalates consequential exceptions only to its caller.

## Test-first evidence awareness (read-only, not an implementation gate)
- For applicable behavioral changes, note whether a focused RED pre-change failure, GREEN post-change pass, and REFACTOR regression recheck are available; missing evidence is a coverage gap, not an invented code defect. Do not require test-first for untestable/cosmetic/performance-only tasks; performance may use baseline and comparable measurements. Examine only genuinely affected behavior and avoid assuming test tooling or framework.
- Never create tests in the protected original project during this read-only assignment. Safe isolated scratch checks are allowed only within the stated read-only boundary. Preserve subagent reporting and STOP rules.

## Procedure
Inspect only risk categories genuinely relevant to the actual system:
- Correctness: invariants, malformed inputs, boundary cases, time, encoding, numeric handling.
- Failure recovery: partial operations, retries, idempotency, timeouts, backups, restore paths.
- Data/contracts: persistence, migrations, schemas, API/ABI, file formats, older clients and compatibility; changes to prior behavior and data invariants (regression risks).
- Security/privacy: authentication, authorization, injection, secrets, supply chain, sensitive data handling.
- Concurrency: races, locking, message ordering, background jobs, reentrancy where applicable.
- Performance: CPU, RAM, I/O, latency, scaling, quotas and failure under load. Ask for representative bottleneck/benchmark evidence when practicable; a claimed speedup cannot excuse broken conventions/contracts or an unapproved redesign.
- Operations: rollout, rollback, monitoring, user/process/tenant isolation only where present.

Prioritize a small set of material risks; present each as `scenario -> consequence -> evidence/confidence -> mitigation -> verification`. For code-change readiness, explicitly state which existing behaviors/contracts need regression coverage; identify whether any pre-existing failures or untested boundaries limit confidence. A safe rollout/rollback check may be required before CRITICAL deployment, but do not run destructive recovery experiments in production. Do not speculate about missing infrastructure. If only analyzing risk, finish safe analysis and report serious findings to the calling agent when delegated, or to the user when acting as parent. Reserve `task_status: BLOCKED` for unsafe continuation, not the severity of a finding. When release readiness is explicitly requested, distinguish `review_verdict: BLOCK | FIX | NO_FINDINGS` (findings) from `release_readiness: READY | HOLD | UNDETERMINED | NOT_ASSESSED` (required gates/evidence). A mandatory missing check means HOLD, not a fabricated code defect. Otherwise return risk findings without forcing a verdict. A subagent uses the compact internal report; a parent responds in the user’s preferred format.

## Future failure / latent defect focus
Apply the shared adaptive future-failure gate to changed and affected paths. Where relevant, assess concurrency (races/deadlocks/lock contention), lifecycle leaks/unclosed resources, async rejection/hangs, timeouts/retry storms/duplicate work, lost updates/partial writes, queue backlog/starvation/stuck workers, memory/CPU/N+1 growth, crash/restart recovery, compatibility and input/session/time boundaries. Trace realistic triggers and consequences; distinguish `CONFIRMED`, `POTENTIAL`, `UNVERIFIED`. Recommend minimal safe falsifiable tests, label unrun checks, and report residual risks. Do not mandate exhaustive categories, heavy tests or unauthorized fixes. This remains read-only and does not duplicate the owner's implementation/review.
