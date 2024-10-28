import os
import shutil
import sys
import pandas as pd


def copy_files_from_excel(excel_path):
    df = pd.read_excel(excel_path)

    for index, row in df.iterrows():
        source_path = row["source"]
        destination_path = row["destination"]
        source_path = os.path.abspath(source_path)
        destination_path = os.path.abspath(destination_path)

        try:
            shutil.copy(source_path, destination_path)
            print(f"{source_path} -> {destination_path} => Copy Done.")
        except Exception as e:
            print(
                f"Error occurs during file copy: {source_path} -> {destination_path}. Error: {e}"
            )


def main():
    if len(sys.argv) < 2:
        print("Input Excel File Path")
        return

    excel_path = sys.argv[1]
    copy_files_from_excel(excel_path)


if __name__ == "__main__":
    main()
