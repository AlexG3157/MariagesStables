import unittest
import json
import GaleShapley

class TestGaleShapley(unittest.TestCase):

    def setUp(self):

        with open("test_cases.json", 'r') as file:

            self.test_data = json.load(file)['GaleShapley']

    def test_student_optimal_from_file(self):
        
        for case in self.test_data:
            i = 0
            with self.subTest(msg= f"Test n {i}"):
                
                etu = case["etu"]
                spe = case["spe"]
                cap = case["cap"]
                
                exp_etu = case["res_etu"]
                exp_spe = case["res_spe"]

                res_etu,i = GaleShapley.GaleShapleyCoteEtudiant(etu,spe,cap)
                res_spe = GaleShapley.GaleShapleyCoteParcours(etu, spe, cap)
                
                self.assertEqual(exp_etu, res_etu)
                self.assertEqual(exp_spe, res_spe)
                i+=1

class TestUnstablePairs(unittest.TestCase):

    def setUp(self):

        with open("test_cases.json", 'r') as file:

            self.test_data = json.load(file)['UnstablePairs']

    def test_student_optimal_from_file(self):
        
        for case in self.test_data:
            i = 0
            with self.subTest(msg= f"Test n {i}"):
                
                etu = case["etu"]
                spe = case["spe"]
                affec = case['affec']

                exp_res = set(tuple(p) for p in case['unstable'])

                unstable = GaleShapley.paires_instables(spe, etu, affec)
                
                self.assertEqual(exp_res, unstable)
                i+=1

if __name__ == '__main__':
    unittest.main()