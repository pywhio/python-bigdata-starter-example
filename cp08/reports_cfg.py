import numpy as np

re_cfg = {
    're-site':{'groupby_fields':['交易网点','交易类型'],
                'agg_fields':{'交易金额':'sum'},
              },
    're-customer':{'groupby_fields':['客户id','交易类型'],
                'agg_fields':{'交易金额':np.sum},
              },
    }
