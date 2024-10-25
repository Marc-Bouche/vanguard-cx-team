import string
import numpy as np
import pandas as pd
import re
import matplotlib.pyplot as plt
import seaborn as sns
import math

#---------------------------------------------------------------------------------------------------#

# Function 1
# This function calculates the total number of errors per client based on deviations from the expected order.
# Grouped by client_id

def calculate_error_count_client(df):
    """Calculates the error count per client based on the process_step sequence."""

    # Group by client_id
    grouped_data = df.groupby('client_id')

    # Initialize a list to store results
    result_data = []

    # Define the expected order
    expected_order = ['confirm','step_3','step_2','step_1','start']

    # Iterate through each group
    for client_id, group in grouped_data:
        actual_sequence = group['process_step'].tolist()

        # Initialize error count for this client
        error_count = 0
        current_index = 0

        # Check if the actual sequence follows the expected order
        for step in actual_sequence:
            step_index = expected_order.index(step)

            # If step appears before the current index in the expected order, it's an error
            if step_index < current_index:
                error_count += 1

            # Update the current index to the step's position in the expected order
            current_index = step_index

        # Append the result for this client
        result_data.append({"client_id": client_id, "error_count": error_count})

    # Convert the results to a DataFrame
    result_df = pd.DataFrame(result_data)

    return result_df

#---------------------------------------------------------------------------------------------------#

# Fuction 2
# T-test for duration
def perform_t_tests(dfs_test):
    t_tests_results = []  # List to store the results
    for df_pair in dfs_test:
        # Extract the test and control groups
        test_group = df_pair[0]
        control_group = df_pair[1]
        # Calculate the means for test and control groups
        mean_test = test_group.mean()
        mean_control = control_group.mean()
        # Perform t-test (independent two-sample t-test with unequal variances)
        t_stat, p_value = stats.ttest_ind(test_group, control_group, equal_var=False, alternative='greater')
        # Store the p_value and the means in the specified format
        t_tests_results.append((p_value, ({'mean_test': mean_test}, {'mean_control': mean_control})))
    return t_tests_results

#---------------------------------------------------------------------------------------------------#

# Fuction 3
# Identidfy outliers
def tukeys_test_outliers(data):
    Q1 = data.quantile(0.25)
    Q3 = data.quantile(0.75)
    IQR = Q3 - Q1
    # Define bounds for the outliers
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    # Identify the outliers
    outliers = data[(data < lower_bound) | (data > upper_bound)]
    return outliers
