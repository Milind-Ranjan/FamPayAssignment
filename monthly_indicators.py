import os
import sys
import math
import pandas as pd


def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values(["ticker", "date"])
    return df


def aggregate_monthly(df: pd.DataFrame) -> pd.DataFrame:
    month = df["date"].dt.to_period("M")
    g = df.groupby(["ticker", month], sort=True)
    open_ = g["open"].first()
    close_ = g["close"].last()
    high_ = g["high"].max()
    low_ = g["low"].min()
    out = (
        pd.concat(
            [open_.rename("open"), high_.rename("high"), low_.rename("low"), close_.rename("close")],
            axis=1,
        )
        .reset_index()
        .rename(columns={"date": "month"})
    )
    out["date"] = out["month"].dt.to_timestamp("M")
    out = out.drop(columns=["month"])
    out = out.sort_values(["ticker", "date"]).reset_index(drop=True)
    return out


def sma(series: pd.Series, window: int) -> pd.Series:
    return series.rolling(window=window, min_periods=window).mean()


def ema(series: pd.Series, window: int) -> pd.Series:
    if len(series) < window:
        return pd.Series([math.nan] * len(series), index=series.index, dtype="float64")
    anchor = series.rolling(window=window, min_periods=window).mean()
    seeded = pd.Series([math.nan] * len(series), index=series.index, dtype="float64")
    seeded.iloc[window - 1] = anchor.iloc[window - 1]
    seeded.iloc[window:] = series.iloc[window:]
    return seeded.ewm(alpha=2.0 / (window + 1.0), adjust=False).mean()


def add_indicators(monthly: pd.DataFrame) -> pd.DataFrame:
    monthly = monthly.copy()
    monthly["sma_10"] = monthly.groupby("ticker", group_keys=False)["close"].apply(lambda s: sma(s, 10))
    monthly["sma_20"] = monthly.groupby("ticker", group_keys=False)["close"].apply(lambda s: sma(s, 20))
    monthly["ema_10"] = monthly.groupby("ticker", group_keys=False)["close"].apply(lambda s: ema(s, 10))
    monthly["ema_20"] = monthly.groupby("ticker", group_keys=False)["close"].apply(lambda s: ema(s, 20))
    return monthly


def write_symbol_files(monthly: pd.DataFrame, output_dir: str) -> None:
    os.makedirs(output_dir, exist_ok=True)
    for symbol, g in monthly.groupby("ticker"):
        g = g.sort_values("date")
        g = g.tail(24)
        out_path = os.path.join(output_dir, f"result_{symbol}.csv")
        g.to_csv(out_path, index=False)


def main():
    input_path = "/Users/milindranjan/Downloads/FamPay/dataset.csv"
    output_dir = os.getcwd()
    df = load_data(input_path)
    monthly = aggregate_monthly(df)
    monthly = add_indicators(monthly)
    write_symbol_files(monthly, output_dir)


if __name__ == "__main__":
    sys.exit(main())
