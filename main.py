import os
import shutil
import sys

import pandas as pd


def copy_files_from_excel(excel_path):
    # Excel 파일에서 데이터를 읽어오기
    df = pd.read_excel(excel_path)

    for index, row in df.iterrows():
        source_path = row['source']
        destination_path = row['destination']

        # 현재 디렉토리 기준으로 경로 설정
        source_path = os.path.abspath(source_path)
        destination_path = os.path.abspath(destination_path)

        try:
            # 파일 복사
            shutil.copy(source_path, destination_path)
            print(f"{source_path} -> {destination_path} 복사 완료.")
        except Exception as e:
            print(f"파일 복사 중 오류 발생: {source_path} -> {destination_path}. 오류: {e}")


def main():
    # 첫 번째 인자로 엑셀 파일 경로를 받음
    if len(sys.argv) < 2:
        print("엑셀 파일 경로를 입력해주세요.")
        return

    excel_path = sys.argv[1]
    copy_files_from_excel(excel_path)


if __name__ == "__main__":
    main()
