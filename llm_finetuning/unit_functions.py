from datetime import datetime

import pandas as pd


def filter_on_col_range(df, col, upper=None, lower=None):
    df = df.copy()
    df = df[(df[col] < upper) & (df[col] > lower)]
    return df


def filter_on_col(df, col, val=None):
    df = df.copy()
    if type(val) != list:
        df = df[(df[col] == val)]
    else:
        df = df[(df[col].isin(val))]
    return df


def filter_on_col_less_than(df, col, val=None):
    df = df.copy()
    df = df[(df[col] < val)]
    return df


def filter_on_col_greater_than(df, col, val=None):
    df = df.copy()
    df = df[(df[col] > val)]
    return df


def filter_ytd(df, time_col):
    df = df.copy()
    df[time_col] = pd.to_datetime(df[time_col])
    start_date = datetime.today().strftime("%Y-%m-%d")[:4] + "-01-01"
    df_sub = df[df[time_col] >= start_date].copy()
    return df_sub


def filter_on_date_col(df, time_col, date=None):
    df = df.copy()
    df[time_col] = pd.to_datetime(df[time_col])
    df = df[(df[time_col] == date)]
    return df

def filter_on_date_col_range(df, time_col, begin_date=None, end_date=None):
    df = df.copy()
    END_DT = datetime.strptime(end_date, "%Y-%m-%d")
    START_DT = datetime.strptime(begin_date, "%Y-%m-%d")
    START_DATE = START_DT.date()
    END_DATE = END_DT.date()

    df[time_col] = pd.to_datetime(df[time_col])
    df = df[
        (df[time_col].dt.date <= END_DATE)
        & (df[time_col].dt.date >= START_DATE)
    ]
    return df.copy()


def wow_growth_sum(df, time_col, target_col):
    df["_week"] = (
        df[time_col].dt.year.astype(str)
        + "-"
        + df[time_col].dt.isocalendar().week.astype(str).str.zfill(2)
    )

    df_agg = (
        value_sum_df(df, "_week", target_col)
        .sort_values(["_week"])
        .reset_index(drop=True)
    )
    df_agg["percent_change"] = df_agg[target_col].pct_change()

    return df_agg


def wow_growth_median(df, time_col, target_col):
    df["_week"] = (
        df[time_col].dt.year.astype(str)
        + "-"
        + df[time_col].dt.isocalendar().week.astype(str).str.zfill(2)
    )

    df_agg = (
        value_median_df(df, "_week", target_col)
        .sort_values(["_week"])
        .reset_index(drop=True)
    )
    df_agg["percent_change"] = df_agg[target_col].pct_change()

    return df_agg


def mom_growth_sum(df, time_col, target_col):
    df["_month"] = (
        df[time_col].dt.year.astype(str)
        + "-"
        + df[time_col].dt.month.astype(str).str.zfill(2)
    )

    df_agg = (
        value_sum_df(df, "_month", target_col)
        .sort_values(["_month"])
        .reset_index(drop=True)
    )
    df_agg["percent_change"] = df_agg[target_col].pct_change()

    return df_agg


def mom_growth_median(df, time_col, target_col):
    df["_month"] = (
        df[time_col].dt.year.astype(str)
        + "-"
        + df[time_col].dt.month.astype(str).str.zfill(2)
    )

    df_agg = (
        value_median_df(df, "_month", target_col)
        .sort_values(["_month"])
        .reset_index(drop=True)
    )
    df_agg["percent_change"] = df_agg[target_col].pct_change()

    return df_agg


def daily_growth_median(df, time_col, target_col):
    df[time_col] = df[time_col].dt.date

    df_agg = (
        value_median_df(df, time_col, target_col)
        .sort_values([time_col])
        .reset_index(drop=True)
    )
    df_agg["percent_change"] = df_agg[target_col].pct_change()

    return df_agg


# Contribution Function
def value_sum_df(df, col, target_col):
    df_contribution = df.groupby(col)[target_col].sum().reset_index()
    return df_contribution


def value_avg_df(df, col, target_col):
    df_contribution = df.groupby(col)[target_col].mean().reset_index()
    return df_contribution


def value_median_df(df, col, target_col):
    df_contribution = df.groupby(col)[target_col].median().reset_index()
    return df_contribution


def value_count_df(df, col):
    return df.groupby(col).size().reset_index(name="count")


def top(df, target_col, top_n=5):
    df_agg = df.sort_values(by=target_col, ascending=False).head(top_n)
    return df_agg


def bottom(df, target_col, bottom_n=5):
    df_agg = df.sort_values(by=target_col, ascending=False).tail(bottom_n)
    return df_agg


def get_unique_col_items(df, col):
    return list(df[col].unique())

def sum(df, target_col):
    df = df.copy()
    return df[target_col].sum()


def avg(df, target_col):
    df = df.copy()
    return df[target_col].mean()


def median(df, target_col):
    df = df.copy()
    return df[target_col].median()


def distinct_count(df, col):
    return df[col].nunique()


def percentile(df, target_col, perc=0.5):
    return df[target_col].quantile(perc)
