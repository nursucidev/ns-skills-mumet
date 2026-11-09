---
name: ns-impact-map
description: Identify affected callers, dependencies, and compatibility contracts before code changes. Use when modifying shared modules, APIs, data schemas, build outputs, configuration, or behavior with unclear downstream impact.
---
# NS Impact Map

## Agent role, STOP, and reporting (self-contained)
- **Role:** parent = main agent serving user; subagent = separately delegated worker, including nested workers. Loading this skill never changes role. A subagent **MUST NOT** ask/contact/notify the user, request approval, or invoke user-facing input tools. Report only to the calling agent, which relays upward.
- **Canonical STOP:** If delegated work cannot safely continue because proceeding risks credible major harm or unauthorized production/destructive/data/secrets/cost effects, or needs a consequential decision with no safe authorized default: **STOP the entire delegated task immediately**, including optional work; report evidence (redact secrets), impact, safe options, decision/permission needed and unfinished work **only to caller**; **END**. Never ask/wait for user. A severe finding during an authorized safely continuing read-only review is not automatically a task blocker; finish the review and use `review_verdict: BLOCK` if warranted. A CRITICAL risk rating alone is not a STOP trigger.
- **Report:** only subagents use compact `task_status`, `result`, `evidence/check_results`, `findings`, `decisions_needed`, `remaining`, plus `review_verdict` for reviews. `task_status` is work progress (`COMPLETED`, `PARTIAL`, `BLOCKED`), separate from check results (`PASS`, `FAIL`, `NOT_RUN`, `BLOCKED`, `INCONCLUSIVE`, `PRE_EXISTING_FAIL`) and review verdict (`BLOCK`, `FIX`, `NO_FINDINGS`). Parent follows the user's format.

## Ownership and read-only boundary
Dependency/consumer mapping only. Do not edit code or conduct an entire risk/diff review. Inspect source and existing test evidence.

**Read-only boundary:** preserve original workspace/Git state, user data, production and remote systems unchanged. Do not run tools **there** that may write files, caches, logs, databases, or remote state. A requested review permits **safe local disposable sandbox checks without extra approval** only within that request's scope: create the scratch copy **outside the original workspace**, isolate shared caches, symlinks, credentials, volumes, sockets and live network/services, and clean up only the scratch. No production/network writes, spending, destructive work, unknown installers or access beyond task scope is implied. Honor explicit no-execution/no-write restrictions. If effects or isolation are uncertain, do not execute; mark `NOT_RUN` or `BLOCKED` with evidence. Never claim unrun checks passed.

## Adaptive fidelity & minimal-complete-change gate (self-contained)
- Discover the real language(s), framework/toolchain **if any**, architecture, conventions, and affected contracts from the project; never assume a stack. No-framework projects use their established style and idiomatic platform/language mechanisms.
- Preserve established project structure, file roles, supported framework integration/lifecycle, behavior and contracts. Prefer existing project code/patterns, then compatible framework/platform facilities, then installed dependencies, then minimal readable custom code; omit unneeded scope and avoid speculative abstractions/dependencies. **Do not bypass a framework or replace project architecture with native/custom code only for brevity or assumed speed.**
- Native/low-level code remains valid when idiomatic, supported within the project mechanism, or justified by an authorized unmet need. A deliberate architecture/data-format deviation requires authorized scope and proportionate compatibility/regression checks. For performance work, confirm a bottleneck and compare results when practical; optimize within conventions first, preserve safety/correctness, and label unmeasured gains unverified. A delegated worker escalates consequential exceptions only to its caller.

## Test-first evidence awareness (read-only, not an implementation gate)
- For applicable behavioral changes, note whether a focused RED pre-change failure, GREEN post-change pass, and REFACTOR regression recheck are available; missing evidence is a coverage gap, not an invented code defect. Do not require test-first for untestable/cosmetic/performance-only tasks; performance may use baseline and comparable measurements. Examine only genuinely affected behavior and avoid assuming test tooling or framework.
- Never create tests in the protected original project during this read-only assignment. Safe isolated scratch checks are allowed only within the stated read-only boundary. Preserve subagent reporting and STOP rules.

## Procedure
1. Identify the actual symbol, behavior, interface, schema, event, configuration, or output artifact and the proposed change.
2. Trace direct references with appropriate language tooling or targeted text search. Avoid a full-repository scan without a reason.
3. Map relevant framework/project lifecycle points, conventions, generated artifacts and architecture boundaries; native bypasses may break these even if output appears unchanged. Consider indirect consumers only when relevant: dependency injection, reflection, dynamic imports, plugins, generated code, serialization, database migrations, clients, integrations, and tests.
4. List **protected existing behaviors/invariants** for affected consumers (including error paths, earlier clients/versions and data formats when applicable). Describe credible regression scenarios and a small verification suggestion **only for actually or plausibly affected boundaries**; do not require an edge-case test for cosmetic-only edits. Separate observed consumers from plausible external ones; do not invent test names or coverage.
5. Deliver a compact `changed boundary -> existing consumer/behavior -> regression risk -> check/evidence` map, known pre-existing failures only if supported by an observed unchanged baseline, and remaining unknowns. Never claim exhaustive coverage without evidence.
