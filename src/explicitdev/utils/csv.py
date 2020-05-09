import csv
from pathlib import Path


def save_alchemy_query_to_csv(query_results, file_path: Path, row_convert_func=None):
    with open(file_path, mode='w')as file:
        csv_writer = csv.DictWriter(file, fieldnames=query_results[0]._asdict().keys())
        csv_writer.writeheader()
        for row in query_results:
            if row_convert_func:
                row = row._asdict()
                row = row_convert_func(row)
            csv_writer.writerow(row)
