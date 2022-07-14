import csv
import json
import re
import sys
import io


sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

with open("prok_2021~.csv", encoding="utf-8") as f:
    reader = csv.reader(f)
    ls = [row for row in reader]
    data = ls[1][0]
    print(data)
    with open(
        "test.kifu",
        "w",
        encoding="ANSI",
    ) as k:
        k.write(data)
