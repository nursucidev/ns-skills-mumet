"""V13 Feature Walkthrough written-policy contracts; not live-agent behavior tests."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
FEATURE = (ROOT/'skills/ns-new-feature/SKILL.md').read_text()
REVIEW = (ROOT/'skills/ns-review-diff/SKILL.md').read_text()
BUG = (ROOT/'skills/ns-fix-bug/SKILL.md').read_text()
IMPACT = (ROOT/'skills/ns-impact-map/SKILL.md').read_text()
RISK = (ROOT/'skills/ns-risk-review/SKILL.md').read_text()
AGENTS = (ROOT/'AGENTS.md').read_text()
RULES = (ROOT/'RULES.md').read_text()
README = (ROOT/'README.md').read_text()

class FeatureWalkthroughContracts(unittest.TestCase):
    def test_01_version_consistency(self):
        for p in ('README.md', 'AGENTS.md', 'RULES.md', 'TEST_REPORT.md'):
            self.assertRegex((ROOT/p).read_text().splitlines()[0],r'(?i)v13')

    def test_02_workflow_owned_by_new_feature(self):
        self.assertIn('## Adaptive Feature Walkthrough', FEATURE)
        self.assertIn('ns-new-feature', README)

    def test_03_inside_spec_before_plan(self):
        self.assertRegex(FEATURE, r'(?s)\*\*SPEC = what/why.*?Feature Walkthrough.*?\*\*PLAN = how/check')
        self.assertRegex(README, r'(?is)Feature Walkthrough.*spec\.md')

    def test_04_scope_adaptive(self):
        self.assertRegex(FEATURE, r'(?i)`LIGHT`[^\n]*?not mandatory')
        self.assertRegex(FEATURE, r'`STANDARD`.*?(?:feature|Feature Walkthrough)')
        self.assertIn('`CRITICAL`', FEATURE)

    def test_05_entry_actions_success_failure(self):
        for term in ('entry point', 'user action', 'success', 'failure', 'validation', 'resulting state'):
            self.assertIn(term, FEATURE.lower())

    def test_06_technology_neutral(self):
        for term in ('UI', 'API', 'CLI', 'background job'):
            self.assertIn(term, FEATURE)
        self.assertRegex(FEATURE, r'(?i)no.*(?:mandatory|forced).*wireframe')

    def test_07_no_unapproved_scope(self):
        self.assertRegex(FEATURE, r'(?i)do not invent.*(?:features|menus|fields|screens)')
        self.assertRegex(FEATURE, r'(?i)assumptions|unknowns')

    def test_08_link_to_acceptance_criteria(self):
        self.assertRegex(FEATURE, r'(?i)walkthrough.*?acceptance criteria')
        self.assertRegex(FEATURE, r'(?i)(?:acceptance criteria|criteria).*?tasks.*?tests')

    def test_09_crosscheck_after_implementation(self):
        self.assertRegex(FEATURE, r'(?i)(?:implementation|implemented).*?walkthrough')
        self.assertRegex(REVIEW, r'(?i)walkthrough.*?(?:implementation|implemented)|(?:implementation|implemented).*?walkthrough')

    def test_10_plan_no_duplicate_spec(self):
        self.assertRegex(FEATURE, r'(?i)plan.*?(?:refer|link).*?walkthrough')
        self.assertRegex(FEATURE, r'(?i)(?:avoid|without|do not).*?(?:duplicat|repeat).*?(?:spec|walkthrough)')

    def test_11_separate_file_optional(self):
        self.assertIn('feature-flow.md', FEATURE)
        self.assertRegex(FEATURE, r'(?i)only.*?(?:complex|large)|optional.*?(?:complex|large)')

    def test_12_plan_only_not_forced_to_create_spec(self):
        self.assertRegex(FEATURE, r'(?i)plan-only.*?not.*?(?:force|require|create).*?spec')

    def test_13_global_authority_consistent(self):
        self.assertIn('Adaptive Feature Walkthrough', AGENTS)
        self.assertIn('Feature Walkthrough', RULES)
        self.assertRegex(AGENTS, r'(?i)spec.*?walkthrough.*?plan')

    def test_14_other_skills_no_forced_new_spec(self):
        self.assertIn('Feature Walkthrough', BUG)
        self.assertIn('Feature Walkthrough', IMPACT)
        self.assertIn('Feature Walkthrough', RISK)
        self.assertRegex(BUG, r'(?i)no.*(?:mandatory|new).*?(?:walkthrough|feature spec)')

    def test_15_readme_concrete_example(self):
        for term in ('Add User', 'duplicate', 'password', 'failure', 'spec.md', 'plan.md'):
            self.assertIn(term.lower(), README.lower())

    def test_16_no_new_skill_or_full_ux_document_ritual(self):
        self.assertRegex(README, r'(?i)not.*(?:sixth|new) skill')
        self.assertRegex(RULES, r'(?i)no.*(?:mandatory|forced).*?(?:mockup|wireframe|new file)')

if __name__ == '__main__': unittest.main()
