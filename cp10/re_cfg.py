re_day_cfg={
    're_site':{'time_field':'timescale',
                'groupby_fields': ['交易网点','交易类型'],
                'agg_fields': {'交易金额_sum':'sum', '交易金额_count':'sum'},
                },
    're_customer':{'time_field':'timescale',
                'groupby_fields': ['客户id','交易类型'],
                'agg_fields': {'交易金额_sum':'sum', '交易金额_count':'sum'},
                },
}

pg_conn_dict = {
	"host": "localhost",
	"dbname": "postgres",
	"user":"postgres",
	"password":"root"
}
