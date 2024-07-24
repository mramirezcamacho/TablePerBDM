import pandas as pd
from OKRsData import ordersOfNewAdquireRs

for x, y in ordersOfNewAdquireRs.items():
    sumatoria = 0
    for city, value in y.items():
        sumatoria += value
    print(x, sumatoria)
