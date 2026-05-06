import unittest
import json
import GaleShapley

class TestGaleShapley(unittest.TestCase):

    def setUp(self):

        with open("test_cases.json", 'r') as file:

            self.test_data = json.load(file)['GaleShapley']

    def test_Gale_Shapley_json(self):
        
        for i,case in enumerate(self.test_data):
            with self.subTest(msg= f"Gale Shapley Test n° {i}"):
                
                etu = case["etu"]
                spe = case["spe"]
                cap = case["cap"]
                
                exp_etu = case["res_etu"]
                exp_spe = case["res_spe"]

                res_etu,i = GaleShapley.GaleShapleyCoteEtudiant(etu,spe,cap)
                res_spe = GaleShapley.GaleShapleyCoteParcours(etu, spe, cap)
                
                self.assertEqual(exp_etu, res_etu)
                self.assertEqual(exp_spe, res_spe)

class TestUnstablePairs(unittest.TestCase):

    def setUp(self):

        with open("test_cases.json", 'r') as file:

            self.test_data = json.load(file)['UnstablePairs']

    def test_unstable_pairs(self):
        
        for i,case in enumerate(self.test_data):
            with self.subTest(msg= f"Unstable Pairs n°{i}"):
                
                etu = case["etu"]
                spe = case["spe"]
                affec = case['affec']

                exp_res = set(tuple(p) for p in case['unstable'])

                unstable = GaleShapley.paires_instables(spe, etu, affec)
                
                self.assertEqual(exp_res, unstable)

if __name__ == '__main__':
    unittest.main()