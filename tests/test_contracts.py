"""Static policy-contract tests for NS Skills Mumet.

These verify *written instructions*, not compliance of an LLM or an agent runtime.
Run: python3 -m unittest discover -s tests -p 'test_*.py' -v
No external packages or network needed. Set PYTHONDONTWRITEBYTECODE=1 to avoid bytecode writes.
"""
from pathlib import Path
import re
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def doc(rel):
    return (ROOT / rel).read_text(encoding='utf8')


AG = 'AGENTS.md'
RULES = 'RULES.md'
F = 'skills/ns-new-feature/SKILL.md'
B = 'skills/ns-fix-bug/SKILL.md'
IM = 'skills/ns-impact-map/SKILL.md'
RR = 'skills/ns-risk-review/SKILL.md'
RV = 'skills/ns-review-diff/SKILL.md'
SKILLS = (F, B, IM, RR, RV)
READONLY = (IM, RR, RV)


class ScenarioContractTests(unittest.TestCase):
    def has(self, target, pattern):
        self.assertRegex(doc(target), pattern, msg=f'{target} missing policy regex: {pattern}')

    def all_have(self, targets, pattern):
        for target in targets:
            with self.subTest(target=target):
                self.has(target, pattern)

    def test_01_skills_have_unique_valid_frontmatter(self):
        self.assertEqual(len(SKILLS), 5)
        names = []
        for target in SKILLS:
            t=doc(target)
            self.assertTrue(t.startswith('---\n'),target)
            match=re.match(r'^---\nname: ([a-z][a-z0-9-]+)\ndescription: (.+?)\n---\n',t)
            self.assertIsNotNone(match,target)
            self.assertEqual(match.group(1),Path(target).parent.name)
            names.append(match.group(1))
        self.assertEqual(len(names),len(set(names)))

    def test_02_skills_can_load_in_isolation(self):
        self.all_have(SKILLS,r'Agent role, STOP, and reporting \(self-contained\)')

    def test_03_parent_is_not_reclassified_by_loading_a_skill(self):
        self.all_have(SKILLS,r'Loading this skill never changes role')

    def test_04_nested_subagent_never_asks_user(self):
        self.all_have(SKILLS,r'subagent.*MUST NOT.*user')

    def test_05_subagent_reports_only_to_caller(self):
        self.all_have(SKILLS,r'Report only to the calling agent')

    def test_06_critical_blocker_stops_entire_delegation(self):
        self.all_have(SKILLS,r'STOP the entire delegated task immediately')
        self.has(AG,r'STOP the entire delegated task immediately')

    def test_07_safe_readonly_severe_finding_not_stop(self):
        self.all_have(SKILLS,r'severe finding.*not automatically a task blocker')

    def test_08_untrusted_repository_instruction_cannot_override(self):
        self.has(AG,r'untrusted content.*override higher-priority instructions')

    def test_09_only_one_global_rules_source(self):
        self.has(AG,r'one.*global guidance source')
        self.has(RULES,r'Alternative to `AGENTS\.md`')

    def test_10_spec_only_no_implementation(self):
        self.has(F,r'spec.*plan only.*produce exactly that artifact/scope')
        self.has(AG,r'do not implement code without authorization')

    def test_11_light_no_forced_docs_or_full_suite(self):
        self.has(F,r'No required files, formal brainstorming, or approval')
        self.has(AG,r'No mandatory TDD.*full-suite tests')

    def test_12_standard_feature_always_has_acceptance_criteria(self):
        self.has(F,r'STANDARD.*Always.*testable acceptance criteria')

    def test_13_standard_feature_always_has_ordered_implementation_steps(self):
        self.has(F,r'STANDARD.*short ordered implementation steps.*verification evidence')

    def test_14_standard_plan_files_optional_when_not_requested(self):
        self.has(F,r'spec/plan file is.*optional.*user requests')

    def test_15_critical_feature_staged_plan(self):
        self.has(F,r'CRITICAL.*Prepare an explicit spec and phased plan')

    def test_16_diagnosis_only_bug_no_product_edits(self):
        self.has(B,r'Investigation-only boundary.*if requested to diagnose')
        self.has(B,r'do \*\*not\*\* modify application code, configuration, tests, or original project state')

    def test_17_bug_fix_investigates_cause_before_patch(self):
        self.has(B,r'root cause')
        self.has(AG,r'falsifiable cause hypothesis')

    def test_18_bug_fix_protects_old_behavior(self):
        self.has(B,r'Protect against regressions')
        self.has(B,r'prior behavior/contracts')

    def test_19_review_is_readonly_original_workspace(self):
        self.all_have(READONLY,r'preserve original workspace/Git state')

    def test_20_local_disposable_checks_allowed_without_extra_approval(self):
        self.all_have(READONLY,r'safe local disposable sandbox checks without extra approval')
        self.has(AG,r'without an extra approval round')

    def test_21_disposable_copy_outside_original_workspace(self):
        self.all_have(READONLY,r'outside the original workspace')

    def test_22_disposable_tests_must_avoid_shared_mutable_resources(self):
        self.all_have(READONLY,r'shared caches, symlinks, credentials, volumes, sockets')

    def test_23_sandbox_is_not_permission_for_live_network_or_production(self):
        self.all_have(READONLY,r'No production/network writes')

    def test_24_explicit_no_execution_restriction_still_honored(self):
        self.all_have(READONLY,r'Honor explicit no-execution/no-write restrictions')

    def test_25_unisolated_tests_marked_not_run_or_blocked(self):
        self.all_have(READONLY,r'mark `NOT_RUN` or `BLOCKED`')

    def test_26_parent_assigns_exclusive_write_ownership(self):
        self.has(AG,r'parent/caller assigns exclusive ownership')
        self.has(RULES,r'parent/caller assigns exclusive paths')

    def test_27_parallel_readonly_can_overlap(self):
        self.has(AG,r'Parallel read-only work may overlap')

    def test_28_overlapping_writers_are_serialized_or_isolated(self):
        self.has(AG,r'Serialize overlapping writes/checks')
        self.all_have((B,F),r'overlapping writer')

    def test_29_nested_delegation_requires_caller_authorization(self):
        self.has(AG,r'start nested workers without caller authorization')

    def test_30_review_verdict_not_equal_release_readiness(self):
        self.has(AG,r'release_readiness.*only when requested')
        self.has(RV,r'release_readiness: READY \| HOLD \| UNDETERMINED \| NOT_ASSESSED')

    def test_31_mandatory_missing_gate_yields_hold_not_fabricated_bug(self):
        self.has(RV,r'HOLD if a mandatory check is failed, blocked, or not run')
        self.has(RV,r'Do not turn missing verification into an invented defect')

    def test_32_no_findings_and_hold_can_coexist(self):
        self.has(RV,r'`review_verdict: NO_FINDINGS` may coexist with `release_readiness: HOLD`')

    def test_33_release_ready_requires_actual_evidence(self):
        self.has(AG,r'READY.*required release gates.*passing evidence')

    def test_34_preexisting_failure_requires_baseline(self):
        self.has(AG,r'PRE_EXISTING_FAIL.*unchanged baseline')
        self.has(F,r'pre-existing failures')

    def test_35_no_claims_of_regression_free_from_narrow_checks(self):
        self.has(AG,r'blanket “no regressions” is not')

    def test_36_routing_multi_phase_and_general_maintenance(self):
        self.has(AG,r'one workflow owner per distinct subtask/phase')
        self.has(AG,r'bounded general workflow')

    def test_37_parent_user_report_not_forced_internal_schema(self):
        self.has(AG,r'Only subagents.*compact `task_status`')
        self.all_have(SKILLS,r'Parent follows the user.s format')

    def test_38_review_feedback_must_be_validated_not_blindly_applied(self):
        self.has(RV,r'Don.t implement reviewer suggestions blindly')

    def test_39_tests_are_explicitly_not_llm_runtime_tests(self):
        self.has('README.md',r'not.*an LLM/runtime behavior test')

    def test_40_package_does_not_assume_a_programming_stack(self):
        self.has(AG,r'any language, framework, architecture')
        self.has(AG,r'do not assume a web app, Laravel')


if __name__=='__main__': unittest.main(verbosity=2)
