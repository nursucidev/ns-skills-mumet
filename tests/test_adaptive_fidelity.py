"""V10 technology-neutral scenario contracts, not live-agent behavior tests."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
AG = ROOT / 'AGENTS.md'
RULES = ROOT / 'RULES.md'
README = ROOT / 'README.md'
SKILLS = tuple(sorted((ROOT / 'skills').glob('*/SKILL.md')))


def read(path):
    return path.read_text(encoding='utf-8')


class AdaptiveFidelityScenarios(unittest.TestCase):
    def contains(self, file, pattern):
        self.assertRegex(read(file), pattern, f'{file} must include: {pattern}')

    def all_skills(self, pattern):
        for path in SKILLS:
            with self.subTest(skill=path.parent.name):
                self.contains(path, pattern)

    def test_01_unfamiliar_stack_detect_before_choosing_solution(self):
        self.contains(AG, r'Discover, never assume.*Identify the actual language')
        self.contains(RULES, r'never assume a stack')
        self.all_skills(r'Discover the real language\(s\).*never assume a stack')

    def test_02_project_without_framework_is_first_class(self):
        self.contains(AG, r'For a framework-free project')
        self.contains(RULES, r'Framework-free projects')
        self.all_skills(r'No-framework projects')

    def test_03_mixed_project_respects_each_boundary(self):
        self.contains(AG, r'Different modules may have different conventions')
        self.contains(README, r'Mixed or unfamiliar stack')

    def test_04_native_shortcut_cannot_replace_supported_framework_pattern(self):
        self.contains(AG, r'over replacing them with a native/custom bypass merely because')
        self.contains(RULES, r'over native/custom bypasses done merely for brevity')
        self.all_skills(r'Do not bypass a framework or replace project architecture with native/custom code only for brevity or assumed speed')

    def test_05_project_file_roles_and_lifecycle_are_protected(self):
        self.contains(AG, r'file roles, lifecycle hooks')
        self.contains(RULES, r'file roles')
        self.all_skills(r'project structure, file roles, supported framework integration/lifecycle')

    def test_06_existing_code_reused_before_new_library_or_wrapper(self):
        self.contains(AG, r'Choose the smallest \*complete\* change, in order:.*reuse existing project code')
        self.all_skills(r'Prefer existing project code/patterns, then compatible framework/platform facilities')

    def test_07_correctness_outranks_line_count(self):
        self.contains(AG, r'Smallest diff is a preference.*after.*correctness')
        self.contains(README, r'outrank raw line count')

    def test_08_native_code_remains_available_when_justified(self):
        self.contains(AG, r'Native and low-level code is not forbidden')
        self.contains(RULES, r'Native/low-level code is allowed when')
        self.all_skills(r'Native/low-level code remains valid when idiomatic')

    def test_09_integration_or_data_layout_cannot_be_changed_silently(self):
        self.contains(AG, r'Never silently migrate implementation style, lifecycle, storage format, or architecture')
        self.contains(RULES, r'Do not silently change architecture or data format')

    def test_10_performance_optimization_is_allowed_and_measured_when_practical(self):
        self.contains(AG, r'Performance is a valid goal, not a bypass')
        self.contains(AG, r'before/after measure when practicable')
        self.all_skills(r'compare results when practical')

    def test_11_unproven_speedup_is_not_reported_as_verified(self):
        self.contains(AG, r'If measurement is unavailable, label performance as unverified')
        self.contains(RULES, r'Unmeasured claims stay unverified')
        self.all_skills(r'label unmeasured gains unverified')

    def test_12_requested_architecture_redesign_is_not_accidentally_forbidden(self):
        self.contains(AG, r'deliberate cross-boundary redesign requires task authorization')
        self.contains(RULES, r'cross-boundary redesign needs authorized scope')
        self.all_skills(r'deliberate architecture/data-format deviation requires authorized scope')

    def test_13_review_checks_native_bypass_and_speed_claims(self):
        self.contains(ROOT / 'skills/ns-review-diff/SKILL.md', r'reject unsupported native/custom bypasses')
        self.contains(ROOT / 'skills/ns-review-diff/SKILL.md', r'performance claims against measurements')

    def test_14_impact_map_and_risk_review_consider_architecture_and_speed(self):
        self.contains(ROOT / 'skills/ns-impact-map/SKILL.md', r'framework/project lifecycle points')
        self.contains(ROOT / 'skills/ns-risk-review/SKILL.md', r'claimed speedup cannot excuse broken conventions/contracts')

    def test_15_parent_is_only_path_for_consequential_exceptions(self):
        self.contains(AG, r'obtain a consequential exception decision through the parent')
        self.all_skills(r'escalates consequential exceptions only to its caller')

    def test_16_gate_does_not_add_a_skill_or_force_stack_specific_tests(self):
        self.assertEqual(len(SKILLS), 5)
        self.contains(AG, r'not.*a new skill, mandatory checklist, or extra agent')
        self.contains(README, r'not a predefined language-specific test list')
        self.contains(AG, r'No blanket number of tests')


if __name__ == '__main__':
    unittest.main(verbosity=2)
