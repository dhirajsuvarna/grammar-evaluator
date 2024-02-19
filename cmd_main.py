import typing
import typer
import logging
import sys
import pandas as pd
import tomllib
import time

# from enum import Enum
from constants import Tools
from pathlib import Path
from logging import FileHandler, StreamHandler
from grammar_checker import grammar_checker

############################################
# set logger
logging.basicConfig(
    handlers=[
        FileHandler("cmd.log", "w", encoding="utf-8"),
        StreamHandler(sys.stdout),
    ],
    level=logging.INFO,
    format="{asctime} | {filename} | {levelname} | {message}",
    datefmt="%d-%m-%Y %H:%M:%S",
    style="{",
)

logger = logging.getLogger()


def check_grammar(iRow):
    print(f"--------------------------\n{iRow}")
    for tool in Tools:
        iRow[tool.name] = grammar_checker(tool, iRow["USER_ANSWER"])

    return iRow


def main(data_file: Path = typer.Argument(..., help="Input csv file")):

    df = pd.read_csv(str(data_file), encoding="utf-8")
    df = df[df["USER_ANSWER"].notna()]

    num_rows = df.shape[0]
    step_size = 9
    df_list = []
    for index in range(0, num_rows, step_size):
        print(f"processing: {index} : {index + step_size}")
        small_df = df.iloc[index : index + step_size]

        # df = df.iloc[0:2]

        small_df = small_df.apply(check_grammar, axis=1)
        df_list.append(small_df)

        print(f"Sleeping...")
        time.sleep(61)
        # print(df)

    all_df = pd.concat(df_list, axis=0)
    all_df.to_csv("processed.csv", index=False, encoding="utf-8")


if __name__ == "__main__":
    typer.run(main)
