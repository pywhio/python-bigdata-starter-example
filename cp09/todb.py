import pandas as pd
from sqlalchemy import create_engine
from reports_cfg import re_cfg, add_timefield, pg_conn_dict
import sys,traceback

def report_df(df, add_fields=None, re_cfg=re_cfg):
    #根据新增字段配置，增加字段
    result = {}
    df = df.apply(add_timefield, axis='columns') if add_fields else df
    for report_name, agg_cfg in re_cfg.items():
        #根据配置执行grouby和aggegration操作
        df_agg = df.groupby(agg_cfg['groupby_fields']).agg(agg_cfg['agg_fields'])
        #根据是否2层columns,看是降为1层
        if df_agg.columns.nlevels ==2 :
            df_agg.columns = ['_'.join(c) for c in df_agg.columns]
        #根据配置重命名
        df_agg.rename(agg_cfg['map_fields'], axis='columns')
        result[report_name] = df_agg
    return result

def agg2db(filename):
    result = []
    uri = 'postgresql://%s:%s@%s:%s/%s' % (pg_conn_dict['user'], pg_conn_dict['password'], pg_conn_dict['host'],5432,pg_conn_dict['dbname'])
    print('db uri:',uri)
    con = create_engine(uri)
    dfo = pd.read_csv(filename)
    dfs = report_df(dfo, add_fields=add_timefield, re_cfg=re_cfg)
    for tablename, df in dfs.items():
        try:
            df.to_sql(tablename, con=con, if_exists='append')
        except :
            #traceback.format_exc() return current exception info string
            log = traceback.format_exc()
            result.append([1,tablename,log])
            break
        log = 'table:%s , insert records:%s' % (tablename, len(df))
        result.append([0,tablename,log])
        print(log)
    return result

if __name__ == '__main__':
    result = agg2db('QLR201902071000-merged.csv')
    print('return: %s' % result)


# ➜  cp09 git:(master) ✗ python todb.py
# db uri: postgresql://postgres:root@localhost:5432/postgres
# table:re_site , insert records:2
# table:re_customer , insert records:3
# return: [[0, 're_site', 'table:re_site , insert records:2'], [0, 're_customer', 'table:re_customer , insert records:3']]
# ➜  cp09 git:(master) ✗


#
# ➜  cp09 git:(master) ✗ python todb.py
# db uri: postgresql://p33ostgres:ro3ot22@localhost:5432/postgres
# return: [[1, 're_site', 'Traceback (most recent call last):\n  File "/Users/zengqingbo/project/.direnv/python-3.6.5/lib/python3.6/site-packages/sqlalchemy/engine/base.py", line 2158, in _wrap_pool_connect\n    return fn()\n  File "/Users/zengqingbo/project/.direnv/python-3.6.5/lib/python3.6/site-packages/sqlalchemy/pool.py", line 403, in connect\n    return _ConnectionFairy._checkout(self)\n  File "/Users/zengqingbo/project/.direnv/python-3.6.5/lib/python3.6/site-packages/sqlalchemy/pool.py", line 791, in _checkout\n    fairy = _ConnectionRecord.checkout(pool)\n  File "/Users/zengqingbo/project/.direnv/python-3.6.5/lib/python3.6/site-packages/sqlalchemy/pool.py", line 532, in checkout\n    rec = pool._do_get()\n  File "/Users/zengqingbo/project/.direnv/python-3.6.5/lib/python3.6/site-packages/sqlalchemy/pool.py", line 1196, in _do_get\n    self._dec_overflow()\n  File "/Users/zengqingbo/project/.direnv/python-3.6.5/lib/python3.6/site-packages/sqlalchemy/util/langhelpers.py", line 66, in __exit__\n    compat.reraise(exc_type, exc_value, exc_tb)\n  File "/Users/zengqingbo/project/.direnv/python-3.6.5/lib/python3.6/site-packages/sqlalchemy/util/compat.py", line 187, in reraise\n    raise value\n  File "/Users/zengqingbo/project/.direnv/python-3.6.5/lib/python3.6/site-packages/sqlalchemy/pool.py", line 1193, in _do_get\n    return self._create_connection()\n  File "/Users/zengqingbo/project/.direnv/python-3.6.5/lib/python3.6/site-packages/sqlalchemy/pool.py", line 350, in _create_connection\n    return _ConnectionRecord(self)\n  File "/Users/zengqingbo/project/.direnv/python-3.6.5/lib/python3.6/site-packages/sqlalchemy/pool.py", line 477, in __init__\n    self.__connect(first_connect_check=True)\n  File "/Users/zengqingbo/project/.direnv/python-3.6.5/lib/python3.6/site-packages/sqlalchemy/pool.py", line 674, in __connect\n    connection = pool._invoke_creator(self)\n  File "/Users/zengqingbo/project/.direnv/python-3.6.5/lib/python3.6/site-packages/sqlalchemy/engine/strategies.py", line 106, in connect\n    return dialect.connect(*cargs, **cparams)\n  File "/Users/zengqingbo/project/.direnv/python-3.6.5/lib/python3.6/site-packages/sqlalchemy/engine/default.py", line 411, in connect\n    return self.dbapi.connect(*cargs, **cparams)\n  File "/Users/zengqingbo/project/.direnv/python-3.6.5/lib/python3.6/site-packages/psycopg2/__init__.py", line 130, in connect\n    conn = _connect(dsn, connection_factory=connection_factory, **kwasync)\npsycopg2.OperationalError: FATAL:  role "p33ostgres" does not exist\n\n\nThe above exception was the direct cause of the following exception:\n\nTraceback (most recent call last):\n  File "todb.py", line 30, in agg2db\n    df.to_sql(tablename, con=con, if_exists=\'append\')\n  File "/Users/zengqingbo/project/.direnv/python-3.6.5/lib/python3.6/site-packages/pandas/core/generic.py", line 2127, in to_sql\n    dtype=dtype)\n  File "/Users/zengqingbo/project/.direnv/python-3.6.5/lib/python3.6/site-packages/pandas/io/sql.py", line 450, in to_sql\n    chunksize=chunksize, dtype=dtype)\n  File "/Users/zengqingbo/project/.direnv/python-3.6.5/lib/python3.6/site-packages/pandas/io/sql.py", line 1148, in to_sql\n    table.create()\n  File "/Users/zengqingbo/project/.direnv/python-3.6.5/lib/python3.6/site-packages/pandas/io/sql.py", line 561, in create\n    if self.exists():\n  File "/Users/zengqingbo/project/.direnv/python-3.6.5/lib/python3.6/site-packages/pandas/io/sql.py", line 549, in exists\n    return self.pd_sql.has_table(self.name, self.schema)\n  File "/Users/zengqingbo/project/.direnv/python-3.6.5/lib/python3.6/site-packages/pandas/io/sql.py", line 1176, in has_table\n    schema or self.meta.schema,\n  File "/Users/zengqingbo/project/.direnv/python-3.6.5/lib/python3.6/site-packages/sqlalchemy/engine/base.py", line 2055, in run_callable\n    with self.contextual_connect() as conn:\n  File "/Users/zengqingbo/project/.direnv/python-3.6.5/lib/python3.6/site-packages/sqlalchemy/engine/base.py", line 2123, in contextual_connect\n    self._wrap_pool_connect(self.pool.connect, None),\n  File "/Users/zengqingbo/project/.direnv/python-3.6.5/lib/python3.6/site-packages/sqlalchemy/engine/base.py", line 2162, in _wrap_pool_connect\n    e, dialect, self)\n  File "/Users/zengqingbo/project/.direnv/python-3.6.5/lib/python3.6/site-packages/sqlalchemy/engine/base.py", line 1476, in _handle_dbapi_exception_noconnection\n    exc_info\n  File "/Users/zengqingbo/project/.direnv/python-3.6.5/lib/python3.6/site-packages/sqlalchemy/util/compat.py", line 203, in raise_from_cause\n    reraise(type(exception), exception, tb=exc_tb, cause=cause)\n  File "/Users/zengqingbo/project/.direnv/python-3.6.5/lib/python3.6/site-packages/sqlalchemy/util/compat.py", line 186, in reraise\n    raise value.with_traceback(tb)\n  File "/Users/zengqingbo/project/.direnv/python-3.6.5/lib/python3.6/site-packages/sqlalchemy/engine/base.py", line 2158, in _wrap_pool_connect\n    return fn()\n  File "/Users/zengqingbo/project/.direnv/python-3.6.5/lib/python3.6/site-packages/sqlalchemy/pool.py", line 403, in connect\n    return _ConnectionFairy._checkout(self)\n  File "/Users/zengqingbo/project/.direnv/python-3.6.5/lib/python3.6/site-packages/sqlalchemy/pool.py", line 791, in _checkout\n    fairy = _ConnectionRecord.checkout(pool)\n  File "/Users/zengqingbo/project/.direnv/python-3.6.5/lib/python3.6/site-packages/sqlalchemy/pool.py", line 532, in checkout\n    rec = pool._do_get()\n  File "/Users/zengqingbo/project/.direnv/python-3.6.5/lib/python3.6/site-packages/sqlalchemy/pool.py", line 1196, in _do_get\n    self._dec_overflow()\n  File "/Users/zengqingbo/project/.direnv/python-3.6.5/lib/python3.6/site-packages/sqlalchemy/util/langhelpers.py", line 66, in __exit__\n    compat.reraise(exc_type, exc_value, exc_tb)\n  File "/Users/zengqingbo/project/.direnv/python-3.6.5/lib/python3.6/site-packages/sqlalchemy/util/compat.py", line 187, in reraise\n    raise value\n  File "/Users/zengqingbo/project/.direnv/python-3.6.5/lib/python3.6/site-packages/sqlalchemy/pool.py", line 1193, in _do_get\n    return self._create_connection()\n  File "/Users/zengqingbo/project/.direnv/python-3.6.5/lib/python3.6/site-packages/sqlalchemy/pool.py", line 350, in _create_connection\n    return _ConnectionRecord(self)\n  File "/Users/zengqingbo/project/.direnv/python-3.6.5/lib/python3.6/site-packages/sqlalchemy/pool.py", line 477, in __init__\n    self.__connect(first_connect_check=True)\n  File "/Users/zengqingbo/project/.direnv/python-3.6.5/lib/python3.6/site-packages/sqlalchemy/pool.py", line 674, in __connect\n    connection = pool._invoke_creator(self)\n  File "/Users/zengqingbo/project/.direnv/python-3.6.5/lib/python3.6/site-packages/sqlalchemy/engine/strategies.py", line 106, in connect\n    return dialect.connect(*cargs, **cparams)\n  File "/Users/zengqingbo/project/.direnv/python-3.6.5/lib/python3.6/site-packages/sqlalchemy/engine/default.py", line 411, in connect\n    return self.dbapi.connect(*cargs, **cparams)\n  File "/Users/zengqingbo/project/.direnv/python-3.6.5/lib/python3.6/site-packages/psycopg2/__init__.py", line 130, in connect\n    conn = _connect(dsn, connection_factory=connection_factory, **kwasync)\nsqlalchemy.exc.OperationalError: (psycopg2.OperationalError) FATAL:  role "p33ostgres" does not exist\n (Background on this error at: http://sqlalche.me/e/e3q8)\n']]
# ➜  cp09 git:(master) ✗
