"""V11 adaptive RED-GREEN-REFACTOR written-policy tests; NOT live-agent evals."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
AG = ROOT / 'AGENTS.md'
RULES = ROOT / 'RULES.md'
README = ROOT / 'README.md'
F = ROOT / 'skills/ns-new-feature/SKILL.md'
B = ROOT / 'skills/ns-fix-bug/SKILL.md'
RV = ROOT / 'skills/ns-review-diff/SKILL.md'
SKILLS = sorted((ROOT / 'skills').glob('*/SKILL.md'))

def read(path):
    return path.read_text(encoding='utf8')

class AdaptiveRedGreenRefactor(unittest.TestCase):
    def has(self, path, regex):
        self.assertRegex(read(path), regex, str(path))

    def test_01_parent_canonical_cycle(self):
        self.has(AG, r'RED.*GREEN.*REFACTOR')
        self.has(RULES, r'RED.*GREEN.*REFACTOR')

    def test_02_technology_neutral_no_hardcoded_test_stacks(self):
        self.has(AG, r'language.*framework.*agnostic')
        self.has(AG, r'project.s existing test tools')

    def test_03_red_precedes_product_change(self):
        self.has(AG, r'RED.*before.*implementation')
        self.has(F, r'RED.*before.*implementation')

    def test_04_red_must_fail_for_right_reason(self):
        self.has(AG, r'fail for the expected behavioral reason')
        self.has(F, r'fail for the expected behavioral reason')
        self.has(B, r'fail for the expected behavioral reason')

    def test_05_green_smallest_compatible_fix(self):
        self.has(AG, r'GREEN.*smallest.*project conventions')
        self.has(F, r'GREEN.*smallest.*project conventions')
        self.has(B, r'GREEN.*smallest.*project conventions')

    def test_06_refactor_not_obligatory_and_retest(self):
        self.has(AG, r'REFACTOR.*only if beneficial.*rerun')
        self.has(F, r'REFACTOR.*only if beneficial.*rerun')
        self.has(B, r'REFACTOR.*only if beneficial.*rerun')

    def test_07_light_is_not_heavy_ceremony(self):
        self.has(AG, r'LIGHT.*optional.*smallest meaningful check')
        self.has(F, r'LIGHT.*optional.*smallest meaningful check')

    def test_08_standard_behavior_prioritizes_red_green(self):
        self.has(AG, r'STANDARD.*testable behavior.*prefer.*RED')
        self.has(F, r'STANDARD.*testable behavior.*prefer.*RED')
        self.has(B, r'STANDARD.*testable behavior.*prefer.*RED')

    def test_09_critical_validates_risks_without_unsafe_tests(self):
        self.has(AG, r'CRITICAL.*safe.*isolated.*risk')
        self.has(F, r'CRITICAL.*safe.*isolated.*risk')
        self.has(B, r'CRITICAL.*safe.*isolated.*risk')

    def test_10_no_fake_red_no_broken_existing_tests(self):
        self.has(AG, r'Never manufacture a RED failure')
        self.has(AG, r'do not weaken or disable tests')

    def test_11_no_test_harness_or_unsafe_run_exception(self):
        self.has(AG, r'If a meaningful executable RED is unavailable')
        self.has(RULES, r'RED is unavailable')
        self.has(F, r'RED is unavailable')
        self.has(B, r'RED is unavailable')

    def test_12_documents_and_analyses_not_forced_product_tdd(self):
        self.has(AG, r'spec-only.*plan-only.*read-only')
        self.has(RULES, r'spec-only.*plan-only.*read-only')

    def test_13_readonly_does_not_create_tests_in_original_project(self):
        self.has(RV, r'RED.*read-only.*scratch')

    def test_14_bug_root_cause_then_reproducer(self):
        self.has(B, r'root.cause.*RED.*reproducer')

    def test_15_regression_checks_survive_refactor(self):
        self.has(AG, r'REFACTOR.*existing.*regression')
        self.has(RV, r'RED.*GREEN.*REFACTOR')

    def test_16_maintainer_skills_testing_distinct_from_code(self):
        self.has(README, r'Skill-author RED.*baseline.*without.*rule')
        self.has(README, r'not proof of live-agent compliance')

    def test_17_update_instructions_manual_upgrade(self):
        self.has(README, r'Updating an existing CLI installation')
        self.has(README, r'back up')
        self.has(README, r'replace.*five.*skill')
        self.has(README, r'global guidance.*merge')

    def test_18_do_not_assume_cli_install_location(self):
        self.has(README, r'actual installed skills directory')
        self.has(README, r'restart.*reload')

    def test_19_all_five_independent_skill_pages_remain_self_contained(self):
        self.assertEqual(len(SKILLS), 5)
        for page in SKILLS:
            self.has(page, r'Agent role, STOP, and reporting \(self-contained\)')
            self.has(page, r'Adaptive fidelity & minimal-complete-change gate')

    def test_20_performance_does_not_require_artificial_failing_benchmark(self):
        self.has(AG, r'Performance.*baseline.*do not invent a failing test')
        self.has(README, r'performance.*baseline.*comparison')

if __name__ == '__main__':
    unittest.main(verbosity=2)
