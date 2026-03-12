--
-- PostgreSQL database dump
--

\restrict 0l7hXAW0Qj7tlfVvKSkCrRZwkuu5MhcAg2v6ZHnAdLQYBvdSibGgF5yxjQU0KCx

-- Dumped from database version 18.3
-- Dumped by pg_dump version 18.3

-- Started on 2026-03-12 11:38:33

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 2 (class 3079 OID 17393)
-- Name: timescaledb; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS timescaledb WITH SCHEMA public;


--
-- TOC entry 5674 (class 0 OID 0)
-- Dependencies: 2
-- Name: EXTENSION timescaledb; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION timescaledb IS 'Enables scalable inserts and complex queries for time-series data (Community Edition)';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 237 (class 1259 OID 17386)
-- Name: dsm_records; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.dsm_records (
    "timestamp" timestamp without time zone NOT NULL,
    plant_id integer NOT NULL,
    schedule numeric(20,2),
    actual numeric(20,2),
    deviation numeric(10,2),
    penalty numeric(12,2)
);


ALTER TABLE public.dsm_records OWNER TO postgres;

--
-- TOC entry 236 (class 1259 OID 17379)
-- Name: realtime_data; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.realtime_data (
    "timestamp" timestamp without time zone NOT NULL,
    plant_id integer NOT NULL,
    frequency numeric(5,2),
    generation numeric(20,2),
    schedule numeric(20,2),
    deviation numeric(10,2)
);


ALTER TABLE public.realtime_data OWNER TO postgres;

--
-- TOC entry 235 (class 1259 OID 17364)
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying(50) NOT NULL,
    password_hash text NOT NULL,
    role character varying(20) NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.users OWNER TO postgres;

--
-- TOC entry 234 (class 1259 OID 17363)
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO postgres;

--
-- TOC entry 5675 (class 0 OID 0)
-- Dependencies: 234
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- TOC entry 5385 (class 2604 OID 17367)
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- TOC entry 5358 (class 0 OID 17420)
-- Dependencies: 239
-- Data for Name: hypertable; Type: TABLE DATA; Schema: _timescaledb_catalog; Owner: postgres
--

COPY _timescaledb_catalog.hypertable (id, schema_name, table_name, associated_schema_name, associated_table_prefix, num_dimensions, chunk_sizing_func_schema, chunk_sizing_func_name, chunk_target_size, compression_state, compressed_hypertable_id, status) FROM stdin;
1	public	realtime_data	_timescaledb_internal	_hyper_1	1	_timescaledb_functions	calculate_chunk_interval	0	0	\N	0
\.


--
-- TOC entry 5364 (class 0 OID 17513)
-- Dependencies: 247
-- Data for Name: chunk; Type: TABLE DATA; Schema: _timescaledb_catalog; Owner: postgres
--

COPY _timescaledb_catalog.chunk (id, hypertable_id, schema_name, table_name, compressed_chunk_id, dropped, status, osm_chunk, creation_time) FROM stdin;
\.


--
-- TOC entry 5368 (class 0 OID 17566)
-- Dependencies: 251
-- Data for Name: chunk_column_stats; Type: TABLE DATA; Schema: _timescaledb_catalog; Owner: postgres
--

COPY _timescaledb_catalog.chunk_column_stats (id, hypertable_id, chunk_id, column_name, range_start, range_end, valid) FROM stdin;
\.


--
-- TOC entry 5360 (class 0 OID 17470)
-- Dependencies: 243
-- Data for Name: dimension; Type: TABLE DATA; Schema: _timescaledb_catalog; Owner: postgres
--

COPY _timescaledb_catalog.dimension (id, hypertable_id, column_name, column_type, aligned, num_slices, partitioning_func_schema, partitioning_func, interval_length, compress_interval_length, integer_now_func_schema, integer_now_func) FROM stdin;
1	1	timestamp	timestamp without time zone	t	\N	\N	\N	604800000000	\N	\N	\N
\.


--
-- TOC entry 5362 (class 0 OID 17494)
-- Dependencies: 245
-- Data for Name: dimension_slice; Type: TABLE DATA; Schema: _timescaledb_catalog; Owner: postgres
--

COPY _timescaledb_catalog.dimension_slice (id, dimension_id, range_start, range_end) FROM stdin;
\.


--
-- TOC entry 5366 (class 0 OID 17546)
-- Dependencies: 248
-- Data for Name: chunk_constraint; Type: TABLE DATA; Schema: _timescaledb_catalog; Owner: postgres
--

COPY _timescaledb_catalog.chunk_constraint (chunk_id, dimension_slice_id, constraint_name, hypertable_constraint_name) FROM stdin;
\.


--
-- TOC entry 5381 (class 0 OID 17826)
-- Dependencies: 269
-- Data for Name: compression_chunk_size; Type: TABLE DATA; Schema: _timescaledb_catalog; Owner: postgres
--

COPY _timescaledb_catalog.compression_chunk_size (chunk_id, compressed_chunk_id, uncompressed_heap_size, uncompressed_toast_size, uncompressed_index_size, compressed_heap_size, compressed_toast_size, compressed_index_size, numrows_pre_compression, numrows_post_compression, numrows_frozen_immediately) FROM stdin;
\.


--
-- TOC entry 5380 (class 0 OID 17814)
-- Dependencies: 268
-- Data for Name: compression_settings; Type: TABLE DATA; Schema: _timescaledb_catalog; Owner: postgres
--

COPY _timescaledb_catalog.compression_settings (relid, compress_relid, segmentby, orderby, orderby_desc, orderby_nullsfirst, index) FROM stdin;
\.


--
-- TOC entry 5373 (class 0 OID 17697)
-- Dependencies: 260
-- Data for Name: continuous_agg; Type: TABLE DATA; Schema: _timescaledb_catalog; Owner: postgres
--

COPY _timescaledb_catalog.continuous_agg (mat_hypertable_id, raw_hypertable_id, parent_mat_hypertable_id, user_view_schema, user_view_name, partial_view_schema, partial_view_name, direct_view_schema, direct_view_name, materialized_only, finalized) FROM stdin;
\.


--
-- TOC entry 5382 (class 0 OID 17850)
-- Dependencies: 270
-- Data for Name: continuous_agg_migrate_plan; Type: TABLE DATA; Schema: _timescaledb_catalog; Owner: postgres
--

COPY _timescaledb_catalog.continuous_agg_migrate_plan (mat_hypertable_id, start_ts, end_ts, user_view_definition) FROM stdin;
\.


--
-- TOC entry 5383 (class 0 OID 17861)
-- Dependencies: 272
-- Data for Name: continuous_agg_migrate_plan_step; Type: TABLE DATA; Schema: _timescaledb_catalog; Owner: postgres
--

COPY _timescaledb_catalog.continuous_agg_migrate_plan_step (mat_hypertable_id, step_id, status, start_ts, end_ts, type, config) FROM stdin;
\.


--
-- TOC entry 5374 (class 0 OID 17734)
-- Dependencies: 261
-- Data for Name: continuous_aggs_bucket_function; Type: TABLE DATA; Schema: _timescaledb_catalog; Owner: postgres
--

COPY _timescaledb_catalog.continuous_aggs_bucket_function (mat_hypertable_id, bucket_func, bucket_width, bucket_origin, bucket_offset, bucket_timezone, bucket_fixed_width) FROM stdin;
\.


--
-- TOC entry 5377 (class 0 OID 17775)
-- Dependencies: 264
-- Data for Name: continuous_aggs_hypertable_invalidation_log; Type: TABLE DATA; Schema: _timescaledb_catalog; Owner: postgres
--

COPY _timescaledb_catalog.continuous_aggs_hypertable_invalidation_log (hypertable_id, lowest_modified_value, greatest_modified_value) FROM stdin;
\.


--
-- TOC entry 5375 (class 0 OID 17751)
-- Dependencies: 262
-- Data for Name: continuous_aggs_invalidation_threshold; Type: TABLE DATA; Schema: _timescaledb_catalog; Owner: postgres
--

COPY _timescaledb_catalog.continuous_aggs_invalidation_threshold (hypertable_id, watermark) FROM stdin;
\.


--
-- TOC entry 5378 (class 0 OID 17782)
-- Dependencies: 265
-- Data for Name: continuous_aggs_materialization_invalidation_log; Type: TABLE DATA; Schema: _timescaledb_catalog; Owner: postgres
--

COPY _timescaledb_catalog.continuous_aggs_materialization_invalidation_log (materialization_id, lowest_modified_value, greatest_modified_value) FROM stdin;
\.


--
-- TOC entry 5379 (class 0 OID 17793)
-- Dependencies: 266
-- Data for Name: continuous_aggs_materialization_ranges; Type: TABLE DATA; Schema: _timescaledb_catalog; Owner: postgres
--

COPY _timescaledb_catalog.continuous_aggs_materialization_ranges (materialization_id, lowest_modified_value, greatest_modified_value) FROM stdin;
\.


--
-- TOC entry 5376 (class 0 OID 17763)
-- Dependencies: 263
-- Data for Name: continuous_aggs_watermark; Type: TABLE DATA; Schema: _timescaledb_catalog; Owner: postgres
--

COPY _timescaledb_catalog.continuous_aggs_watermark (mat_hypertable_id, watermark) FROM stdin;
\.


--
-- TOC entry 5372 (class 0 OID 17678)
-- Dependencies: 258
-- Data for Name: metadata; Type: TABLE DATA; Schema: _timescaledb_catalog; Owner: postgres
--

COPY _timescaledb_catalog.metadata (key, value, include_in_telemetry) FROM stdin;
install_timestamp	2026-03-11 11:56:00.206317+05:30	t
timescaledb_version	2.24.0	f
exported_uuid	34f589f7-3cf1-4b8e-bf1c-34e6ff06bbe0	t
\.


--
-- TOC entry 5359 (class 0 OID 17453)
-- Dependencies: 241
-- Data for Name: tablespace; Type: TABLE DATA; Schema: _timescaledb_catalog; Owner: postgres
--

COPY _timescaledb_catalog.tablespace (id, hypertable_id, tablespace_name) FROM stdin;
\.


--
-- TOC entry 5371 (class 0 OID 17592)
-- Dependencies: 253
-- Data for Name: bgw_job; Type: TABLE DATA; Schema: _timescaledb_config; Owner: postgres
--

COPY _timescaledb_config.bgw_job (id, application_name, schedule_interval, max_runtime, max_retries, retry_period, proc_schema, proc_name, owner, scheduled, fixed_schedule, initial_start, hypertable_id, config, check_schema, check_name, timezone) FROM stdin;
\.


--
-- TOC entry 5668 (class 0 OID 17386)
-- Dependencies: 237
-- Data for Name: dsm_records; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.dsm_records ("timestamp", plant_id, schedule, actual, deviation, penalty) FROM stdin;
\.


--
-- TOC entry 5667 (class 0 OID 17379)
-- Dependencies: 236
-- Data for Name: realtime_data; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.realtime_data ("timestamp", plant_id, frequency, generation, schedule, deviation) FROM stdin;
\.


--
-- TOC entry 5666 (class 0 OID 17364)
-- Dependencies: 235
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, username, password_hash, role, created_at) FROM stdin;
\.


--
-- TOC entry 5676 (class 0 OID 0)
-- Dependencies: 250
-- Name: chunk_column_stats_id_seq; Type: SEQUENCE SET; Schema: _timescaledb_catalog; Owner: postgres
--

SELECT pg_catalog.setval('_timescaledb_catalog.chunk_column_stats_id_seq', 1, false);


--
-- TOC entry 5677 (class 0 OID 0)
-- Dependencies: 249
-- Name: chunk_constraint_name; Type: SEQUENCE SET; Schema: _timescaledb_catalog; Owner: postgres
--

SELECT pg_catalog.setval('_timescaledb_catalog.chunk_constraint_name', 1, false);


--
-- TOC entry 5678 (class 0 OID 0)
-- Dependencies: 246
-- Name: chunk_id_seq; Type: SEQUENCE SET; Schema: _timescaledb_catalog; Owner: postgres
--

SELECT pg_catalog.setval('_timescaledb_catalog.chunk_id_seq', 1, false);


--
-- TOC entry 5679 (class 0 OID 0)
-- Dependencies: 271
-- Name: continuous_agg_migrate_plan_step_step_id_seq; Type: SEQUENCE SET; Schema: _timescaledb_catalog; Owner: postgres
--

SELECT pg_catalog.setval('_timescaledb_catalog.continuous_agg_migrate_plan_step_step_id_seq', 1, false);


--
-- TOC entry 5680 (class 0 OID 0)
-- Dependencies: 242
-- Name: dimension_id_seq; Type: SEQUENCE SET; Schema: _timescaledb_catalog; Owner: postgres
--

SELECT pg_catalog.setval('_timescaledb_catalog.dimension_id_seq', 1, true);


--
-- TOC entry 5681 (class 0 OID 0)
-- Dependencies: 244
-- Name: dimension_slice_id_seq; Type: SEQUENCE SET; Schema: _timescaledb_catalog; Owner: postgres
--

SELECT pg_catalog.setval('_timescaledb_catalog.dimension_slice_id_seq', 1, false);


--
-- TOC entry 5682 (class 0 OID 0)
-- Dependencies: 238
-- Name: hypertable_id_seq; Type: SEQUENCE SET; Schema: _timescaledb_catalog; Owner: postgres
--

SELECT pg_catalog.setval('_timescaledb_catalog.hypertable_id_seq', 1, true);


--
-- TOC entry 5683 (class 0 OID 0)
-- Dependencies: 252
-- Name: bgw_job_id_seq; Type: SEQUENCE SET; Schema: _timescaledb_config; Owner: postgres
--

SELECT pg_catalog.setval('_timescaledb_config.bgw_job_id_seq', 1000, false);


--
-- TOC entry 5684 (class 0 OID 0)
-- Dependencies: 234
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 1, false);


--
-- TOC entry 5434 (class 2606 OID 17392)
-- Name: dsm_records dsm_records_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dsm_records
    ADD CONSTRAINT dsm_records_pkey PRIMARY KEY ("timestamp", plant_id);


--
-- TOC entry 5431 (class 2606 OID 17385)
-- Name: realtime_data realtime_data_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.realtime_data
    ADD CONSTRAINT realtime_data_pkey PRIMARY KEY ("timestamp", plant_id);


--
-- TOC entry 5427 (class 2606 OID 17376)
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- TOC entry 5429 (class 2606 OID 17378)
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- TOC entry 5432 (class 1259 OID 18299)
-- Name: realtime_data_timestamp_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX realtime_data_timestamp_idx ON public.realtime_data USING btree ("timestamp" DESC);


-- Completed on 2026-03-12 11:38:34

--
-- PostgreSQL database dump complete
--

\unrestrict 0l7hXAW0Qj7tlfVvKSkCrRZwkuu5MhcAg2v6ZHnAdLQYBvdSibGgF5yxjQU0KCx

