import pandas as pd

class MembershipAttack:

    def __init__(self, original_database: pd.DataFrame, sample_database:
            pd.DataFrame):
        if len(original_database.index) == 0:
            raise Exception("Original database size must be greater than zero")

        if len(sample_database.index) == 0:
            raise Exception("Sample database size must be greater than zero")

        self.original_database = original_database
        self.sample_database = sample_database

    def calculate_prior_success(self) -> float:
        return len(self.sample_database.index) / len(self.original_database.index)

    def calculate_posterior_success(self, target_qids: dict) -> float:
        """Receives a dictionary of "column": "value" association for QIDs"""

        # Calculate the size of the partition formed by the QIDs in the
        # original database by reducing the dataframe to the smallest dataframe
        # that matches the QID values
        for column, value in target_qids.items():
            if column not in self.original_database.columns:
                raise Exception(f'Column {column} not found in original database')

            self.original_database = self.original_database.loc[(self.original_database[column] == value)]

        # Calculate the size of the partition formed by the QIDs in the
        # sample database
        for column, value in target_qids.items():
            if column not in self.sample_database.columns:
                raise Exception(f'Column {column} not found in sample database')

            self.sample_database = self.sample_database.loc[(self.sample_database[column] == value)]

        return len(self.sample_database) / len(self.original_database)

    def __call__(self, target_qids):
        prior = self.calculate_prior_success()
        posterior = self.calculate_posterior_success(target_qids)

        vulnerability = posterior / prior
        return vulnerability

    def calculate_expected_vulnerability(self):
        pass
