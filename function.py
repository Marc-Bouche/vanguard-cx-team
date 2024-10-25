import string
import numpy as np
import pandas as pd
import re
import matplotlib.pyplot as plt
import seaborn as sns
import math

#---------------------------------------------------------------------------------------------------#

# Function 1
# This function calculate the error rate based on the process_step sequence
# Where entire sequences are marked as valid or invalid based on whether all steps appear in order.
# Grouped by client_id

def calculate_error_rate_client(df):

    # Group by client_id
    grouped_data = df.groupby(['client_id'])

    # Initialize error count
    error_count = 0
    total_sequences = 0

    # Define the expected order
    expected_order = ['confirm','step_3','step_2','step_1','start']

    # Iterate through each group
    for _, group in grouped_data:
        actual_sequence = group['process_step'].tolist()

        # Check if the actual sequence follows the expected order
        current_index = 0
        is_valid_sequence = True

        for step in actual_sequence:
            if step in expected_order:
                step_index = expected_order.index(step)

                # If step appears before the current index in the expected order, it's an error
                if step_index < current_index:
                    is_valid_sequence = False
                    break
                # Update the current index to the step's position in the expected order
                current_index = step_index
            else:
                # Step not found in expected_order, marking as error
                is_valid_sequence = False
                break

        # If the sequence was not valid, increment the error count
        if not is_valid_sequence:
            error_count += 1

        total_sequences += 1

    # Calculate error rate
    error_rate = (error_count / total_sequences) * 100

    return error_rate
#---------------------------------------------------------------------------------------------------#

# Function 2
# This function also calculate the error rate based on the process_step sequence
# Where every out-of-order step is counted, regardless of whether the entire sequence is valid or not.
# Grouped by client_id

def calculate_error_rate_client_new(df):
    """Calculates the error rate based on the process_step sequence."""

    # Group by client_id
    grouped_data = df.groupby('client_id')

    # Initialize error count
    error_count = 0
    total_sequences = 0

    # Define the expected order
    expected_order = ['confirm','step_3','step_2','step_1','start']

    # Iterate through each group
    for _, group in grouped_data:
        actual_sequence = group['process_step'].tolist()

        # Check if the actual sequence follows the expected order
        current_index = 0
        is_valid_sequence = True

        for step in actual_sequence:
                step_index = expected_order.index(step)

                # If step appears before the current index in the expected order, it's an error
                if step_index < current_index:
                    error_count += 1
                # Update the current index to the step's position in the expected order
                current_index = step_index

        total_sequences += 1

    # Calculate error rate
    error_rate = (error_count / total_sequences) * 100

    return error_rate
#---------------------------------------------------------------------------------------------------#

# Function 3
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

# Function 4
# Same as function 1 but grouped by visit_id, not client_id.


def calculate_error_rate_visit(df):
    """Calculates the error rate based on the process_step sequence."""

    # Group by visit_id
    grouped_data = df.groupby('visit_id')

    # Initialize error count
    error_count = 0
    total_sequences = 0

    # Define the expected order
    expected_order = ['confirm','step_3','step_2','step_1','start']

    # Iterate through each group
    for _, group in grouped_data:
        actual_sequence = group['process_step'].tolist()

        # Check if the actual sequence follows the expected order
        current_index = 0
        is_valid_sequence = True

        for step in actual_sequence:
            if step in expected_order:
                step_index = expected_order.index(step)

                # If step appears before the current index in the expected order, it's an error
                if step_index < current_index:
                    is_valid_sequence = False
                    break
                # Update the current index to the step's position in the expected order
                current_index = step_index
            else:
                # Step not found in expected_order, marking as error
                is_valid_sequence = False
                break

        # If the sequence was not valid, increment the error count
        if not is_valid_sequence:
            error_count += 1

        total_sequences += 1

    # Calculate error rate
    error_rate = (error_count / total_sequences) * 100

    return error_rate
#---------------------------------------------------------------------------------------------------#

# Fuction 5
# The function directly counts each out-of-order step as an error. 
# It increments the error count for every individual step that appears before the current position in the expected order.
# Grouped by visit_id

def calculate_error_rate_visit_new(df):
    """Calculates the error rate based on the process_step sequence."""

    # Group by visit_id
    grouped_data = df.groupby('visit_id')

    # Initialize error count
    error_count = 0
    total_sequences = 0

    # Define the expected order
    expected_order = ['confirm','step_3','step_2','step_1','start']

    # Iterate through each group
    for _, group in grouped_data:
        actual_sequence = group['process_step'].tolist()

        # Check if the actual sequence follows the expected order
        current_index = 0
        is_valid_sequence = True

        for step in actual_sequence:
                step_index = expected_order.index(step)

                # If step appears before the current index in the expected order, it's an error
                if step_index < current_index:
                    error_count += 1
                # Update the current index to the step's position in the expected order
                current_index = step_index

        total_sequences += 1

    # Calculate error rate
    error_rate = (error_count / total_sequences) * 100

    return error_rate

#---------------------------------------------------------------------------------------------------#

# Fuction 6
#T-test for duration
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

# Fuction 7
# Identidfy outliers
#def tukeys_test_outliers(data):
    Q1 = data.quantile(0.25)
    Q3 = data.quantile(0.75)
    IQR = Q3 - Q1
    # Define bounds for the outliers
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    # Identify the outliers
    outliers = data[(data < lower_bound) | (data > upper_bound)]
    return outliers
