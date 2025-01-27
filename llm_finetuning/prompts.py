def get_code_gen_prompt(metadata_dict, few_shot_ex):
    base_template = (
        """\
            Think as a python programmer. There are the following functions have been written and are available to you

            Non Date Filter Functions

            1. def filter_on_col_range(df, col, upper=None, lower=None):
            description - this function can take a pandas dataframe df, and filter on a particular column called col based on upper value upper and a lower value lower
            returns a filtered dataframe

            2. def filter_on_col(df, col, val=None):
            description - this function can take a pandas dataframe df, and filter on a particular column called col == val
            returns a filtered dataframe

            2.1. def filter_on_col_less_than(df, col, val=None):
            description - this function can take a pandas dataframe df, and filter on a particular column called col <= val
            returns a filtered dataframe

            2.2. def filter_on_col_greater_than(df, col, val=None):
            description - this function can take a pandas dataframe df, and filter on a particular column called col >= val
            returns a filtered dataframe

            Date Filter Functions`

            3. def filter_ytd(df, time_col):
            description - returns a filtered dataframe with only those rows that are within year till date range or ytd as per time_col

            4. def filter_on_date_col_range(df, time_col, begin_date=None, end_date=None):
            description - this function can take a pandas dataframe df, and filter on the date column called time_col based on begin_date and end_date
            returns a filtered dataframe


            Aggregate Functions

            Any of the below aggregate function can take a dataframe from the Filter functions as input
            these functions return a dataframe

            7. def value_sum_df(df, col, target_col):
            description - it takes a dataframe df, and calculates the sum of target_col for each col item
            col can also be a list of columns
            target_col will take only a single column
            returns an aggregated dataframe containing col and the corresponding aggregated target_col value

            11. def value_count_df(df, col):
            description - calculates how many times each value in col occurs
            returns a dataframe containing col and count of how many times all the values in the col appeared as 'count'
            it contains 2 columns only - col and 'count'

            12. def value_avg_df(df, col,target_col):
            description - calculates the average of target_col for each col item
            returns an aggregated dataframe containing col and and the corresponding aggregated target_col value
            13. def value_median_df(df, col,target_col):
            description - calculates the median of target_col for each col item
            returns an aggregated dataframe containing col and and the corresponding aggregated target_col value


            Selection Functions

            8. def top(df, col, target_col, top_n=5):
            description - it takes an aggregated dataframe as input and returns the 'top_n' items in col ordered by values in target_col
            this takes dataframe from Filter Functions or Aggregate Functions
            returns a dataframe sorted in descending order of the target_col value containing col and target_col

            12. def get_unique_col_items(df,col):
            description - returns a list of unique items in the column col in the dataframe df
            returns a list of items

            13. def bottom(df, col, target_col, bottom_n=5):
            description - it takes an aggregated dataframe as input and returns the lowest ‘bottom_n’ items in col ordered by values in target_col
            this takes dataframe from Filter Functions or Aggregate Functions
            returns a dataframe sorted in ascending order of the target_col value containing col and target_col


            Summarize Functions
            Any of the below summarize function can take a dataframe from the Filter functions or Aggregate Functions as input

            9. def distinct_count(df, col):
            descripton - counts the unique number of values in column col
            return an integer

            6. def sum(df, target_col):
            description - this function takes a pandas dataframe df and returns the summation value of the column target_col
            returns a single numerical value which is the sum of the target_col

            15. def avg(df, target_col):
            description - this function takes a pandas dataframe df and returns the average value of the column target_col
            returns a single numerical value which is the average of the target_col
            16. def percentile(df, target_col,perc=0.5):
            description - this function takes a pandas dataframe df and returns perc percentile value in target_col
            returns a single numerical value which is the 'perc' percentile of target_col in df
            17. def median(df, target_col):
            description - this function takes a pandas dataframe df and returns the median value of the column target_col
            returns a single numerical value which is the median of the target_col

            Growth Functions

            5.def wow_growth_sum(df, date_col, target_col):
            description - this function takes a date filtered dataframe and returns the week on week growth for all the weeks in the data frame over the weekly summation of target_col.
            returns a dataframe containing the wow_growth. The columns are '_week', target_col and 'percent_change'.
                        in order to calculate week on week growth in weekly sum values between start_date and end_date. Filter the dataframe between start_date and end_date and call wow_growth_sum. Dont call value_sum_df.
            5.def wow_growth_median(df, date_col, target_col, agg='sum'):
            description - this function takes a date filtered dataframe and returns the week on week growth for all the weeks in the data frame over the weekly median of target_col.
            returns a dataframe containing the wow_growth. The columns are '_week', target_col and 'percent_change'.
            in order to calculate week on week growth in weekly median values between start_date and end_date. Filter the dataframe between start_date and end_date and call wow_growth_median.Dont call value_median_df.
            5.def mom_growth_median(df, date_col, target_col, agg='sum'):
            description - this function takes a date filtered dataframe and returns the week on week growth for all the months in the data frame over the mothly median of target_col.
            returns a dataframe containing the mom_growth. The columns are '_month', target_col and 'percent_change'.
            in order to calculate month on month growth in monthly median values between start_date and end_date. Filter the dataframe between start_date and end_date and call mom_growth_median.Dont call value_median_df.
            5.def mom_growth_sum(df, date_col, target_col, agg='sum'):
            description - this function takes a date filtered dataframe and returns the week on week growth for all the months in the data frame over the mothly sum of target_col.
            returns a dataframe containing the mom_growth. The columns are '_month', target_col and 'percent_change'.
            in order to calculate month on month growth in monthly sum values between start_date and end_date. Filter the dataframe between start_date and end_date and call mom_growth_sum.Dont call value_median_df.
            5.def daily_growth_median(df, time_col, target_col):
            description - this function takes a date filtered dataframe and returns the week on week growth for all the days in the data frame over the daily median of target_col.
            returns a dataframe containing the daily growth. The columns are time_col, target_col and 'percent_change'.
            in order to calculate daily growth in daily median values between start_date and end_date. Filter the dataframe between start_date and end_date and call daily_growth_median.Dont call value_median_df.

            There is a dataframe 'sample_df' and the row and column descriptions are available here:
            """
        + str(metadata_dict)
        + """
            You should -
            based on the question asked below, use the above functions only to write a snippet
            Date Filtering functions don't work on Aggregation output dataframe
            When using the date filtering, always figure out both the being_date and end_date
            usage of any other functions other than the ones mentioned above or for loops is strictly forbidden
            choose the right dataframe and the appropriate functions to use in a suitable order
            If some column description includes negative counts, please change the sign to positive and compute

            If you are not confident of answering the question using the given functions, please start your response with [Not answerable]. Answering any question is forbidden if you cannot compute the answer from the underlying data.

            Remember the following details about the use case -
            """
        + few_shot_ex
        + """
            Strictly output the executable part of the code and any non executable statements or comment is strictly forbidden
            Few Guidelines for code generation-
            1. For counting the unique number of values in a column use distinct_count
            2. For counting the occurence of unique value in a column use value_vount
            3. Always convert dates into strftime("%Y-%m-%d") format
            4. begin_date and end_date must be specified when calling filter_on_date_col_range and should be strings
            5. Loops are strictly forbidden
            6. Make sure to round off and numbers in the print, more than 3 digit after decimal is strictly forbidden.
            7. If asked for median values use value_median_df
            8. For any percentile value computation use percentile
            9. Don't add unnecessary whitespaces in the code
            10. Compute the begin and end dates programmatically if not specified
            Only output the executable part of the code
            Any non executable statements or headers or footers comments are strictly forbidden

            Print the result in human readable form.
        """
    )

    return base_template



