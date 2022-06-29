import unittest
import pandas as pd

from membership.modules.membership import MembershipAttack

class TestMembershipAttack(unittest.TestCase):
    # @TODO: Refactor this test to test the whole functionality (calculating
    # vulnerability) instead of testing prior and posterior separately

    def setUp(self):
        # Create original and sample databases
        original = pd.DataFrame({
            'ID': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            'CIDADE': ['SP', 'MG', 'MG', 'RJ', 'RJ', 'RJ', 'RJ', 'SP', 'SP', 'SP'],
            'SEXO': ['F', 'F', 'F', 'M', 'M', 'M', 'M', 'M', 'M', 'M'],
            'IDADE': ['31-40', '21-30', '21-30', '21-30', '21-30', '21-30', '31-40', '31-40', '31-40', '31-40'],
            'AS1': ['0', '1', '1', '0', '1', '0', '0', '1', '0', '1']
        })

        sample = pd.DataFrame({
            'ID': [1, 2, 4, 5],
            'CIDADE': ['SP', 'MG', 'RJ', 'RJ'],
            'SEXO': ['F', 'F', 'M', 'M'],
            'IDADE': ['31-40', '21-30', '21-30', '21-30'],
            'AS2': ['1', '0', '0', '1']
        })

        self.membership = MembershipAttack(original, sample)

    def test_calculate_prior(self):
        self.assertTrue(self.membership.calculate_prior_success() == 0.4)

    def test_calculate_posterior_unique_individual(self):
        target_qids = {
            'CIDADE': 'SP',
            'SEXO': 'F',
            'IDADE': '31-40'
        }

        self.assertTrue(self.membership.calculate_posterior_success(target_qids) == 1.0)

    def test_calculate_posterior_unique_in_sample_not_unique_in_original(self):
        target_qids = {
            'CIDADE': 'MG',
            'SEXO': 'F',
            'IDADE': '21-30'
        }

        self.assertTrue(self.membership.calculate_posterior_success(target_qids) == 0.5)

    def test_calculate_posterior_not_unique_individual(self):
        target_qids = {
            'CIDADE': 'RJ',
            'SEXO': 'M',
            'IDADE': '21-30'
        }

        self.assertTrue(self.membership.calculate_posterior_success(target_qids) == (2 / 3))

    def test_invalid_column_in_original_throws_exception(self):
        pass

    def test_invalid_column_in_sample_throws_exception(self):
        pass
