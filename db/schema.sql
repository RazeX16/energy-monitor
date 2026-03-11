--
-- PostgreSQL database dump
--

\restrict YKTitxgo65YOkaGkKF4CfCSQnNlbqgfu0QzatxY8TAsiupiXw9bzcl5as8yUilY

-- Dumped from database version 18.3
-- Dumped by pg_dump version 18.3

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
-- Name: timescaledb; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS timescaledb WITH SCHEMA public;


--
-- Name: EXTENSION timescaledb; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION timescaledb IS 'Enables scalable inserts and complex queries for time-series data (Community Edition)';


--
-- PostgreSQL database dump complete
--

\unrestrict YKTitxgo65YOkaGkKF4CfCSQnNlbqgfu0QzatxY8TAsiupiXw9bzcl5as8yUilY

