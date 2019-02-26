import pandas as pd
from reports_cfg import re_cfg
import sys,os

sys.path.append('../')
from cp03.merge_csv  import get_FileSize

def report(filename,re_cfg=re_cfg):
    result = {}
    df = pd.read_csv(filename)
    print('loaded csv file: %s' % filename)
    for report_name, agg_cfg in re_cfg.items():
        csv_name = os.path.splitext(filename)[0]+'-'+report_name+'.csv'
        df.groupby(agg_cfg['groupby_fields']).agg(agg_cfg['agg_fields']).to_csv(csv_name)
        print('generated report file: %s' % csv_name)
        result[csv_name] = [True,get_FileSize(csv_name)] if os.path.isfile(csv_name) else [False,None]
    print('return result: %s' % result)
    return result

if __name__ == '__main__':
    report('QLR201902071000-merged.csv')


# ➜  cp08 git:(master) ✗ python pandas_report.py
# loaded csv file: QLR201902071000-merged.csv
# generated report file: QLR201902071000-merged-re-site.csv
# generated report file: QLR201902071000-merged-re-customer.csv
# return result: {'QLR201902071000-merged-re-site.csv': [True, 0.08], 'QLR201902071000-merged-re-customer.csv': [True, 0.09]}
