from sqlalchemy import create_engine, select, and_,text, between
from sqlalchemy.sql import table, column ,literal_column, func
from re_cfg import re_day_cfg, pg_conn_dict
from joblib import Parallel, delayed
from colorama import Fore, Back, Style
import pandas as pd
import sys,traceback
from dateutil.parser import parse

def getcon(pg_conn_dict=pg_conn_dict):
    uri = 'postgresql://%s:%s@%s:%s/%s' % (pg_conn_dict['user'], pg_conn_dict['password'], pg_conn_dict['host'],5432,pg_conn_dict['dbname'])
    print(f'{Fore.GREEN}db uri: %s{Style.RESET_ALL}' % uri)
    con = create_engine(uri)
    return con

def agg_many_tables(tables,date, agg_table_fun, re_day_cfg=re_day_cfg, con = getcon()):
    print(f'{Fore.RED}CALL %s{Style.RESET_ALL}' % agg_table_fun.__name__)
    results=[]
    for source_table, dest_table  in tables.items():
        result = agg_table_fun(source_table, dest_table, date, re_day_cfg[source_table], con)
        results.append(result)
    print(f'{Fore.RED}return results: %s{Style.RESET_ALL}' % results)
    return results

def agg_table_pd(source_table, dest_table, date, re_day_cfg, con):
    time_field = re_day_cfg['time_field']
    sql = "select * from {0} where {1}>='{2:%Y-%m-%d %H:%M}' and {1}<'{3:%Y-%m-%d %H:%M}'".format(source_table,column(time_field),*date)
    df = pd.read_sql(sql,con)
    df = df[(df[time_field]>=date[0]) & (df[time_field]<date[1])]
    df_agg = df.groupby(re_day_cfg['groupby_fields']).agg(re_day_cfg['agg_fields'])
    df_agg[time_field] = date[0]
    log = 'table:%s , insert records:%s' % (dest_table, len(df_agg))
    try:
        df_agg.to_sql(dest_table, con=con, if_exists='append')
    except:
        log = traceback.format_exc()
        return [1,dest_table,log]
    print(Fore.BLUE + log + Style.RESET_ALL)
    return [0,dest_table,log]

def agg_table_sql(source_table, dest_table, date, re_day_cfg, con):
    time_field = re_day_cfg['time_field']
    sel = select([
        literal_column("'{:%Y-%m-%d %H:%M}'::timestamp".format(date[0])).label(time_field),
        *[column(field) for field in re_day_cfg['groupby_fields']],
        *[func.__getattr__(aggfunc)(column(field)).label(field) for field, aggfunc in re_day_cfg['agg_fields'].items()],
    ]).select_from(table(source_table)).where(
        and_(
            text("{} >= '{:%Y-%m-%d %H:%M}'".format(column(time_field), date[0])),
            text("{} < '{:%Y-%m-%d %H:%M}'".format(column(time_field), date[1])),
        )
    ).group_by(
        *re_day_cfg['groupby_fields']
    )
    t = table(dest_table, *sel.columns)
    ins = t.insert().from_select(sel.columns, sel, False)
    print(Fore.GREEN + str(ins) + Style.RESET_ALL)
    try:
        result = con.execute(ins)
        status=0
        log = 'table:%s , insert records:%s' % (dest_table, result.rowcount)
    except:
        status=1
        log = traceback.format_exc()
    print(Fore.BLUE + log + Style.RESET_ALL)
    return [status,dest_table,log]

if __name__ == '__main__':
    agg_many_tables({'re_site':'re_site_d','re_customer':'re_customer_d' },
                    list(map(parse, ['201802071000+8','201802071100+8'])),
                    agg_table_pd
                    )
    print('\n\n')
    agg_many_tables({'re_site':'re_site_d','re_customer':'re_customer_d' },
                    list(map(parse, ['201802071000+8','201802071100+8'])),
                    agg_table_sql
                    )
