import pandas as pd
from reports_cfg import re_cfg, add_timefield
import sys,os

sys.path.append('../')
from cp03.merge_csv  import get_FileSize

def report(filename, add_fields=None, re_cfg=re_cfg):
    result = {}
    df = pd.read_csv(filename)
    print('loaded csv file: %s' % filename)

    #根据新增字段配置，增加字段
    df = df.apply(add_timefield, axis='columns') if add_fields else df

    for report_name, agg_cfg in re_cfg.items():
        csv_name = os.path.splitext(filename)[0]+'-'+report_name+'.csv'

        #根据配置执行grouby和aggegration操作
        df_agg = df.groupby(agg_cfg['groupby_fields']).agg(agg_cfg['agg_fields'])
        #根据是否2层columns,看是降为1层
        if df_agg.columns.nlevels ==2 :
            df_agg.columns = ['_'.join(c) for c in df_agg.columns]

        #根据配置重命名
        df_agg.rename(agg_cfg['map_fields'], axis='columns')

        #输出csv
        df_agg.to_csv(csv_name)
        print('generated report file: %s' % csv_name)
        result[csv_name] = [True,get_FileSize(csv_name)] if os.path.isfile(csv_name) else [False,None]
    print('return result: %s' % result)
    return result

if __name__ == '__main__':
    report('QLR201902071000-merged.csv', add_fields=add_timefield)


# ➜  cp08 git:(master) ✗ python pandas_report.py
# loaded csv file: QLR201902071000-merged.csv
# generated report file: QLR201902071000-merged-re-site.csv
# generated report file: QLR201902071000-merged-re-customer.csv
# return result: {'QLR201902071000-merged-re-site.csv': [True, 0.08], 'QLR201902071000-merged-re-customer.csv': [True, 0.09]}
