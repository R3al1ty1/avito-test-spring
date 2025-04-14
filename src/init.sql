SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

CREATE TABLE public.products (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    date_time timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    type character varying(50) NOT NULL,
    reception_id uuid NOT NULL,
    order_in_reception integer NOT NULL,
    CONSTRAINT product_type_check CHECK (((type)::text = ANY ((ARRAY['электроника'::character varying, 'одежда'::character varying, 'обувь'::character varying])::text[])))
);


ALTER TABLE public.products OWNER TO postgres;

CREATE SEQUENCE public.product_order_in_reception_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.product_order_in_reception_seq OWNER TO postgres;

ALTER SEQUENCE public.product_order_in_reception_seq OWNED BY public.products.order_in_reception;

CREATE TABLE public.pvz (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    registration_date timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    city character varying(100) NOT NULL,
    CONSTRAINT pvz_city_check CHECK (((city)::text = ANY ((ARRAY['Москва'::character varying, 'Санкт-Петербург'::character varying, 'Казань'::character varying])::text[])))
);


ALTER TABLE public.pvz OWNER TO postgres;

CREATE TABLE public.receptions (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    date_time timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    pvz_id uuid NOT NULL,
    status character varying(20) DEFAULT 'in_progress'::character varying NOT NULL,
    CONSTRAINT reception_status_check CHECK (((status)::text = ANY ((ARRAY['in_progress'::character varying, 'close'::character varying])::text[])))
);


ALTER TABLE public.receptions OWNER TO postgres;

CREATE TABLE public.users (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    email character varying(255) NOT NULL,
    password_hash character varying(255) NOT NULL,
    role character varying(20) NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT users_role_check CHECK (((role)::text = ANY ((ARRAY['employee'::character varying, 'moderator'::character varying])::text[])))
);


ALTER TABLE public.users OWNER TO postgres;

ALTER TABLE ONLY public.products ALTER COLUMN order_in_reception SET DEFAULT nextval('public.product_order_in_reception_seq'::regclass);

COPY public.products (id, date_time, type, reception_id, order_in_reception) FROM stdin;
\.

COPY public.pvz (id, registration_date, city) FROM stdin;
\.

COPY public.receptions (id, date_time, pvz_id, status) FROM stdin;
\.

COPY public.users (id, email, password_hash, role, created_at) FROM stdin;
\.

SELECT pg_catalog.setval('public.product_order_in_reception_seq', 1, false);

ALTER TABLE ONLY public.products
    ADD CONSTRAINT product_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.pvz
    ADD CONSTRAINT pvz_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.receptions
    ADD CONSTRAINT reception_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);

CREATE INDEX idx_product_reception_id ON public.products USING btree (reception_id);

CREATE INDEX idx_reception_pvz_id ON public.receptions USING btree (pvz_id);

CREATE INDEX idx_reception_status ON public.receptions USING btree (status);

ALTER TABLE ONLY public.products
    ADD CONSTRAINT product_reception_id_fkey FOREIGN KEY (reception_id) REFERENCES public.receptions(id);

ALTER TABLE ONLY public.receptions
    ADD CONSTRAINT reception_pvz_id_fkey FOREIGN KEY (pvz_id) REFERENCES public.pvz(id);
