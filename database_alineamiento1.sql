--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.3
-- Dumped by pg_dump version 9.5.3

-- Started on 2016-11-29 21:06:33

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 2116 (class 1262 OID 12373)
-- Name: postgres; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE postgres WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'Spanish_Ecuador.1252' LC_CTYPE = 'Spanish_Ecuador.1252';


ALTER DATABASE postgres OWNER TO postgres;

\connect postgres

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 2117 (class 1262 OID 12373)
-- Dependencies: 2116
-- Name: postgres; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON DATABASE postgres IS 'default administrative connection database';


--
-- TOC entry 1 (class 3079 OID 12355)
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- TOC entry 2120 (class 0 OID 0)
-- Dependencies: 1
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 181 (class 1259 OID 16392)
-- Name: archivos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE archivos (
    nombre_archivo character varying(30),
    tipo_archivo character varying(3),
    inidice_linea integer NOT NULL,
    linea text,
    retention_time double precision,
    first_scan integer,
    max_scan integer,
    last_scan integer,
    pk_ty character varying(10),
    peak_height character varying(10),
    concentracion character varying(20),
    corr_max_porc character varying(10),
    por_tot character varying(10)
);


ALTER TABLE archivos OWNER TO postgres;

--
-- TOC entry 183 (class 1259 OID 16429)
-- Name: procesos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE procesos (
    oid integer NOT NULL,
    tiempo_ejecucion_alineamiento double precision,
    tiempo_ejecucion_proceso double precision,
    intervalo_time double precision,
    intensidad_aceptacion integer,
    min_interval_confianza double precision,
    max_interval_confianza double precision,
    archivo character varying(255),
    num_alineaciones integer
);


ALTER TABLE procesos OWNER TO postgres;

--
-- TOC entry 182 (class 1259 OID 16400)
-- Name: resultados; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE resultados (
    oid integer NOT NULL,
    intervalo_time double precision,
    intensidad_aceptacion integer,
    min_interval_confianza double precision,
    max_interval_confianza double precision,
    line_result text,
    col1 character varying(255),
    col2 character varying(255),
    col3 character varying(255),
    col4 character varying(255),
    archivo character varying(255)
);


ALTER TABLE resultados OWNER TO postgres;

--
-- TOC entry 2119 (class 0 OID 0)
-- Dependencies: 6
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


-- Completed on 2016-11-29 21:06:33

--
-- PostgreSQL database dump complete
--

