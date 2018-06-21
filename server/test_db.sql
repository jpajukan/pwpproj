--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: account; Type: TABLE; Schema: public; Owner: vagrant; Tablespace: 
--

CREATE TABLE account (
    id integer NOT NULL,
    name character varying(64) NOT NULL,
    user_id integer
);


ALTER TABLE account OWNER TO vagrant;

--
-- Name: account_id_seq; Type: SEQUENCE; Schema: public; Owner: vagrant
--

CREATE SEQUENCE account_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE account_id_seq OWNER TO vagrant;

--
-- Name: account_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: vagrant
--

ALTER SEQUENCE account_id_seq OWNED BY account.id;


--
-- Name: admin; Type: TABLE; Schema: public; Owner: vagrant; Tablespace: 
--

CREATE TABLE admin (
    id integer NOT NULL,
    user_id integer,
    password_hash character varying(128) NOT NULL
);


ALTER TABLE admin OWNER TO vagrant;

--
-- Name: admin_id_seq; Type: SEQUENCE; Schema: public; Owner: vagrant
--

CREATE SEQUENCE admin_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE admin_id_seq OWNER TO vagrant;

--
-- Name: admin_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: vagrant
--

ALTER SEQUENCE admin_id_seq OWNED BY admin.id;


--
-- Name: card; Type: TABLE; Schema: public; Owner: vagrant; Tablespace: 
--

CREATE TABLE card (
    id integer NOT NULL,
    name character varying(64) NOT NULL,
    sha character varying(128) NOT NULL,
    account_id integer
);


ALTER TABLE card OWNER TO vagrant;

--
-- Name: card_id_seq; Type: SEQUENCE; Schema: public; Owner: vagrant
--

CREATE SEQUENCE card_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE card_id_seq OWNER TO vagrant;

--
-- Name: card_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: vagrant
--

ALTER SEQUENCE card_id_seq OWNED BY card.id;


--
-- Name: register; Type: TABLE; Schema: public; Owner: vagrant; Tablespace: 
--

CREATE TABLE register (
    id integer NOT NULL,
    name character varying(64) NOT NULL,
    sha character varying(128) NOT NULL,
    type integer
);


ALTER TABLE register OWNER TO vagrant;

--
-- Name: register_id_seq; Type: SEQUENCE; Schema: public; Owner: vagrant
--

CREATE SEQUENCE register_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE register_id_seq OWNER TO vagrant;

--
-- Name: register_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: vagrant
--

ALTER SEQUENCE register_id_seq OWNED BY register.id;


--
-- Name: transaction; Type: TABLE; Schema: public; Owner: vagrant; Tablespace: 
--

CREATE TABLE transaction (
    id integer NOT NULL,
    balance_change double precision NOT NULL,
    "timestamp" timestamp without time zone,
    account_id integer,
    card_id integer,
    register_id integer,
    user_id integer
);


ALTER TABLE transaction OWNER TO vagrant;

--
-- Name: transaction_id_seq; Type: SEQUENCE; Schema: public; Owner: vagrant
--

CREATE SEQUENCE transaction_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE transaction_id_seq OWNER TO vagrant;

--
-- Name: transaction_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: vagrant
--

ALTER SEQUENCE transaction_id_seq OWNED BY transaction.id;


--
-- Name: user; Type: TABLE; Schema: public; Owner: vagrant; Tablespace: 
--

CREATE TABLE "user" (
    id integer NOT NULL,
    name character varying(64) NOT NULL,
    email character varying(64) NOT NULL,
    phone character varying(20)
);


ALTER TABLE "user" OWNER TO vagrant;

--
-- Name: user_id_seq; Type: SEQUENCE; Schema: public; Owner: vagrant
--

CREATE SEQUENCE user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE user_id_seq OWNER TO vagrant;

--
-- Name: user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: vagrant
--

ALTER SEQUENCE user_id_seq OWNED BY "user".id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY account ALTER COLUMN id SET DEFAULT nextval('account_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY admin ALTER COLUMN id SET DEFAULT nextval('admin_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY card ALTER COLUMN id SET DEFAULT nextval('card_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY register ALTER COLUMN id SET DEFAULT nextval('register_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY transaction ALTER COLUMN id SET DEFAULT nextval('transaction_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY "user" ALTER COLUMN id SET DEFAULT nextval('user_id_seq'::regclass);


--
-- Data for Name: account; Type: TABLE DATA; Schema: public; Owner: vagrant
--

COPY account (id, name, user_id) FROM stdin;
1	Ruokatili	1
2	Viinatili	1
3	Ruokatili	2
4	Säästötili	3
5	Salatili	4
\.


--
-- Name: account_id_seq; Type: SEQUENCE SET; Schema: public; Owner: vagrant
--

SELECT pg_catalog.setval('account_id_seq', 5, true);


--
-- Data for Name: admin; Type: TABLE DATA; Schema: public; Owner: vagrant
--

COPY admin (id, user_id, password_hash) FROM stdin;
1	6	$6$rounds=656000$xJpdXgkw57laCfhP$N/i7ts7iqLg6F7zsOmmOMsP/WFC5B9ODAIh6JLyDPmTrSaemBskH80SCfsAjWI0JUUhx23Mq1RczebaRJXeAy1
\.


--
-- Name: admin_id_seq; Type: SEQUENCE SET; Schema: public; Owner: vagrant
--

SELECT pg_catalog.setval('admin_id_seq', 1, true);


--
-- Data for Name: card; Type: TABLE DATA; Schema: public; Owner: vagrant
--

COPY card (id, name, sha, account_id) FROM stdin;
1	Opiskelijakortti	8a1470b1f84c72f2a733ba485f67a3ec30bfddf2ddce574493cb0365107fc148	1
2	Kännykkä	cefaade15a1e34513ceb1837cc1c44144e90e41379b3356f42b255ca1492c646	1
3	Opiskelijakortti	034f5e8d6d75496524c5947923874ed55715989cf4c36b539622085049500336	2
4	Opiskelijakortti	2910e53e04d59ecbeeb95469616942713b2f1cc2474a974fe540641d5a825399	3
5	Kännykkä	f7410cd85a86dafae2ac08151b070251499523bb8e1ac529855fe84c183c238f	4
6	Opiskelijakortti	0cbd75f30cfb44dd568f5530c63afca88efa72ef9185fc2b91fcc30724fcc9e9	5
7	Orpokortti	c9c00df9280750d4b207d4739b604aa72c4d040badea5fa5a76779851d13d264	\N
\.


--
-- Name: card_id_seq; Type: SEQUENCE SET; Schema: public; Owner: vagrant
--

SELECT pg_catalog.setval('card_id_seq', 7, true);


--
-- Data for Name: register; Type: TABLE DATA; Schema: public; Owner: vagrant
--

COPY register (id, name, sha, type) FROM stdin;
1	Kahvihuone	acdf285926053bcbe9182e18b72062b1fc4d64a3d81e8bff52f399f956a57e88	0
2	Kiltahuone	d0e126c321575bf2b42f45755e1fb1525219d22d03b4baa4c81fbdd8bca3cdef	0
3	Admin	0afb00138d8e73348ec1fe41fd3d3a8fcbd90156b263bfa5791ba0e095f42cfc	1
\.


--
-- Name: register_id_seq; Type: SEQUENCE SET; Schema: public; Owner: vagrant
--

SELECT pg_catalog.setval('register_id_seq', 3, true);


--
-- Data for Name: transaction; Type: TABLE DATA; Schema: public; Owner: vagrant
--

COPY transaction (id, balance_change, "timestamp", account_id, card_id, register_id, user_id) FROM stdin;
1	10	2017-02-26 13:54:21.263779	1	1	3	1
2	1	2017-02-26 13:54:21.278578	1	2	3	1
3	100	2017-02-26 13:54:21.29707	2	3	3	1
4	20	2017-02-26 13:54:21.31056	3	4	3	2
5	30	2017-02-26 13:54:21.327222	4	5	3	3
6	50	2017-02-26 13:54:21.340452	5	6	3	4
7	-11	2017-02-26 13:54:21.354694	1	1	1	1
8	-80.5	2017-02-26 13:54:21.368769	2	3	2	1
9	-12.5999999999999996	2017-02-26 13:54:21.405192	3	4	1	2
10	-4	2017-02-26 13:54:21.419284	3	4	2	2
11	-5.20000000000000018	2017-02-26 13:54:21.432567	4	5	2	3
12	-15	2017-02-26 13:54:21.446378	4	5	1	3
13	-3	2017-02-26 13:54:21.462954	4	5	1	3
14	-10.5999999999999996	2017-02-26 13:54:21.475522	5	6	3	4
15	-2.60000000000000009	2017-02-26 13:54:21.488564	5	6	1	4
16	-30.1000000000000014	2017-02-26 13:54:21.501096	5	6	2	4
\.


--
-- Name: transaction_id_seq; Type: SEQUENCE SET; Schema: public; Owner: vagrant
--

SELECT pg_catalog.setval('transaction_id_seq', 16, true);


--
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: vagrant
--

COPY "user" (id, name, email, phone) FROM stdin;
1	Matti Matikainen	matti@matikainen.fi	0501234567
2	Mervi Matikainen	mervi@matikainen.fi	0509894172
3	Heikki Herranen	heikki@herranen.com	0400123123
4	Touko Pekkala	toukopouko@example.com	\N
5	Päivi Lipponen	paevi@jippii.fi	0401231231
6	admin	admin@localhost	\N
\.


--
-- Name: user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: vagrant
--

SELECT pg_catalog.setval('user_id_seq', 6, true);


--
-- Name: account_pkey; Type: CONSTRAINT; Schema: public; Owner: vagrant; Tablespace: 
--

ALTER TABLE ONLY account
    ADD CONSTRAINT account_pkey PRIMARY KEY (id);


--
-- Name: admin_pkey; Type: CONSTRAINT; Schema: public; Owner: vagrant; Tablespace: 
--

ALTER TABLE ONLY admin
    ADD CONSTRAINT admin_pkey PRIMARY KEY (id);


--
-- Name: admin_user_id_key; Type: CONSTRAINT; Schema: public; Owner: vagrant; Tablespace: 
--

ALTER TABLE ONLY admin
    ADD CONSTRAINT admin_user_id_key UNIQUE (user_id);


--
-- Name: card_pkey; Type: CONSTRAINT; Schema: public; Owner: vagrant; Tablespace: 
--

ALTER TABLE ONLY card
    ADD CONSTRAINT card_pkey PRIMARY KEY (id);


--
-- Name: card_sha_key; Type: CONSTRAINT; Schema: public; Owner: vagrant; Tablespace: 
--

ALTER TABLE ONLY card
    ADD CONSTRAINT card_sha_key UNIQUE (sha);


--
-- Name: register_name_key; Type: CONSTRAINT; Schema: public; Owner: vagrant; Tablespace: 
--

ALTER TABLE ONLY register
    ADD CONSTRAINT register_name_key UNIQUE (name);


--
-- Name: register_pkey; Type: CONSTRAINT; Schema: public; Owner: vagrant; Tablespace: 
--

ALTER TABLE ONLY register
    ADD CONSTRAINT register_pkey PRIMARY KEY (id);


--
-- Name: register_sha_key; Type: CONSTRAINT; Schema: public; Owner: vagrant; Tablespace: 
--

ALTER TABLE ONLY register
    ADD CONSTRAINT register_sha_key UNIQUE (sha);


--
-- Name: transaction_pkey; Type: CONSTRAINT; Schema: public; Owner: vagrant; Tablespace: 
--

ALTER TABLE ONLY transaction
    ADD CONSTRAINT transaction_pkey PRIMARY KEY (id);


--
-- Name: user_email_key; Type: CONSTRAINT; Schema: public; Owner: vagrant; Tablespace: 
--

ALTER TABLE ONLY "user"
    ADD CONSTRAINT user_email_key UNIQUE (email);


--
-- Name: user_pkey; Type: CONSTRAINT; Schema: public; Owner: vagrant; Tablespace: 
--

ALTER TABLE ONLY "user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


--
-- Name: account_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY account
    ADD CONSTRAINT account_user_id_fkey FOREIGN KEY (user_id) REFERENCES "user"(id);


--
-- Name: admin_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY admin
    ADD CONSTRAINT admin_user_id_fkey FOREIGN KEY (user_id) REFERENCES "user"(id);


--
-- Name: card_account_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY card
    ADD CONSTRAINT card_account_id_fkey FOREIGN KEY (account_id) REFERENCES account(id);


--
-- Name: transaction_account_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY transaction
    ADD CONSTRAINT transaction_account_id_fkey FOREIGN KEY (account_id) REFERENCES account(id);


--
-- Name: transaction_card_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY transaction
    ADD CONSTRAINT transaction_card_id_fkey FOREIGN KEY (card_id) REFERENCES card(id);


--
-- Name: transaction_register_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY transaction
    ADD CONSTRAINT transaction_register_id_fkey FOREIGN KEY (register_id) REFERENCES register(id);


--
-- Name: transaction_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY transaction
    ADD CONSTRAINT transaction_user_id_fkey FOREIGN KEY (user_id) REFERENCES "user"(id);


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

