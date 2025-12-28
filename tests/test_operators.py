import unittest
from codex_operators import cubic_inverse, sovereign_deflate, has_sovereign_signature, CANONICAL, CUBIC

class TestCodexOperators(unittest.TestCase):
    def test_cubic_inverse(self):
        y = CUBIC['PI']
        recovered = cubic_inverse(y)
        self.assertAlmostEqual(recovered, CANONICAL['PI'], places=10)

    def test_sovereign_deflate(self):
        y = CUBIC['PI']
        recovered = sovereign_deflate(y)
        self.assertAlmostEqual(recovered, CANONICAL['PI'], places=10)

    def test_signature(self):
        self.assertTrue(has_sovereign_signature(CUBIC['PI'], CANONICAL['PI']))

if __name__ == '__main__':
    unittest.main()