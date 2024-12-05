import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.model_selection import KFold
import os
import time
import random


class KFoldValidator:
    """
    Class for k-fold cross-validation.

    Parameters:
    - model : model for validation.
    - n_splits : int
        Number of folds. Default is 10.
    - seed : int
        Random seed for reproducibility. Default is 7.
    - k_fold_type : KFold
        Type of k-fold split strategy. Default is KFold.
    - score_type : callable
        Scoring metric function. Default is accuracy_score.

    Internal Working:
    -----------------
    1. Setup: Configures the basic parameters for k-fold cross-validation.
    2. Validation: Performs validation using the indices generated by KFold.
    3. Scoring: Calculates the score based on the provided scoring metric.
    4. Average of Scores: Calculates and returns the average of scores.

    Returns:
    - float: containing the average score after validation.
    """

    def __init__(self, model, n_splits=10, seed=7, k_fold_type=KFold, score_type=accuracy_score, params={}):
        self.model = model
        self.n_splits = n_splits
        self.kf = k_fold_type(n_splits=n_splits, shuffle=True, random_state=seed)
        self.models = []
        self.seed = seed
        self.score_type = score_type
        self.params = params

    def validate(self, X, y, y_divide=None):
        """
        Perform k-fold validation.

        Parameters:
        - X : np.array
            Features.
        - y : np.array
            Labels.
        - y_divide : np.array, optional
            Used for more advanced split strategies.

        Returns:
        - tuple: containing the average of scores for each fold.
        """
        fold_scores = []
        self._seed_everything(self.seed)

        for train_index, test_index in self.kf.split(X, y_divide):
            start_time = time.time()
            X_train = self.slicing(X, train_index)
            X_test = self.slicing(X, test_index)
            y_train = self.slicing(y, train_index)
            y_test = self.slicing(y, test_index)

            model = self.model(ridge_params=self.params['ridge'], xgb_params=self.params['xgb'])

            self.models.append(model.fit(X_train, y_train))
            y_pred = model.predict(X_test)

            score = self.score_type[0](y_test, y_pred)
            score1 = self.score_type[1](y_test, y_pred)
            fold_scores.append((score, score1))

            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"Fold score: {score:.2f}, {score1:.2f}, Time elapsed: {elapsed_time:.2f} seconds")

        print("Scores per fold:", fold_scores)

        # Separando os scores
        score_0 = [s[0] for s in fold_scores]
        score_1 = [s[1] for s in fold_scores]

        # Calculando a média
        mean_score_0 = np.mean(score_0)
        mean_score_1 = np.mean(score_1)

        print("Mean score 0:", mean_score_0)
        print("Mean score 1:", mean_score_1)

        return mean_score_0, mean_score_1

    @staticmethod
    def _seed_everything(seed):
        """
        Fix all seeds for reproducibility.

        Parameters:
        - seed : int
            Seed value.
        """
        random.seed(seed)
        np.random.seed(seed)
        os.environ['PYTHONHASHSEED'] = str(seed)

    @staticmethod
    def slicing(data, indices, reset_index=False):
        """
        Slice data based on provided indices.

        Parameters:
        - data : np.array or pd.DataFrame or pd.Series
            Data to slice.
        - indices : np.array
            Indices for slicing.
        - reset_index : bool, optional
            Whether the index should be reset. Default is False.

        Returns:
        - np.array or pd.DataFrame: Sliced data.
        """
        if isinstance(data, pd.DataFrame) or isinstance(data, pd.Series):
            sliced_data = data.iloc[indices]
            if reset_index:
                sliced_data = sliced_data.reset_index(drop=True)
            return sliced_data
        else:
            return data[indices]

    def predict_avg(self, X_test):
        """
        Predict using the average of all models from k-fold validation.

        Parameters:
        - X_test : np.array
            Test features.

        Returns:
        - np.array: Predicted values.
        """
        self._seed_everything(self.seed)
        predictions = np.zeros(X_test.shape[0])
        for model in self.models:
            if model is None:
                raise ValueError("Um dos modelos não foi inicializado corretamente.")
            else:
                predictions += model.predict(X_test)
        return predictions / self.n_splits

    @staticmethod
    def calculate_final_score(scores_w1, scores_w5, scores_w10):
        """
        Calculates the final score based on multiple scores and associated weights.

        Parameters:
        - scores_w1 : float
            Score associated with weight w1. (Objective A)
        - scores_w5 : float
            Score associated with weight w5. (Objective B)
        - scores_w10 : float
            Score associated with weight w10. (Objective C)

        Internal Working:
        -----------------
        1. Weight Calculation: Multiplies constants 23189, 1608, and 1342 (Number of rows in the test set) by their respective weights 1, 5, and 5.
        2. Final Score Calculation: Calculates the weighted average of the scores using the calculated weights.
        3. Print Results: Displays the weights and the final score.

        Returns:
        - float: The calculated final score.
        """
        # Calculate the weights
        weight_w1 = 23189 * 1
        weight_w5 = 1608 * 5
        weight_w10 = 1342 * 5

        # Calculate the final score
        final_score = (scores_w1 * weight_w1 + scores_w5 * weight_w5 + scores_w10 * weight_w10) / (
                weight_w1 + weight_w5 + weight_w10)

        # Print the results
        print(
            f'weight_w1: {weight_w1}, weight_w5: {weight_w5}, weight_w10: {weight_w10}, final_score: {final_score:.5f}')
        print(f'w1: {scores_w1:.5f}, w5: {scores_w5:.5f}, w10: {scores_w10:.5f}, final_score: {final_score:.5f}')

        return final_score


def generate_submission(mask_w1, mask_w5, mask_w10, preds_iter_w1, preds_iter_w5, preds_iter_w10, path):
    """
    Generates a submission file using given predictions and masks.

    Parameters:
    - mask_w1, mask_w5, mask_w10 : array-like
        Boolean masks for filtering the data based on the 'w' values of 1, 5, and 10 respectively.
    - preds_iter_w1, preds_iter_w5, preds_iter_w10 : array-like
        Predicted values corresponding to the masks.
    - path : string
        Directory path to the sample submission file.

    Internal Working:
    -----------------
    1. Data Loading: Loads the 'data_pivot_load.csv' file and prepares it for processing.
    2. Sorting and Categorizing: Sorts the data based on the 'BS' and 'Time' columns and categorizes 'BS' and 'RUType' columns.
    3. Data Splitting: Isolates the test data where the 'Energy' value is -1.
    4. Printing Data Shapes: Prints the shape of the data filtered using masks.
    5. Prediction DataFrames: Creates three separate DataFrames for predictions corresponding to each mask.
    6. Assigning Predictions: Depending on the 'w' value, assigns the relevant predictions to the 'Energy' column.
    7. Preparing Final Submission:
      a. Reads the sample submission file.
      b. Constructs an 'ID' column in the data.
      c. Filters out the rows required for submission and selects 'ID' and 'Energy' columns.
      d. Writes the final submission DataFrame to 'submission.csv'.

    Returns:
    - DataFrame: The final submission DataFrame containing 'ID' and 'Energy' columns.
    """
    data = pd.read_csv('../data/data_pivot_load.csv')
    sorted_data = data.copy()
    sorted_data['Time'] = pd.to_datetime(sorted_data['Time'])
    sorted_data = sorted_data.sort_values(['BS', 'Time'])
    sorted_data['BS_cat'] = sorted_data['BS'].astype('category').cat.codes
    sorted_data['RUType_cat'] = sorted_data['RUType'].astype('category').cat.codes

    # Split the data while respecting the temporal order
    test_data = sorted_data[sorted_data['Energy'] == -1]
    submission_data = test_data[['Time', 'BS', 'Energy', 'w', 'RUType_cat']]

    # Print shapes using masks
    print(submission_data[mask_w1].shape)
    print(submission_data[mask_w5].shape)
    print(submission_data[mask_w10].shape)

    # Create prediction dataframes
    preds_w1 = pd.DataFrame(preds_iter_w1, index=submission_data.index, columns=['Energy_pred'])
    preds_w5 = pd.DataFrame(preds_iter_w5, index=submission_data.index, columns=['Energy_pred'])
    preds_w10 = pd.DataFrame(preds_iter_w10, index=submission_data.index, columns=['Energy_pred'])

    # Assign predictions based on the value of 'w'
    submission_data.loc[mask_w1, 'Energy'] = preds_w1.loc[mask_w1, 'Energy_pred']
    submission_data.loc[mask_w5, 'Energy'] = preds_w5.loc[mask_w5, 'Energy_pred']
    submission_data.loc[mask_w10, 'Energy'] = preds_w10.loc[mask_w10, 'Energy_pred']

    # Print results
    print(submission_data.shape)
    print(submission_data[mask_w1].head(10))
    print(submission_data[mask_w5].head(10))
    print(submission_data[mask_w10].head(10))

    template_submission = pd.read_csv(f'{path}sample_submission.csv')
    submission_data['ID'] = submission_data['Time'].astype(str) + '_' + submission_data['BS']

    print(template_submission['ID'].head())
    print(submission_data['ID'].head())

    # Filter only required IDs and columns for the final submission
    required_ids = template_submission['ID']
    final_submission = submission_data[submission_data['ID'].isin(required_ids)][['ID', 'Energy']]

    final_submission.reset_index(drop=True, inplace=True)
    print(final_submission.head(10))
    print(final_submission.shape)

    final_submission.to_csv('submission.csv', index=False)
    return final_submission