from pathlib import Path
import unittest
ROOT = Path(__file__).resolve().parents[1]
class FutureFailurePolicy(unittest.TestCase):
    def test_shared_gate(self):
        for f in ['AGENTS.md','RULES.md','skills/ns-risk-review/SKILL.md','skills/ns-new-feature/SKILL.md','skills/ns-fix-bug/SKILL.md','skills/ns-review-diff/SKILL.md']:
            with self.subTest(file=f):
                s=(ROOT/f).read_text()
                self.assertTrue('future failure' in s.lower() or 'future-failure' in s.lower())
                for state in ('CONFIRMED','POTENTIAL','UNVERIFIED'): self.assertIn(state,s)
    def test_risk_categories(self):
        s=(ROOT/'AGENTS.md').read_text().lower()
        for x in ('deadlocks','unclosed streams','retry storms','lost updates','starvation','n+1','restart','timezones'):
            with self.subTest(category=x): self.assertIn(x,s)
    def test_no_extra_skill(self):
        self.assertEqual(len(list((ROOT/'skills').glob('*/SKILL.md'))),5)
if __name__=='__main__': unittest.main()
