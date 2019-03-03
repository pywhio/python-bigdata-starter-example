CREATE TABLE public.re_site
(
    timescale timestamp with time zone,
    "交易网点" text COLLATE pg_catalog."default",
    "交易类型" text COLLATE pg_catalog."default",
    "交易金额_sum" bigint,
    "交易金额_count" bigint
);

CREATE TABLE public.re_site_d
(
    timescale timestamp with time zone,
    "交易网点" text COLLATE pg_catalog."default",
    "交易类型" text COLLATE pg_catalog."default",
    "交易金额_sum" bigint,
    "交易金额_count" bigint
);

CREATE TABLE public.re_customer
(
    timescale timestamp with time zone,
    "客户id" text COLLATE pg_catalog."default",
    "交易类型" text COLLATE pg_catalog."default",
    "交易金额_sum" bigint,
    "交易金额_count" bigint
);

CREATE TABLE public.re_customer_d
(
    timescale timestamp with time zone,
    "客户id" text COLLATE pg_catalog."default",
    "交易类型" text COLLATE pg_catalog."default",
    "交易金额_sum" bigint,
    "交易金额_count" bigint
);
