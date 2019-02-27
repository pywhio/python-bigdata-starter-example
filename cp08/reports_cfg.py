import numpy as np


def add_timefield(s):
    """recieve a row Series ,transform it, then return the Series"""
    s['timescale'] = str(s['交易时间'])[:-2]
    return s

re_cfg = {
    ## pandas has 'mean', 'median', 'prod', 'sum', 'std', 'var', 'count'
    're-site':{
                'groupby_fields':['timescale','交易网点','交易类型'],  #可对add_fields中定义的字段进行groupby操作
                'agg_fields':{'交易金额':['sum','count']}, #可对单个字段增加不同运算方法
                'map_fields':{} #对最终输出字段重命名
              },

    ## numpy has np.sum , np.mean , np.std, np.var .... and user define func
    're-customer':{
                'groupby_fields':['timescale','客户id','交易类型'],
                'agg_fields':{'交易金额':[np.sum,'count']},
                'map_fields':{}
              },
    }
