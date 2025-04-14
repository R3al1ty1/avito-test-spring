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

SET default_tablespace = '';

SET default_table_access_method = heap;

CREATE TABLE public.products (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    date_time timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    type character varying(50) NOT NULL,
    reception_id uuid NOT NULL,
    order_in_reception integer NOT NULL,
    CONSTRAINT product_type_check CHECK (((type)::text = ANY (ARRAY[('электроника'::character varying)::text, ('одежда'::character varying)::text, ('обувь'::character varying)::text])))
);


ALTER TABLE public.products OWNER TO postgres;

CREATE SEQUENCE public.product_order_in_reception_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE public.product_order_in_reception_seq OWNER TO postgres;

ALTER SEQUENCE public.product_order_in_reception_seq OWNED BY public.products.order_in_reception;

CREATE TABLE public.pvz (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    registration_date timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    city character varying(100) NOT NULL,
    CONSTRAINT pvz_city_check CHECK (((city)::text = ANY (ARRAY[('Москва'::character varying)::text, ('Санкт-Петербург'::character varying)::text, ('Казань'::character varying)::text])))
);


ALTER TABLE public.pvz OWNER TO postgres;

CREATE TABLE public.receptions (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    date_time timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    pvz_id uuid NOT NULL,
    status character varying(20) DEFAULT 'in_progress'::character varying NOT NULL,
    CONSTRAINT reception_status_check CHECK (((status)::text = ANY (ARRAY[('in_progress'::character varying)::text, ('close'::character varying)::text])))
);


ALTER TABLE public.receptions OWNER TO postgres;

CREATE TABLE public.users (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    email character varying(255) NOT NULL,
    password_hash character varying(255) NOT NULL,
    role character varying(20) NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT users_role_check CHECK (((role)::text = ANY (ARRAY[('employee'::character varying)::text, ('moderator'::character varying)::text])))
);


ALTER TABLE public.users OWNER TO postgres;

ALTER TABLE ONLY public.products ALTER COLUMN order_in_reception SET DEFAULT nextval('public.product_order_in_reception_seq'::regclass);

COPY public.products (id, date_time, type, reception_id, order_in_reception) FROM stdin;
56ce39ea-ffbc-48a7-b85a-d96d7ce497ae	2025-04-14 17:11:37.982804+00	электроника	12570bda-545e-4b88-bacb-fee282682e73	1
6b762723-7e5a-473e-909b-3e57f45888cf	2025-04-14 17:11:41.434953+00	обувь	12570bda-545e-4b88-bacb-fee282682e73	2
37487550-a261-46e2-968a-287ee8a2dd2f	2025-04-14 17:12:11.536186+00	обувь	6e02b329-ab24-49e3-a325-9f73759941d2	3
7261e8ae-7aa3-42a2-87c8-a1021d5d3dbc	2025-04-14 17:12:19.351501+00	электроника	6e02b329-ab24-49e3-a325-9f73759941d2	4
f2ddbe12-6fd5-4a72-8969-5c6ddce909d1	2025-04-14 17:12:25.490448+00	одежда	6e02b329-ab24-49e3-a325-9f73759941d2	5
729dd4a0-cd80-4273-b63d-e151a5e572a0	2025-04-14 17:12:26.165191+00	одежда	6e02b329-ab24-49e3-a325-9f73759941d2	6
11cfad1e-2573-4606-848c-6cf9701a6c63	2025-04-14 17:12:26.692643+00	одежда	6e02b329-ab24-49e3-a325-9f73759941d2	7
44c14c2a-5e79-49f9-870a-60731dc023d3	2025-04-14 17:12:48.94211+00	одежда	9f53ae04-1ff7-415e-9a6d-8d9d2872e55f	8
f5777ffc-a2a4-4861-96c9-d47189c1f9d3	2025-04-14 17:12:49.407256+00	одежда	9f53ae04-1ff7-415e-9a6d-8d9d2872e55f	9
07b9f787-3f72-4274-a59a-ec85de14e46f	2025-04-14 17:12:49.818519+00	одежда	9f53ae04-1ff7-415e-9a6d-8d9d2872e55f	10
\.

COPY public.pvz (id, registration_date, city) FROM stdin;
dfe664a4-0c81-4368-a8c6-9a6f0449de55	2025-04-14 17:09:52.96284+00	Москва
65f9855a-ecc9-4c9c-97fb-51937878e064	2025-04-14 17:09:58.640275+00	Казань
\.

COPY public.receptions (id, date_time, pvz_id, status) FROM stdin;
9f53ae04-1ff7-415e-9a6d-8d9d2872e55f	2025-04-14 17:10:44.715551+00	65f9855a-ecc9-4c9c-97fb-51937878e064	in_progress
12570bda-545e-4b88-bacb-fee282682e73	2025-04-14 17:11:04.964668+00	dfe664a4-0c81-4368-a8c6-9a6f0449de55	close
6e02b329-ab24-49e3-a325-9f73759941d2	2025-04-14 17:12:08.05292+00	dfe664a4-0c81-4368-a8c6-9a6f0449de55	in_progress
\.

COPY public.users (id, email, password_hash, role, created_at) FROM stdin;
f643c11b-a7a0-456b-95a7-754d59940bd6	ikworkmail@yandex.ru	$2b$12$fO7k5uGyx74OfJDGXstxReuMd67LYfBSUWoTY3IHDdVNMJ7hm4MLq	employee	2025-04-14 17:13:29.98829+00
\.

SELECT pg_catalog.setval('public.product_order_in_reception_seq', 10, true);

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
