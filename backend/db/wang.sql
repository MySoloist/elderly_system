--
-- PostgreSQL database dump
--

\restrict 9iuTt60GbbZu5pBx5Ra7sPASr1oA5BNSKX0b2NcPw1MkeSiY9JnsDfxZ2sV3qK7

-- Dumped from database version 17.9
-- Dumped by pg_dump version 17.9

-- Started on 2026-04-13 15:34:58

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
-- TOC entry 2 (class 3079 OID 78208)
-- Name: postgis; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS postgis WITH SCHEMA public;


--
-- TOC entry 6222 (class 0 OID 0)
-- Dependencies: 2
-- Name: EXTENSION postgis; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION postgis IS 'PostGIS geometry and geography spatial types and functions';


--
-- TOC entry 1736 (class 1247 OID 79702)
-- Name: deliverystatus; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.deliverystatus AS ENUM (
    'ASSIGNED',
    'IN_TRANSIT',
    'DELIVERED',
    'FAILED'
);


ALTER TYPE public.deliverystatus OWNER TO postgres;

--
-- TOC entry 1733 (class 1247 OID 79694)
-- Name: mealstatus; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.mealstatus AS ENUM (
    'AVAILABLE',
    'UNAVAILABLE',
    'OUT_OF_STOCK'
);


ALTER TYPE public.mealstatus OWNER TO postgres;

--
-- TOC entry 1772 (class 1247 OID 114722)
-- Name: notificationstatus; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.notificationstatus AS ENUM (
    'UNREAD',
    'READ'
);


ALTER TYPE public.notificationstatus OWNER TO postgres;

--
-- TOC entry 1769 (class 1247 OID 114712)
-- Name: notificationtype; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.notificationtype AS ENUM (
    'DELIVERY_EXCEPTION',
    'ORDER_OVERDUE',
    'SYSTEM_ALERT',
    'USER_ACTION'
);


ALTER TYPE public.notificationtype OWNER TO postgres;

--
-- TOC entry 1730 (class 1247 OID 79680)
-- Name: orderstatus; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.orderstatus AS ENUM (
    'PENDING',
    'CONFIRMED',
    'PREPARING',
    'DELIVERING',
    'COMPLETED',
    'CANCELLED'
);


ALTER TYPE public.orderstatus OWNER TO postgres;

--
-- TOC entry 1760 (class 1247 OID 106510)
-- Name: todostatus; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.todostatus AS ENUM (
    'PENDING',
    'IN_PROGRESS',
    'COMPLETED',
    'CANCELLED'
);


ALTER TYPE public.todostatus OWNER TO postgres;

--
-- TOC entry 1757 (class 1247 OID 106497)
-- Name: todotype; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.todotype AS ENUM (
    'ORDER_OVERDUE',
    'MEAL_PENDING',
    'USER_INFO_UPDATE',
    'STAFF_SCHEDULE',
    'COMMUNITY_REGISTRATION',
    'ANNOUNCEMENT_PENDING'
);


ALTER TYPE public.todotype OWNER TO postgres;

--
-- TOC entry 1727 (class 1247 OID 79672)
-- Name: userstatus; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.userstatus AS ENUM (
    'ACTIVE',
    'INACTIVE',
    'SUSPENDED'
);


ALTER TYPE public.userstatus OWNER TO postgres;

--
-- TOC entry 1724 (class 1247 OID 79662)
-- Name: usertype; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.usertype AS ENUM (
    'elderly',
    'member',
    'deliverer',
    'admin'
);


ALTER TYPE public.usertype OWNER TO postgres;

--
-- TOC entry 797 (class 1255 OID 79638)
-- Name: update_deliverer_location(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.update_deliverer_location() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    UPDATE deliverer_profiles 
    SET current_location = NEW.location,
        last_active = NOW()
    WHERE user_id = NEW.user_id
      AND user_id IN (SELECT id FROM users WHERE user_type = 'deliverer');
    RETURN NEW;
END;
$$;


ALTER FUNCTION public.update_deliverer_location() OWNER TO postgres;

--
-- TOC entry 976 (class 1255 OID 79640)
-- Name: update_timestamp(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.update_timestamp() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$;


ALTER FUNCTION public.update_timestamp() OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 250 (class 1259 OID 79711)
-- Name: admin_profiles; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.admin_profiles (
    user_id integer NOT NULL,
    name character varying(50) NOT NULL,
    phone character varying(20),
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.admin_profiles OWNER TO postgres;

--
-- TOC entry 243 (class 1259 OID 79544)
-- Name: ai_conversations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ai_conversations (
    id integer NOT NULL,
    user_id integer,
    conversation_id character varying(100) NOT NULL,
    user_query text NOT NULL,
    ai_response text NOT NULL,
    conversation_type character varying(50),
    created_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.ai_conversations OWNER TO postgres;

--
-- TOC entry 242 (class 1259 OID 79543)
-- Name: ai_conversations_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ai_conversations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.ai_conversations_id_seq OWNER TO postgres;

--
-- TOC entry 6223 (class 0 OID 0)
-- Dependencies: 242
-- Name: ai_conversations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ai_conversations_id_seq OWNED BY public.ai_conversations.id;


--
-- TOC entry 241 (class 1259 OID 79529)
-- Name: announcements; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.announcements (
    id integer NOT NULL,
    title character varying(100) NOT NULL,
    content text NOT NULL,
    type character varying(50),
    priority character varying(20) DEFAULT 'normal'::character varying,
    status character varying(20) DEFAULT 'active'::character varying,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.announcements OWNER TO postgres;

--
-- TOC entry 240 (class 1259 OID 79528)
-- Name: announcements_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.announcements_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.announcements_id_seq OWNER TO postgres;

--
-- TOC entry 6224 (class 0 OID 0)
-- Dependencies: 240
-- Name: announcements_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.announcements_id_seq OWNED BY public.announcements.id;


--
-- TOC entry 256 (class 1259 OID 79770)
-- Name: categories; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.categories (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    description character varying(255),
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.categories OWNER TO postgres;

--
-- TOC entry 255 (class 1259 OID 79769)
-- Name: categories_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.categories_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.categories_id_seq OWNER TO postgres;

--
-- TOC entry 6225 (class 0 OID 0)
-- Dependencies: 255
-- Name: categories_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.categories_id_seq OWNED BY public.categories.id;


--
-- TOC entry 245 (class 1259 OID 79564)
-- Name: communities; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.communities (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    address character varying(255),
    contact_phone character varying(20),
    manager_name character varying(50),
    manager_phone character varying(20),
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now(),
    status character varying(20)
);


ALTER TABLE public.communities OWNER TO postgres;

--
-- TOC entry 244 (class 1259 OID 79563)
-- Name: communities_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.communities_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.communities_id_seq OWNER TO postgres;

--
-- TOC entry 6226 (class 0 OID 0)
-- Dependencies: 244
-- Name: communities_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.communities_id_seq OWNED BY public.communities.id;


--
-- TOC entry 227 (class 1259 OID 79337)
-- Name: deliverer_profiles; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.deliverer_profiles (
    user_id integer NOT NULL,
    name character varying(50) NOT NULL,
    phone character varying(20),
    vehicle_type character varying(50),
    status character varying(20) DEFAULT 'offline'::character varying,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now(),
    area_id integer,
    avatar character varying(255),
    latitude character varying(20),
    longitude character varying(20),
    location_updated_at timestamp with time zone,
    CONSTRAINT check_deliverer_status CHECK (((status)::text = ANY ((ARRAY['available'::character varying, 'busy'::character varying, 'offline'::character varying, 'admin_online'::character varying])::text[])))
);


ALTER TABLE public.deliverer_profiles OWNER TO postgres;

--
-- TOC entry 235 (class 1259 OID 79414)
-- Name: deliveries; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.deliveries (
    id integer NOT NULL,
    order_id integer,
    deliverer_id integer,
    end_time timestamp with time zone,
    estimated_time timestamp with time zone,
    status character varying(20),
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now(),
    actual_time timestamp with time zone,
    is_assigned_by_admin boolean DEFAULT false
);


ALTER TABLE public.deliveries OWNER TO postgres;

--
-- TOC entry 234 (class 1259 OID 79413)
-- Name: deliveries_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.deliveries_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.deliveries_id_seq OWNER TO postgres;

--
-- TOC entry 6227 (class 0 OID 0)
-- Dependencies: 234
-- Name: deliveries_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.deliveries_id_seq OWNED BY public.deliveries.id;


--
-- TOC entry 268 (class 1259 OID 131074)
-- Name: delivery_areas; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.delivery_areas (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    description text,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.delivery_areas OWNER TO postgres;

--
-- TOC entry 267 (class 1259 OID 131073)
-- Name: delivery_areas_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.delivery_areas_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.delivery_areas_id_seq OWNER TO postgres;

--
-- TOC entry 6228 (class 0 OID 0)
-- Dependencies: 267
-- Name: delivery_areas_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.delivery_areas_id_seq OWNED BY public.delivery_areas.id;


--
-- TOC entry 237 (class 1259 OID 79457)
-- Name: elder_member_relations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.elder_member_relations (
    id integer NOT NULL,
    elder_id integer,
    member_id integer,
    relationship character varying(50),
    is_primary boolean DEFAULT false,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.elder_member_relations OWNER TO postgres;

--
-- TOC entry 236 (class 1259 OID 79456)
-- Name: elder_member_relations_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.elder_member_relations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.elder_member_relations_id_seq OWNER TO postgres;

--
-- TOC entry 6229 (class 0 OID 0)
-- Dependencies: 236
-- Name: elder_member_relations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.elder_member_relations_id_seq OWNED BY public.elder_member_relations.id;


--
-- TOC entry 225 (class 1259 OID 79304)
-- Name: elderly_profiles; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.elderly_profiles (
    user_id integer NOT NULL,
    name character varying(50) NOT NULL,
    phone character varying(20),
    address character varying(255),
    dietary_preferences text,
    location public.geography(Point,4326),
    age integer,
    gender character varying(10),
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now(),
    community_id integer,
    health_tag_id integer,
    avatar character varying(255)
);


ALTER TABLE public.elderly_profiles OWNER TO postgres;

--
-- TOC entry 249 (class 1259 OID 79614)
-- Name: emergency_calls; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.emergency_calls (
    id integer NOT NULL,
    elderly_id integer,
    emergency_type character varying(50),
    message text,
    response_status character varying(20) DEFAULT 'pending'::character varying,
    response_time timestamp with time zone,
    created_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.emergency_calls OWNER TO postgres;

--
-- TOC entry 248 (class 1259 OID 79613)
-- Name: emergency_calls_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.emergency_calls_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.emergency_calls_id_seq OWNER TO postgres;

--
-- TOC entry 6230 (class 0 OID 0)
-- Dependencies: 248
-- Name: emergency_calls_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.emergency_calls_id_seq OWNED BY public.emergency_calls.id;


--
-- TOC entry 254 (class 1259 OID 79754)
-- Name: exceptions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.exceptions (
    id integer NOT NULL,
    delivery_id integer NOT NULL,
    type character varying(50) NOT NULL,
    description text,
    created_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.exceptions OWNER TO postgres;

--
-- TOC entry 253 (class 1259 OID 79753)
-- Name: exceptions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.exceptions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.exceptions_id_seq OWNER TO postgres;

--
-- TOC entry 6231 (class 0 OID 0)
-- Dependencies: 253
-- Name: exceptions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.exceptions_id_seq OWNED BY public.exceptions.id;


--
-- TOC entry 270 (class 1259 OID 155674)
-- Name: favorites; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.favorites (
    id integer NOT NULL,
    user_id integer NOT NULL,
    user_type character varying(20) NOT NULL,
    meal_id integer NOT NULL,
    created_at timestamp with time zone DEFAULT now(),
    CONSTRAINT favorites_new_user_type_check CHECK (((user_type)::text = ANY ((ARRAY['elderly'::character varying, 'member'::character varying])::text[])))
);


ALTER TABLE public.favorites OWNER TO postgres;

--
-- TOC entry 269 (class 1259 OID 155673)
-- Name: favorites_new_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.favorites_new_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.favorites_new_id_seq OWNER TO postgres;

--
-- TOC entry 6232 (class 0 OID 0)
-- Dependencies: 269
-- Name: favorites_new_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.favorites_new_id_seq OWNED BY public.favorites.id;


--
-- TOC entry 247 (class 1259 OID 79576)
-- Name: health_records; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.health_records (
    id integer NOT NULL,
    elderly_id integer,
    height numeric(5,2),
    weight numeric(5,2),
    blood_pressure character varying(20),
    blood_sugar numeric(5,2),
    allergies text,
    medications text,
    doctor_advice text,
    recorded_at timestamp with time zone DEFAULT now(),
    created_by integer
);


ALTER TABLE public.health_records OWNER TO postgres;

--
-- TOC entry 246 (class 1259 OID 79575)
-- Name: health_records_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.health_records_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.health_records_id_seq OWNER TO postgres;

--
-- TOC entry 6233 (class 0 OID 0)
-- Dependencies: 246
-- Name: health_records_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.health_records_id_seq OWNED BY public.health_records.id;


--
-- TOC entry 264 (class 1259 OID 114690)
-- Name: health_reminders; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.health_reminders (
    id integer NOT NULL,
    sender_id integer NOT NULL,
    receiver_id integer NOT NULL,
    reminder_type character varying(50) NOT NULL,
    content text NOT NULL,
    status character varying(20) DEFAULT 'pending'::character varying,
    scheduled_time timestamp without time zone,
    sent_time timestamp without time zone,
    read_time timestamp without time zone,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.health_reminders OWNER TO postgres;

--
-- TOC entry 263 (class 1259 OID 114689)
-- Name: health_reminders_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.health_reminders_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.health_reminders_id_seq OWNER TO postgres;

--
-- TOC entry 6234 (class 0 OID 0)
-- Dependencies: 263
-- Name: health_reminders_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.health_reminders_id_seq OWNED BY public.health_reminders.id;


--
-- TOC entry 262 (class 1259 OID 106556)
-- Name: health_tags; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.health_tags (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    description text,
    color character varying(20),
    created_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.health_tags OWNER TO postgres;

--
-- TOC entry 261 (class 1259 OID 106555)
-- Name: health_tags_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.health_tags_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.health_tags_id_seq OWNER TO postgres;

--
-- TOC entry 6235 (class 0 OID 0)
-- Dependencies: 261
-- Name: health_tags_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.health_tags_id_seq OWNED BY public.health_tags.id;


--
-- TOC entry 229 (class 1259 OID 79358)
-- Name: meals; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.meals (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    price numeric(10,2) NOT NULL,
    description text,
    special_tag character varying(50),
    image_url character varying(255),
    status character varying(20) DEFAULT 'available'::character varying,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now(),
    category_id integer,
    tag_id integer
);


ALTER TABLE public.meals OWNER TO postgres;

--
-- TOC entry 228 (class 1259 OID 79357)
-- Name: meals_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.meals_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.meals_id_seq OWNER TO postgres;

--
-- TOC entry 6236 (class 0 OID 0)
-- Dependencies: 228
-- Name: meals_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.meals_id_seq OWNED BY public.meals.id;


--
-- TOC entry 226 (class 1259 OID 79322)
-- Name: member_profiles; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.member_profiles (
    user_id integer NOT NULL,
    name character varying(50) NOT NULL,
    phone character varying(20),
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now(),
    avatar character varying(255)
);


ALTER TABLE public.member_profiles OWNER TO postgres;

--
-- TOC entry 233 (class 1259 OID 79394)
-- Name: order_items; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.order_items (
    id integer NOT NULL,
    order_id integer,
    meal_id integer,
    quantity integer NOT NULL,
    unit_price numeric(10,2) NOT NULL,
    subtotal numeric(10,2) NOT NULL,
    created_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.order_items OWNER TO postgres;

--
-- TOC entry 232 (class 1259 OID 79393)
-- Name: order_items_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.order_items_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.order_items_id_seq OWNER TO postgres;

--
-- TOC entry 6237 (class 0 OID 0)
-- Dependencies: 232
-- Name: order_items_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.order_items_id_seq OWNED BY public.order_items.id;


--
-- TOC entry 231 (class 1259 OID 79373)
-- Name: orders; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.orders (
    id integer NOT NULL,
    elderly_id integer,
    total_amount numeric(10,2) NOT NULL,
    payment_method character varying(50),
    payment_status character varying(20) DEFAULT 'pending'::character varying,
    status character varying(20) DEFAULT 'pending_payment'::character varying,
    delivery_address character varying(255),
    notes text,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now(),
    scheduled_time timestamp with time zone,
    order_type character varying(20) DEFAULT 'immediate'::character varying,
    CONSTRAINT check_order_status CHECK (((status)::text = ANY (ARRAY['pending_payment'::text, 'pending_schedule'::text, 'pending_accept'::text, 'delivering'::text, 'completed'::text, 'cancelled'::text])))
);


ALTER TABLE public.orders OWNER TO postgres;

--
-- TOC entry 230 (class 1259 OID 79372)
-- Name: orders_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.orders_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.orders_id_seq OWNER TO postgres;

--
-- TOC entry 6238 (class 0 OID 0)
-- Dependencies: 230
-- Name: orders_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.orders_id_seq OWNED BY public.orders.id;


--
-- TOC entry 252 (class 1259 OID 79724)
-- Name: payments; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.payments (
    id integer NOT NULL,
    order_id integer NOT NULL,
    payment_method character varying(50) NOT NULL,
    amount double precision NOT NULL,
    transaction_id character varying(100),
    status character varying(20),
    created_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.payments OWNER TO postgres;

--
-- TOC entry 251 (class 1259 OID 79723)
-- Name: payments_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.payments_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.payments_id_seq OWNER TO postgres;

--
-- TOC entry 6239 (class 0 OID 0)
-- Dependencies: 251
-- Name: payments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.payments_id_seq OWNED BY public.payments.id;


--
-- TOC entry 239 (class 1259 OID 79481)
-- Name: reviews; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.reviews (
    id integer NOT NULL,
    order_id integer,
    elderly_id integer,
    rating integer,
    content text,
    created_at timestamp with time zone DEFAULT now(),
    status character varying(20) DEFAULT 'approved'::character varying,
    images text[],
    updated_at timestamp with time zone,
    reply text,
    ai_reviewed integer DEFAULT 0,
    ai_replied integer DEFAULT 0,
    deliverer_id integer,
    reviewer_type character varying(20) NOT NULL,
    CONSTRAINT check_rating CHECK (((rating >= 1) AND (rating <= 5))),
    CONSTRAINT reviews_rating_check CHECK (((rating >= 1) AND (rating <= 5))),
    CONSTRAINT reviews_reviewer_type_check CHECK (((reviewer_type)::text = ANY ((ARRAY['elderly'::character varying, 'family'::character varying])::text[])))
);


ALTER TABLE public.reviews OWNER TO postgres;

--
-- TOC entry 238 (class 1259 OID 79480)
-- Name: reviews_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.reviews_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.reviews_id_seq OWNER TO postgres;

--
-- TOC entry 6240 (class 0 OID 0)
-- Dependencies: 238
-- Name: reviews_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.reviews_id_seq OWNED BY public.reviews.id;


--
-- TOC entry 266 (class 1259 OID 114745)
-- Name: staff_schedules; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.staff_schedules (
    id integer NOT NULL,
    staff_id integer NOT NULL,
    schedule_date date NOT NULL,
    time_slot character varying(20) NOT NULL,
    status character varying(20) DEFAULT 'confirmed'::character varying,
    note text,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.staff_schedules OWNER TO postgres;

--
-- TOC entry 265 (class 1259 OID 114744)
-- Name: staff_schedules_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.staff_schedules_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.staff_schedules_id_seq OWNER TO postgres;

--
-- TOC entry 6241 (class 0 OID 0)
-- Dependencies: 265
-- Name: staff_schedules_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.staff_schedules_id_seq OWNED BY public.staff_schedules.id;


--
-- TOC entry 258 (class 1259 OID 79786)
-- Name: tags; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tags (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    description character varying(255),
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.tags OWNER TO postgres;

--
-- TOC entry 257 (class 1259 OID 79785)
-- Name: tags_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tags_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tags_id_seq OWNER TO postgres;

--
-- TOC entry 6242 (class 0 OID 0)
-- Dependencies: 257
-- Name: tags_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tags_id_seq OWNED BY public.tags.id;


--
-- TOC entry 224 (class 1259 OID 79290)
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying(50) NOT NULL,
    password_hash character varying(255) NOT NULL,
    user_type character varying(20) NOT NULL,
    status character varying(20) DEFAULT 'active'::character varying,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now(),
    email character varying(100),
    last_login timestamp with time zone,
    openid character varying(100),
    unionid character varying(100),
    CONSTRAINT check_user_type CHECK (((user_type)::text = ANY ((ARRAY['elderly'::character varying, 'member'::character varying, 'deliverer'::character varying, 'admin'::character varying])::text[])))
);


ALTER TABLE public.users OWNER TO postgres;

--
-- TOC entry 223 (class 1259 OID 79289)
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
-- TOC entry 6243 (class 0 OID 0)
-- Dependencies: 223
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- TOC entry 260 (class 1259 OID 81921)
-- Name: voice_synthesis; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.voice_synthesis (
    id integer NOT NULL,
    user_id integer,
    text_content text NOT NULL,
    voice_url character varying(500),
    voice_type character varying(50),
    language character varying(20),
    speed double precision,
    status character varying(20),
    created_at timestamp with time zone DEFAULT now(),
    completed_at timestamp with time zone
);


ALTER TABLE public.voice_synthesis OWNER TO postgres;

--
-- TOC entry 259 (class 1259 OID 81920)
-- Name: voice_synthesis_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.voice_synthesis_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.voice_synthesis_id_seq OWNER TO postgres;

--
-- TOC entry 6244 (class 0 OID 0)
-- Dependencies: 259
-- Name: voice_synthesis_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.voice_synthesis_id_seq OWNED BY public.voice_synthesis.id;


--
-- TOC entry 5799 (class 2604 OID 79547)
-- Name: ai_conversations id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ai_conversations ALTER COLUMN id SET DEFAULT nextval('public.ai_conversations_id_seq'::regclass);


--
-- TOC entry 5794 (class 2604 OID 79532)
-- Name: announcements id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.announcements ALTER COLUMN id SET DEFAULT nextval('public.announcements_id_seq'::regclass);


--
-- TOC entry 5815 (class 2604 OID 79773)
-- Name: categories id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categories ALTER COLUMN id SET DEFAULT nextval('public.categories_id_seq'::regclass);


--
-- TOC entry 5801 (class 2604 OID 79567)
-- Name: communities id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.communities ALTER COLUMN id SET DEFAULT nextval('public.communities_id_seq'::regclass);


--
-- TOC entry 5781 (class 2604 OID 79417)
-- Name: deliveries id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.deliveries ALTER COLUMN id SET DEFAULT nextval('public.deliveries_id_seq'::regclass);


--
-- TOC entry 5833 (class 2604 OID 131077)
-- Name: delivery_areas id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.delivery_areas ALTER COLUMN id SET DEFAULT nextval('public.delivery_areas_id_seq'::regclass);


--
-- TOC entry 5785 (class 2604 OID 79460)
-- Name: elder_member_relations id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.elder_member_relations ALTER COLUMN id SET DEFAULT nextval('public.elder_member_relations_id_seq'::regclass);


--
-- TOC entry 5806 (class 2604 OID 79617)
-- Name: emergency_calls id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.emergency_calls ALTER COLUMN id SET DEFAULT nextval('public.emergency_calls_id_seq'::regclass);


--
-- TOC entry 5813 (class 2604 OID 79757)
-- Name: exceptions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.exceptions ALTER COLUMN id SET DEFAULT nextval('public.exceptions_id_seq'::regclass);


--
-- TOC entry 5836 (class 2604 OID 155677)
-- Name: favorites id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.favorites ALTER COLUMN id SET DEFAULT nextval('public.favorites_new_id_seq'::regclass);


--
-- TOC entry 5804 (class 2604 OID 79579)
-- Name: health_records id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.health_records ALTER COLUMN id SET DEFAULT nextval('public.health_records_id_seq'::regclass);


--
-- TOC entry 5825 (class 2604 OID 114693)
-- Name: health_reminders id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.health_reminders ALTER COLUMN id SET DEFAULT nextval('public.health_reminders_id_seq'::regclass);


--
-- TOC entry 5823 (class 2604 OID 106559)
-- Name: health_tags id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.health_tags ALTER COLUMN id SET DEFAULT nextval('public.health_tags_id_seq'::regclass);


--
-- TOC entry 5769 (class 2604 OID 79361)
-- Name: meals id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.meals ALTER COLUMN id SET DEFAULT nextval('public.meals_id_seq'::regclass);


--
-- TOC entry 5779 (class 2604 OID 79397)
-- Name: order_items id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_items ALTER COLUMN id SET DEFAULT nextval('public.order_items_id_seq'::regclass);


--
-- TOC entry 5773 (class 2604 OID 79376)
-- Name: orders id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders ALTER COLUMN id SET DEFAULT nextval('public.orders_id_seq'::regclass);


--
-- TOC entry 5811 (class 2604 OID 79727)
-- Name: payments id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.payments ALTER COLUMN id SET DEFAULT nextval('public.payments_id_seq'::regclass);


--
-- TOC entry 5789 (class 2604 OID 79484)
-- Name: reviews id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reviews ALTER COLUMN id SET DEFAULT nextval('public.reviews_id_seq'::regclass);


--
-- TOC entry 5829 (class 2604 OID 114748)
-- Name: staff_schedules id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.staff_schedules ALTER COLUMN id SET DEFAULT nextval('public.staff_schedules_id_seq'::regclass);


--
-- TOC entry 5818 (class 2604 OID 79789)
-- Name: tags id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tags ALTER COLUMN id SET DEFAULT nextval('public.tags_id_seq'::regclass);


--
-- TOC entry 5758 (class 2604 OID 79293)
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- TOC entry 5821 (class 2604 OID 81924)
-- Name: voice_synthesis id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.voice_synthesis ALTER COLUMN id SET DEFAULT nextval('public.voice_synthesis_id_seq'::regclass);


--
-- TOC entry 6196 (class 0 OID 79711)
-- Dependencies: 250
-- Data for Name: admin_profiles; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.admin_profiles (user_id, name, phone, created_at, updated_at) FROM stdin;
32	王雪祥	13783898556	2026-04-01 11:30:42.64467+08	2026-04-01 20:31:08.317444+08
\.


--
-- TOC entry 6189 (class 0 OID 79544)
-- Dependencies: 243
-- Data for Name: ai_conversations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ai_conversations (id, user_id, conversation_id, user_query, ai_response, conversation_type, created_at) FROM stdin;
69	32	a4929728	你好	您好！我是老年人膳食服务管理系统的智能助手。很高兴为您服务。\n\n请问有什么可以帮您？比如：\n- 查看或管理订单\n- 管理用户信息\n- 管理餐品菜单\n- 查看系统统计数据\n- 了解系统操作指南\n\n请告诉我您需要什么帮助。	admin_assistant	2026-04-01 19:50:57.052348+08
70	32	4cf2d3ac	你会干什么？	我是老年人膳食服务管理系统的智能助手，主要功能包括：\n\n1. **订单管理**：帮助您查看、处理、统计订单信息\n2. **用户管理**：协助管理老年用户信息、偏好设置等\n3. **餐品管理**：提供菜单更新、营养搭配建议等功能\n4. **系统操作指导**：解答操作疑问，提供最佳实践建议\n5. **数据统计**：生成用餐统计、营养分析等报告\n\n请告诉我您需要哪方面的帮助？	admin_assistant	2026-04-01 19:51:09.148123+08
71	32	be0d6218	如何添加新的配送员？	在老年人膳食服务管理系统中添加新配送员的步骤如下：\n\n1. **登录管理员账户**  \n   进入系统后台管理界面。\n\n2. **进入“配送员管理”模块**  \n   通常在左侧菜单栏或“用户管理”分类下可找到。\n\n3. **点击“添加配送员”**  \n   填写配送员基本信息，包括：\n   - 姓名、联系电话\n   - 身份证号（用于备案）\n   - 负责配送区域（可多选或填写）\n   - 账号密码（用于登录配送端APP）\n\n4. **设置权限与状态**  \n   - 选择可接单时段（如全天/仅午晚餐）\n   - 设置初始状态为“可用”或“休息”\n\n5. **保存并通知**  \n   保存后系统将自动生成配送员账号，需将账号信息告知配送员。\n\n**建议**：添加后可在“培训资料”模块推送配送规范文档，确保服务标准化。如有疑问可随时进一步询问！	admin_assistant	2026-04-01 20:09:51.897054+08
72	32	f8d69c97	如何查看订单统计？	在老年人膳食服务管理系统中，您可以通过以下步骤查看订单统计：\n\n1. **登录管理员账户**：进入系统后台管理界面。\n2. **导航至“订单管理”或“统计分析”模块**（具体名称可能因系统版本略有不同）。\n3. **选择“订单统计”或类似选项**，系统通常会提供按日、周、月或自定义时间段的统计视图。\n4. **查看关键数据**：包括订单总数、完成率、热门餐品、用户订购趋势等图表或报表。\n\n如需导出数据或更详细的筛选（如按社区、餐别统计），请使用页面上的筛选或导出功能。如有操作疑问，可参考系统内置帮助文档或联系技术支持。	admin_assistant	2026-04-01 21:14:33.955326+08
73	32	9b47cdce	如何添加新的配送员？	在老年人膳食服务管理系统中添加新配送员，请按以下步骤操作：\n\n1. **登录管理员账户**  \n   进入系统后台管理界面。\n\n2. **进入“配送员管理”模块**  \n   通常在左侧菜单栏或“用户管理”分类下可找到。\n\n3. **点击“添加配送员”**  \n   填写配送员基本信息，包括：\n   - 姓名、联系电话\n   - 负责配送区域（如社区、街道）\n   - 账号（用于登录配送端）\n   - 初始密码（建议要求首次登录后修改）\n\n4. **设置权限与状态**  \n   可勾选配送员可接单的时间段，并默认设置为“可用”状态。\n\n5. **保存并通知**  \n   保存后，系统将自动生成配送员账号。请及时将账号信息告知配送员，并提醒其下载配送端APP（如有）。\n\n**建议**：添加后可在“订单分配测试”中模拟派单，确保配送员能正常接收订单信息。如有疑问，可查看系统帮助文档或联系技术支持。	admin_assistant	2026-04-02 08:07:49.352585+08
74	33	35ff6ce3	hello	您好！很高兴为您服务。我是老年人膳食服务助手，可以为您提供餐品推荐、价格咨询、配送时间等信息，也可以根据您的健康状况提供饮食建议。\n\n请问有什么可以帮助您的吗？	elderly_assistant	2026-04-03 17:27:36.623932+08
75	32	0f2d8754	hello	您好！我是老年人膳食服务管理系统的智能助手。请问有什么可以帮助您的吗？	admin_assistant	2026-04-03 23:38:42.560967+08
76	32	2b911750	如何添加新的配送员？	在老年人膳食服务管理系统中添加新配送员的步骤如下：\n\n1. **登录管理员账户**：进入系统后台管理界面。\n2. **进入“配送员管理”模块**：通常在左侧菜单栏或“用户管理”分类下。\n3. **点击“添加配送员”按钮**：进入信息填写页面。\n4. **填写配送员信息**：\n   - 姓名、联系方式\n   - 身份证号（用于实名认证）\n   - 负责配送区域（可多选或手动输入）\n   - 账号密码（用于登录配送端APP）\n5. **设置权限与状态**：选择“启用”账户，并分配配送任务权限。\n6. **保存并通知**：系统将自动发送账号信息至配送员手机。\n\n**建议**：添加后及时安排配送员培训，并提醒其下载配送端APP。	admin_assistant	2026-04-03 23:38:48.830836+08
78	33	6e598686-d346-49bb-9446-c0d5913ff9c2	hello	你好呀！很高兴见到你。今天天气不错，你过得怎么样呀？有什么想聊的或者需要帮忙的，随时告诉我哦！ 😊	elderly_assistant	2026-04-05 22:51:40.160368+08
79	32	366aa521-b71a-47a0-bfbd-206f0446e898	如何添加新的配送员？	作为颐养膳食系统的管理员，添加新的配送员是一项基础且重要的工作。以下是详细、专业的操作流程和业务建议：\n\n### **一、 核心业务流程说明**\n在添加配送员前，请理解其涉及的完整业务流：\n1.  **信息录入**：管理员在后台系统录入配送员基本信息，建立账户。\n2.  **权限与区域配置**：为配送员分配负责的送餐区域（如XX社区、XX楼层）及相应的系统操作权限。\n3.  **上岗培训与准备**：确保配送员了解送餐流程、服务规范，并配备必要的工具（如保温箱、工牌等）。\n4.  **任务分配与上线**：系统将其纳入排班计划，开始接收并执行配送任务。\n\n### **二、 系统操作步骤建议**\n以下为通用的后台管理操作指南，具体路径可能因系统版本略有不同：\n\n**步骤1：登录管理系统**\n*   使用**管理员账户**登录颐养膳食系统后台。\n\n**步骤2：进入人员管理模块**\n*   在左侧导航栏或主菜单中，找到 **“人员管理”**、**“员工管理”** 或 **“配送员管理”** 等相关入口。\n\n**步骤3：新增配送员信息**\n*   点击 **“新增”**、**“添加配送员”** 或类似按钮。\n*   在弹出的表单中，准确填写以下核心信息（*为通常必填项）：\n    *   **基础信息**：姓名*、性别、联系电话*、身份证号（用于背景核查）。\n    *   **账户信息**：创建系统登录账号*（通常为手机号）、设置初始密码*（并强制要求首次登录后修改）。\n    *   **工作信息**：入职日期、所属团队/站点（如果有多站点管理）。\n    *   **紧急联系人**：姓名及电话，以备应急之需。\n\n**步骤4：配置权限与负责区域**\n*   **这是关键步骤**，直接影响后续任务分配：\n    *   **区域绑定**：在配送员信息页或单独配置页面，为其分配具体的 **“负责送餐区域”**（如：A栋、B区1-5层等）。确保与系统中的餐区划分一致。\n    *   **权限设置**：通常配送员移动端APP权限包括：查看配送任务、确认取餐、上报送达、异常情况反馈等。确保勾选相应的功能模块权限。\n\n**步骤5：保存并通知**\n*   保存所有信息后，系统将生成配送员账户。\n*   **重要**：将账号、初始密码及APP下载方式正式通知给该配送员，并指导其登录和熟悉移动端操作。\n\n### **三、 业务管理最佳实践与建议**\n1.  **入职审核**：在系统录入前，应完成配送员的入职手续，包括健康证明、基本培训等，确保符合为老送餐的服务要求。\n2.  **分阶段授权**：对于新配送员，初期可先分配较小或较简单的送餐区域，待其熟悉流程后再调整。\n3.  **与排班系统联动**：添加配送员后，需及时在 **“排班管理”** 模块中为其安排班次，否则他将无法接收到配送任务。\n4.  **信息维护**：定期更新配送员状态（如在岗、休假、离职），离职人员应及时**禁用或归档**其账户，而非直接删除，以保留历史数据。\n5.  **安全与隐私**：妥善保管配送员个人信息，遵守相关法律法规。\n\n### **四、 常见问题与排查**\n*   **配送员登录失败**：检查账号状态是否“启用”，密码是否正确，或联系系统技术支持。\n*   **无法看到配送任务**：检查其负责区域是否配置正确，以及当日是否已为其排班。\n*   **权限不足**：返回权限设置页面，检查其功能权限是否勾选完整。\n\n**总结**：添加配送员不仅是系统操作，更是融入服务团队的管理动作。请确保**系统信息准确、权限配置清晰、业务培训到位**，三者结合才能保障送餐服务流程顺畅，为长者提供准时、温情的送餐服务。\n\n如果系统界面与上述描述有差异，或操作中遇到具体技术问题，建议查阅系统的**管理员手册**或联系**系统实施顾问/技术支持**获取最直接的帮助。	admin_assistant	2026-04-05 22:51:53.978698+08
80	32	1ddc225b-0e31-4cde-9242-45a64215cadf	如何添加新的配送员？	作为颐养膳食系统的管理员，添加新的配送员是确保餐品准时、准确送达长者手中的关键环节。以下是详细、专业的操作流程和业务建议：\n\n### **一、 系统操作步骤（核心流程）**\n\n1.  **登录管理员后台**：\n    *   使用您的管理员账号和密码登录颐养膳食系统管理后台。\n\n2.  **进入人员管理模块**：\n    *   在左侧导航菜单或主控制面板中，找到并点击 **“人员管理”**、**“员工管理”** 或 **“配送员管理”** 等相关入口。\n\n3.  **选择“添加配送员”**：\n    *   在配送员列表页面，找到并点击 **“新增”**、**“添加配送员”** 或类似的按钮。\n\n4.  **填写配送员详细信息**（关键步骤）：\n    *   **基础信息**：\n        *   **姓名**：配送员的真实姓名。\n        *   **工号/员工编号**：系统可自动生成或手动录入唯一标识。\n        *   **手机号码**：**（必填且需验证）** 用于系统登录、接收派单通知和联系。\n        *   **登录密码**：设置初始密码，或由系统生成临时密码，要求首次登录后修改。\n    *   **业务信息**：\n        *   **所属区域/站点**：指定该配送员负责的配送区域、社区或中央厨房站点。这是进行智能派单的基础。\n        *   **配送工具**：登记电动车、汽车等，便于识别和管理。\n        *   **状态**：设置为 **“启用”**。\n    *   **权限与角色**：\n        *   在系统角色中，为其分配 **“配送员”** 角色。此角色通常包含：查看指派订单、更新配送状态（接单、取餐、送达）、上报异常、查看长者基本地址信息等权限。**切勿分配超出其职责范围的权限。**\n\n5.  **保存并通知**：\n    *   仔细核对信息后，点击“保存”或“提交”。\n    *   系统创建成功后，**务必通知该配送员**，并提供其登录账号（手机号）和初始密码，指导其下载配送端APP或使用小程序，并完成首次登录和密码修改。\n\n### **二、 业务流程与管理员须知（专业建议）**\n\n1.  **岗前培训与资质审核**：\n    *   **系统培训**：在添加至系统前，确保配送员已接受系统操作培训，包括如何接单、确认取餐、扫码送达、处理异常（如长者不在家、地址错误等）。\n    *   **服务规范培训**：强调服务礼仪、与长者的沟通技巧、餐品轻拿轻放、核对餐品与订单信息的重要性。\n    *   **安全与健康核查**：确保其持有有效的健康证（根据当地法规），并对其进行交通安全教育。\n\n2.  **区域与排班规划**：\n    *   **科学划分区域**：根据长者分布密度、送餐距离、路况，合理划分配送区域，并与系统中的区域设置匹配。\n    *   **设置排班**：在系统中为配送员设置工作日、排班时间（如早班、午班），确保送餐高峰期有足够人力覆盖。部分系统支持与排班模块联动。\n\n3.  **与订单系统的联动**：\n    *   配送员添加后，系统在派单时（自动或手动）会将其纳入对应区域的可用配送员池。\n    *   管理员需在后台监控 **“订单分配”** 和 **“配送状态看板”**，确保新配送员能正常接收和完成订单。\n\n4.  **绩效与监督**：\n    *   **设置关键指标**：如准时送达率、订单准确率、客户（长者）投诉率等。系统通常有配送员绩效统计功能。\n    *   **定期查看数据**：通过系统报表，定期回顾新配送员的配送数据，及时发现问题并进行辅导。\n\n5.  **账号安全与维护**：\n    *   强调账号专人专用，禁止共享。\n    *   若配送员离职，管理员应立即在系统中将其状态改为 **“禁用”** 或 **“离职”**，而非直接删除，以保留历史配送记录，确保数据完整性。\n\n### **三、 异常情况处理预案**\n\n*   **配送员无法登录**：检查其账号状态是否为“启用”，并协助重置密码。\n*   **接收不到订单**：检查其所属区域设置是否与当前派单区域匹配，以及排班时间是否正确。\n*   **配送中出现问题**：指导配送员使用配送端APP内的“上报异常”功能，并及时在后台跟进处理。\n\n### **总结**\n\n添加新配送员不仅是系统内的一个操作，更是一个管理流程的起点。**核心在于：系统信息准确录入 + 岗前业务培训 + 合理的区域排班规划 + 持续的绩效关注。** 请确保在将其投入实际配送前，完成所有必要的前置步骤，以保障整个送餐服务链条的顺畅与可靠。\n\n如果您在具体操作中遇到任何系统界面或字段差异，可以随时提供更多信息，我将为您提供更针对性的指导。	admin_assistant	2026-04-05 22:52:18.873526+08
81	32	a0c39651-e26b-40be-9a57-784c6cbe347a	系统有哪些快捷键？	作为颐养膳食系统的管理员，了解并熟练使用系统快捷键可以显著提升日常操作效率，优化对院内长者膳食服务的管理流程。以下是系统核心快捷键、操作建议及相关的业务流程说明：\n\n### **一、 系统通用快捷键（跨模块适用）**\n这些快捷键在系统的大部分界面中均可使用，是提高导航和基础操作效率的关键。\n\n1.  **全局导航与操作**\n    *   `Ctrl + S`：**快速保存**。在编辑长者信息、食谱、供应商资料等任何表单后，使用此快捷键可避免点击保存按钮，确保数据不丢失。\n    *   `Ctrl + F`：**页面内查找**。在长列表（如长者名单、菜品库、订单列表）中快速定位特定条目。\n    *   `Esc`：**关闭当前弹窗/返回**。快速取消操作或关闭不需要的对话框。\n    *   `F5`：**刷新当前页面**。更新数据列表，获取最新信息（如新提交的订餐、更新的库存）。\n\n2.  **列表与数据管理**\n    *   `Enter`：在选中列表中的某条记录后，**快速进入详情或编辑模式**（等效于双击）。\n    *   `Tab` / `Shift + Tab`：在表单的各个输入框之间**顺序/逆序跳转**，提高数据录入速度。\n\n### **二、 核心业务模块快捷键与操作流程**\n结合养老膳食的关键业务流程，以下快捷键能帮助您更流畅地完成日常任务。\n\n#### **1. 长者信息与膳食计划管理**\n*   **业务流程**：维护长者档案 -> 评估营养需求 -> 制定/调整个性化膳食计划。\n*   **关键快捷键**：\n    *   在长者列表界面，输入**长者姓名拼音首字母**或**房号**可快速筛选列表。\n    *   在编辑膳食计划时，使用 `Ctrl + C` / `Ctrl + V` 可**快速复制相似食谱**，用于为需求相近的长者制定计划。\n\n#### **2. 食谱设计与菜单发布**\n*   **业务流程**：设计周期食谱 -> 审核营养搭配 -> 发布每日菜单。\n*   **关键快捷键**：\n    *   `Ctrl + N`：在食谱库或菜单编制页面，**快速创建新菜品或新一日菜单**。\n    *   在拖拽式菜单编排界面，使用 **键盘方向键** 微调菜品顺序。\n    *   发布菜单前，使用 `Ctrl + P` 可**快速调起打印预览**，查看送餐单或厨房加工单。\n\n#### **3. 订餐统计与厨房作业**\n*   **业务流程**：汇总各渠道订餐 -> 生成生产计划与领料单 -> 分拣配送。\n*   **关键快捷键**：\n    *   在订餐统计总表界面，`Ctrl + E` 可**快速导出Excel报表**，方便交给厨房或财务。\n    *   在分拣配送界面，使用 **数字键** 可快速录入实际配送份数或特殊餐食数量。\n\n#### **4. 库存与采购管理**\n*   **业务流程**：监控库存预警 -> 生成采购计划 -> 录入入库单。\n*   **关键快捷键**：\n    *   在库存列表，按 `F3` 可**快速筛选“低于安全库存”的物品**。\n    *   在创建采购单时，`Ctrl + A` 可**快速全选推荐采购的物料**。\n\n### **三、 给管理员的专业操作建议**\n\n1.  **分阶段熟悉**：建议先熟练掌握通用快捷键（`Ctrl+S`, `Ctrl+F`），再针对您日常负责最多的模块（如订餐统计或食谱设计）学习专用快捷键。\n2.  **结合业务流程使用**：将快捷键嵌入到标准工作流中。例如，在完成每日菜单编排后，习惯性使用 `Ctrl+S` 保存，再使用 `Ctrl+P` 预览打印，形成肌肉记忆。\n3.  **培训团队成员**：在护理站或厨房的终端电脑旁，可以张贴一份“常用快捷键提示表”，帮助一线操作员提高数据录入和查询速度，减少工作差错。\n4.  **善用查询与筛选**：面对数百位长者的订餐数据时，灵活使用 `Ctrl+F` 和各类筛选快捷键，是快速响应个别长者需求变更的关键。\n\n### **四、 重要提示**\n*   部分高级快捷键可能因系统版本或权限设置略有不同，您可以在系统内**“个人设置”或“帮助中心”** 查看最准确的列表。\n*   快捷键的核心目的是**辅助**高效管理，对于复杂或重要的批量操作（如批量调整膳食计划），建议仍以界面操作为主，确保无误。\n\n熟练掌握这些快捷键，将助您从繁琐的重复点击中解放出来，更专注于膳食服务的营养搭配、个性化关怀和运营优化等核心价值工作。如有特定模块的操作效率问题，可随时提出。	admin_assistant	2026-04-05 22:52:34.761001+08
82	32	5a3e6b42-5ec8-4395-b2ae-c798b016ba49	系统有哪些快捷键？	作为颐养膳食系统的管理员，了解并熟练使用系统快捷键可以**显著提升日常操作效率**，尤其是在处理批量订单、快速查询和日常巡检时。\n\n以下是系统核心模块的常用快捷键清单及使用建议，适用于Web端管理后台：\n\n---\n\n### **一、通用全局快捷键（跨模块有效）**\n\n这些快捷键在系统大多数页面都适用，是管理员必须掌握的高效操作基础。\n\n| 快捷键 | 功能说明 | 适用场景与操作建议 |\n| :--- | :--- | :--- |\n| **F1** | 打开当前页面/功能的帮助文档 | 在任何不熟悉的页面，按F1可快速调出针对性操作指南。 |\n| **Ctrl + F** | 页面内搜索（查找） | 在长列表（如住户列表、菜品清单）中快速定位特定信息。 |\n| **Ctrl + S** | 保存当前表单 | 在编辑住户信息、配置餐谱、修改菜品后快速保存，避免忘记点击保存按钮。 |\n| **Esc** | 关闭当前弹窗/侧边栏 | 快速取消操作或关闭弹出的详情窗口，返回主界面。 |\n| **Ctrl + Z** | 撤销上一步操作 | 在餐谱编排、订单调整等可编辑区域误操作时，快速回退。 |\n\n---\n\n### **二、核心业务模块快捷键**\n\n#### **1. 订单与配送管理**\n此模块快捷键旨在帮助您快速处理每日大量的订餐确认、变更和配送任务。\n\n| 快捷键 | 功能说明 | 业务流程说明与建议 |\n| :--- | :--- | :--- |\n| **F5** | 刷新订单列表 | 在配送看板页面，按F5可实时获取最新订单状态（如“已下单”、“配送中”、“已完成”），确保信息同步。 |\n| **Ctrl + E** | 快速编辑选中订单 | 在订单列表选中一行后，按此快捷键可直接进入编辑模式，修改餐别、备注或特殊需求，比鼠标点击更快。 |\n| **Ctrl + D** | 标记为“已配送” | 在配送员终端或管理后台的配送列表中，选中订单后按此键，可一键更新状态，提升批量确认效率。 |\n| **Alt + S** | 快速搜索订单 | 光标会自动跳转至订单搜索框，可直接输入住户姓名、房号或订单号进行查询。 |\n\n#### **2. 住户与营养管理**\n用于快速查询和更新住户健康信息与膳食计划。\n\n| 快捷键 | 功能说明 | 业务流程说明与建议 |\n| :--- | :--- | :--- |\n| **Ctrl + P** | 打印当前住户膳食计划表 | 在查看某位住户的周/月膳食计划时，快速调起打印预览，用于归档或交给厨房备餐。 |\n| **Alt + H** | 高亮显示特殊饮食需求 | 在住户列表页面，按此键可将有“糖尿病餐”、“低嘌呤餐”等标签的住户行高亮，便于快速识别。 |\n\n#### **3. 菜品与餐谱管理**\n用于高效编排每周餐谱和管理菜品库。\n\n| 快捷键 | 功能说明 | 业务流程说明与建议 |\n| :--- | :--- | :--- |\n| **Ctrl + C / Ctrl + V** | 复制与粘贴菜品 | 在编排餐谱时，从“菜品库”拖拽或复制一个菜品后，可在多天餐谱中快速粘贴，提高重复菜品的设置速度。 |\n| **Ctrl + F** | 在菜品库中查找 | 当菜品库庞大时，直接按此键搜索菜品名称或食材，快速定位。 |\n| **空格键** | 预览选中菜品详情 | 在菜品列表中，选中一个菜品后按空格键，可弹出浮窗显示菜品图片、营养成分和禁忌，方便快速核对。 |\n\n#### **4. 报表与统计**\n用于快速生成和导出常用业务报表。\n\n| 快捷键 | 功能说明 | 业务流程说明与建议 |\n| :--- | :--- | :--- |\n| **Ctrl + E** | 导出当前报表 | 在“月度用餐统计”、“营养摄入分析”等报表页面，按此键可直接将当前视图数据导出为Excel文件。 |\n| **← / → 方向键** | 切换报表时间周期 | 在图形化报表页面，使用左右方向键可以快速切换查看“上周”、“本周”、“上月”、“本月”的数据对比。 |\n\n---\n\n### **三、给管理员的专业操作建议**\n\n1.  **分角色记忆**：根据您的主要职责（如侧重**订单配送**或**营养管理**），优先熟练掌握对应模块的快捷键。\n2.  **结合业务流程使用**：\n    *   **晨间巡检流程**：打开系统 → 按 **Alt+S** 快速搜索昨日异常订单 → 用 **Ctrl+E** 快速编辑处理 → 按 **F5** 刷新看板确认。\n    *   **每周餐谱编排流程**：在餐谱界面，使用 **Ctrl+F** 从菜品库找菜 → 用 **Ctrl+C/V** 快速填充每日餐别 → 用 **空格键** 预览关键菜品详情进行复核。\n3.  **培养肌肉记忆**：将最常用的2-3个快捷键（如 **Ctrl+S保存**、**Ctrl+F查找**）作为习惯，长期下来将节省大量时间。\n4.  **留意界面提示**：系统在部分按钮的悬停提示或页面角落，会标注可用的快捷键，请多加留意。\n\n> **请注意**：部分快捷键可能因系统版本或浏览器不同而略有差异。最准确的方式是查看系统内 **「帮助中心」** 或 **「个人设置」** 中的快捷键列表。以上清单基于通用管理后台设计，涵盖了颐养膳食系统管理员最高频的操作场景。\n\n如果您需要了解某个特定流程（如“处理批量退餐”）的详细快捷键组合，我可以为您进一步说明。	admin_assistant	2026-04-05 22:55:36.141946+08
83	32	598a4255-70cf-41a5-b97d-3a765a981acf	如何添加新的配送员？	作为颐养膳食系统的管理员，添加新的配送员是一项基础且重要的人员管理工作。以下是详细的操作流程、业务建议及注意事项：\n\n### **一、 核心操作步骤（系统内）**\n\n通常，配送员管理模块位于系统的 **“人员管理”**、**“配送管理”** 或 **“员工管理”** 菜单下。具体路径可能因系统版本略有不同。\n\n1.  **登录系统**：使用您的管理员账号登录颐养膳食系统后台。\n2.  **进入添加界面**：\n    *   导航至 **“配送员管理”** 或类似功能模块。\n    *   在列表页面，找到并点击 **“新增配送员”**、**“添加”** 或 **“+”** 按钮。\n3.  **填写配送员信息**：\n    *   **基础信息（必填）**：姓名、性别、手机号码（用于登录和联系）、身份证号（用于实名认证和合同备案）。\n    *   **账号信息**：系统通常会为手机号自动创建登录账号。您需要设置初始密码，或让配送员首次登录时通过短信验证码自行设置。\n    *   **工作信息**：分配所属的配送站点或区域、设置员工编号、入职日期。\n    *   **状态设置**：确保其账号状态为 **“启用”** 或 **“在职”**。\n4.  **分配权限与角色**：\n    *   在系统角色或权限设置中，为该配送员勾选 **“配送员”** 角色。此角色通常包含以下功能权限：\n        *   查看并接收配送任务单。\n        *   更新订单配送状态（如：已接单、配送中、已送达）。\n        *   上传签收凭证（如拍照）。\n        *   查看个人排班与绩效。\n5.  **保存并通知**：\n    *   仔细核对所有信息后，点击 **“保存”** 或 **“提交”**。\n    *   系统保存成功后，记录下配送员的登录账号（通常是手机号），并**及时通知该配送员**，告知其登录方式、初始密码以及需要下载的相关APP（如移动端配送员应用）。\n\n### **二、 业务流程与线下管理建议**\n\n系统操作只是第一步，规范的业务流程能确保配送服务质量和安全。\n\n1.  **入职培训与备案（先于系统添加）**：\n    *   **资质审核**：收集配送员的健康证、身份证、驾驶证（如需骑车/驾车）等复印件，进行备案。\n    *   **安全与服务培训**：必须进行岗前培训，内容包括：食品安全知识（如餐品保温、防污染）、配送服务规范、礼貌用语、紧急情况处理、系统APP操作等。\n    *   **签订协议**：签订劳动合同或劳务协议，明确职责、薪酬和安全责任。\n\n2.  **与运营流程对接**：\n    *   **排班管理**：在系统或排班表中将该配送员纳入相应的配送班次和区域。\n    *   **设备配发**：配发工作服、保温箱、车辆等必要装备，并登记在册。\n    *   **试运行**：初期可安排跟随老员工熟悉路线和流程，或分配少量订单进行实操。\n\n3.  **绩效与质量管理**：\n    *   在系统中，确保该配送员能被纳入后续的**绩效考核体系**（如准时率、投诉率、客户评价等）。\n    *   告知其评价标准，以便明确工作目标。\n\n### **三、 关键注意事项**\n\n*   **信息准确性**：手机号和身份证号务必准确，关系到登录、联系和工资发放。\n*   **权限最小化原则**：只授予配送工作所必需的权限，不要开放如菜品定价、客户信息批量导出等敏感或无关权限，确保系统安全。\n*   **账号安全**：提醒配送员首次登录后立即修改密码，并定期更换。\n*   **状态同步**：若配送员离职或调岗，务必及时在系统中将其状态更改为 **“停用”** 或调整其角色，并回收相关权限，防止信息泄露或误操作。\n*   **数据联动**：添加成功后，该配送员应能立即在“任务分配”、“排班管理”等关联模块中被选择和使用。\n\n### **四、 问题排查**\n\n*   **无法添加**：检查是否有必填字段遗漏，或手机号、身份证号是否与已有账号重复。\n*   **配送员无法登录**：确认账号是否已“启用”，手机号是否正确，网络是否正常。\n*   **看不到配送任务**：检查其所属配送区域、排班日期是否正确，以及任务是否已成功分配至该区域或人员。\n\n**总结**：添加新配送员应遵循 **“线下入职培训 → 系统信息录入 → 权限角色分配 → 上岗对接运营”** 的完整流程。系统操作是核心环节，但前后的业务管理是服务质量和团队稳定的保障。\n\n如果您在具体操作中遇到系统界面不一致或字段不明确的情况，可以查阅系统的帮助文档，或联系我们的技术支持团队获取针对您当前系统版本的精确指导。	admin_assistant	2026-04-05 22:58:23.889655+08
84	32	7783c268-ccef-466f-86dc-0cc1c90eb895	?????AI??	AI回复生成失败：	admin_assistant	2026-04-05 23:00:26.938756+08
85	32	0276a05d-e1b7-48cd-8c9e-372838111730	?????AI??	AI回复生成失败：	admin_assistant	2026-04-05 23:01:50.438655+08
86	32	f15fb7bd-42c5-4f03-a164-2e7d86eb4062	如何添加新的配送员？	作为颐养膳食系统的管理员，添加新的配送员是日常运营中的一项重要工作。为了确保配送流程的顺畅、高效和可追溯，请遵循以下专业、详细的操作流程和业务建议：\n\n### **一、 核心业务流程说明**\n\n在添加配送员之前，请理解其在系统中的业务角色：\n1.  **职责**：负责将餐食从中央厨房或配送点，安全、准时地送达至长者手中。\n2.  **关键信息**：配送员的个人信息、联系方式、负责区域、健康资质等是系统管理的核心。\n3.  **关联模块**：配送员信息将与“订单管理”、“配送排班”、“配送追踪”、“绩效统计”等模块深度联动。\n\n### **二、 系统操作步骤详解（以典型系统为例）**\n\n请登录管理员后台，按照以下路径操作：\n\n**路径：** `人员管理` -> `配送员管理` -> `新增配送员`\n\n**需填写的核心信息字段及注意事项：**\n\n1.  **基础信息**\n    *   **姓名**：填写真实姓名，用于线下核对与沟通。\n    *   **工号/员工ID**：系统唯一标识，建议按规则生成（如`PSY2024001`）。\n    *   **联系方式**：**必须填写准确有效的手机号**，用于接收配送任务、系统登录验证及紧急联络。\n    *   **登录账号**：通常为手机号或指定账号，用于配送端APP登录。\n    *   **初始密码**：设置默认密码或由系统生成，并**强制要求首次登录后修改**。\n\n2.  **业务信息**\n    *   **负责区域/站点**：从下拉列表中选择该配送员所属的配送站或负责的社区/楼栋。这是进行智能派单的基础。\n    *   **排班周期**：设置其常规工作班次（如早班、晚班、全职），以便系统自动排班。\n    *   **状态**：务必设置为“`在职`”或“`启用`”，否则无法分配任务。\n\n3.  **资质与安全信息（至关重要）**\n    *   **健康证信息**：上传有效期内的健康证照片，并填写证号与到期日期。**系统应设置到期前自动提醒**。\n    *   **交通工具**：登记配送使用的车辆类型（电动车、汽车等）及车牌号，便于管理。\n    *   **紧急联系人**：填写备用联系人及电话，以应对突发情况。\n\n4.  **权限与设置**\n    *   **APP功能权限**：确认其配送端APP的权限，通常包括：接收订单、导航、确认取餐/送达、上报异常、签收拍照等。\n    *   **数据查看范围**：通常配送员只能查看与自己相关的订单和客户信息。\n\n**完成填写后**：点击“保存”或“提交”。系统成功创建后，应通过短信或内部通知，将账号信息发送给该配送员。\n\n### **三、 管理员操作建议与最佳实践**\n\n1.  **岗前培训与资料核验**：\n    *   **线下先行**：在系统添加前，务必完成配送员的面试、背景了解及合同签订。\n    *   **资质核验**：必须线下查验并留存健康证、身份证等原件复印件，确保系统信息真实。\n    *   **操作培训**：对配送员进行系统性的培训，包括：配送端APP使用、服务规范（礼貌用语、餐品核对）、异常情况处理流程、食品安全及保温要求等。\n\n2.  **系统配置与测试**：\n    *   **测试账号**：添加后，建议管理员用测试订单为该配送员分配一个简单的任务，让其熟悉全流程。\n    *   **设备准备**：确保配送员手机已安装好配送端APP，并能正常登录、定位和使用。\n\n3.  **纳入运营流程**：\n    *   **排班计划**：将其加入下周或即日的配送排班计划中。\n    *   **通知相关方**：必要时，通知其所属站点的站长或相关调度人员。\n    *   **首次配送陪同**：对于重要区域，可安排有经验的配送员带领一次，熟悉路线和长者情况。\n\n### **四、 后续管理与风险控制**\n\n1.  **信息维护**：定期检查并更新配送员的健康证等资质信息，确保不过期。\n2.  **绩效关注**：初期关注其配送准时率、客户反馈（如有评价系统）等数据，及时提供辅导。\n3.  **权限管理**：若配送员离职，**务必第一时间在系统中将其状态变更为“离职”或“停用”**，并禁用其登录账号，以保障数据与配送安全。\n\n**总结**：添加配送员不仅是系统中的一个操作步骤，更是一个涉及 **`人事-培训-系统配置-运营衔接`** 的完整管理流程。严谨的线下核验与培训，配合系统化的信息录入与权限管理，是确保整个养老膳食配送服务链稳定、可靠运行的基础。\n\n如果您在具体操作中遇到字段不符或流程疑问，可以随时提供您系统的界面截图或描述，我将为您提供更针对性的指导。	admin_assistant	2026-04-05 23:03:08.905172+08
87	32	ef79b959-a53a-4f46-8393-71c574dc7db5	?????AI??	您好！作为颐养膳食系统的专业管理员助手，我将为您提供详细、专业的解答。\n\n首先，您的问题“?????AI??” 可能由于输入或传输原因，未能准确传达您的意图。在养老膳食系统的管理场景中，管理员通常会关注以下几个核心方面：\n\n1.  **系统操作与功能**：如菜单管理、营养分析、订单处理、配送管理等。\n2.  **业务流程优化**：如从订餐、备餐到配送、反馈的完整流程。\n3.  **数据与报表**：如用餐统计、营养摄入报告、成本分析等。\n4.  **异常处理**：如退订、换餐、过敏处理、配送延迟等。\n5.  **系统维护与支持**：如用户管理、权限设置、系统更新等。\n\n为了更精准地为您提供帮助，请您参考以下常见业务场景，并告诉我您具体想了解哪个方面，或重新描述您的问题：\n\n---\n\n### **核心业务场景与操作建议**\n\n#### **1. 菜单与营养管理**\n*   **业务流程**：营养师制定周期食谱 → 管理员录入系统并配置营养数据（热量、蛋白质、微量元素等） → 发布给长者选择。\n*   **操作建议**：\n    *   **差异化配置**：针对糖尿病、高血压、痛风等常见慢病，设置对应的“治疗膳食”标签，系统可自动过滤或提醒。\n    *   **智能推荐**：利用系统的AI营养分析功能，为新食谱或个性化订餐提供营养均衡性建议。\n    *   **定期更新**：根据季节、食材库存和长者反馈，定期优化食谱库。\n\n#### **2. 订餐与订单处理**\n*   **业务流程**：长者/家属通过终端（APP、平板、电话）订餐 → 系统汇总订单并生成厨房备餐单与配送清单 → 厨房按单备餐 → 配送员按楼层/房号配送。\n*   **操作建议**：\n    *   **设置订餐截止时间**：为厨房备餐留出合理时间，系统自动关闭超时订单。\n    *   **处理特殊需求**：在订单界面预留“备注”字段，用于收集“软食”、“切碎”、“免葱蒜”等要求，并确保醒目地传递至厨房。\n    *   **批量操作与导出**：熟练使用系统的批量确认、打印、导出Excel功能，提高日结效率。\n\n#### **3. 配送与追溯管理**\n*   **业务流程**：打包并贴上包含房号、姓名、膳食类型的标签 → 配送员扫码或签收确认 → 系统记录送达时间。\n*   **操作建议**：\n    *   **实现全程可追溯**：确保从订餐、备餐到配送的每个环节都在系统中有记录，便于查询和问责。\n    *   **处理未送达情况**：制定标准流程，如联系长者、确认原因、协调厨房留餐或退款，并在系统中记录原因。\n\n#### **4. 反馈与改进闭环**\n*   **业务流程**：收集用餐反馈（通过系统评分、意见栏、护理员转达） → 管理员定期汇总分析 → 将“口味过咸”、“米饭过硬”等有效反馈提交给营养师与厨师长 → 优化后续食谱。\n*   **操作建议**：\n    *   **主动设置反馈渠道**：在订餐界面或送餐后推送简单的满意度调查。\n    *   **建立定期复盘会议**：联合营养师、厨师长、护理部，每月基于系统数据（剩餐率、好评/差评菜品）进行复盘。\n\n#### **5. 数据管理与报表**\n*   **关键报表**：\n    *   **每日订餐统计表**：各餐次、各菜品的数量，指导采购与备餐。\n    *   **长者个人营养摄入周/月报**：可提供给家属或健康管理师。\n    *   **月度膳食成本分析报表**：分析食材成本占比，辅助成本控制。\n*   **操作建议**：熟悉系统报表生成功能，定期将关键数据呈现给管理层，作为决策支持。\n\n---\n\n### **如果您遇到的具体问题是...**\n\n*   **“如何为一位新入住的糖尿病长者设置饮食限制？”**\n    *   **操作**：在长者个人档案的“膳食偏好/禁忌”模块中，选择“糖尿病膳食”，并可根据其具体情况勾选“低糖”、“低GI”等子项。系统将在其订餐时自动屏蔽或警示不合适的菜品。\n*   **“今天有大量退订，如何处理？”**\n    *   **操作**：\n        1.  立即在系统“订单管理”中查看退订集中时段及原因（如有录入）。\n        2.  紧急通知厨房调整备餐量，减少浪费。\n        3.  调查原因：是菜品问题、配送问题还是活动冲突？并在系统中记录调查结果及改进措施。\n*   **“需要生成上月的营养分析总报告。”**\n    *   **操作**：进入系统“报表中心”，选择“营养分析报表”，时间范围选择上月，对象选择“全院”或特定楼栋，生成报告。报告通常包含平均热量摄入、营养素达标率等。\n\n请您根据您的实际工作需要，**提供更具体的问题描述**，例如：\n*   “如何处理长者临时换餐的需求？”\n*   “系统里的营养分析数据怎么校准？”\n*   “配送任务怎么分配和跟踪最有效率？”\n\n我将为您提供更具针对性、步骤清晰的专业操作指南。	admin_assistant	2026-04-05 23:03:40.396931+08
88	32	4f01bfc1-0e88-4fee-b62f-9a703b2f16a6	系统有哪些快捷键？	作为颐养膳食系统的管理员，了解并熟练使用系统快捷键可以显著提升日常操作效率，优化对院内长者膳食服务的管理流程。以下是系统核心快捷键、操作建议及相关的业务流程说明：\n\n### **一、 系统核心快捷键一览**\n\n为方便记忆，快捷键设计通常遵循通用逻辑（如Ctrl+S保存）并兼顾膳食业务高频操作。\n\n| 功能模块 | 快捷键 | 说明 |\n| :--- | :--- | :--- |\n| **通用操作** | `Ctrl + S` | **保存**当前表单或配置（如修改食谱、住户信息后）。 |\n| | `Ctrl + F` | 在当前页面或列表中**快速查找**（如查找特定长者、菜品）。 |\n| | `F5` | **刷新**当前数据列表（如订单列表、库存清单）。 |\n| | `Esc` | 关闭当前弹窗或取消当前操作。 |\n| **食谱与菜单管理** | `Ctrl + N` | 在食谱库中**新建**一个食谱或菜品。 |\n| | `Ctrl + E` | **编辑**当前选中的食谱或周期菜单。 |\n| | `Ctrl + P` | **打印**当前周/日的膳食计划或特殊饮食清单。 |\n| **订单与配送** | `Ctrl + O` | 快速进入**今日订单**总览页面。 |\n| | `Alt + C` | 在订单处理界面，快速**确认**选中订单（表示已备餐/已出餐）。 |\n| | `Alt + D` | 在订单处理界面，为选中订单标记为**配送中**。 |\n| **住户管理** | `Ctrl + H` | 快速打开**住户（长者）档案**管理列表。 |\n| | `Enter` | 在住户列表选中某位长者后，按回车键快速进入其**详细信息与饮食禁忌**页面。 |\n\n### **二、 专业操作建议与业务流程结合**\n\n1.  **每日订单处理流程（高效核验与派单）**\n    *   **流程**：查看今日总订单 (`Ctrl+O`) → 按楼栋或餐别筛选 (`Ctrl+F`) → 核对特殊饮食（如低糖、软食）→ 批量确认备餐完成 (`Alt+C`) → 标记开始配送 (`Alt+D`)。\n    *   **建议**：利用 `Ctrl+F` 快速定位特定护理区或特殊餐别的订单，避免滚动查找，确保配送准确无误。\n\n2.  **周期食谱制定与调整流程**\n    *   **流程**：新建下周食谱 (`Ctrl+N`) → 从食谱库拖拽或选择菜品 → 保存 (`Ctrl+S`) → 微调某日菜品 (`Ctrl+E`) → 最终打印 (`Ctrl+P`) 提交厨房及公示。\n    *   **建议**：在编辑 (`Ctrl+E`) 时，结合 `Ctrl+F` 快速查找替代菜品，以应对临时食材短缺问题。\n\n3.  **住户饮食信息更新流程**\n    *   **流程**：打开住户列表 (`Ctrl+H`) → 查找需更新信息的长者 (`Ctrl+F` 输入姓名或房号) → 回车 (`Enter`) 进入详情页 → 更新饮食禁忌、偏好或医嘱 → 保存 (`Ctrl+S`)。\n    *   **建议**：此流程确保长者饮食信息变更能即时同步至食谱和订单系统，保障餐饮安全。\n\n### **三、 重要提示**\n\n1.  **上下文敏感性**：部分快捷键（如 `Ctrl+E` 编辑）仅在特定模块（如选中具体条目后）生效。\n2.  **浏览器差异**：部分系统快捷键可能与浏览器快捷键冲突（如 `Ctrl+P` 通常是打印网页），在系统内操作时，系统快捷键通常优先。\n3.  **最佳实践**：\n    *   **新管理员培训**：建议将上述快捷键列表作为培训材料的一部分，并结合实际业务流程进行模拟操作。\n    *   **张贴速查表**：可在管理员工作站附近张贴快捷键速查表，方便随时查阅，形成肌肉记忆。\n    *   **关注系统提示**：在系统内各按钮或菜单项后，通常会有快捷键提示（如“保存(S)”），请多加留意。\n\n熟练掌握这些快捷键，将使您从繁琐的点击操作中解放出来，更专注于膳食搭配的合理性、特殊需求的满足以及整体服务质量的提升。如果您需要了解某个特定模块更详细的快捷键，或在实际操作中遇到问题，可随时查阅系统内置的“帮助”文档或联系技术支持。	admin_assistant	2026-04-05 23:04:36.998987+08
89	32	5244eb6b-0287-4b25-bec4-ff5f71aa817e	如何添加新的配送员？	作为颐养膳食系统的管理员，添加新的配送员是一项基础且重要的工作，以确保送餐服务的高效与准确。以下是详细的操作流程和专业建议：\n\n### **一、 核心业务流程说明**\n在添加配送员之前，请理解其涉及的完整业务闭环：\n1.  **人员入职与培训**：配送员需完成健康检查、合同签订及服务规范培训。\n2.  **系统信息录入**：管理员在后台将配送员信息数字化，建立其工作账户。\n3.  **任务分配与绑定**：将配送员与特定的配送区域、社区、楼栋或长者进行关联。\n4.  **上岗与执行**：配送员通过移动端APP接收任务，完成取餐、配送、打卡等操作。\n5.  **监督与考核**：管理员通过系统跟踪其配送时效、服务评价等数据。\n\n### **二、 系统操作步骤详解（以典型系统为例）**\n通常，您可以通过系统管理后台的 **“人员管理”** 或 **“配送管理”** 模块完成添加。\n\n**路径示例**：`后台首页 > 员工管理 > 配送员管理 > 添加新配送员`\n\n**需填写的核心信息字段及注意事项**：\n\n| 字段类别 | 具体字段 | 填写说明与专业建议 |\n| :--- | :--- | :--- |\n| **基础信息** | 姓名、性别、联系方式 | 必须准确，联系方式将用于系统登录和任务通知。 |\n| **账户信息** | 登录账号、初始密码 | 建议使用手机号作为账号。初始密码应强制要求首次登录后修改。 |\n| **健康信息** | 健康证编号、有效期 | **至关重要**！必须上传有效的健康证扫描件，并设置到期提醒，确保合规。 |\n| **区域绑定** | 负责配送区域、社区、楼栋 | 根据配送员的常住地或负责范围进行合理划分，实现网格化管理，提高效率。 |\n| **排班信息** | 工作班次、默认配送时段 | 与膳食计划时间挂钩，确保配送员在送餐高峰期在线。 |\n| **设备信息** | 配送工具（电动车/自行车编号） | 便于资产管理和安全追踪。 |\n\n**操作后动作**：\n1.  **信息确认**：保存前仔细核对所有信息，尤其是联系方式和负责区域。\n2.  **通知与培训**：生成账户后，**务必通知配送员本人**，并指导其下载、登录员工端APP，培训其使用接单、导航、签到、标记送达、异常上报等功能。\n3.  **权限检查**：确认该配送员账号在系统中只能看到和操作其负责区域内的任务，保护长者隐私。\n\n### **三、 专业管理建议**\n1.  **入职审核标准化**：将“健康证齐全”和“通过系统操作培训”作为系统账户激活的前置条件。\n2.  **启动“试用期”标签**：新配送员初期，可在其账号添加备注，并将其任务复杂度降低（如先配送固定楼层），方便跟踪指导。\n3.  **与膳食计划联动**：添加配送员后，及时检查或调整其负责区域的 **“膳食计划-配送设置”**，确保排班与送餐时间匹配。\n4.  **建立电子档案**：系统内不仅录入信息，还可上传合同、培训记录、考核结果等，形成完整的电子人事档案。\n5.  **安全与应急**：确保配送员知晓紧急联系人（如社区管理员、护理站）和突发情况（如长者无人应门）的处理流程，并在系统中预设这些联系信息。\n\n### **四、 常见问题与排查**\n*   **问题**：配送员无法看到分配的任务。\n    *   **排查**：检查其账号是否已启用；确认其“负责区域”设置是否准确；核对任务生成的时间是否在其排班时段内。\n*   **问题**：配送员APP无法登录。\n    *   **排查**：确认账号密码正确；检查账号是否被禁用；确认网络连接正常。\n\n**总结**：添加配送员不仅是信息录入，更是将其纳入整个服务流程的关键环节。请确保**线下入职流程**与**线上系统配置**无缝衔接，并重视后续的培训与监督，这样才能保障从厨房到长者手中的“最后一公里”服务温暖、准时、可靠。\n\n如果您在具体操作中遇到字段不符或流程差异，可提供您系统的界面截图或字段描述，我将为您提供更精准的指导。	admin_assistant	2026-04-05 23:06:13.490273+08
90	32	187036fc-c2f7-4533-94e1-e297c3101266	如何添加新的配送员？	作为颐养膳食系统的管理员，添加新的配送员是确保送餐服务顺畅运行的关键操作。以下是详细、专业的操作流程和业务建议：\n\n### **一、 核心业务流程说明**\n在添加配送员前，请确保已完成以下前置步骤：\n1.  **人员招聘与合同签订**：人事部门已完成配送员的招聘、背景审查（特别是无犯罪记录、健康证明等，因其服务对象为老年人）并签订正式劳动合同。\n2.  **岗前培训**：配送员已接受系统性的岗前培训，内容包括：\n    *   **服务规范**：对待老年人的礼仪、沟通技巧、隐私保护。\n    *   **食品安全**：餐品保温、卫生要求、配送箱清洁消毒。\n    *   **系统操作**：APP/设备使用、订单查看、状态更新、异常上报。\n    *   **安全与应急**：交通安全、突发情况（如老人不适）处理流程。\n3.  **物料配备**：已为配送员配发工作服、工牌、配送箱、保温设备、交通工具（或补贴标准）及系统操作终端（手机/设备）。\n\n### **二、 系统操作步骤详解（以典型系统为例）**\n请登录管理员后台，按照以下路径操作：\n\n**路径：** `后台管理` -> `人员管理` -> `配送员管理` -> `添加配送员`\n\n**需填写的核心信息及注意事项：**\n\n| 字段项 | 填写说明与业务建议 |\n| :--- | :--- |\n| **基本信息** | **姓名、身份证号**：必须与合同信息一致，用于身份核验。 |\n| | **手机号码**：**至关重要**。用于系统登录、接收派单、联系老人。务必确保准确。 |\n| | **入职日期**：与实际劳动合同日期一致，关系到考勤、薪资计算起点。 |\n| **账号信息** | **登录账号**：通常为手机号或工号。建议统一规则（如手机号）。 |\n| | **初始密码**：设置默认密码（如`123456`），并**强制要求首次登录修改**。为安全起见，可启用短信验证码登录。 |\n| | **所属区域/站点**：**必须准确分配**。根据配送员的常驻地点或负责片区选择，这是智能派单的基础。 |\n| **业务信息** | **配送工具**：登记交通工具（电动车/汽车），用于路线规划和时效评估。 |\n| | **排班与班次**：设置默认工作班次（如早班、晚班），或加入排班计划。确保与餐厅出餐时间、老人用餐时间匹配。 |\n| | **负责老人/楼栋**（若系统支持）：可初步绑定其负责配送的特定老人或楼栋，适用于“专人专送”模式。 |\n| **状态与权限** | **账户状态**：初始设置为“**启用**”。 |\n| | **操作权限**：通常配送员端权限固定（接单、上报、签收等），此处确认即可。 |\n\n**操作后动作：**\n1.  **点击“保存”或“提交”**。\n2.  **通知配送员**：将账号、初始密码、系统下载/登录方式、以及首次修改密码的强制要求，正式通知给该配送员。\n3.  **安排试运行**：建议安排1-2天在老配送员带领下进行跟单试送，熟悉流程后再独立接单。\n\n### **三、 后续管理与优化建议**\n1.  **绩效与培训档案关联**：在系统中，将该配送员与未来的**培训记录**、**绩效考核**（准时率、投诉率、老人评价）模块进行关联。\n2.  **启用电子围栏与签到**：若系统支持，为其配置配送区域的电子围栏，并启用上班签到、到点打卡功能，提升管理精度。\n3.  **定期账号审计**：定期检查配送员账号的活跃度和操作日志，确保账号安全。\n4.  **建立沟通群组**：将其加入工作通讯群（如企业微信、钉钉群），确保政策、通知、临时调班等信息传达畅通。\n\n### **四、 风险控制点**\n*   **信息准确性**：手机号、负责区域错误将直接导致派单混乱和配送失败。\n*   **权限最小化**：仅开放配送工作必需的权限，防止数据泄露或误操作。\n*   **安全第一**：反复强调配送途中的交通安全和食品安全，系统应支持配送员一键上报异常（如交通意外、老人紧急情况）。\n\n通过以上系统操作与业务流程的紧密结合，您可以高效、规范地将新配送员纳入服务体系，并为后续的精细化管理打下坚实基础。如果在具体操作中遇到字段不符或流程疑问，可随时查阅系统手册或联系技术支持。	admin_assistant	2026-04-06 12:46:53.894725+08
91	32	03628d9f-c121-4590-ac6a-2ebcaeb56295	如何添加新的配送员？	作为颐养膳食系统的管理员，添加新的配送员是一项基础且重要的工作。以下是详细、专业的操作流程和业务建议，旨在确保配送员信息准确、职责清晰，并能顺利融入送餐服务体系。\n\n### **一、 核心业务流程说明**\n\n在添加配送员之前，请理解其在系统中的角色定位：\n1.  **信息载体**：配送员是连接“厨房生产”、“配送调度”与“长者签收”的关键节点。\n2.  **责任主体**：其信息将关联到配送任务、餐品交接、异常反馈及服务评价。\n3.  **权限对象**：根据职责，需配置相应的系统操作权限（如APP接单、上报状态等）。\n\n标准的业务流程为：**信息收集与审核 → 系统录入与配置 → 培训与启用 → 归档备案**。\n\n---\n\n### **二、 详细操作步骤与建议**\n\n#### **步骤一：前期信息收集与审核（系统外准备）**\n在操作系统前，务必完成线下审核，确保人员合规。\n1.  **收集必备信息**：\n    *   **基础信息**：姓名、性别、联系方式、身份证号。\n    *   **健康信息**：有效期内的健康证明（餐饮行业必备）。\n    *   **资质信息**：驾驶证、行驶证（若使用机动车）、电动车备案信息（若使用电动车）。\n    *   **合同信息**：劳动合同或合作协议，明确服务范围、责任与保密条款。\n2.  **进行岗前审核**：\n    *   **背景核实**：确认无不良记录。\n    *   **健康与安全培训**：完成食品安全、个人防护及交通安全基础培训。\n    *   **路线熟悉**：要求其预先了解核心配送区域及长者集中点位。\n\n#### **步骤二：系统内录入与配置（核心操作）**\n此步骤在颐养膳食系统**管理后台**进行。\n1.  **登录管理后台**：使用管理员账户登录。\n2.  **进入人员管理模块**：通常位于 `组织架构`、`员工管理` 或 `配送管理` 菜单下。\n3.  **新增配送员**：\n    *   点击 `新增员工` 或 `添加配送员` 按钮。\n    *   填写表单信息：\n        *   **账号信息**：创建登录账号（通常为手机号）、设置初始密码。\n        *   **个人信息**：填入步骤一收集的姓名、电话等。\n        *   **岗位与权限**：\n            *   **岗位**：选择“配送员”或类似岗位。\n            *   **权限组**：分配“配送员”权限组，确保其只能访问和操作相关功能（如：查看分配任务、上报送达/异常、修改个人状态）。\n        *   **关联信息**（若系统支持）：\n            *   **所属站点/厨房**：指定其负责的配餐起点。\n            *   **默认配送区域**：绑定其负责的楼栋、社区或路线。\n    *   **上传附件**：将健康证、证件照等电子版上传至系统备案。\n4.  **保存并通知**：\n    *   保存信息后，系统可能自动向配送员手机发送账号激活通知。\n    *   请将账号、初始密码及系统APP下载方式正式告知该配送员。\n\n#### **步骤三：岗前系统培训与测试启用**\n1.  **操作培训**：指导配送员使用配送端APP/小程序，核心功能包括：\n    *   登录与打卡。\n    *   接收并确认配送任务。\n    *   执行“取餐-送达-签收”流程操作。\n    *   上报异常情况（如：长者不在家、餐品问题、交通延误）。\n    *   查看配送历史与注意事项。\n2.  **试运行**：安排其在老员工带领下进行1-2天试配送，熟悉系统操作与实地流程。\n3.  **正式启用**：试运行无误后，在系统将其状态调整为“在职”或“可用”，即可开始独立接收配送任务。\n\n#### **步骤四：档案归档与持续管理**\n1.  **建立电子档案**：在系统内确保其信息完整。\n2.  **建立纸质档案备份**：将个人信息、合同、资质复印件等归档保存，以备核查。\n3.  **纳入日常管理**：将其纳入排班、考勤、绩效考核与定期培训体系。\n\n---\n\n### **三、 关键注意事项与最佳实践**\n\n1.  **信息准确至上**：联系方式、身份证号必须准确无误，这是责任追溯的基础。\n2.  **权限最小化原则**：严格限制配送员的系统权限，仅开放其职责所需功能，保障数据安全。\n3.  **安全与保密教育**：必须强调对长者住址、健康状况等信息的保密义务。\n4.  **同步更新通讯群组**：将其加入工作联络群（如微信工作群），确保调度指令和信息畅通。\n5.  **定期复审资质**：设置提醒，在健康证等资质到期前及时通知更新，并在系统中替换新文件。\n\n### **四、 常见问题与处理建议**\n\n*   **问题**：配送员无法登录APP。\n    *   **检查**：账号是否激活？密码是否正确？账号是否被禁用？\n*   **问题**：配送员看不到分配的任务。\n    *   **检查**：系统内是否已将其关联到正确的配送区域和班次？其状态是否为“可用”？\n*   **问题**：添加时系统提示“手机号已存在”。\n    *   **处理**：确认是否为老员工复用，或联系上级管理员核查。\n\n**总结**：添加配送员不仅是简单的信息录入，更是一个包含 **“审核-配置-培训-管理”** 的完整闭环流程。严谨执行此流程，能显著提升配送服务质量的稳定性和可管理性，为长者提供更可靠、安心的送餐服务。\n\n如果您在具体操作中遇到任何系统界面或字段不明确的情况，可随时提供截图，我将为您提供更针对性的指导。	admin_assistant	2026-04-06 14:05:14.369061+08
92	33	22bfdd2d-a648-443d-8652-6d927316acab	hello	你好呀！很高兴见到你。今天过得怎么样？有什么想聊的或者需要帮忙的吗？我在这儿陪着你呢。 😊	elderly_assistant	2026-04-06 14:06:33.356358+08
93	33	f6d4c10f-8a66-4b72-bcfa-0450ce0c5b26	nihao	你好呀！很高兴见到你。我是你的AI助手，有什么问题或者想聊聊天，随时告诉我哦！ 😊	elderly_assistant	2026-04-06 14:52:43.579852+08
94	33	2a8c90de-0c92-45fa-8bec-183f2f8043ed	nihao	你好呀！很高兴见到你。我是你的AI助手，有什么问题或者想聊聊天，随时告诉我哦。今天过得怎么样呀？ 😊	elderly_assistant	2026-04-06 14:56:53.734959+08
95	32	73759eef-c8c1-485d-9252-ac553b642236	如何查看订单统计？	作为颐养膳食系统的管理员，您可以通过以下专业、详细的流程查看订单统计，以便进行业务分析和决策支持。\n\n### **一、 核心操作路径（建议）**\n\n通常，系统会提供两种主要的查看方式：\n\n1.  **仪表盘/首页概览**：\n    *   **位置**：登录系统后，管理员首页通常会有一个“数据看板”或“统计概览”模块。\n    *   **内容**：这里会以图表（如柱状图、折线图、饼图）和关键指标卡片的形式，直观展示**今日/本周/本月的订单总数、总金额、热门套餐、用餐时段分布**等核心数据。这是获取快速洞察的首选入口。\n\n2.  **专门的“订单统计”或“报表中心”模块**：\n    *   **位置**：在左侧或顶部的导航菜单中，寻找 **“数据统计”**、**“报表分析”**、**“订单报表”** 或 **“经营分析”** 等类似名称的菜单项。\n    *   **功能**：这是进行深度、自定义分析的核心区域。进入后，您通常会看到以下功能结构。\n\n### **二、 详细业务流程与操作建议**\n\n在“订单统计”模块中，建议您按以下专业流程进行操作：\n\n**步骤1：设定统计维度与筛选条件**\n一个专业的统计始于明确的分析目标。系统通常会提供以下筛选器，请根据您的管理需求进行组合：\n*   **时间范围**：选择 **今日、昨日、本周、本月、自定义日期区间**（这是最常用的功能，用于分析特定活动或时段的效果）。\n*   **订单状态**：筛选 **已下单、已确认、备餐中、已配送、已完成、已取消** 的订单，用于分析不同流程环节的转化与问题。\n*   **用餐类型**：区分 **堂食、自提、送餐上门**，分析不同服务模式的占比和趋势。\n*   **支付方式**：查看 **账户余额、现金、刷卡、线上支付** 等各方式的占比。\n*   **住户/客户群体**：可按 **楼栋、楼层、护理等级、特定住户** 进行筛选，用于个性化服务分析或家属对账。\n*   **餐别**：统计 **早餐、午餐、晚餐、加餐** 的订单情况。\n\n**步骤2：选择与解读核心统计报表**\n设定条件后，系统通常会生成以下几类关键报表，请关注其业务含义：\n\n1.  **订单趋势分析图**：\n    *   **形式**：折线图或柱状图。\n    *   **解读**：查看订单数量或金额随时间（日、周、月）的变化趋势。用于评估营销活动效果、发现周期性规律（如周末与工作日的差异）、预测未来备餐量。\n\n2.  **订单构成分析图**：\n    *   **形式**：饼图或环形图。\n    *   **解读**：分析不同**套餐、菜品、用餐类型、支付方式**的销售额或订单量占比。帮助您识别最受欢迎的菜品，优化菜单结构和采购计划。\n\n3.  **明细数据统计表**：\n    *   **形式**：可排序、分页的表格。\n    *   **关键字段**：订单号、住户姓名、用餐时间、套餐详情、数量、金额、订单状态、支付方式、配送员等。\n    *   **操作**：支持 **导出为Excel/PDF**，用于财务对账、存档或进一步线下分析。\n\n**步骤3：执行操作与决策支持**\n基于报表数据，您可以：\n*   **运营优化**：发现用餐高峰时段，合理调配厨房和配送人力。\n*   **菜单调整**：根据菜品销量排行，淘汰滞销菜品，加大热门菜品供应。\n*   **财务对账**：导出的明细表可与财务系统核对，确保账实相符。\n*   **个性化关怀**：关注特定住户（如糖尿病餐、流食）的订单规律，确保服务到位。\n*   **营销评估**：对比活动前后的订单数据，量化营销活动效果。\n\n### **三、 专业提醒与最佳实践**\n\n1.  **定期查看**：建议建立每日查看“今日概览”，每周分析“周报”，每月深度复盘“月报”的例行工作制度。\n2.  **关注异常**：特别留意**订单取消率**的突然升高或某个时段**投诉订单**的集中出现，这可能是餐饮质量、配送或系统问题的信号。\n3.  **权限管理**：确保只有授权的管理人员可以访问完整的统计数据和明细，保护住户隐私和商业数据安全。\n4.  **系统更新**：关注系统更新日志，新的统计功能或更直观的图表可能被加入。\n\n如果您在系统中找不到上述对应菜单或功能，可能是权限配置或系统版本问题。**建议您：**\n1.  检查您的管理员账号是否拥有“数据报表”或“统计查询”等相关权限。\n2.  查阅系统的**帮助文档**或**操作手册**。\n3.  联系您的**系统实施顾问**或**技术支持团队**，获取针对您当前系统版本的最准确指引。\n\n通过系统化的订单统计分析，您可以将运营数据转化为实际的管理决策，从而提升养老膳食服务的效率、满意度和精细化水平。	admin_assistant	2026-04-07 09:44:40.276028+08
96	33	8d7961ae-ab22-4273-9f05-16ce3818a9de	你好	你好呀！很高兴见到你。今天过得怎么样？有什么想聊的，或者需要帮忙的，随时告诉我哦。我在这儿陪着你呢！ 🌼	elderly_assistant	2026-04-07 22:50:29.063836+08
97	33	e88c1590-620b-4d0d-8963-899aec5e944d	你好	你好呀！很高兴见到你。今天过得怎么样？有什么想聊的或者需要帮忙的，随时告诉我哦。我在这儿陪着你呢！ 🌼	elderly_assistant	2026-04-07 23:49:54.941132+08
98	33	713a8095-955f-42b5-9e20-799cdef24843	喂喂喂测试测试。	喂，你好呀！我在这儿呢，听得很清楚哦。  \n有什么想聊的，或者需要帮忙的，尽管慢慢说，我陪着你呢！ 😊	elderly_assistant	2026-04-11 19:24:46.274566+08
99	33	2578c3b0-1e10-49df-bfad-2a00a8991221	喂喂喂测试测试。	喂喂喂，听到了听到了！我在这儿呢，您慢慢说，我听着呢。有什么需要帮忙的，尽管告诉我，咱们一起想办法。😊	elderly_assistant	2026-04-11 19:27:40.395675+08
100	33	546f8007-96fe-4127-982f-73df56683c0f	请问你会什么呀？	哎呀，孩子，谢谢你这么问我呀！我这个老伙计虽然年纪大，但记性还不错，能帮你不少忙呢。\n\n我会陪你聊天解闷儿，听你说说心里话；能帮你记事儿，提醒你吃药、出门带钥匙；天气变了我会告诉你添衣服，还能给你讲讲故事、说说新闻。你想学用手机、找电视节目，我也能慢慢教你。\n\n总之啊，你闷了、有事儿了，随时叫我就行。咱们慢慢说，不着急。	elderly_assistant	2026-04-11 19:28:03.013907+08
101	33	cbb515b1-3902-42cc-8f1c-76fbc9ae581d	喂喂喂测试测试。	喂喂喂，听到了听到了！我在这儿呢，您慢慢说，我听着呢。😊  \n\n要是想试试我能不能帮上忙，您尽管开口——比如问问天气、聊聊天，或者需要记个事儿、讲个故事都行。您说什么我都乐意听！  \n\n（如果是在试声音或者设备，您也可以告诉我，我可以陪您多试几句～）	elderly_assistant	2026-04-11 20:07:21.357267+08
102	33	4e3169fb-ce0d-4e80-bcbb-8adb41db2383	喂喂喂测试测试。	喂喂喂，听到了听到了！我在这儿呢，您慢慢说，我听着呢。有什么需要帮忙的，您尽管告诉我，我会陪着您慢慢聊的。😊	elderly_assistant	2026-04-11 20:10:59.734216+08
103	33	eab1c54e-8430-447a-aebd-8295d3c04b6c	喂喂喂测试测试。	喂，你好呀！我在这儿呢，能听到你的声音。  \n刚才是在测试吗？没问题，我随时都在，有什么想问的、想聊的，慢慢跟我说就好。 😊	elderly_assistant	2026-04-11 20:23:28.901552+08
104	32	ef2dca95-31ee-4bbb-b1a8-972f555a0022	如何添加新的配送员？	作为颐养膳食系统的管理员，添加新的配送员是一项基础且重要的人员管理工作。以下是详细的操作流程、业务建议及注意事项，旨在确保配送员信息准确、职责清晰，并能顺利融入送餐服务体系。\n\n### **一、 核心操作流程（系统内操作）**\n\n通常，系统会在 **“人员管理”** 或 **“配送管理”** 模块下提供配送员管理功能。具体路径可能为：\n`后台管理 > 员工管理 > 配送员管理` 或 `运营管理 > 配送团队 > 添加配送员`。\n\n**标准步骤：**\n\n1.  **进入添加页面**：在配送员列表页面，点击“新增”、“添加配送员”或类似按钮。\n2.  **填写基本信息**（带*号为必填项）：\n    *   **账号信息**：登录账号（通常为手机号）、初始密码（需告知配送员首次登录后修改）。\n    *   **身份信息**：姓名、性别、手机号（**至关重要，用于联系和APP登录**）、身份证号（用于背景核查，可选但建议）。\n    *   **入职信息**：所属站点/配送区域、入职日期、员工编号。\n3.  **设置配送属性**：\n    *   **绑定配送工具**：选择电动车、自行车等，并填写车牌号/工具编号，便于管理。\n    *   **设定负责区域**：从预设的区域列表中选择该配送员负责的送餐小区、楼栋或路线。**这是确保订单精准分配的关键**。\n    *   **排班设置**：指定其工作日、班次（如早班、午班、晚班）或设置为弹性班次。\n4.  **权限与状态设置**：\n    *   **系统权限**：通常配送员端APP权限固定（接单、导航、上报、签到等），此处主要确认其是否激活“接单”权限。\n    *   **账户状态**：设置为“启用”。\n5.  **保存并通知**：保存信息后，系统通常会生成账号。**务必及时将账号、密码及APP下载方式通知到配送员本人**。\n\n### **二、 业务流程与线下管理建议（系统操作之外）**\n\n专业的配送员管理远不止系统录入，更在于完整的入职与管理流程：\n\n1.  **入职前准备**：\n    *   **资质审核**：查验身份证、健康证（餐饮配送相关）、电动车驾驶证等，确保合规。\n    *   **安全培训**：必须进行食品安全、配送安全、交通规则及服务礼仪的岗前培训。\n    *   **合同签订**：签订劳动合同或服务协议，明确职责、薪酬、保险等。\n\n2.  **配送员培训内容**：\n    *   **APP操作**：如何登录、接单、查看订单详情、使用导航、确认送达、处理异常（如无法联系老人、地址错误）。\n    *   **服务规范**：敲门/通话礼仪、餐品核对、特殊关怀（如为高龄老人摆放好餐食）、保温箱使用与清洁。\n    *   **安全与应急**：配送途中安全、恶劣天气应对、突发情况（如老人身体不适）上报流程。\n\n3.  **试运行与跟进**：\n    *   **老带新**：安排经验丰富的配送员带领熟悉路线和重点客户。\n    *   **初期跟踪**：管理员在前几天应关注其订单完成情况、送达时效和客户反馈（如有评价系统）。\n    *   **装备配发**：发放工服、保温箱、头盔等标识性装备。\n\n### **三、 关键注意事项**\n\n*   **信息准确性**：手机号必须本人常用且准确，这是通信和系统验证的根基。\n*   **区域划分明确**：清晰的区域划分能极大提升配送效率和订单分配的公平性，避免争单或漏单。\n*   **权限最小化**：仅开放配送工作所需的最小系统权限，保护用户数据安全。\n*   **动态管理**：定期复核配送员状态（在职/离职），及时在系统中调整。离职人员务必立即**停用账号**，防止数据泄露。\n*   **建立档案**：建议建立线下或电子人事档案，包含合同、证件复印件、培训记录等，便于管理。\n\n### **四、 总结与最佳实践**\n\n**操作口诀： “先线下，后线上；先培训，后上岗；权责清，区域明。”**\n\n作为管理员，您不仅是信息的录入者，更是流程的监督者。一个规范的配送员添加流程应该是：\n**招聘审核 → 合同培训 → 系统录入 → 装备配发 → 实地带教 → 考核上岗**。\n\n通过系统与线下管理的紧密结合，您不仅能将配送员信息成功添加到颐养膳食系统中，更能打造一支专业、可靠、有温度的送餐服务团队，从而保障养老服务“最后一公里”的质量与安全。\n\n如果在具体操作中遇到字段不符或权限问题，请参考您的系统使用手册或联系系统技术支持。	admin_assistant	2026-04-11 20:38:32.79188+08
\.


--
-- TOC entry 6187 (class 0 OID 79529)
-- Dependencies: 241
-- Data for Name: announcements; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.announcements (id, title, content, type, priority, status, created_at, updated_at) FROM stdin;
3	紧急通知	近期天气寒冷，请老人注意保暖	emergency	high	active	2026-03-31 18:46:17.80617+08	2026-03-31 18:46:17.80617+08
4	test	test	system	normal	active	2026-04-04 15:36:05.741459+08	2026-04-04 15:36:05.741459+08
1	系统维护通知	系统将于本周日凌晨2点进行维护，预计持续2小	system	normal	active	2026-03-31 18:46:17.80617+08	2026-04-08 21:04:22.047504+08
5	test1	test1	system	normal	active	2026-04-09 20:22:12.852075+08	2026-04-09 20:22:47.433903+08
6	123	123	system	normal	active	2026-04-09 20:23:00.716456+08	2026-04-09 20:23:00.716456+08
8	test草稿	test草稿	system	normal	draft	2026-04-09 20:29:57.385011+08	2026-04-09 20:31:24.703307+08
10	555这是一个草稿	555这是一个草稿	system	normal	draft	2026-04-09 20:34:44.536439+08	2026-04-09 20:34:44.536439+08
9	111草稿	111草稿	system	normal	draft	2026-04-09 20:31:43.419336+08	2026-04-09 20:39:47.281462+08
7	这是一个草稿	这是一个草稿	system	normal	draft	2026-04-09 20:28:07.640598+08	2026-04-09 20:44:29.63779+08
2	新功能上线	老人端新增健康监测功能，请及时更新	notice	normal	draft	2026-03-31 18:46:17.80617+08	2026-04-09 20:51:48.01459+08
\.


--
-- TOC entry 6202 (class 0 OID 79770)
-- Dependencies: 256
-- Data for Name: categories; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.categories (id, name, description, created_at, updated_at) FROM stdin;
4	主食	主食类餐品	2026-03-31 20:40:06.040883+08	2026-03-31 20:40:06.040883+08
5	凉菜	凉菜类餐品	2026-03-31 20:40:06.040883+08	2026-03-31 20:40:06.040883+08
6	荤菜	荤菜类餐品	2026-03-31 20:40:06.040883+08	2026-03-31 20:40:06.040883+08
7	辅食	辅食类餐品	2026-03-31 20:40:06.040883+08	2026-03-31 20:40:06.040883+08
10	营养套餐	\N	2026-04-02 08:45:12.532754+08	2026-04-02 08:45:12.532754+08
\.


--
-- TOC entry 6191 (class 0 OID 79564)
-- Dependencies: 245
-- Data for Name: communities; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.communities (id, name, address, contact_phone, manager_name, manager_phone, created_at, updated_at, status) FROM stdin;
4	安康社区	北京市西城区安康街101号	010-55555555	赵主任	13900139003	2026-04-01 14:29:00.000492+08	2026-04-07 19:42:28.2475+08	正常
5	长寿社区	北京市丰台区长寿路202号	010-44444444	刘主任	13900139004	2026-04-01 14:29:00.000492+08	2026-04-07 19:42:28.2475+08	正常
6	新一社区	test	136356669978	李主任	136356669978	2026-04-07 19:03:15.747729+08	2026-04-07 19:42:28.2475+08	正常
1	幸福社区	北京市朝阳区幸福路123号	010-88888888	王主任	010-88888888	2026-04-01 14:29:00.000492+08	2026-04-07 19:46:02.175846+08	正常
3	和谐社区	北京市东城区和谐路789号	010-66666666	张主任	010-66666666	2026-04-01 14:29:00.000492+08	2026-04-07 19:47:52.447831+08	暂停服务
2	阳光社区	北京市海淀区阳光街456号	010-77777777	李主任	010-77777777	2026-04-01 14:29:00.000492+08	2026-04-07 19:48:00.260297+08	正常
\.


--
-- TOC entry 6173 (class 0 OID 79337)
-- Dependencies: 227
-- Data for Name: deliverer_profiles; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.deliverer_profiles (user_id, name, phone, vehicle_type, status, created_at, updated_at, area_id, avatar, latitude, longitude, location_updated_at) FROM stdin;
75	张腿子	17836553396	摩托车	offline	2026-04-07 18:10:46.663373+08	2026-04-07 18:51:53.318118+08	1	http://localhost:7678/static/uploads/avatars/c5b2739f-6031-4911-8be2-a68174c25a63.jpg	\N	\N	\N
51	微信配送员	13783898556	汽车	available	2026-04-06 08:25:45.94966+08	2026-04-12 15:00:24.195548+08	4	\N	32.145359971788196	114.03694173177084	2026-04-12 07:00:24.197988+08
43	王师傅	13800138010	自行车	offline	2026-04-01 12:02:32.453091+08	2026-04-12 09:48:52.498556+08	2	\N	32.11683	114.05857	2026-04-05 16:13:20.054739+08
42	李师傅	13800138009	电动车	offline	2026-04-01 12:02:32.453091+08	2026-04-12 09:48:52.498556+08	1	http://localhost:7678/static/uploads/avatars/7b97a389-257d-4fdf-a5ad-818d5b2d8a6d.jpg	32.145359971788196	114.03694173177084	2026-04-07 12:31:08.436396+08
45	狗腿子	1314521	摩托车	available	2026-04-02 10:17:20.669981+08	2026-04-12 10:42:58.867093+08	4	\N	32.145359971788196	114.03694173177084	2026-04-12 02:42:58.868411+08
\.


--
-- TOC entry 6181 (class 0 OID 79414)
-- Dependencies: 235
-- Data for Name: deliveries; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.deliveries (id, order_id, deliverer_id, end_time, estimated_time, status, created_at, updated_at, actual_time, is_assigned_by_admin) FROM stdin;
1	36	42	\N	\N	DELIVERED	2026-04-02 20:57:47.652874+08	2026-04-02 21:57:54.813566+08	2026-04-02 13:57:54.820377+08	f
2	35	42	\N	\N	DELIVERED	2026-04-02 22:03:54.894199+08	2026-04-02 22:05:01.709113+08	2026-04-02 14:05:01.712568+08	f
3	37	42	\N	\N	DELIVERED	2026-04-02 22:13:14.532943+08	2026-04-02 22:14:27.714442+08	2026-04-02 14:14:27.716638+08	f
4	38	42	\N	\N	DELIVERED	2026-04-02 22:21:54.833821+08	2026-04-02 22:22:14.921519+08	2026-04-02 14:22:14.924325+08	f
5	72	42	\N	\N	DELIVERED	2026-04-03 08:18:24.737374+08	2026-04-03 08:19:29.071581+08	2026-04-03 00:19:29.074148+08	f
7	77	42	\N	\N	DELIVERED	2026-04-03 08:54:22.838669+08	2026-04-03 08:57:59.291785+08	2026-04-03 00:57:59.296337+08	f
8	32	42	\N	\N	DELIVERED	2026-04-03 09:13:13.650008+08	2026-04-03 09:13:30.251946+08	2026-04-03 01:13:30.256389+08	f
9	79	42	\N	\N	DELIVERED	2026-04-03 15:21:24.629137+08	2026-04-03 15:21:48.69949+08	2026-04-03 07:21:48.700881+08	f
10	80	42	\N	\N	DELIVERED	2026-04-03 23:42:02.052259+08	2026-04-03 23:42:21.417141+08	2026-04-03 15:42:21.424733+08	f
11	82	42	\N	\N	DELIVERED	2026-04-04 17:27:18.712832+08	2026-04-04 17:27:27.497788+08	2026-04-04 09:27:27.499389+08	f
15	39	43	\N	2026-04-04 13:00:00+08	DELIVERED	2026-04-04 18:42:33.610122+08	2026-04-04 18:46:50.9742+08	2026-04-04 10:46:50.977511+08	t
16	83	43	\N	\N	ASSIGNED	2026-04-04 18:57:19.983813+08	2026-04-04 18:57:19.983813+08	\N	f
12	81	45	\N	2026-04-04 13:00:00+08	DELIVERED	2026-04-04 18:04:05.85666+08	2026-04-04 21:45:09.177157+08	2026-04-04 13:45:09.18218+08	t
17	85	42	\N	\N	DELIVERED	2026-04-05 16:15:08.156901+08	2026-04-05 16:15:12.029206+08	2026-04-05 08:15:12.033995+08	f
20	86	42	\N	\N	DELIVERED	2026-04-05 17:11:44.465227+08	2026-04-05 17:11:57.965008+08	2026-04-05 09:11:57.967172+08	f
21	75	51	\N	\N	DELIVERED	2026-04-06 09:07:58.854905+08	2026-04-06 09:08:14.999717+08	2026-04-06 01:08:15.003312+08	f
22	74	51	\N	\N	DELIVERED	2026-04-06 09:09:41.037778+08	2026-04-06 09:16:13.048781+08	2026-04-06 01:16:13.053784+08	f
18	84	42	\N	\N	DELIVERED	2026-04-05 16:15:36.037378+08	2026-04-06 09:17:27.222264+08	2026-04-06 01:17:27.22448+08	f
6	78	42	2026-04-06 01:31:29.579895+08	\N	DELIVERED	2026-04-03 08:47:29.538343+08	2026-04-06 09:31:29.57569+08	2026-04-06 01:31:29.579895+08	f
23	73	51	2026-04-06 01:35:08.103873+08	\N	DELIVERED	2026-04-06 09:35:06.228269+08	2026-04-06 09:35:08.100252+08	2026-04-06 01:35:08.103873+08	f
24	88	51	2026-04-06 01:38:48.281158+08	\N	DELIVERED	2026-04-06 09:38:37.701093+08	2026-04-06 09:38:48.277096+08	2026-04-06 01:38:48.281158+08	f
25	89	51	2026-04-06 01:39:41.486242+08	\N	DELIVERED	2026-04-06 09:39:39.375929+08	2026-04-06 09:39:41.484893+08	2026-04-06 01:39:41.486242+08	f
26	90	51	2026-04-06 01:56:03.786739+08	\N	DELIVERED	2026-04-06 09:51:10.170434+08	2026-04-06 09:56:03.778636+08	2026-04-06 01:56:03.786739+08	f
27	91	51	2026-04-06 02:00:59.727507+08	\N	DELIVERED	2026-04-06 10:00:43.761447+08	2026-04-06 10:00:59.725031+08	2026-04-06 02:00:59.727507+08	f
28	92	51	2026-04-06 02:02:33.25999+08	\N	DELIVERED	2026-04-06 10:02:24.951314+08	2026-04-06 10:02:33.257256+08	2026-04-06 02:02:33.25999+08	f
29	93	51	2026-04-06 02:05:50.05557+08	\N	DELIVERED	2026-04-06 10:05:36.449152+08	2026-04-06 10:05:50.049642+08	2026-04-06 02:05:50.05557+08	f
19	76	45	2026-04-06 02:13:31.216903+08	\N	DELIVERED	2026-04-05 16:18:47.070735+08	2026-04-06 10:13:31.212154+08	2026-04-06 02:13:31.216903+08	f
31	95	45	2026-04-06 02:13:44.185963+08	\N	DELIVERED	2026-04-06 10:13:42.669659+08	2026-04-06 10:13:44.183006+08	2026-04-06 02:13:44.185963+08	f
32	96	51	2026-04-06 02:14:57.476052+08	\N	DELIVERED	2026-04-06 10:14:55.487286+08	2026-04-06 10:14:57.473845+08	2026-04-06 02:14:57.476052+08	f
34	98	51	2026-04-06 02:21:43.040233+08	\N	DELIVERED	2026-04-06 10:21:35.356158+08	2026-04-06 10:21:43.035538+08	2026-04-06 02:21:43.040233+08	f
33	97	51	2026-04-06 02:21:44.24835+08	\N	DELIVERED	2026-04-06 10:17:25.676454+08	2026-04-06 10:21:44.244882+08	2026-04-06 02:21:44.24835+08	f
30	94	51	2026-04-06 02:21:45.454789+08	\N	DELIVERED	2026-04-06 10:07:50.163215+08	2026-04-06 10:21:45.451555+08	2026-04-06 02:21:45.454789+08	f
35	99	51	2026-04-06 02:27:51.384463+08	\N	DELIVERED	2026-04-06 10:26:21.806746+08	2026-04-06 10:27:51.381313+08	2026-04-06 02:27:51.384463+08	f
36	101	51	2026-04-06 02:29:50.483523+08	\N	DELIVERED	2026-04-06 10:29:49.006773+08	2026-04-06 10:29:50.482698+08	2026-04-06 02:29:50.483523+08	f
37	102	51	2026-04-06 02:31:53.294897+08	\N	DELIVERED	2026-04-06 10:31:51.822842+08	2026-04-06 10:31:53.292158+08	2026-04-06 02:31:53.294897+08	f
38	103	51	2026-04-06 02:34:44.472898+08	\N	DELIVERED	2026-04-06 10:34:43.153953+08	2026-04-06 10:34:44.47105+08	2026-04-06 02:34:44.472898+08	f
39	104	51	2026-04-06 02:37:39.19106+08	\N	DELIVERED	2026-04-06 10:37:37.715658+08	2026-04-06 10:37:39.188436+08	2026-04-06 02:37:39.19106+08	f
40	100	51	2026-04-06 02:41:13.703543+08	\N	DELIVERED	2026-04-06 10:39:47.828573+08	2026-04-06 10:41:13.69989+08	2026-04-06 02:41:13.703543+08	f
41	105	51	2026-04-06 02:46:37.191532+08	\N	DELIVERED	2026-04-06 10:46:35.002321+08	2026-04-06 10:46:37.188212+08	2026-04-06 02:46:37.191532+08	f
42	106	51	2026-04-06 03:37:12.713263+08	\N	DELIVERED	2026-04-06 11:37:10.456426+08	2026-04-06 11:37:12.711738+08	2026-04-06 03:37:12.713263+08	f
43	107	51	2026-04-06 04:37:27.299924+08	\N	DELIVERED	2026-04-06 12:36:54.549733+08	2026-04-06 12:37:27.296927+08	2026-04-06 04:37:27.299924+08	f
44	108	51	2026-04-06 07:10:54.060505+08	\N	DELIVERED	2026-04-06 15:10:47.866003+08	2026-04-06 15:10:54.055726+08	2026-04-06 07:10:54.060505+08	f
45	109	51	2026-04-06 07:39:57.242794+08	\N	DELIVERED	2026-04-06 15:39:55.659014+08	2026-04-06 15:39:57.240098+08	2026-04-06 07:39:57.242794+08	f
46	112	51	2026-04-07 04:39:06.132876+08	\N	DELIVERED	2026-04-07 12:39:04.379015+08	2026-04-07 12:39:06.130373+08	2026-04-07 04:39:06.132876+08	f
47	111	51	2026-04-07 04:46:29.235369+08	\N	DELIVERED	2026-04-07 12:46:27.607955+08	2026-04-07 12:46:29.232034+08	2026-04-07 04:46:29.235369+08	f
48	110	51	2026-04-07 04:46:49.143867+08	\N	DELIVERED	2026-04-07 12:46:40.653406+08	2026-04-07 12:46:49.140812+08	2026-04-07 04:46:49.143867+08	f
49	113	51	\N	\N	ASSIGNED	2026-04-07 13:29:24.710293+08	2026-04-07 13:29:24.710293+08	\N	f
50	119	51	\N	2026-04-07 13:00:00+08	IN_TRANSIT	2026-04-07 19:48:43.645459+08	2026-04-07 19:53:50.155637+08	\N	t
53	126	51	2026-04-08 10:08:29.449764+08	\N	DELIVERED	2026-04-08 18:08:16.204884+08	2026-04-08 18:08:29.447876+08	2026-04-08 10:08:29.449764+08	f
54	127	51	2026-04-08 10:20:21.123602+08	\N	DELIVERED	2026-04-08 18:20:18.637113+08	2026-04-08 18:20:21.120775+08	2026-04-08 10:20:21.123602+08	f
55	128	51	2026-04-08 10:22:43.106858+08	\N	DELIVERED	2026-04-08 18:22:40.972889+08	2026-04-08 18:22:43.104855+08	2026-04-08 10:22:43.105836+08	f
56	129	51	2026-04-08 10:23:53.027993+08	\N	DELIVERED	2026-04-08 18:23:49.979717+08	2026-04-08 18:23:53.025722+08	2026-04-08 10:23:53.027993+08	f
57	130	51	2026-04-08 10:27:19.985394+08	\N	DELIVERED	2026-04-08 18:27:18.123451+08	2026-04-08 18:27:19.984235+08	2026-04-08 10:27:19.985394+08	f
58	131	51	2026-04-08 10:28:56.597856+08	\N	DELIVERED	2026-04-08 18:28:54.453222+08	2026-04-08 18:28:56.594823+08	2026-04-08 10:28:56.597856+08	f
59	146	51	2026-04-09 12:58:19.730607+08	\N	DELIVERED	2026-04-09 20:58:09.06944+08	2026-04-09 20:58:19.728195+08	2026-04-09 12:58:19.730607+08	f
61	162	51	2026-04-11 07:54:06.42972+08	\N	DELIVERED	2026-04-11 15:53:52.734628+08	2026-04-11 15:54:06.42678+08	2026-04-11 07:54:06.42972+08	f
60	163	51	2026-04-11 08:14:04.575607+08	\N	DELIVERED	2026-04-11 15:53:39.770743+08	2026-04-11 16:14:04.572131+08	2026-04-11 08:14:04.575607+08	f
52	120	51	2026-04-11 08:14:05.817156+08	2026-04-07 21:59:57.837557+08	DELIVERED	2026-04-07 21:33:53.84652+08	2026-04-11 16:14:05.815488+08	2026-04-11 08:14:05.817156+08	f
62	167	51	\N	\N	ASSIGNED	2026-04-11 16:16:11.141482+08	2026-04-11 16:16:11.141482+08	\N	f
63	169	51	2026-04-11 08:19:19.999624+08	\N	DELIVERED	2026-04-11 16:19:17.399489+08	2026-04-11 16:19:19.997727+08	2026-04-11 08:19:19.999624+08	f
\.


--
-- TOC entry 6214 (class 0 OID 131074)
-- Dependencies: 268
-- Data for Name: delivery_areas; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.delivery_areas (id, name, description, created_at, updated_at) FROM stdin;
1	城东区域	城市东部区域	2026-04-06 09:00:12.133479+08	2026-04-06 09:00:12.133479+08
2	城西区域	城市西部区域	2026-04-06 09:00:12.133479+08	2026-04-06 09:00:12.133479+08
3	城南区域	城市南部区域	2026-04-06 09:00:12.133479+08	2026-04-06 09:00:12.133479+08
4	城北区域	城市北部区域	2026-04-06 09:00:12.133479+08	2026-04-06 09:00:12.133479+08
\.


--
-- TOC entry 6183 (class 0 OID 79457)
-- Dependencies: 237
-- Data for Name: elder_member_relations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.elder_member_relations (id, elder_id, member_id, relationship, is_primary, created_at, updated_at) FROM stdin;
3	35	44	parent	f	2026-04-02 10:53:23.073399+08	2026-04-02 10:53:23.073399+08
4	37	44	parent	f	2026-04-02 12:27:41.037702+08	2026-04-02 12:27:41.037702+08
7	36	44	亲戚	f	2026-04-07 16:07:52.698723+08	2026-04-07 16:07:52.698723+08
8	76	44	其他	f	2026-04-07 18:52:55.266049+08	2026-04-07 18:52:55.266049+08
5	38	39	parent	f	2026-04-02 12:31:41.925771+08	2026-04-11 20:34:33.2223+08
9	38	44	亲戚	t	2026-04-09 21:28:21.647921+08	2026-04-11 20:34:33.2223+08
10	33	39	other	f	2026-04-11 10:08:33.070012+08	2026-04-11 20:35:34.938316+08
6	33	44	parent	t	2026-04-04 14:19:49.560705+08	2026-04-11 20:35:34.938316+08
\.


--
-- TOC entry 6171 (class 0 OID 79304)
-- Dependencies: 225
-- Data for Name: elderly_profiles; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.elderly_profiles (user_id, name, phone, address, dietary_preferences, location, age, gender, created_at, updated_at, community_id, health_tag_id, avatar) FROM stdin;
76	孙大爷	19635687856	3楼		\N	80	男	2026-04-07 18:43:04.076775+08	2026-04-07 19:07:17.845201+08	2	\N	http://localhost:7678/static/uploads/avatars/437efe8e-0ead-4c15-a2ec-c37c1472593f.jpg
38	刘大爷	13800138005	2号楼2单元302室	{"tastes": ["light", "low_oil"], "allergies": ["nuts", "wheat"], "special_needs": "23123"}	0101000020E6100000680586AC6E195D40473D44A33BF44340	72	男	2026-04-01 12:02:32.453091+08	2026-04-09 22:56:45.960413+08	1	6	\N
33	elderly0001	13783898556	6号楼2单元505室	{"tastes": ["light", "sour"], "allergies": ["seafood", "egg"], "special_needs": "test"}	0101000020E6100000A298BC0166995C4034BBEEAD48744040	99	male	2026-04-01 11:41:53.084914+08	2026-04-09 22:57:27.698937+08	1	\N	http://localhost:7678/static/uploads/avatars/2872d155-a110-4ef8-ae9e-0a9b88f79a2e.jpg
34	张大爷	13800138001	3号楼2单元501室	低糖、低盐	0101000020E6100000103CBEBD6B195D400588821953F44340	78	男	2026-04-01 12:02:32.453091+08	2026-04-03 23:37:10.20693+08	1	2	\N
35	李奶奶	13800138002	5号楼1单元302室	无糖、清淡	0101000020E6100000CDCAF6216F195D40DBC01DA853F44340	82	女	2026-04-01 12:02:32.453091+08	2026-04-03 23:37:33.619098+08	1	4	\N
36	王大爷	13800138003	2号楼3单元401室	软烂、易消化	0101000020E61000008C0FB3976D195D40D17AF83251F44340	85	男	2026-04-01 12:02:32.453091+08	2026-04-03 23:37:33.628721+08	1	3	\N
37	赵奶奶	13800138004	8号楼2单元303室	低盐、低脂	0101000020E61000009E279EB305865C4096986725AD124040	76	女	2026-04-01 12:02:32.453091+08	2026-04-05 14:12:00.168813+08	1	5	\N
51	微信用户oMv1	\N	\N	\N	\N	\N	\N	2026-04-05 22:34:19.105616+08	2026-04-05 22:34:19.105616+08	\N	\N	\N
\.


--
-- TOC entry 6195 (class 0 OID 79614)
-- Dependencies: 249
-- Data for Name: emergency_calls; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.emergency_calls (id, elderly_id, emergency_type, message, response_status, response_time, created_at) FROM stdin;
1	33	family_call	向王大明发起电话求助	pending	\N	2026-04-04 12:33:56.450206+08
2	33	family_call	向王大明发起电话求助	pending	\N	2026-04-04 12:35:51.359017+08
3	33	family_sms	向王大明发送求助短信	pending	\N	2026-04-04 12:35:56.021505+08
4	33	family_sms	向王大明发送求助短信	pending	\N	2026-04-04 12:36:00.603075+08
5	33	police	拨打110	pending	\N	2026-04-04 12:36:22.65049+08
6	33	family_call	向小王发起电话求助	pending	\N	2026-04-04 12:39:39.981523+08
7	33	family_sms	向小王发送求助短信	pending	\N	2026-04-04 12:39:42.393258+08
8	33	in-wechat-app	向张小明发送消息：test	pending	\N	2026-04-04 13:43:01.835885+08
9	33	in-wechat-app	向张小明发送消息求助	pending	\N	2026-04-04 13:43:01.875498+08
10	33	family_call	向小王发起电话求助	pending	\N	2026-04-04 14:21:52.29276+08
11	33	in-wechat-app	向小王发送消息：test	pending	\N	2026-04-04 14:23:51.371137+08
12	33	in-wechat-app	向小王发送消息求助	pending	\N	2026-04-04 14:23:51.412929+08
13	33	in-wechat-app	向小王发送消息：我饿了，想吃饭	pending	\N	2026-04-04 14:31:42.713464+08
14	33	in-wechat-app	向小王发送消息求助	pending	\N	2026-04-04 14:31:42.74538+08
15	33	in-wechat-app	向小王发送消息：我不舒服，需要帮助	pending	\N	2026-04-04 14:34:21.433377+08
16	33	in-wechat-app	向小王发送消息求助	pending	\N	2026-04-04 14:34:21.464406+08
17	33	in-wechat-app	向小王发送消息：我想你了，有空来看我	pending	\N	2026-04-04 14:45:34.583038+08
18	33	in-wechat-app	向小王发送消息求助	pending	\N	2026-04-04 14:45:34.626288+08
19	33	in-wechat-app	向小王发送消息：我饿了，想吃饭	pending	\N	2026-04-04 14:46:22.475612+08
20	33	in-wechat-app	向小王发送消息求助	pending	\N	2026-04-04 14:46:22.502713+08
21	33	in-wechat-app	向小王发送消息：我想你了，有空来看我	pending	\N	2026-04-04 14:46:31.506211+08
22	33	in-wechat-app	向小王发送消息求助	pending	\N	2026-04-04 14:46:31.537901+08
23	35	in-wechat-app	向小王发送消息：我饿了，想吃饭	pending	\N	2026-04-04 14:47:30.536655+08
24	35	in-wechat-app	向小王发送消息求助	pending	\N	2026-04-04 14:47:30.578749+08
25	33	in-wechat-app	向小王发送消息：我累了	pending	\N	2026-04-04 15:00:51.320811+08
26	33	in-wechat-app	向小王发送消息求助	pending	\N	2026-04-04 15:00:51.361597+08
27	33	in-wechat-app	向小王发送消息：1111	pending	\N	2026-04-04 15:06:07.720721+08
28	33	family_call	向小王发起电话求助	pending	\N	2026-04-07 15:07:47.764665+08
29	33	family_sms	向小王发送求助短信	pending	\N	2026-04-07 15:07:53.217404+08
30	33	family_sms	向小王发送求助短信	pending	\N	2026-04-07 15:07:56.388419+08
31	33	family_call	向小王发起电话求助	pending	\N	2026-04-09 21:38:20.209578+08
32	33	family_sms	向小王发送求助短信	pending	\N	2026-04-09 21:38:24.78951+08
33	33	family_sms	向小王发送求助短信	pending	\N	2026-04-09 21:38:27.704162+08
34	33	in-wechat-app	向小王发送消息：请输入消息内容	pending	\N	2026-04-09 21:38:55.945038+08
\.


--
-- TOC entry 6200 (class 0 OID 79754)
-- Dependencies: 254
-- Data for Name: exceptions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.exceptions (id, delivery_id, type, description, created_at) FROM stdin;
1	6	address_error	test	2026-04-04 15:46:49.930519+08
2	6	elderly_not_home	test	2026-04-04 15:51:17.690047+08
3	6	elderly_not_home	1111	2026-04-04 16:14:53.775537+08
4	6	elderly_not_home	ads	2026-04-04 16:59:28.662197+08
5	6	elderly_not_home	管理员，来帮帮忙！！	2026-04-04 17:25:52.837968+08
\.


--
-- TOC entry 6216 (class 0 OID 155674)
-- Dependencies: 270
-- Data for Name: favorites; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.favorites (id, user_id, user_type, meal_id, created_at) FROM stdin;
1	33	elderly	10	2026-04-04 10:27:35.578147+08
2	44	member	10	2026-04-04 22:09:03.673334+08
3	44	member	12	2026-04-04 22:17:39.298914+08
4	44	member	9	2026-04-04 22:18:16.186067+08
5	44	member	11	2026-04-04 22:18:18.621527+08
7	44	member	13	2026-04-06 16:24:36.907442+08
8	33	elderly	12	2026-04-12 09:27:41.932629+08
9	34	elderly	9	2026-04-12 09:28:20.062+08
11	44	member	15	2026-04-12 09:30:27.04544+08
12	44	member	17	2026-04-12 09:30:28.094067+08
13	44	member	18	2026-04-12 09:30:30.742255+08
\.


--
-- TOC entry 6193 (class 0 OID 79576)
-- Dependencies: 247
-- Data for Name: health_records; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.health_records (id, elderly_id, height, weight, blood_pressure, blood_sugar, allergies, medications, doctor_advice, recorded_at, created_by) FROM stdin;
5	33	185.00	80.00	80	20.00	无	test	test	2026-04-03 22:28:01.466809+08	33
6	35	150.00	60.00	145/92	7.20	青霉素过敏	硝苯地平缓释片、二甲双胍', '按时服药，监测血压血糖，控制主食摄入	按时服药，监测血压血糖，控制主食摄入	2026-04-05 10:41:39.25541+08	35
7	33	\N	1.00	1	1.00	1	1	1	2026-04-05 17:42:08.614131+08	33
8	33	2.00	2.00	2	2.00	2	2	2	2026-04-03 17:46:48.066+08	33
9	38	\N	22.00	22/22	22.00	\N	\N	体温: 22.0°C\n心率: 22次/分钟\n备注: 22\n健康标签: hypertension	2026-04-09 22:48:32.651514+08	44
10	38	\N	1.00	1/1	1.00	\N	\N	体温: 1.0°C\n心率: 1次/分钟\n备注: 1\n健康标签: hypertension	2026-04-09 22:56:19.888391+08	44
\.


--
-- TOC entry 6210 (class 0 OID 114690)
-- Dependencies: 264
-- Data for Name: health_reminders; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.health_reminders (id, sender_id, receiver_id, reminder_type, content, status, scheduled_time, sent_time, read_time, created_at, updated_at) FROM stdin;
1	44	33	diet	test	read	2026-04-04 15:30:00	\N	2026-04-04 15:35:24.652168	2026-04-04 15:31:05.967687+08	2026-04-04 15:35:24.650265+08
2	44	33	checkup	下周去体检	pending	2026-04-05 17:53:00	\N	\N	2026-04-05 17:54:13.878236+08	2026-04-05 17:54:13.878236+08
3	44	33	health	test	read	2026-04-05 17:55:00	\N	2026-04-05 17:56:33.057097	2026-04-05 17:56:05.035996+08	2026-04-05 17:56:33.05533+08
\.


--
-- TOC entry 6208 (class 0 OID 106556)
-- Dependencies: 262
-- Data for Name: health_tags; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.health_tags (id, name, description, color, created_at) FROM stdin;
1	良好	健康状况正常	#67C23A	2026-04-03 22:42:27.763833+08
2	需关注	需要特别关注的健康状况	#E6A23C	2026-04-03 22:42:27.763833+08
3	高血压	高血压患者	#F56C6C	2026-04-03 22:42:27.763833+08
4	糖尿病	糖尿病患者	#909399	2026-04-03 22:42:27.763833+08
5	心脏病	心脏病患者	#409EFF	2026-04-03 22:42:27.763833+08
6	独居	独居老人	#67C23A	2026-04-03 22:42:27.763833+08
7	视力障碍	视力有障碍的老人	#E6A23C	2026-04-03 22:42:27.763833+08
8	听力障碍	听力有障碍的老人	#F56C6C	2026-04-03 22:42:27.763833+08
\.


--
-- TOC entry 6175 (class 0 OID 79358)
-- Dependencies: 229
-- Data for Name: meals; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.meals (id, name, price, description, special_tag, image_url, status, created_at, updated_at, category_id, tag_id) FROM stdin;
12	清蒸鱼	38.00	新鲜清蒸鱼，营养丰富	高蛋白	https://ts2.tc.mm.bing.net/th/id/OIP-C.x5hMn0tZRn9B06iRhfr2pgHaEJ?rs=1&pid=ImgDetMain&o=7&rm=3	available	2026-03-31 20:40:06.040883+08	2026-04-05 23:12:20.118065+08	6	11
10	蔬菜沙拉	18.00	新鲜蔬菜沙拉，健康低脂	素食	https://bpic.588ku.com/back_origin_min_pic/23/06/01/af0222972cbdf9878ba02146edd795ce.jpg!/fw/750/quality/99/unsharp/true/compress/true	available	2026-03-31 20:40:06.040883+08	2026-04-05 23:17:17.523149+08	5	9
15	宫保鸡丁	10.00	好吃极了	高蛋白,营养	https://materials.cdn.bcebos.com/images/60200061/57f231070d1608e83b39254db6276693.jpeg	available	2026-04-02 14:44:48.031908+08	2026-04-02 14:44:48.031908+08	4	11
17	手工饺子	10.00	好吃	高蛋白,易消化	https://img95.699pic.com/photo/60022/2752.jpg_wh860.jpg	available	2026-04-05 18:04:42.994207+08	2026-04-05 18:04:42.994207+08	4	11
9	营养套餐B	28.00	营养均衡的套餐，包含主食、蔬菜和蛋白质	\N	https://ts4.tc.mm.bing.net/th/id/OIP-C.ig0CXZT7L2flJG8jpnbSEAHaJ8?rs=1&pid=ImgDetMain&o=7&rm=3	available	2026-03-31 20:40:06.040883+08	2026-04-05 23:53:46.058414+08	4	11
11	小米粥	8.00	养胃小米粥	\N	https://ts3.tc.mm.bing.net/th/id/OIP-C.v7FwgJn9ZXxfZr0QVGYL8gHaE8?rs=1&pid=ImgDetMain&o=7&rm=3	available	2026-03-31 20:40:06.040883+08	2026-04-05 23:53:55.400611+08	10	13
13	鸡蛋羹	12.00	嫩滑鸡蛋羹	易消化	https://ts3.tc.mm.bing.net/th/id/OIP-C.muQJ9rYzQSe2tjf6raZo-gHaF7?rs=1&pid=ImgDetMain&o=7&rm=3	available	2026-03-31 20:40:06.040883+08	2026-04-06 15:55:42.488778+08	7	12
18	酱板鸭	10.00	好吃	高蛋白,营养	https://pic1.zhimg.com/v2-b01e6837638e0232531332901aeb8f70_b.jpg	available	2026-04-11 11:03:23.390198+08	2026-04-11 11:03:23.390198+08	4	11
\.


--
-- TOC entry 6172 (class 0 OID 79322)
-- Dependencies: 226
-- Data for Name: member_profiles; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.member_profiles (user_id, name, phone, created_at, updated_at, avatar) FROM stdin;
39	张小明	13800138006	2026-04-01 12:02:32.453091+08	2026-04-01 12:02:32.453091+08	\N
40	李小红	13800138007	2026-04-01 12:02:32.453091+08	2026-04-01 12:02:32.453091+08	\N
41	王大明	13800138008	2026-04-01 12:02:32.453091+08	2026-04-01 12:02:32.453091+08	\N
44	小王	17838556638	2026-04-02 10:01:51.668261+08	2026-04-06 17:16:10.184563+08	http://localhost:7678/static/uploads/avatars/7e092f52-537b-4c56-a793-835da2f8d31b.jpg
\.


--
-- TOC entry 6179 (class 0 OID 79394)
-- Dependencies: 233
-- Data for Name: order_items; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.order_items (id, order_id, meal_id, quantity, unit_price, subtotal, created_at) FROM stdin;
29	32	9	1	28.00	28.00	2026-04-01 12:25:15.179315+08
30	33	12	1	38.00	38.00	2026-04-01 12:25:27.672541+08
31	34	11	1	8.00	8.00	2026-04-01 12:25:29.147678+08
32	35	10	1	18.00	18.00	2026-04-01 20:04:07.894435+08
33	36	13	1	12.00	12.00	2026-04-01 20:04:44.351558+08
34	38	10	1	18.00	18.00	2026-04-02 22:19:16.850777+08
35	39	10	1	18.00	18.00	2026-04-02 22:53:10.516208+08
68	72	12	1	38.00	38.00	2026-04-03 08:14:21.805288+08
69	73	13	1	12.00	12.00	2026-04-03 08:29:31.374051+08
70	74	15	1	10.00	10.00	2026-04-03 08:31:55.856211+08
71	75	10	1	18.00	18.00	2026-04-03 08:33:11.308754+08
72	76	10	1	18.00	18.00	2026-04-03 08:35:29.491413+08
73	77	10	1	18.00	18.00	2026-04-03 08:37:51.736097+08
74	78	10	1	18.00	18.00	2026-04-03 08:43:12.656015+08
75	79	13	1	12.00	12.00	2026-04-03 15:18:52.4673+08
76	80	10	1	18.00	18.00	2026-04-03 23:41:25.557947+08
77	81	13	1	12.00	12.00	2026-04-03 23:43:35.75695+08
78	82	12	1	38.00	38.00	2026-04-04 17:27:03.775196+08
79	83	13	1	12.00	12.00	2026-04-04 18:56:35.71936+08
80	84	13	1	12.00	12.00	2026-04-05 14:13:11.403457+08
81	85	13	1	12.00	12.00	2026-04-05 16:14:52.912687+08
82	86	10	1	18.00	18.00	2026-04-05 17:11:08.058086+08
84	88	12	1	38.00	38.00	2026-04-06 09:38:21.355572+08
85	89	12	1	38.00	38.00	2026-04-06 09:39:29.564544+08
86	90	12	1	38.00	38.00	2026-04-06 09:41:13.917721+08
87	91	10	1	18.00	18.00	2026-04-06 09:59:08.108704+08
88	92	12	1	38.00	38.00	2026-04-06 10:02:06.352937+08
89	93	12	1	38.00	38.00	2026-04-06 10:05:29.709148+08
90	94	12	1	38.00	38.00	2026-04-06 10:07:44.093898+08
91	95	12	1	38.00	38.00	2026-04-06 10:10:19.905303+08
92	96	12	1	38.00	38.00	2026-04-06 10:14:32.675181+08
93	97	17	1	10.00	10.00	2026-04-06 10:17:09.206281+08
94	98	12	1	38.00	38.00	2026-04-06 10:21:17.976618+08
95	99	17	1	10.00	10.00	2026-04-06 10:26:14.123481+08
96	100	10	1	18.00	18.00	2026-04-06 10:27:20.037917+08
97	101	12	1	38.00	38.00	2026-04-06 10:29:40.738626+08
98	102	12	1	38.00	38.00	2026-04-06 10:31:14.685911+08
99	103	12	1	38.00	38.00	2026-04-06 10:34:28.911124+08
100	104	12	1	38.00	38.00	2026-04-06 10:36:47.311163+08
101	105	12	1	38.00	38.00	2026-04-06 10:46:26.944197+08
102	106	15	1	10.00	10.00	2026-04-06 11:35:50.81318+08
103	107	12	1	38.00	38.00	2026-04-06 12:36:46.260902+08
104	108	12	1	38.00	38.00	2026-04-06 15:10:38.287376+08
105	109	12	1	38.00	38.00	2026-04-06 15:39:30.04506+08
106	110	10	1	18.00	18.00	2026-04-06 15:40:45.901735+08
107	111	13	1	12.00	12.00	2026-04-06 18:07:20.961391+08
108	112	13	1	12.00	12.00	2026-04-07 12:38:38.930127+08
109	113	12	1	38.00	38.00	2026-04-07 13:28:38.820085+08
110	114	12	1	38.00	38.00	2026-04-07 16:13:10.886774+08
111	115	12	1	38.00	38.00	2026-04-07 16:14:07.632535+08
112	116	12	2	38.00	76.00	2026-04-07 16:14:33.713124+08
113	117	10	1	18.00	18.00	2026-04-07 16:16:52.718795+08
114	118	10	1	18.00	18.00	2026-04-07 16:17:08.976556+08
115	119	17	1	10.00	10.00	2026-04-07 19:21:59.904824+08
116	120	12	1	38.00	38.00	2026-04-07 21:29:57.837557+08
117	121	12	1	38.00	38.00	2026-04-08 17:45:49.359779+08
118	122	12	1	38.00	38.00	2026-04-08 18:02:04.580455+08
119	123	12	1	38.00	38.00	2026-04-08 18:02:25.512232+08
120	124	12	1	38.00	38.00	2026-04-08 18:02:50.043124+08
121	125	12	1	38.00	38.00	2026-04-08 18:03:16.490438+08
122	126	12	1	38.00	38.00	2026-04-08 18:03:36.264477+08
123	127	12	1	38.00	38.00	2026-04-08 18:20:04.397924+08
124	128	10	1	18.00	18.00	2026-04-08 18:22:29.798207+08
125	129	11	1	8.00	8.00	2026-04-08 18:23:42.530648+08
126	130	12	1	38.00	38.00	2026-04-08 18:27:10.365402+08
127	131	17	1	10.00	10.00	2026-04-08 18:28:46.662002+08
128	132	12	1	38.00	38.00	2026-04-08 19:39:18.478436+08
129	133	12	1	38.00	38.00	2026-04-09 11:04:34.212081+08
130	135	12	1	38.00	38.00	2026-04-09 11:37:49.494979+08
131	136	11	1	8.00	8.00	2026-04-09 11:45:33.743772+08
132	137	12	1	38.00	38.00	2026-04-09 11:48:57.006013+08
133	138	12	1	38.00	38.00	2026-04-09 11:49:28.257445+08
134	139	12	1	38.00	38.00	2026-04-09 11:54:26.518344+08
135	140	12	1	38.00	38.00	2026-04-09 12:03:10.856528+08
136	141	12	1	38.00	38.00	2026-04-09 12:06:07.893675+08
137	142	9	1	28.00	28.00	2026-04-09 12:09:38.061236+08
138	143	12	1	38.00	38.00	2026-04-09 12:11:08.915341+08
139	144	11	1	8.00	8.00	2026-04-09 12:13:32.579697+08
140	145	12	1	38.00	38.00	2026-04-09 12:16:21.896911+08
141	146	12	1	38.00	38.00	2026-04-09 12:17:09.002909+08
142	147	12	1	38.00	38.00	2026-04-09 13:02:25.093932+08
143	148	12	1	38.00	38.00	2026-04-09 13:17:18.86319+08
144	149	12	1	38.00	38.00	2026-04-09 13:18:02.312425+08
145	150	12	2	38.00	76.00	2026-04-11 12:07:53.252312+08
146	151	18	2	10.00	20.00	2026-04-11 12:12:35.919294+08
147	152	10	1	18.00	18.00	2026-04-11 12:20:57.03654+08
148	152	12	1	38.00	38.00	2026-04-11 12:20:57.03654+08
149	153	10	1	18.00	18.00	2026-04-11 12:22:03.79111+08
150	153	12	1	38.00	38.00	2026-04-11 12:22:03.79111+08
151	153	15	1	10.00	10.00	2026-04-11 12:22:03.79111+08
152	154	15	1	10.00	10.00	2026-04-11 14:02:28.624308+08
153	155	13	1	12.00	12.00	2026-04-11 14:04:33.65089+08
154	155	18	1	10.00	10.00	2026-04-11 14:04:33.65089+08
155	156	13	1	12.00	12.00	2026-04-11 14:13:00.751561+08
156	156	15	1	10.00	10.00	2026-04-11 14:13:00.751561+08
157	157	9	1	28.00	28.00	2026-04-11 14:14:32.481142+08
158	157	11	1	8.00	8.00	2026-04-11 14:14:32.481142+08
159	158	9	1	28.00	28.00	2026-04-11 14:15:48.497729+08
160	158	11	1	8.00	8.00	2026-04-11 14:15:48.497729+08
161	159	15	1	10.00	10.00	2026-04-11 14:20:39.360933+08
162	161	10	1	18.00	18.00	2026-04-11 15:41:39.576903+08
163	161	12	1	38.00	38.00	2026-04-11 15:41:39.576903+08
164	162	10	1	18.00	18.00	2026-04-11 15:45:10.965885+08
165	162	12	1	38.00	38.00	2026-04-11 15:45:10.965885+08
166	163	12	2	38.00	76.00	2026-04-11 15:47:12.962605+08
167	164	11	1	8.00	8.00	2026-04-11 15:54:50.055591+08
168	164	17	1	10.00	10.00	2026-04-11 15:54:50.055591+08
169	165	11	1	8.00	8.00	2026-04-11 16:04:02.404417+08
170	165	17	1	10.00	10.00	2026-04-11 16:04:02.404417+08
171	166	11	1	8.00	8.00	2026-04-11 16:06:00.749896+08
172	166	17	1	10.00	10.00	2026-04-11 16:06:00.749896+08
173	167	15	1	10.00	10.00	2026-04-11 16:13:38.613652+08
174	167	17	1	10.00	10.00	2026-04-11 16:13:38.613652+08
175	168	11	1	8.00	8.00	2026-04-11 16:16:55.426701+08
176	168	17	1	10.00	10.00	2026-04-11 16:16:55.426701+08
177	169	11	1	8.00	8.00	2026-04-11 16:17:26.098059+08
178	169	17	1	10.00	10.00	2026-04-11 16:17:26.098059+08
\.


--
-- TOC entry 6177 (class 0 OID 79373)
-- Dependencies: 231
-- Data for Name: orders; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.orders (id, elderly_id, total_amount, payment_method, payment_status, status, delivery_address, notes, created_at, updated_at, scheduled_time, order_type) FROM stdin;
99	33	10.00	微信支付	paid	completed	幸福小区3号楼2单元501室		2026-04-06 10:26:14.123481+08	2026-04-06 10:27:51.381313+08	\N	immediate
101	33	38.00	微信支付	paid	completed	幸福小区3号楼2单元501室		2026-04-06 10:29:40.738626+08	2026-04-06 10:29:50.482698+08	\N	immediate
102	33	38.00	微信支付	paid	completed	幸福小区3号楼2单元501室		2026-04-06 10:31:14.685911+08	2026-04-06 10:31:53.292158+08	\N	immediate
103	33	38.00	微信支付	paid	completed	幸福小区3号楼2单元501室		2026-04-06 10:34:28.911124+08	2026-04-06 10:34:44.47105+08	\N	immediate
34	37	8.00	\N	paid	completed	幸福小区3号楼2单元501室		2026-04-02 12:25:29.147+08	2026-04-02 16:38:03.433962+08	\N	immediate
104	33	38.00	微信支付	paid	completed	幸福小区3号楼2单元501室		2026-04-06 10:36:47.311163+08	2026-04-06 10:37:39.188436+08	\N	immediate
100	33	18.00	微信支付	paid	completed	幸福小区3号楼2单元501室		2026-04-06 10:27:20.037917+08	2026-04-06 10:41:13.69989+08	\N	immediate
33	33	38.00	\N	paid	completed	幸福小区3号楼2单元501室		2026-04-02 12:25:27.672+08	2026-04-02 17:23:23.309141+08	\N	immediate
105	33	38.00	微信支付	paid	completed	幸福小区3号楼2单元501室		2026-04-06 10:46:26.944197+08	2026-04-06 10:46:37.188212+08	\N	immediate
106	33	10.00	\N	\N	completed	6号楼2单元505室		2026-04-06 11:35:50.81318+08	2026-04-06 11:37:12.711738+08	\N	immediate
107	33	38.00	微信支付	paid	completed	幸福小区3号楼2单元501室		2026-04-06 12:36:46.260902+08	2026-04-06 12:37:27.296927+08	\N	immediate
35	33	18.00	微信支付	paid	completed	test	test	2026-04-02 20:04:07.894+08	2026-04-02 22:05:01.709113+08	\N	immediate
36	38	12.00	\N	pending	completed	幸福小区2号楼2单元302室	test	2026-04-02 20:04:44.351+08	2026-04-02 22:11:21.496551+08	\N	immediate
108	33	38.00	微信支付	paid	completed	幸福小区3号楼2单元501室		2026-04-06 15:10:38.287376+08	2026-04-06 15:10:54.055726+08	\N	immediate
109	33	38.00	微信支付	paid	completed	幸福小区3号楼2单元501室		2026-04-06 15:39:30.04506+08	2026-04-06 15:39:57.240098+08	\N	immediate
37	33	18.00		paid	completed	test	test	2026-04-02 20:04:07.894+08	2026-04-02 22:14:27.714442+08	\N	immediate
38	33	18.00	微信支付	paid	completed	幸福小区3号楼2单元501室		2026-04-02 22:19:16.850777+08	2026-04-02 22:22:14.921519+08	\N	immediate
112	33	12.00	微信支付	paid	completed	幸福小区3号楼2单元501室		2026-04-07 12:38:38.930127+08	2026-04-07 12:39:06.130373+08	\N	immediate
72	33	38.00	微信支付	paid	completed	幸福小区3号楼2单元501室		2026-04-03 08:14:21.805288+08	2026-04-03 08:19:29.071581+08	\N	immediate
111	33	12.00	微信支付	paid	completed	幸福小区3号楼2单元501室		2026-04-06 18:07:20.961391+08	2026-04-07 12:46:29.232034+08	\N	immediate
110	33	18.00	微信支付	paid	completed	幸福小区3号楼2单元501室		2026-04-06 15:40:45.901735+08	2026-04-07 12:46:49.140812+08	\N	immediate
77	37	18.00	微信支付	paid	completed	8号楼2单元303室		2026-04-03 08:37:51.736097+08	2026-04-03 08:57:59.291785+08	\N	immediate
113	33	38.00	\N	\N	delivering	6号楼2单元505室		2026-04-07 13:28:38.820085+08	2026-04-07 13:29:24.710293+08	\N	immediate
114	36	38.00	微信支付	paid	pending_accept	幸福小区3号楼2单元501室		2026-04-07 16:13:10.886774+08	2026-04-07 16:13:14.678935+08	\N	immediate
32	33	28.00	\N	pending	completed	幸福小区3号楼2单元501室		2026-04-02 12:25:15.179+08	2026-04-03 15:18:36.604611+08	\N	immediate
116	36	76.00	\N	\N	pending_accept	2号楼3单元401室		2026-04-07 16:14:33.713124+08	2026-04-07 16:14:51.319595+08	\N	immediate
115	36	38.00	\N	\N	pending_accept	2号楼3单元401室		2026-04-07 16:14:07.632535+08	2026-04-07 16:14:53.764905+08	\N	immediate
79	35	12.00	\N	\N	completed	5号楼1单元302室		2026-04-03 15:18:52.4673+08	2026-04-03 15:21:48.69949+08	\N	immediate
117	36	18.00	\N	\N	pending_payment	2号楼3单元401室		2026-04-07 16:16:52.718795+08	2026-04-07 16:16:52.718795+08	\N	immediate
118	36	18.00	\N	\N	pending_payment	2号楼3单元401室		2026-04-07 16:17:08.976556+08	2026-04-07 16:17:08.976556+08	\N	immediate
80	33	18.00	微信支付	paid	completed	幸福小区3号楼2单元501室		2026-04-03 23:41:25.557947+08	2026-04-03 23:42:21.417141+08	\N	immediate
119	36	10.00	cash	paid	delivering	2号楼3单元401室	test	2026-04-07 19:21:59.904824+08	2026-04-07 19:53:50.155637+08	\N	immediate
82	33	38.00	微信支付	paid	completed	幸福小区3号楼2单元501室		2026-04-04 17:27:03.775196+08	2026-04-04 17:27:27.497788+08	\N	immediate
121	33	38.00	\N	\N	cancelled	幸福小区3号楼2单元501室		2026-04-08 17:45:49.359779+08	2026-04-08 17:45:56.53996+08	\N	immediate
122	76	38.00	\N	\N	pending_payment	3楼		2026-04-08 18:02:04.580455+08	2026-04-08 18:02:04.580455+08	\N	immediate
123	76	38.00	\N	\N	pending_payment	3楼		2026-04-08 18:02:25.512232+08	2026-04-08 18:02:25.512232+08	\N	immediate
39	33	18.00	微信支付	paid	completed	幸福小区3号楼2单元501室		2026-04-02 22:53:10.516208+08	2026-04-04 18:46:50.9742+08	\N	immediate
124	76	38.00	\N	\N	pending_payment	3楼		2026-04-08 18:02:50.043124+08	2026-04-08 18:02:50.043124+08	\N	immediate
125	76	38.00	\N	\N	pending_payment	3楼		2026-04-08 18:03:16.490438+08	2026-04-08 18:03:16.490438+08	\N	immediate
83	33	12.00	微信支付	paid	delivering	幸福小区3号楼2单元501室		2026-04-04 18:56:35.71936+08	2026-04-04 18:57:19.983813+08	\N	immediate
81	37	12.00	\N	\N	completed	8号楼2单元303室		2026-04-03 23:43:35.75695+08	2026-04-04 21:45:09.177157+08	\N	immediate
126	33	38.00	\N	\N	completed	6号楼2单元505室		2026-04-08 18:03:36.264477+08	2026-04-08 18:08:29.447876+08	\N	immediate
85	33	12.00	微信支付	paid	completed	幸福小区3号楼2单元501室		2026-04-05 16:14:52.912687+08	2026-04-05 16:15:12.029206+08	\N	immediate
127	76	38.00	\N	\N	completed	3楼		2026-04-08 18:20:04.397924+08	2026-04-08 18:20:21.120775+08	\N	immediate
86	33	18.00	微信支付	paid	completed	幸福小区3号楼2单元501室		2026-04-05 17:11:08.058086+08	2026-04-05 17:11:57.965008+08	\N	immediate
128	76	18.00	\N	\N	completed	3楼		2026-04-08 18:22:29.798207+08	2026-04-08 18:22:43.104855+08	\N	immediate
75	37	18.00	微信支付	paid	completed	8号楼2单元303室		2026-04-03 08:33:11.308754+08	2026-04-06 09:08:14.999717+08	\N	immediate
74	37	10.00	微信支付	paid	completed	8号楼2单元303室		2026-04-03 08:31:55.856211+08	2026-04-06 09:16:13.048781+08	\N	immediate
84	33	12.00	微信支付	paid	completed	幸福小区3号楼2单元501室		2026-04-05 14:13:11.403457+08	2026-04-06 09:17:27.222264+08	\N	immediate
78	37	18.00	微信支付	paid	completed	8号楼2单元303室		2026-04-03 08:43:12.656015+08	2026-04-06 09:31:29.57569+08	\N	immediate
73	37	12.00	微信支付	paid	completed	8号楼2单元303室		2026-04-03 08:29:31.374051+08	2026-04-06 09:35:08.100252+08	\N	immediate
129	76	8.00	\N	\N	completed	3楼		2026-04-08 18:23:42.530648+08	2026-04-08 18:23:53.025722+08	\N	immediate
88	33	38.00	微信支付	paid	completed	幸福小区3号楼2单元501室		2026-04-06 09:38:21.355572+08	2026-04-06 09:38:48.277096+08	\N	immediate
130	76	38.00	\N	\N	completed	3楼		2026-04-08 18:27:10.365402+08	2026-04-08 18:27:19.984235+08	\N	immediate
89	33	38.00	微信支付	paid	completed	幸福小区3号楼2单元501室		2026-04-06 09:39:29.564544+08	2026-04-06 09:39:41.484893+08	\N	immediate
131	33	10.00	微信支付	paid	completed	幸福小区3号楼2单元501室		2026-04-08 18:28:46.662002+08	2026-04-08 18:28:56.594823+08	\N	immediate
90	33	38.00	微信支付	paid	completed	幸福小区3号楼2单元501室		2026-04-06 09:41:13.917721+08	2026-04-06 09:56:03.778636+08	\N	immediate
120	33	38.00	微信支付	paid	completed	幸福小区3号楼2单元501室		2026-04-07 21:29:57.837557+08	2026-04-11 16:14:05.815488+08	\N	immediate
91	33	18.00	微信支付	paid	completed	幸福小区3号楼2单元501室		2026-04-06 09:59:08.108704+08	2026-04-06 10:00:59.725031+08	\N	immediate
92	33	38.00	微信支付	paid	completed	幸福小区3号楼2单元501室		2026-04-06 10:02:06.352937+08	2026-04-06 10:02:33.257256+08	\N	immediate
93	33	38.00	微信支付	paid	completed	幸福小区3号楼2单元501室		2026-04-06 10:05:29.709148+08	2026-04-06 10:05:50.049642+08	\N	immediate
76	37	18.00	微信支付	paid	completed	8号楼2单元303室		2026-04-03 08:35:29.491413+08	2026-04-06 10:13:31.212154+08	\N	immediate
95	33	38.00	微信支付	paid	completed	幸福小区3号楼2单元501室		2026-04-06 10:10:19.905303+08	2026-04-06 10:13:44.183006+08	\N	immediate
96	33	38.00	微信支付	paid	completed	幸福小区3号楼2单元501室		2026-04-06 10:14:32.675181+08	2026-04-06 10:14:57.473845+08	\N	immediate
98	33	38.00	微信支付	paid	completed	幸福小区3号楼2单元501室		2026-04-06 10:21:17.976618+08	2026-04-06 10:21:43.035538+08	\N	immediate
97	33	10.00	微信支付	paid	completed	幸福小区3号楼2单元501室		2026-04-06 10:17:09.206281+08	2026-04-06 10:21:44.244882+08	\N	immediate
94	33	38.00	微信支付	paid	completed	幸福小区3号楼2单元501室		2026-04-06 10:07:44.093898+08	2026-04-06 10:21:45.451555+08	\N	immediate
132	33	38.00	微信支付	paid	pending_accept	幸福小区3号楼2单元501室		2026-04-08 19:39:18.478436+08	2026-04-08 19:39:21.252647+08	\N	immediate
133	33	38.00	\N	\N	pending_payment	幸福小区3号楼2单元501室		2026-04-09 11:04:34.212081+08	2026-04-09 11:04:34.212081+08	\N	immediate
137	33	38.00	微信支付	paid	pending_accept	幸福小区3号楼2单元501室		2026-04-09 11:48:57.006013+08	2026-04-09 11:53:14.259747+08	2026-04-09 11:49:00+08	scheduled
138	33	38.00	微信支付	paid	pending_accept	幸福小区3号楼2单元501室		2026-04-09 11:49:28.257445+08	2026-04-09 11:53:14.259747+08	2026-04-09 11:50:00+08	scheduled
139	33	38.00	微信支付	paid	pending_accept	幸福小区3号楼2单元501室		2026-04-09 11:54:26.518344+08	2026-04-09 11:56:14.331387+08	2026-04-09 11:56:00+08	scheduled
136	33	8.00	微信支付	paid	pending_accept	幸福小区3号楼2单元501室		2026-04-09 11:45:33.743772+08	2026-04-09 12:00:14.430788+08	2026-04-09 12:00:00+08	scheduled
142	76	28.00	\N	\N	pending_accept	3楼		2026-04-09 12:09:38.061236+08	2026-04-09 12:10:06.12274+08	2026-04-09 12:10:00+08	scheduled
141	76	38.00	\N	\N	pending_accept	3楼		2026-04-09 12:06:07.893675+08	2026-04-09 12:10:11.220268+08	\N	immediate
140	76	38.00	\N	\N	pending_accept	3楼		2026-04-09 12:03:10.856528+08	2026-04-09 12:10:12.24452+08	\N	immediate
143	36	38.00	\N	\N	pending_accept	2号楼3单元401室		2026-04-09 12:11:08.915341+08	2026-04-09 12:11:12.105659+08	2026-04-09 12:12:00+08	scheduled
144	36	8.00	\N	\N	pending_accept	2号楼3单元401室		2026-04-09 12:13:32.579697+08	2026-04-09 12:14:14.752503+08	2026-04-09 12:14:00+08	scheduled
135	33	38.00	\N	\N	cancelled	幸福小区3号楼2单元501室		2026-04-09 11:37:49.494979+08	2026-04-09 13:01:58.917855+08	2026-04-14 12:30:00+08	scheduled
147	33	38.00	微信支付	paid	pending_schedule	幸福小区3号楼2单元501室		2026-04-09 13:02:25.093932+08	2026-04-09 13:02:28.741258+08	2026-06-09 12:00:00+08	scheduled
145	76	38.00	\N	\N	cancelled	3楼		2026-04-09 12:16:21.896911+08	2026-04-09 13:16:34.537331+08	2026-06-09 12:00:00+08	scheduled
148	33	38.00	\N	\N	cancelled	幸福小区3号楼2单元501室		2026-04-09 13:17:18.86319+08	2026-04-09 13:17:43.240739+08	2026-06-09 12:00:00+08	scheduled
149	76	38.00	\N	\N	cancelled	3楼		2026-04-09 13:18:02.312425+08	2026-04-09 13:18:21.304004+08	2026-06-09 12:00:00+08	scheduled
146	76	38.00	\N	\N	completed	3楼		2026-04-09 12:17:09.002909+08	2026-04-09 20:58:19.728195+08	2026-04-09 12:18:00+08	scheduled
151	33	20.00	\N	\N	pending_payment	幸福小区3号楼2单元501室		2026-04-11 12:12:35.919294+08	2026-04-11 12:12:35.919294+08	\N	immediate
150	38	76.00	\N	\N	pending_accept	2号楼2单元302室		2026-04-11 12:07:53.252312+08	2026-04-11 12:13:34.151948+08	\N	immediate
152	38	56.00	\N	\N	pending_accept	2号楼2单元302室		2026-04-11 12:20:57.03654+08	2026-04-11 12:21:29.781453+08	\N	immediate
153	36	66.00	\N	\N	pending_payment	2号楼3单元401室		2026-04-11 12:22:03.79111+08	2026-04-11 12:22:03.79111+08	\N	immediate
154	33	10.00	微信支付	paid	pending_accept	幸福小区3号楼2单元501室		2026-04-11 14:02:28.624308+08	2026-04-11 14:02:57.01595+08	\N	immediate
155	38	22.00	\N	\N	pending_accept	2号楼2单元302室		2026-04-11 14:04:33.65089+08	2026-04-11 14:04:38.519747+08	\N	immediate
156	38	22.00	\N	\N	pending_accept	2号楼2单元302室		2026-04-11 14:13:00.751561+08	2026-04-11 14:13:21.213297+08	\N	immediate
157	38	36.00	\N	\N	cancelled	2号楼2单元302室		2026-04-11 14:14:32.481142+08	2026-04-11 14:14:53.987799+08	2026-04-11 14:15:00+08	scheduled
158	38	36.00	\N	\N	pending_accept	2号楼2单元302室		2026-04-11 14:15:48.497729+08	2026-04-11 14:27:04.582659+08	2026-04-11 14:16:00+08	scheduled
159	33	10.00	微信支付	paid	pending_accept	幸福小区3号楼2单元501室		2026-04-11 14:20:39.360933+08	2026-04-11 14:27:04.582659+08	2026-04-11 14:21:00+08	scheduled
161	38	56.00	\N	\N	pending_accept	2号楼2单元302室		2026-04-11 15:41:39.576903+08	2026-04-11 15:42:07.91283+08	2026-04-11 15:42:00+08	scheduled
162	38	56.00	\N	\N	completed	2号楼2单元302室		2026-04-11 15:45:10.965885+08	2026-04-11 15:54:06.42678+08	2026-04-11 15:46:00+08	scheduled
164	38	18.00	\N	\N	pending_accept	2号楼2单元302室		2026-04-11 15:54:50.055591+08	2026-04-11 15:55:07.923004+08	2026-04-11 15:55:00+08	scheduled
165	38	18.00	\N	\N	pending_accept	2号楼2单元302室		2026-04-11 16:04:02.404417+08	2026-04-11 16:04:07.91613+08	2026-04-11 16:04:00+08	scheduled
166	38	18.00	\N	\N	pending_accept	2号楼2单元302室		2026-04-11 16:06:00.749896+08	2026-04-11 16:06:03.292038+08	\N	immediate
163	33	76.00	微信支付	paid	completed	幸福小区3号楼2单元501室		2026-04-11 15:47:12.962605+08	2026-04-11 16:14:04.572131+08	2026-04-11 15:48:00+08	scheduled
167	38	20.00	\N	\N	delivering	2号楼2单元302室		2026-04-11 16:13:38.613652+08	2026-04-11 16:16:11.141482+08	\N	immediate
168	38	18.00	\N	\N	pending_accept	2号楼2单元302室		2026-04-11 16:16:55.426701+08	2026-04-11 16:16:56.551531+08	\N	immediate
169	38	18.00	\N	\N	completed	2号楼2单元302室		2026-04-11 16:17:26.098059+08	2026-04-11 16:19:19.997727+08	2026-04-11 16:18:00+08	scheduled
\.


--
-- TOC entry 6198 (class 0 OID 79724)
-- Dependencies: 252
-- Data for Name: payments; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.payments (id, order_id, payment_method, amount, transaction_id, status, created_at) FROM stdin;
1	33	微信支付	38	TXN000033	completed	2026-04-02 12:25:27.672+08
2	34	微信支付	8	TXN000034	completed	2026-04-02 12:25:29.147+08
5	35	微信支付	18	TXN351775122137	completed	2026-04-02 17:28:57.13805+08
6	38	微信支付	18	TXN381775139634	completed	2026-04-02 22:20:34.304109+08
7	72	微信支付	38	TXN721775175465	completed	2026-04-03 08:17:45.785566+08
8	39	微信支付	18	TXN391775198036	completed	2026-04-03 14:33:56.764592+08
9	79	微信支付	12	TXN2026040315190879	paid	2026-04-03 15:19:08.023085+08
10	80	微信支付	18	TXN801775230891	completed	2026-04-03 23:41:31.797309+08
11	81	微信支付	12	TXN2026040323433881	paid	2026-04-03 23:43:38.724606+08
12	82	微信支付	38	TXN821775294827	completed	2026-04-04 17:27:07.290813+08
13	83	微信支付	12	TXN831775300202	completed	2026-04-04 18:56:42.360751+08
14	84	微信支付	12	TXN841775369596	completed	2026-04-05 14:13:16.587073+08
15	85	微信支付	12	TXN851775376896	completed	2026-04-05 16:14:56.485027+08
16	86	微信支付	18	TXN861775380271	completed	2026-04-05 17:11:11.184315+08
18	88	微信支付	38	TXN881775439505	completed	2026-04-06 09:38:25.037403+08
19	89	微信支付	38	TXN891775439573	completed	2026-04-06 09:39:33.157086+08
20	90	微信支付	38	TXN901775439678	completed	2026-04-06 09:41:18.863467+08
21	91	微信支付	18	TXN911775440752	completed	2026-04-06 09:59:12.280271+08
22	92	微信支付	38	TXN921775440929	completed	2026-04-06 10:02:09.541781+08
23	93	微信支付	38	TXN931775441133	completed	2026-04-06 10:05:33.320873+08
24	94	微信支付	38	TXN941775441266	completed	2026-04-06 10:07:46.663864+08
25	95	微信支付	38	TXN951775441423	completed	2026-04-06 10:10:23.398181+08
26	96	微信支付	38	TXN961775441676	completed	2026-04-06 10:14:36.381018+08
27	97	微信支付	10	TXN971775441832	completed	2026-04-06 10:17:12.613149+08
28	98	微信支付	38	TXN981775442081	completed	2026-04-06 10:21:21.528041+08
29	99	微信支付	10	TXN991775442378	completed	2026-04-06 10:26:18.097602+08
30	100	微信支付	18	TXN1001775442444	completed	2026-04-06 10:27:24.756848+08
31	101	微信支付	38	TXN1011775442584	completed	2026-04-06 10:29:44.192287+08
32	102	微信支付	38	TXN1021775442677	completed	2026-04-06 10:31:17.669436+08
33	103	微信支付	38	TXN1031775442872	completed	2026-04-06 10:34:32.382314+08
34	104	微信支付	38	TXN1041775443010	completed	2026-04-06 10:36:50.489235+08
35	105	微信支付	38	TXN1051775443591	completed	2026-04-06 10:46:31.134542+08
36	106	微信支付	10	TXN20260406113553106	paid	2026-04-06 11:35:53.449827+08
37	107	微信支付	38	TXN1071775450209	completed	2026-04-06 12:36:49.832466+08
38	108	微信支付	38	TXN1081775459441	completed	2026-04-06 15:10:41.568238+08
39	109	微信支付	38	TXN1091775461174	completed	2026-04-06 15:39:34.546646+08
40	110	微信支付	18	TXN1101775461249	completed	2026-04-06 15:40:49.993772+08
41	111	微信支付	12	TXN1111775524474	completed	2026-04-07 09:14:34.013166+08
42	112	微信支付	12	TXN1121775536724	completed	2026-04-07 12:38:44.378876+08
43	113	微信支付	38	TXN20260407132840113	paid	2026-04-07 13:28:40.46089+08
44	114	微信支付	38	TXN1141775549594	completed	2026-04-07 16:13:14.678935+08
45	116	微信支付	76	TXN20260407161451116	paid	2026-04-07 16:14:51.319595+08
46	115	微信支付	38	TXN20260407161453115	paid	2026-04-07 16:14:53.764905+08
47	120	微信支付	38	TXN1201775568601	completed	2026-04-07 21:30:01.420453+08
48	126	微信支付	38	TXN20260408180348126	paid	2026-04-08 18:03:48.47376+08
49	127	微信支付	38	TXN20260408182008127	paid	2026-04-08 18:20:08.4291+08
50	128	微信支付	18	TXN20260408182232128	paid	2026-04-08 18:22:32.937018+08
51	129	微信支付	8	TXN20260408182346129	paid	2026-04-08 18:23:46.388513+08
52	130	微信支付	38	TXN20260408182712130	paid	2026-04-08 18:27:12.38196+08
53	131	微信支付	10	TXN1311775644129	completed	2026-04-08 18:28:49.75788+08
54	132	微信支付	38	TXN1321775648361	completed	2026-04-08 19:39:21.252647+08
55	136	微信支付	8	TXN1361775706337	completed	2026-04-09 11:45:37.635579+08
56	137	微信支付	38	TXN1371775706544	completed	2026-04-09 11:49:04.620214+08
57	138	微信支付	38	TXN1381775706570	completed	2026-04-09 11:49:30.990281+08
58	139	微信支付	38	TXN1391775706870	completed	2026-04-09 11:54:30.129201+08
59	142	微信支付	28	TXN20260409121006142	paid	2026-04-09 12:10:06.12274+08
60	141	微信支付	38	TXN20260409121011141	paid	2026-04-09 12:10:11.220268+08
61	140	微信支付	38	TXN20260409121012140	paid	2026-04-09 12:10:12.24452+08
62	143	微信支付	38	TXN20260409121112143	paid	2026-04-09 12:11:12.105659+08
63	144	微信支付	8	TXN20260409121335144	paid	2026-04-09 12:13:35.065204+08
64	145	微信支付	38	TXN20260409121627145	paid	2026-04-09 12:16:27.668397+08
65	146	微信支付	38	TXN20260409121711146	paid	2026-04-09 12:17:11.714461+08
66	147	微信支付	38	TXN1471775710948	completed	2026-04-09 13:02:28.741258+08
67	149	微信支付	38	TXN20260409131810149	paid	2026-04-09 13:18:10.261289+08
68	150	微信支付	76	TXN20260411121334150	paid	2026-04-11 12:13:34.151948+08
69	152	微信支付	56	TXN20260411122129152	paid	2026-04-11 12:21:29.781453+08
70	154	微信支付	10	TXN1541775887377	completed	2026-04-11 14:02:57.01595+08
71	155	微信支付	22	TXN20260411140438155	paid	2026-04-11 14:04:38.519747+08
72	156	微信支付	22	TXN20260411141321156	paid	2026-04-11 14:13:21.213297+08
73	157	微信支付	36	TXN20260411141437157	paid	2026-04-11 14:14:37.565753+08
74	158	微信支付	36	TXN20260411141549158	paid	2026-04-11 14:15:49.849159+08
75	159	微信支付	10	TXN1591775888449	completed	2026-04-11 14:20:49.714632+08
76	161	微信支付	56	TXN20260411154146161	paid	2026-04-11 15:41:46.435428+08
77	162	微信支付	56	TXN20260411154512162	paid	2026-04-11 15:45:12.02769+08
78	163	微信支付	76	TXN1631775893643	completed	2026-04-11 15:47:23.04746+08
79	164	微信支付	18	TXN20260411155455164	paid	2026-04-11 15:54:55.21965+08
80	165	微信支付	18	TXN20260411160405165	paid	2026-04-11 16:04:05.288123+08
81	166	微信支付	18	TXN20260411160603166	paid	2026-04-11 16:06:03.292038+08
82	167	微信支付	20	TXN20260411161341167	paid	2026-04-11 16:13:41.965264+08
83	168	微信支付	18	TXN20260411161656168	paid	2026-04-11 16:16:56.551531+08
84	169	微信支付	18	TXN20260411161728169	paid	2026-04-11 16:17:28.390931+08
\.


--
-- TOC entry 6185 (class 0 OID 79481)
-- Dependencies: 239
-- Data for Name: reviews; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.reviews (id, order_id, elderly_id, rating, content, created_at, status, images, updated_at, reply, ai_reviewed, ai_replied, deliverer_id, reviewer_type) FROM stdin;
59	96	33	5	小王评价:好吃极了	2026-04-06 13:34:29.81582+08	approved	{}	2026-04-06 13:34:51.062172+08	好吃就好	0	0	\N	elderly
62	112	33	5	不错	2026-04-07 12:39:22.352999+08	approved	{}	2026-04-07 12:40:08.677593+08	666	0	0	51	elderly
63	126	33	4	家属评价配送员	2026-04-08 18:15:23.037783+08	approved	{}	2026-04-10 22:16:04.842543+08	感谢您对我们配送员的肯定！4分是很好的鼓励，我们会继续努力提升服务细节，比如优化配送时间或加强保温措施，确保餐品以最佳状态送达。期待下次能为您带来更完美的体验！	0	1	\N	family
66	130	76	4	清蒸鱼，家属评价配送员！！！\n	2026-04-08 18:27:43.786738+08	approved	{}	2026-04-10 22:16:21.246003+08	感谢您和家人对清蒸鱼的认可！4分对我们既是鼓励也是鞭策，我们会继续优化配送服务，确保餐品以最佳状态送达。期待下次为您带来更完美的用餐体验！	0	1	\N	family
69	120	33	4	太香了 非常满意	2026-04-12 09:01:35.747311+08	approved	{}	2026-04-12 09:02:10.087175+08	感谢您对我们餐品的认可！“太香了”是对我们厨师团队最大的鼓励。 能得到您“非常满意”的评价，我们非常开心。我们会继续努力，在营养搭配和食材新鲜度上精益求精，争取下次为您带来更完美的5分体验！	0	1	\N	elderly
49	101	33	4	2222 非常满意	2026-04-06 11:26:03.129817+08	approved	{}	2026-04-06 11:44:26.403159+08	感谢您给予4分的好评！ 您的满意是我们前进的动力，我们会继续努力提升餐品质量和服务体验，期待下次能为您带来更完美的用餐感受。	0	1	\N	elderly
18	\N	35	2	饭菜质量太差，要求退款！	2026-04-01 15:09:57.88784+08	rejected	{https://ts1.tc.mm.bing.net/th/id/OIP-C.lJ9J94jtaaiSu1VvMNDp6wHaE8?rs=1&pid=ImgDetMain&o=7&rm=3}	2026-04-06 11:05:11.329127+08	你再说一遍？\n	0	0	\N	elderly
51	106	33	4	test 非常满意	2026-04-06 11:37:33.112429+08	approved	{}	2026-04-06 11:44:26.41105+08	感谢您的评价！很高兴您对我们的服务感到满意，我们会继续努力，为您提供更优质的助餐体验。期待您的再次光临！	0	1	\N	family
52	100	33	4	est 非常满意	2026-04-06 11:38:27.765268+08	approved	{}	2026-04-06 11:44:26.415065+08	感谢您给予4分的好评！您的满意是我们前进的动力，我们会继续努力，为大家提供更优质的助餐服务。期待您的再次光临！	0	1	\N	elderly
54	86	33	4	非常满意	2026-04-06 11:43:18.593975+08	approved	{}	2026-04-06 11:44:26.421967+08	感谢您的好评！很高兴我们的服务能让您满意。您给出的4分是对我们工作的肯定，也是我们继续提升的动力。我们会持续努力，争取为您带来更优质的社区助餐体验。期待您的再次光临！	0	1	42	elderly
11	\N	34	4	服务态度很好，餐品也不错，下次还会订购。	2026-04-01 15:04:46.087321+08	approved	\N	2026-04-06 11:05:11.329127+08	感谢您的认可！很高兴您对我们的服务和餐品感到满意。我们会继续努力，争取下次为您带来更完美的体验，期待您的再次订购！	0	1	\N	elderly
5	33	33	4	菜品很新鲜，味道不错，就是配送稍微晚了一点。	2026-04-01 14:49:55.040129+08	rejected	\N	2026-04-06 11:05:11.329127+08	感谢您的好评！我们会继续保持优质服务，不断改进，为您提供更好的用餐体验！	1	1	\N	elderly
13	\N	36	3	餐品一般，希望能改进一下味道。	2026-04-01 15:04:46.087321+08	approved	\N	2026-04-06 11:05:11.329127+08	感谢您的反馈！我们非常重视您提出的口味建议，会认真研究并优化餐品配方，努力提升用餐体验。期待下次能为您提供更满意的服务！	0	1	\N	elderly
60	90	33	5	家属代评：好吃极了\n	2026-04-06 13:41:04.15944+08	approved	{}	2026-04-06 13:41:30.260632+08	你老人喜欢吃就行\n	0	0	\N	family
61	109	33	2	配送质量差	2026-04-06 15:40:22.393465+08	approved	{}	2026-04-07 13:07:28.157955+08	非常抱歉这次配送服务没能让您满意。 我们非常重视您的反馈，已立即核查配送环节，将重点优化配送员的培训与保温包装，确保餐品能及时、完好地送达。如果您方便，可以私信提供订单号，我们会尽快为您跟进处理。感谢您的督促，我们会努力改进！	0	1	51	elderly
64	128	76	4	家属test配送员	2026-04-08 18:23:00.246538+08	approved	{}	2026-04-10 22:16:21.227755+08	感谢您对我们配送员的认可！ 能得到4分的评价，我们既开心又感到责任在肩。我们会继续优化餐品口味与营养搭配，努力让每一份餐食都更贴近您的期待。期待下次能为您带来更满意的体验！	0	1	\N	family
38	72	33	5	测试内容 非常满意	2026-04-03 14:18:53.279648+08	approved	\N	2026-04-06 11:43:48.936173+08	感谢您对我们社区助餐服务的五星好评！ 您的“非常满意”是对我们最大的鼓励，我们会继续用心提供营养可口的餐食和贴心服务。期待能一直为您服务，祝您用餐愉快！	0	1	\N	elderly
39	38	33	5	蔬菜沙拉6666 非常满意	2026-04-03 14:28:45.102426+08	approved	\N	2026-04-06 11:44:26.371899+08	感谢您对我们蔬菜沙拉的喜爱与支持！ 看到“6666”和5分好评，我们整个团队都备受鼓舞。我们会继续用心准备每一份餐品，期待能一直为您提供满意的服务！	0	1	\N	elderly
15	\N	33	2	餐品凉了，影响口感，很不满意。	2026-04-01 15:04:46.087321+08	approved	\N	2026-04-06 11:05:11.329127+08	非常抱歉给您带来了不佳的用餐体验。餐品温度确实直接影响口感，我们非常重视您反馈的问题。我们会立即核查送餐流程，努力改进保温措施，确保餐品能热乎乎地送达。感谢您的直言，这帮助我们变得更好。期待下次能为您提供满意的服务！	0	1	\N	elderly
9	\N	36	1	配送员很贴心，会提前打电话确认，非常周到。	2026-04-01 14:49:55.040129+08	approved	\N	2026-04-06 11:05:11.329127+08	感谢您对我们配送服务的认可！很高兴听到配送员的贴心服务给您带来了良好的体验，我们会将您的鼓励转达给他。期待继续为您提供周到的助餐服务，祝您用餐愉快！	0	1	\N	elderly
7	\N	34	1	整体服务非常满意，餐品质量很高。	2026-04-01 14:49:55.040129+08	approved	{https://ts1.tc.mm.bing.net/th/id/OIP-C.lJ9J94jtaaiSu1VvMNDp6wHaE8?rs=1&pid=ImgDetMain&o=7&rm=3}	2026-04-06 11:05:11.329127+08	感谢您给予5分好评！很高兴您对餐品质量和服务都感到满意，这是对我们最大的鼓励。我们会继续用心做好每一餐，期待您的持续支持！	0	1	\N	elderly
10	\N	37	4	餐品分量很足，老人吃得很开心。	2026-04-01 14:49:55.040129+08	approved	\N	2026-04-06 11:05:11.329127+08	感谢您的好评！我们会继续努力提供更好的服务，期待您的再次光临。	0	0	\N	elderly
29	\N	34	4	服务态度很好，送餐也很准时，谢谢！	2026-04-01 16:10:54.126983+08	approved	\N	2026-04-06 11:05:11.329127+08	感谢您对我们服务态度和送餐准时的认可！您的4分好评是对我们工作的莫大鼓励，我们也会继续努力，争取为您提供更优质的服务体验。期待您的再次光临！	1	1	\N	elderly
12	\N	35	4	菜品很新鲜，味道不错，就是配送稍微晚了一点。	2026-04-01 15:04:46.087321+08	approved	\N	2026-04-06 11:05:11.329127+08	感谢您的好评！我们会继续努力提供更好的服务，期待您的再次光临。	0	0	\N	elderly
16	\N	33	1	饭菜质量太差，有异味，非常失望！	2026-04-01 15:04:46.087321+08	approved	\N	2026-04-06 11:05:11.329127+08	非常抱歉给您带来了不愉快的用餐体验！ 我们已收到您的反馈，会立即核查餐品质量与卫生情况，并严肃处理。感谢您的监督，我们将全力改进，确保食品安全与口味。如方便，请通过客服热线联系我们，以便进一步了解情况并为您妥善处理。	0	1	\N	elderly
14	\N	37	3	分量有点少，不够吃。	2026-04-01 15:04:46.087321+08	approved	\N	2026-04-06 11:05:11.329127+08	感谢您的反馈！我们非常重视您提出的分量问题，会立即与配餐团队沟通，优化餐食标准。您的意见对我们改进服务至关重要，期待下次能为您提供更满意的用餐体验。	0	1	\N	elderly
4	32	33	5	餐品非常美味，配送及时，服务态度很好！	2026-04-01 14:49:55.040129+08	rejected	{http://localhost:7678/static/video1.mp4}	2026-04-06 11:05:11.329127+08	非常感谢您对我们餐品配送和服务的五星好评！ 您的满意是我们最大的动力，我们会继续努力保持高品质。期待能继续为您提供美味的餐点和贴心的服务！	1	1	\N	elderly
17	\N	34	5	非常满意的一餐，服务态度很好！	2026-04-01 15:09:57.88784+08	approved	{https://ts1.tc.mm.bing.net/th/id/OIP-C.lJ9J94jtaaiSu1VvMNDp6wHaE8?rs=1&pid=ImgDetMain&o=7&rm=3}	2026-04-06 11:05:11.329127+08	感谢您对我们服务的认可！很高兴听到您对餐品和服务的满意评价，您的支持是我们不断进步的动力。期待继续为您提供优质的社区助餐服务！	1	1	\N	elderly
33	\N	33	5	今天的饭菜非常好吃，老人很满意！	2026-04-01 16:51:11.024968+08	approved	\N	2026-04-06 11:05:11.329127+08	非常感谢您对我们餐品的认可！能让老人吃得满意是我们最大的心愿。我们会继续用心做好每一餐，也期待您和家人的持续支持与反馈哦！	0	1	\N	elderly
8	\N	35	4	味道不错，希望能增加更多菜品选择。	2026-04-01 14:49:55.040129+08	approved	{https://ts1.tc.mm.bing.net/th/id/OIP-C.lJ9J94jtaaiSu1VvMNDp6wHaE8?rs=1&pid=ImgDetMain&o=7&rm=3}	2026-04-06 11:05:11.329127+08	感谢您的好评！我们会继续保持优质服务，不断改进，为您提供更好的用餐体验！	0	0	\N	elderly
28	\N	33	5	今天的午餐非常好吃，分量也很足，老人很满意！	2026-04-01 16:10:54.126983+08	approved	{https://ts1.tc.mm.bing.net/th/id/OIP-C.lJ9J94jtaaiSu1VvMNDp6wHaE8?rs=1&pid=ImgDetMain&o=7&rm=3}	2026-04-06 11:05:11.329127+08	感谢您的五星好评！您的满意是我们最大的动力，我们会继续努力提供更好的服务，期待您的再次光临！😊	1	1	\N	elderly
36	\N	35	3	配送有点慢，饭菜到的时候已经凉了，影响了口感。	2026-04-01 17:04:29.281595+08	approved	\N	2026-04-06 11:05:11.329127+08	感谢您的反馈，也理解您对餐品温度和口感的重视。 配送延迟导致餐食变凉确实影响了体验，我们已记录下您的问题，会重点优化配送流程，努力提升保温效果。期待下次能为您提供更好的服务！	0	1	\N	elderly
35	\N	34	4	菜品种类很丰富，就是汤稍微咸了一点，希望下次改进。	2026-04-01 17:04:29.281595+08	approved	\N	2026-04-06 11:05:11.329127+08	感谢您的好评！很高兴您喜欢我们的菜品种类，关于汤品咸度的问题我们已经收到，会立刻反馈给后厨进行调整。期待下次能为您提供更满意的用餐体验！	0	1	\N	elderly
34	\N	33	1	今天的红烧肉做得非常地道，老人吃得很开心，谢谢！	2026-04-01 17:04:29.281595+08	approved	\N	2026-04-06 11:05:11.329127+08	感谢您对我们红烧肉的肯定！能让老人吃得开心，是我们最大的欣慰。 我们会继续用心做好每一餐，期待您的持续支持！	0	1	\N	elderly
37	\N	36	2	今天的菜不新鲜，老人吃了有点不舒服，很失望。	2026-04-01 17:04:29.281595+08	approved	\N	2026-04-06 11:05:11.329127+08	非常抱歉给您带来了不愉快的用餐体验。我们非常重视您反馈的菜品新鲜度问题，这确实是我们需要严格把关的环节。我们会立即核查今日的供餐流程，并加强品控，确保食品安全。对于老人家的不适，我们深表关切，后续会有专人联系您了解具体情况。感谢您的监督，帮助我们改进服务。	0	1	\N	elderly
19	\N	36	4	配送很及时，餐品很美味！	2026-04-01 15:09:57.88784+08	approved	{https://ts1.tc.mm.bing.net/th/id/OIP-C.lJ9J94jtaaiSu1VvMNDp6wHaE8?rs=1&pid=ImgDetMain&o=7&rm=3}	2026-04-06 11:05:11.329127+08	感谢您的好评！很高兴您对配送和餐品都感到满意。我们会继续努力，为您提供更优质的服务，期待您的再次光临！	0	1	\N	elderly
30	\N	35	3	餐品一般，希望能改进一下口味。	2026-04-01 16:10:54.126983+08	approved	{https://ts1.tc.mm.bing.net/th/id/OIP-C.lJ9J94jtaaiSu1VvMNDp6wHaE8?rs=1&pid=ImgDetMain&o=7&rm=3}	2026-04-06 11:05:11.329127+08	感谢您的反馈！我们非常重视您对餐品口味的建议，这能帮助我们更好地优化菜品质量。我们会认真研究您的意见，努力提升餐品口味，期待下次能为您提供更满意的用餐体验。	0	1	\N	elderly
32	\N	37	1	非常不满意，饭菜质量很差，投诉！	2026-04-01 16:10:54.126983+08	rejected	{https://ts1.tc.mm.bing.net/th/id/OIP-C.lJ9J94jtaaiSu1VvMNDp6wHaE8?rs=1&pid=ImgDetMain&o=7&rm=3}	2026-04-06 11:05:11.329127+08	test	0	1	\N	elderly
41	35	33	4	1314521 非常满意	2026-04-03 14:46:44.975086+08	approved	{http://localhost:7678/static/uploads/images/6f0dcab5-8691-4a08-aa96-b41c1bd1ae8c.jpg}	2026-04-06 11:44:26.376865+08	感谢您的好评！很高兴编号1314521的餐品让您满意，我们也会继续努力，为您提供更优质的社区助餐服务。期待您的再次光临！	0	1	\N	elderly
42	77	37	4	家属代评	2026-04-03 15:15:27.284161+08	approved	{http://localhost:7678/static/uploads/images/fee5bf1c-467b-471a-b73a-a444e5500fe3.jpg}	2026-04-06 11:44:26.380669+08	感谢您给予4分的评价！您的肯定是我们进步的动力，我们会继续努力提升餐品质量和服务体验，争取为您和家人带来更满意的助餐服务。期待您的再次支持！	0	1	\N	elderly
43	79	35	4	家属代评 非常满意	2026-04-03 15:22:40.82234+08	approved	{http://localhost:7678/static/uploads/images/6647e0fe-5e75-4bfb-8ce7-2b4c4eac9fe2.jpg}	2026-04-06 11:44:26.384881+08	感谢您和家人的认可！ 能得到4分评价我们很开心，这说明服务还有进步空间。我们会继续优化餐品和服务细节，努力为您和家人提供更满意的用餐体验。期待下次能收获您的5分鼓励！	0	1	\N	elderly
44	105	33	5	111 非常满意	2026-04-06 11:01:59.797968+08	approved	{}	2026-04-06 11:44:26.388181+08	感谢您给予我们5分好评！您的满意是对我们最大的鼓励，我们会继续用心提供优质的助餐服务。期待您常来用餐，祝您生活愉快！	0	1	\N	elderly
46	104	33	3	35345 非常满意	2026-04-06 11:16:15.639217+08	approved	{}	2026-04-06 11:44:26.391475+08	感谢您的评价！我们非常重视每一位用户的反馈，3分的评分提醒我们还有提升的空间。我们会认真对待您的意见，持续优化菜品和服务质量，期待下次能为您带来更好的用餐体验。	0	1	\N	elderly
47	103	33	4	1 非常满意	2026-04-06 11:24:50.705299+08	approved	{}	2026-04-06 11:44:26.395498+08	感谢您给予4分的好评！您的满意是我们前进的动力，我们会继续努力，为大家提供更优质的社区助餐服务。期待您的再次光临！	0	1	\N	elderly
48	102	33	4	1 非常满意	2026-04-06 11:25:17.138905+08	approved	{}	2026-04-06 11:44:26.399289+08	感谢您给予4分的好评！您的满意是我们前进的动力，我们会继续努力，为大家提供更优质的助餐服务。期待您的再次光临！ 	0	1	\N	elderly
50	99	33	4	111 非常满意	2026-04-06 11:31:25.112706+08	approved	{}	2026-04-06 11:44:26.407341+08	感谢您给予4分的好评！您的满意是我们前进的动力，我们也会继续努力，为大家提供更优质的社区助餐服务。期待您的再次光临！	0	1	\N	elderly
53	88	33	4	1 非常满意	2026-04-06 11:40:25.198217+08	approved	{}	2026-04-06 11:44:26.418355+08	感谢您给予4分的好评！您的满意是我们前进的动力，我们会继续努力提升餐品和服务质量，为大家带来更优质的社区助餐体验。期待您的再次光临！ 	0	1	\N	elderly
55	107	33	4	清蒸鱼很好吃	2026-04-06 12:38:02.452773+08	approved	{}	2026-04-06 12:39:30.111001+08	感谢您对我们清蒸鱼的认可！很高兴您喜欢它的味道。 我们会继续努力，在食材新鲜度和营养搭配上持续优化，为您带来更满意的用餐体验。期待您的再次光临！	0	1	\N	elderly
67	131	33	4	25认为虽然3	2026-04-08 18:29:09.141778+08	approved	{}	2026-04-10 22:16:21.254025+08	感谢您给予4分的好评！我们很高兴您对配送服务整体感到满意。虽然您提到“25认为虽然3”，我们理解这其中可能还有可以提升的空间。我们会继续优化配送流程，确保餐品能更快、更稳妥地送达您手中。期待下次为您提供更完美的体验！	0	1	51	elderly
56	97	33	4	配送很及时	2026-04-06 12:38:45.7116+08	approved	{}	2026-04-06 12:39:35.481763+08	感谢您对我们配送服务的认可！很高兴得知您对配送的及时性感到满意。我们会继续努力，进一步提升配送服务的质量，争取为您带来更完美的体验。期待您的继续支持！ 	0	1	51	elderly
57	92	33	4	太好吃了	2026-04-06 12:42:31.973008+08	approved	{}	2026-04-06 12:42:59.867409+08	感谢您的认可！看到您对餐品的味道如此满意，我们真的很开心。 能得到4分评价，说明我们还有进步的空间，我们一定会继续优化食材搭配和烹饪细节，努力把每一餐都做得更美味、更营养。期待下次能为您带来更完美的用餐体验！	0	1	\N	elderly
58	89	33	4	好吃极了	2026-04-06 12:47:50.734722+08	approved	{}	2026-04-06 12:47:57.802653+08	感谢您的好评！很高兴您喜欢我们的餐品，特别是对味道的认可。我们一直致力于在营养搭配和食材新鲜度上做到最好，您的4分鼓励是我们继续进步的动力。我们会持续优化，争取下次为您带来更完美的用餐体验！	0	1	\N	elderly
65	129	76	4	小米粥，家属评价配送员666	2026-04-08 18:24:30.301809+08	approved	{}	2026-04-10 22:16:21.236782+08	感谢您和家人的认可！小米粥能获得好评我们很开心，配送员的服务能得到“666”的点赞更是对我们团队的莫大鼓励。我们会继续用心做好每一餐，在营养搭配和餐品丰富度上持续优化，期待下次为您带来更满意的体验！	0	1	\N	family
68	163	33	4	太好吃了	2026-04-12 08:52:07.407424+08	approved	{}	2026-04-12 08:52:39.2492+08	好吃就好	0	0	\N	elderly
6	34	33	5	营养搭配很合理，老人吃着很放心，会继续订购。	2026-04-01 14:49:55.040129+08	approved	{https://ts1.tc.mm.bing.net/th/id/OIP-C.lJ9J94jtaaiSu1VvMNDp6wHaE8?rs=1&pid=ImgDetMain&o=7&rm=3}	2026-04-12 08:54:42.865298+08	感谢您对我们营养搭配的认可！能让老人吃得放心是我们最大的心愿。您的支持是我们前进的动力，期待能继续为您提供贴心的助餐服务！	0	1	\N	elderly
\.


--
-- TOC entry 5757 (class 0 OID 78527)
-- Dependencies: 219
-- Data for Name: spatial_ref_sys; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.spatial_ref_sys (srid, auth_name, auth_srid, srtext, proj4text) FROM stdin;
\.


--
-- TOC entry 6212 (class 0 OID 114745)
-- Dependencies: 266
-- Data for Name: staff_schedules; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.staff_schedules (id, staff_id, schedule_date, time_slot, status, note, created_at, updated_at) FROM stdin;
19	45	2026-03-30	08:00-10:00	confirmed		2026-04-04 20:42:50.080292+08	2026-04-04 20:42:50.080292+08
20	45	2026-03-30	10:00-12:00	confirmed		2026-04-04 20:42:50.093676+08	2026-04-04 20:42:50.093676+08
21	45	2026-03-30	14:00-16:00	confirmed		2026-04-04 20:42:50.108863+08	2026-04-04 20:42:50.108863+08
22	45	2026-03-30	18:00-20:00	confirmed		2026-04-04 20:42:50.122201+08	2026-04-04 20:42:50.122201+08
23	45	2026-03-30	16:00-18:00	confirmed		2026-04-04 20:42:50.136038+08	2026-04-04 20:42:50.136038+08
24	45	2026-03-31	08:00-10:00	confirmed		2026-04-04 21:06:17.183289+08	2026-04-04 21:06:17.183289+08
25	45	2026-04-05	18:00-20:00	confirmed		2026-04-04 21:06:40.487451+08	2026-04-04 21:06:40.487451+08
26	42	2026-03-30	14:00-16:00	confirmed		2026-04-04 21:08:31.106421+08	2026-04-04 21:08:31.106421+08
27	42	2026-04-05	14:00-16:00	confirmed		2026-04-04 21:08:52.677413+08	2026-04-04 21:08:52.677413+08
28	42	2026-04-05	16:00-18:00	confirmed		2026-04-04 21:08:52.688765+08	2026-04-04 21:08:52.688765+08
29	42	2026-04-05	18:00-20:00	confirmed		2026-04-04 21:08:52.700924+08	2026-04-04 21:08:52.700924+08
30	43	2026-03-30	08:00-10:00	confirmed		2026-04-04 21:22:53.308227+08	2026-04-04 21:22:53.308227+08
31	43	2026-03-30	16:00-18:00	confirmed		2026-04-04 21:22:53.330889+08	2026-04-04 21:22:53.330889+08
\.


--
-- TOC entry 6204 (class 0 OID 79786)
-- Dependencies: 258
-- Data for Name: tags; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tags (id, name, description, created_at, updated_at) FROM stdin;
8	低糖	低糖健康餐品	2026-03-31 20:40:06.040883+08	2026-03-31 20:40:06.040883+08
9	素食	素食餐品	2026-03-31 20:40:06.040883+08	2026-03-31 20:40:06.040883+08
10	清淡	清淡易消化	2026-03-31 20:40:06.040883+08	2026-03-31 20:40:06.040883+08
11	高蛋白	高蛋白营养餐	2026-03-31 20:40:06.040883+08	2026-03-31 20:40:06.040883+08
12	易消化	流食软食	2026-03-31 20:40:06.040883+08	2026-03-31 20:40:06.040883+08
13	营养	营养均衡套餐	2026-03-31 20:40:06.040883+08	2026-03-31 20:40:06.040883+08
\.


--
-- TOC entry 6170 (class 0 OID 79290)
-- Dependencies: 224
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, username, password_hash, user_type, status, created_at, updated_at, email, last_login, openid, unionid) FROM stdin;
33	13783898556	$pbkdf2-sha256$29000$MAZgjDGmdE4JYQyBMGZMyQ$5K.rd1.j7MIDjSnnUMe7HIE39nayqPbe1KRJw/nJ0TU	elderly	ACTIVE	2026-04-01 11:41:53.084914+08	2026-04-01 11:41:53.084914+08	\N	\N	\N	\N
34	elderly1	$pbkdf2-sha256$29000$hNB6zxlDqJVyLqVUqhWi1A$XLEETstMHXPhSB6C42U1DZuhzGvIZd68E1CuX3axgJU	elderly	ACTIVE	2026-04-01 12:02:32.453091+08	2026-04-01 12:02:32.453091+08	\N	\N	\N	\N
35	elderly2	$pbkdf2-sha256$29000$YGyt9X4vhfDe.x/DmBNCaA$WtPRfZipjf/bvRTsm96qPFnRSFaciAFOf31NQe2G6PA	elderly	ACTIVE	2026-04-01 12:02:32.453091+08	2026-04-01 12:02:32.453091+08	\N	\N	\N	\N
36	elderly3	$pbkdf2-sha256$29000$mTMGwFjrPSfEOGeslTLmPA$YDwsWvJDPfM.356WSxxj1NG/0qUK/jQ6G7gBmxilERk	elderly	ACTIVE	2026-04-01 12:02:32.453091+08	2026-04-01 12:02:32.453091+08	\N	\N	\N	\N
37	elderly4	$pbkdf2-sha256$29000$0BojhFCqtVbKmVMKgZAyxg$PGXT4pfSgTftOaThFN3/.mHtI580cfPQSk2EaVbvb4E	elderly	ACTIVE	2026-04-01 12:02:32.453091+08	2026-04-01 12:02:32.453091+08	\N	\N	\N	\N
38	elderly5	$pbkdf2-sha256$29000$FOJcC4Ew5jyn9D4n5Lw3Zg$IEy0qggefk86zKTED82xwgQnN/M8WZKtrlbfb7roeBU	elderly	ACTIVE	2026-04-01 12:02:32.453091+08	2026-04-01 12:02:32.453091+08	\N	\N	\N	\N
39	member1	$pbkdf2-sha256$29000$V.rdO2fsHQPAOOdcq1VqzQ$ZmQRSSdlZugWWI9RJ5vvwGLePHg3ghZ05kPPZMGlkAc	member	ACTIVE	2026-04-01 12:02:32.453091+08	2026-04-01 12:02:32.453091+08	\N	\N	\N	\N
40	member2	$pbkdf2-sha256$29000$3zvn/L83JiRk7N1ba03pvQ$M9UtsvCeRFnidlfsZaAf47ziMC.UHHX2p3OBxm1uU2c	member	ACTIVE	2026-04-01 12:02:32.453091+08	2026-04-01 12:02:32.453091+08	\N	\N	\N	\N
41	member3	$pbkdf2-sha256$29000$f8.Zk9Kac25tbY2x9t5bCw$p6KdH7Gs4.CG1.i2jLNjteIXFpa.V8e8lRD9DpVRfxc	member	ACTIVE	2026-04-01 12:02:32.453091+08	2026-04-01 12:02:32.453091+08	\N	\N	\N	\N
42	deliverer1	$pbkdf2-sha256$29000$RkgphTBGiFHKWav1vjdmjA$9BayT5h6Q1ugWi57vnxNVcYr47KXwPwFg/HlTdH4/uI	deliverer	ACTIVE	2026-04-01 12:02:32.453091+08	2026-04-01 12:02:32.453091+08	\N	\N	\N	\N
43	deliverer2	$pbkdf2-sha256$29000$MgaAMAYAACDEeG/tPScEYA$YNk5iKjDbIYKWGM1nJTu7NOjZ/O4.9oL.8ghYStuhVM	deliverer	ACTIVE	2026-04-01 12:02:32.453091+08	2026-04-01 12:02:32.453091+08	\N	\N	\N	\N
32	admin	$pbkdf2-sha256$29000$ak0JQQiBcO7d.38vZWztPQ$FxM6ByYvkxM.Seg5WSLUW7PHTSfqlNdcXMxH7k132HU	admin	ACTIVE	2026-04-01 11:30:42.64467+08	2026-04-01 21:11:38.863128+08	3540656750@qq.com	\N	\N	\N
44	17838556638	$pbkdf2-sha256$29000$VkpJyZnTmpNSSilFqHXufQ$lQeGEICIlcyPDhZl45mXtiCI/kY.3tu/b/Dl4u9nXMI	member	ACTIVE	2026-04-02 10:01:51.668261+08	2026-04-02 10:01:51.668261+08	\N	\N	\N	\N
45	1314521	$pbkdf2-sha256$29000$as2Zs1bKOSektLY2RqjVmg$RU3/nImxRsEmLjClSGiUF9/BDPCE9hiPP.L0zkD7J6Y	deliverer	ACTIVE	2026-04-02 10:17:20.669981+08	2026-04-02 10:17:20.669981+08	\N	\N	\N	\N
75	17836553396	$pbkdf2-sha256$29000$Vup9DyHkHIPQWqt1LqX0Hg$RLGERWQPKW3aH32gI5qy0cS/vLHWjtbE/WXfNPaDwjk	deliverer	ACTIVE	2026-04-07 18:10:46.646186+08	2026-04-07 18:10:46.646186+08	\N	\N	\N	\N
76	19635687856	$pbkdf2-sha256$29000$nfNeS4lxDmHMWYvxvpcyhg$vVliCGUCgHhvH.LSmAMEwYn79v/lCvwTbJRD6/KjZHg	elderly	ACTIVE	2026-04-07 18:43:04.039611+08	2026-04-07 18:43:04.039611+08	\N	\N	\N	\N
51	wx_oMv1q7QW	$pbkdf2-sha256$29000$03rv3VurtTaGcO49RygF4A$rQ/NEK/9A9H0Wc8iimSxw//YxNIjQGNtjX9/UgfETjc	deliverer	ACTIVE	2026-04-05 22:34:19.105616+08	2026-04-11 13:54:05.467677+08	\N	\N	oMv1q7QW3UREwpqSZUqbnYX95pSA	\N
\.


--
-- TOC entry 6206 (class 0 OID 81921)
-- Dependencies: 260
-- Data for Name: voice_synthesis; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.voice_synthesis (id, user_id, text_content, voice_url, voice_type, language, speed, status, created_at, completed_at) FROM stdin;
49	34	????Piper TTS??????	\N	\N	zh_CN	0.8	failed	2026-04-07 23:32:35.242595+08	\N
28	33	你好呀！很高兴见到你。今天过得怎么样？有什么想聊的或者需要帮忙的吗？我在这儿陪着你呢。 😊	\N	\N	zh_CN	0.8	failed	2026-04-06 14:31:42.464167+08	\N
39	34	????????	\N	\N	zh_CN	0.8	failed	2026-04-07 22:55:11.161501+08	\N
29	33	你好呀！很高兴见到你。今天过得怎么样？有什么想聊的或者需要帮忙的吗？我在这儿陪着你呢。 😊	/static/voices/voice_33cc766633f841abbd0bae6c213a2e91.wav	\N	zh_CN	0.8	completed	2026-04-06 14:43:36.34054+08	2026-04-06 06:43:37.598139+08
30	33	你好呀！很高兴见到你。今天过得怎么样？有什么想聊的或者需要帮忙的吗？我在这儿陪着你呢。 😊	/static/voices/voice_285d2e2110514b13985e7521a08a6997.wav	\N	zh_CN	0.8	completed	2026-04-06 14:45:59.457722+08	2026-04-06 06:46:00.158953+08
40	34	????????	\N	\N	zh_CN	0.8	processing	2026-04-07 22:56:43.677966+08	\N
31	33	你好呀！很高兴见到你。今天过得怎么样？有什么想聊的或者需要帮忙的吗？我在这儿陪着你呢。 😊	/static/voices/voice_de06096445bb427c82ab52e4ae99aebb.wav	\N	zh_CN	0.8	completed	2026-04-06 14:46:01.324126+08	2026-04-06 06:46:01.599894+08
32	33	你好呀！很高兴见到你。今天过得怎么样？有什么想聊的或者需要帮忙的吗？我在这儿陪着你呢。 😊	/static/voices/voice_4c53b58e8694430da33d8cfd82e1c1f6.wav	\N	zh_CN	0.8	completed	2026-04-06 14:46:04.992887+08	2026-04-06 06:46:05.282288+08
41	33	你好呀！很高兴见到你。今天过得怎么样？有什么想聊的，或者需要帮忙的，随时告诉我哦。我在这儿陪着你呢！ 🌼	\N	\N	zh_CN	0.8	processing	2026-04-07 22:57:58.3036+08	\N
33	33	你好呀！很高兴见到你。今天过得怎么样？有什么想聊的或者需要帮忙的吗？我在这儿陪着你呢。 😊	/static/voices/voice_1c3c9d8d11a347c492ed3bd873d81748.wav	\N	zh_CN	0.8	completed	2026-04-06 14:46:23.771594+08	2026-04-06 06:46:24.062711+08
34	33	你好呀！很高兴见到你。今天过得怎么样？有什么想聊的或者需要帮忙的吗？我在这儿陪着你呢。 😊	\N	\N	zh_CN	0.8	failed	2026-04-06 14:47:44.222922+08	\N
42	33	你好呀！很高兴见到你。今天过得怎么样？有什么想聊的，或者需要帮忙的，随时告诉我哦。我在这儿陪着你呢！ 🌼	\N	\N	zh_CN	0.8	processing	2026-04-07 22:58:04.96851+08	\N
35	33	你好呀！很高兴见到你。今天过得怎么样？有什么想聊的或者需要帮忙的吗？我在这儿陪着你呢。 😊	\N	\N	zh_CN	0.8	failed	2026-04-06 14:50:05.72887+08	\N
36	33	你好呀！很高兴见到你。今天过得怎么样？有什么想聊的或者需要帮忙的吗？我在这儿陪着你呢。 😊	\N	\N	zh_CN	0.8	failed	2026-04-06 14:50:07.611925+08	\N
43	33	你好呀！很高兴见到你。今天过得怎么样？有什么想聊的，或者需要帮忙的，随时告诉我哦。我在这儿陪着你呢！ 🌼	\N	\N	zh_CN	0.8	processing	2026-04-07 22:58:22.829716+08	\N
37	33	你好呀！很高兴见到你。今天过得怎么样？有什么想聊的或者需要帮忙的吗？我在这儿陪着你呢。 😊	\N	\N	zh_CN	0.8	failed	2026-04-06 14:50:09.052203+08	\N
38	33	你好呀！很高兴见到你。今天过得怎么样？有什么想聊的，或者需要帮忙的，随时告诉我哦。我在这儿陪着你呢！ 🌼	\N	\N	zh_CN	0.8	failed	2026-04-07 22:50:35.727929+08	\N
44	33	你好呀！很高兴见到你。今天过得怎么样？有什么想聊的，或者需要帮忙的，随时告诉我哦。我在这儿陪着你呢！ 🌼	\N	\N	zh_CN	0.8	processing	2026-04-07 22:59:42.388777+08	\N
45	34	????Piper TTS??????	\N	\N	zh_CN	0.8	failed	2026-04-07 23:27:34.966667+08	\N
62	34	测试本地Piper TTS语音合成功能	/static/voices/voice_b79d1ad005824d55a8779567b1eb2745.wav	\N	zh_CN	0.8	completed	2026-04-07 23:42:06.07289+08	2026-04-07 15:42:11.717047+08
46	33	你好呀！很高兴见到你。今天过得怎么样？有什么想聊的，或者需要帮忙的，随时告诉我哦。我在这儿陪着你呢！ 🌼	\N	\N	zh_CN	0.8	failed	2026-04-07 23:30:04.075537+08	\N
50	34	????Piper TTS??????	\N	\N	zh_CN	0.8	failed	2026-04-07 23:33:45.814499+08	\N
47	34	????Piper TTS??????	\N	\N	zh_CN	0.8	failed	2026-04-07 23:31:16.781568+08	\N
48	33	你好呀！很高兴见到你。今天过得怎么样？有什么想聊的，或者需要帮忙的，随时告诉我哦。我在这儿陪着你呢！ 🌼	\N	\N	zh_CN	0.8	failed	2026-04-07 23:32:25.919165+08	\N
56	33	你好呀！很高兴见到你。今天过得怎么样？有什么想聊的，或者需要帮忙的，随时告诉我哦。我在这儿陪着你呢！ 🌼	\N	\N	zh_CN	0.8	failed	2026-04-07 23:38:32.160419+08	\N
51	34	????Piper TTS??????	\N	\N	zh_CN	0.8	failed	2026-04-07 23:34:54.586628+08	\N
60	34	测试本地Piper TTS语音合成功能	\N	\N	zh_CN	0.8	failed	2026-04-07 23:40:57.433566+08	\N
52	34	????Piper TTS??????	\N	\N	zh_CN	0.8	failed	2026-04-07 23:35:32.588574+08	\N
57	34	????Piper TTS??????	\N	\N	zh_CN	0.8	failed	2026-04-07 23:38:49.237085+08	\N
53	33	你好呀！很高兴见到你。今天过得怎么样？有什么想聊的，或者需要帮忙的，随时告诉我哦。我在这儿陪着你呢！ 🌼	\N	\N	zh_CN	0.8	failed	2026-04-07 23:36:11.566849+08	\N
54	34	????Piper TTS??????	\N	\N	zh_CN	0.8	failed	2026-04-07 23:36:28.519619+08	\N
55	34	????Piper TTS??????	\N	\N	zh_CN	0.8	failed	2026-04-07 23:36:52.603623+08	\N
58	34	测试本地Piper TTS语音合成功能	\N	\N	zh_CN	0.8	failed	2026-04-07 23:39:31.159854+08	\N
59	34	测试本地Piper TTS语音合成功能	\N	\N	zh_CN	0.8	failed	2026-04-07 23:40:28.343405+08	\N
61	33	你好呀！很高兴见到你。今天过得怎么样？有什么想聊的，或者需要帮忙的，随时告诉我哦。我在这儿陪着你呢！ 🌼	\N	\N	zh_CN	0.8	failed	2026-04-07 23:41:13.526186+08	\N
64	33	你好呀！很高兴见到你。今天过得怎么样？有什么想聊的，或者需要帮忙的，随时告诉我哦。我在这儿陪着你呢！ 🌼	/static/voices/voice_417d3c041d8345ceb5ade51982d6bc8b.wav	\N	zh_CN	0.8	completed	2026-04-07 23:43:11.03991+08	2026-04-07 15:43:17.792491+08
63	34	这是一个测试，验证Piper TTS语音合成功能是否正常工作	/static/voices/voice_ebfa99088294494fb6961ef32beb4d7f.wav	\N	zh_CN	0.8	completed	2026-04-07 23:43:05.133042+08	2026-04-07 15:43:11.027487+08
65	33	你好呀！很高兴见到你。今天天气不错，你过得怎么样呀？有什么想聊的或者需要帮忙的，随时告诉我哦！ 😊	\N	\N	zh_CN	0.8	failed	2026-04-07 23:44:52.69725+08	\N
66	34	测试修复后的Piper TTS语音合成功能	\N	\N	zh_CN	0.8	failed	2026-04-07 23:45:01.958628+08	\N
67	34	测试修复后的Piper TTS语音合成功能	\N	\N	zh_CN	0.8	failed	2026-04-07 23:45:29.429129+08	\N
68	34	简单测试	\N	\N	zh_CN	0.8	failed	2026-04-07 23:45:55.487555+08	\N
71	34	测试修复后的Piper TTS语音合成功能	/static/voices/voice_6bb7b938590c4e0c9a82ee7edf73a4f9.wav	\N	zh_CN	0.8	completed	2026-04-07 23:48:57.731365+08	2026-04-07 15:49:03.354805+08
69	33	你好呀！很高兴见到你。今天过得怎么样？有什么想聊的，或者需要帮忙的，随时告诉我哦。我在这儿陪着你呢！ 🌼	/static/voices/voice_7dd309a3b2a64548bd5e9091672f2a06.wav	\N	zh_CN	0.8	completed	2026-04-07 23:47:27.274902+08	2026-04-07 15:47:33.392132+08
70	33	你好呀！很高兴见到你。今天过得怎么样？有什么想聊的，或者需要帮忙的，随时告诉我哦。我在这儿陪着你呢！ 🌼	/static/voices/voice_dbd0c6eb18e04c0bbde40fb6a88e1607.wav	\N	zh_CN	0.8	completed	2026-04-07 23:48:20.190638+08	2026-04-07 15:48:26.601179+08
81	33	你好呀！很高兴见到你。今天过得怎么样？有什么想聊的或者需要帮忙的，随时告诉我哦。我在这儿陪着你呢！ 🌼	/static/voices/voice_fba0db2048e74af7af1324decab1a8d8.wav	\N	zh_CN	0.8	completed	2026-04-08 00:08:11.243544+08	2026-04-07 16:08:18.489388+08
72	33	您好！很高兴为您服务。我是老年人膳食服务助手，可以为您提供餐品推荐、价格咨询、配送时间等信息，也可以根据您的健康状况提供饮食建议。\n\n请问有什么可以帮助您的吗？	/static/voices/voice_f43507fc53bf4213a39fa9e50cc9b5b1.wav	\N	zh_CN	0.8	completed	2026-04-07 23:49:44.783556+08	2026-04-07 15:49:51.318761+08
73	33	你好呀！很高兴见到你。今天过得怎么样？有什么想聊的或者需要帮忙的，随时告诉我哦。我在这儿陪着你呢！ 🌼	/static/voices/voice_c6d314bb0d2e4883a4745926db47cd07.wav	\N	zh_CN	0.8	completed	2026-04-07 23:50:00.601965+08	2026-04-07 15:50:07.831166+08
117	33	喂，你好呀！我在这儿呢，能听到你的声音。  \n刚才是在测试吗？没问题，我随时都在，有什么想问的、想聊的，慢慢跟我说就好。 😊	/static/voices/voice_17027d7238824b0eaa2f4e3720283e4b.wav	elderly	zh_CN	0.8	completed	2026-04-12 08:51:27.625407+08	2026-04-12 00:51:33.00389+08
74	33	你好呀！很高兴见到你。今天过得怎么样？有什么想聊的或者需要帮忙的，随时告诉我哦。我在这儿陪着你呢！ 🌼	/static/voices/voice_d3c0d5ac5a9a4b6b97b8a13ea6c56cf1.wav	\N	zh_CN	0.8	completed	2026-04-07 23:50:49.645548+08	2026-04-07 15:50:55.733032+08
113	33	你好呀！很高兴见到你。今天过得怎么样？有什么想聊的或者需要帮忙的，随时告诉我哦。我在这儿陪着你呢！ 🌼	/static/voices/voice_5744b727baf54440911e375c442f4b22.wav	\N	zh_CN	0.8	completed	2026-04-10 08:33:23.973608+08	2026-04-10 00:33:28.172376+08
75	33	你好呀！很高兴见到你。今天过得怎么样？有什么想聊的或者需要帮忙的，随时告诉我哦。我在这儿陪着你呢！ 🌼	/static/voices/voice_03dabdc5d63a4841a11e12a746277e42.wav	\N	zh_CN	0.8	completed	2026-04-07 23:52:15.175929+08	2026-04-07 15:52:22.24326+08
76	33	你好呀！很高兴见到你。今天过得怎么样？有什么想聊的或者需要帮忙的，随时告诉我哦。我在这儿陪着你呢！ 🌼	/static/voices/voice_99cd3b30221a4fe6adcef70f4200fa98.wav	\N	zh_CN	0.8	completed	2026-04-07 23:53:14.158269+08	2026-04-07 15:53:20.503821+08
77	33	你好呀！很高兴见到你。今天过得怎么样？有什么想聊的或者需要帮忙的，随时告诉我哦。我在这儿陪着你呢！ 🌼	/static/voices/voice_3684f7a9e6ea4682adea44067aa8c9ce.wav	\N	zh_CN	0.8	completed	2026-04-07 23:53:39.113314+08	2026-04-07 15:53:46.292842+08
114	33	你好呀！很高兴见到你。今天过得怎么样？有什么想聊的或者需要帮忙的，随时告诉我哦。我在这儿陪着你呢！ 🌼	/static/voices/voice_f4f2cb119a9146198cb4e6b842b2983c.wav	\N	zh_CN	0.8	completed	2026-04-10 08:34:11.031444+08	2026-04-10 00:34:16.963994+08
78	34	测试修复后的WAV文件格式	/static/voices/voice_ac04b4617ffc4815ba983cbdae32ea3c.wav	\N	zh_CN	0.8	completed	2026-04-07 23:54:53.676339+08	2026-04-07 15:54:59.321092+08
79	33	你好呀！很高兴见到你。今天过得怎么样？有什么想聊的，或者需要帮忙的，随时告诉我哦。我在这儿陪着你呢！ 🌼	/static/voices/voice_65873bee3c28486c852bf069c892da31.wav	\N	zh_CN	0.8	completed	2026-04-07 23:57:33.617201+08	2026-04-07 15:57:40.697129+08
80	33	你好呀！很高兴见到你。今天过得怎么样？有什么想聊的或者需要帮忙的，随时告诉我哦。我在这儿陪着你呢！ 🌼	/static/voices/voice_0bf966d3a50c408da9b98197bf796080.wav	\N	zh_CN	0.8	completed	2026-04-08 00:06:47.4156+08	2026-04-07 16:06:54.161636+08
115	33	您好！很高兴为您服务。我是老年人膳食服务助手，可以为您提供餐品推荐、价格咨询、配送时间等信息，也可以根据您的健康状况提供饮食建议。\n\n请问有什么可以帮助您的吗？	/static/voices/voice_3bb9dc1efdfc493ab18fb474a4123427.wav	elderly	zh_CN	0.8	completed	2026-04-11 20:23:54.745177+08	2026-04-11 12:23:58.214445+08
116	33	喂，你好呀！我在这儿呢，能听到你的声音。  \n刚才是在测试吗？没问题，我随时都在，有什么想问的、想聊的，慢慢跟我说就好。 😊	/static/voices/voice_5bfca56736234674b04815c806bf144d.wav	elderly	zh_CN	0.8	completed	2026-04-12 08:51:21.342352+08	2026-04-12 00:51:27.613199+08
\.


--
-- TOC entry 6245 (class 0 OID 0)
-- Dependencies: 242
-- Name: ai_conversations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ai_conversations_id_seq', 104, true);


--
-- TOC entry 6246 (class 0 OID 0)
-- Dependencies: 240
-- Name: announcements_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.announcements_id_seq', 10, true);


--
-- TOC entry 6247 (class 0 OID 0)
-- Dependencies: 255
-- Name: categories_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.categories_id_seq', 10, true);


--
-- TOC entry 6248 (class 0 OID 0)
-- Dependencies: 244
-- Name: communities_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.communities_id_seq', 6, true);


--
-- TOC entry 6249 (class 0 OID 0)
-- Dependencies: 234
-- Name: deliveries_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.deliveries_id_seq', 63, true);


--
-- TOC entry 6250 (class 0 OID 0)
-- Dependencies: 267
-- Name: delivery_areas_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.delivery_areas_id_seq', 4, true);


--
-- TOC entry 6251 (class 0 OID 0)
-- Dependencies: 236
-- Name: elder_member_relations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.elder_member_relations_id_seq', 10, true);


--
-- TOC entry 6252 (class 0 OID 0)
-- Dependencies: 248
-- Name: emergency_calls_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.emergency_calls_id_seq', 34, true);


--
-- TOC entry 6253 (class 0 OID 0)
-- Dependencies: 253
-- Name: exceptions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.exceptions_id_seq', 5, true);


--
-- TOC entry 6254 (class 0 OID 0)
-- Dependencies: 269
-- Name: favorites_new_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.favorites_new_id_seq', 13, true);


--
-- TOC entry 6255 (class 0 OID 0)
-- Dependencies: 246
-- Name: health_records_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.health_records_id_seq', 10, true);


--
-- TOC entry 6256 (class 0 OID 0)
-- Dependencies: 263
-- Name: health_reminders_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.health_reminders_id_seq', 3, true);


--
-- TOC entry 6257 (class 0 OID 0)
-- Dependencies: 261
-- Name: health_tags_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.health_tags_id_seq', 16, true);


--
-- TOC entry 6258 (class 0 OID 0)
-- Dependencies: 228
-- Name: meals_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.meals_id_seq', 18, true);


--
-- TOC entry 6259 (class 0 OID 0)
-- Dependencies: 232
-- Name: order_items_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.order_items_id_seq', 178, true);


--
-- TOC entry 6260 (class 0 OID 0)
-- Dependencies: 230
-- Name: orders_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.orders_id_seq', 169, true);


--
-- TOC entry 6261 (class 0 OID 0)
-- Dependencies: 251
-- Name: payments_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.payments_id_seq', 84, true);


--
-- TOC entry 6262 (class 0 OID 0)
-- Dependencies: 238
-- Name: reviews_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.reviews_id_seq', 69, true);


--
-- TOC entry 6263 (class 0 OID 0)
-- Dependencies: 265
-- Name: staff_schedules_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.staff_schedules_id_seq', 31, true);


--
-- TOC entry 6264 (class 0 OID 0)
-- Dependencies: 257
-- Name: tags_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tags_id_seq', 13, true);


--
-- TOC entry 6265 (class 0 OID 0)
-- Dependencies: 223
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 76, true);


--
-- TOC entry 6266 (class 0 OID 0)
-- Dependencies: 259
-- Name: voice_synthesis_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.voice_synthesis_id_seq', 117, true);


--
-- TOC entry 5937 (class 2606 OID 79717)
-- Name: admin_profiles admin_profiles_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.admin_profiles
    ADD CONSTRAINT admin_profiles_pkey PRIMARY KEY (user_id);


--
-- TOC entry 5916 (class 2606 OID 79554)
-- Name: ai_conversations ai_conversations_conversation_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ai_conversations
    ADD CONSTRAINT ai_conversations_conversation_id_key UNIQUE (conversation_id);


--
-- TOC entry 5918 (class 2606 OID 79552)
-- Name: ai_conversations ai_conversations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ai_conversations
    ADD CONSTRAINT ai_conversations_pkey PRIMARY KEY (id);


--
-- TOC entry 5912 (class 2606 OID 79540)
-- Name: announcements announcements_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.announcements
    ADD CONSTRAINT announcements_pkey PRIMARY KEY (id);


--
-- TOC entry 5947 (class 2606 OID 79779)
-- Name: categories categories_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_name_key UNIQUE (name);


--
-- TOC entry 5949 (class 2606 OID 79777)
-- Name: categories categories_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_pkey PRIMARY KEY (id);


--
-- TOC entry 5923 (class 2606 OID 79572)
-- Name: communities communities_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.communities
    ADD CONSTRAINT communities_pkey PRIMARY KEY (id);


--
-- TOC entry 5873 (class 2606 OID 79348)
-- Name: deliverer_profiles deliverer_profiles_phone_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.deliverer_profiles
    ADD CONSTRAINT deliverer_profiles_phone_key UNIQUE (phone);


--
-- TOC entry 5875 (class 2606 OID 79346)
-- Name: deliverer_profiles deliverer_profiles_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.deliverer_profiles
    ADD CONSTRAINT deliverer_profiles_pkey PRIMARY KEY (user_id);


--
-- TOC entry 5892 (class 2606 OID 79423)
-- Name: deliveries deliveries_order_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.deliveries
    ADD CONSTRAINT deliveries_order_id_key UNIQUE (order_id);


--
-- TOC entry 5894 (class 2606 OID 79421)
-- Name: deliveries deliveries_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.deliveries
    ADD CONSTRAINT deliveries_pkey PRIMARY KEY (id);


--
-- TOC entry 5968 (class 2606 OID 131083)
-- Name: delivery_areas delivery_areas_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.delivery_areas
    ADD CONSTRAINT delivery_areas_pkey PRIMARY KEY (id);


--
-- TOC entry 5899 (class 2606 OID 79467)
-- Name: elder_member_relations elder_member_relations_elder_id_member_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.elder_member_relations
    ADD CONSTRAINT elder_member_relations_elder_id_member_id_key UNIQUE (elder_id, member_id);


--
-- TOC entry 5901 (class 2606 OID 79465)
-- Name: elder_member_relations elder_member_relations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.elder_member_relations
    ADD CONSTRAINT elder_member_relations_pkey PRIMARY KEY (id);


--
-- TOC entry 5862 (class 2606 OID 79314)
-- Name: elderly_profiles elderly_profiles_phone_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.elderly_profiles
    ADD CONSTRAINT elderly_profiles_phone_key UNIQUE (phone);


--
-- TOC entry 5864 (class 2606 OID 79312)
-- Name: elderly_profiles elderly_profiles_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.elderly_profiles
    ADD CONSTRAINT elderly_profiles_pkey PRIMARY KEY (user_id);


--
-- TOC entry 5931 (class 2606 OID 79623)
-- Name: emergency_calls emergency_calls_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.emergency_calls
    ADD CONSTRAINT emergency_calls_pkey PRIMARY KEY (id);


--
-- TOC entry 5944 (class 2606 OID 79762)
-- Name: exceptions exceptions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.exceptions
    ADD CONSTRAINT exceptions_pkey PRIMARY KEY (id);


--
-- TOC entry 5970 (class 2606 OID 155681)
-- Name: favorites favorites_new_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.favorites
    ADD CONSTRAINT favorites_new_pkey PRIMARY KEY (id);


--
-- TOC entry 5972 (class 2606 OID 155683)
-- Name: favorites favorites_new_user_id_meal_id_user_type_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.favorites
    ADD CONSTRAINT favorites_new_user_id_meal_id_user_type_key UNIQUE (user_id, meal_id, user_type);


--
-- TOC entry 5927 (class 2606 OID 79584)
-- Name: health_records health_records_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.health_records
    ADD CONSTRAINT health_records_pkey PRIMARY KEY (id);


--
-- TOC entry 5962 (class 2606 OID 114700)
-- Name: health_reminders health_reminders_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.health_reminders
    ADD CONSTRAINT health_reminders_pkey PRIMARY KEY (id);


--
-- TOC entry 5958 (class 2606 OID 106566)
-- Name: health_tags health_tags_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.health_tags
    ADD CONSTRAINT health_tags_name_key UNIQUE (name);


--
-- TOC entry 5960 (class 2606 OID 106564)
-- Name: health_tags health_tags_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.health_tags
    ADD CONSTRAINT health_tags_pkey PRIMARY KEY (id);


--
-- TOC entry 5881 (class 2606 OID 79368)
-- Name: meals meals_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.meals
    ADD CONSTRAINT meals_pkey PRIMARY KEY (id);


--
-- TOC entry 5869 (class 2606 OID 79330)
-- Name: member_profiles member_profiles_phone_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.member_profiles
    ADD CONSTRAINT member_profiles_phone_key UNIQUE (phone);


--
-- TOC entry 5871 (class 2606 OID 79328)
-- Name: member_profiles member_profiles_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.member_profiles
    ADD CONSTRAINT member_profiles_pkey PRIMARY KEY (user_id);


--
-- TOC entry 5890 (class 2606 OID 79400)
-- Name: order_items order_items_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT order_items_pkey PRIMARY KEY (id);


--
-- TOC entry 5886 (class 2606 OID 79384)
-- Name: orders orders_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_pkey PRIMARY KEY (id);


--
-- TOC entry 5940 (class 2606 OID 79732)
-- Name: payments payments_order_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.payments
    ADD CONSTRAINT payments_order_id_key UNIQUE (order_id);


--
-- TOC entry 5942 (class 2606 OID 79730)
-- Name: payments payments_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.payments
    ADD CONSTRAINT payments_pkey PRIMARY KEY (id);


--
-- TOC entry 5908 (class 2606 OID 79492)
-- Name: reviews reviews_order_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT reviews_order_id_key UNIQUE (order_id);


--
-- TOC entry 5910 (class 2606 OID 79490)
-- Name: reviews reviews_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT reviews_pkey PRIMARY KEY (id);


--
-- TOC entry 5964 (class 2606 OID 114755)
-- Name: staff_schedules staff_schedules_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.staff_schedules
    ADD CONSTRAINT staff_schedules_pkey PRIMARY KEY (id);


--
-- TOC entry 5966 (class 2606 OID 114757)
-- Name: staff_schedules staff_schedules_staff_id_schedule_date_time_slot_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.staff_schedules
    ADD CONSTRAINT staff_schedules_staff_id_schedule_date_time_slot_key UNIQUE (staff_id, schedule_date, time_slot);


--
-- TOC entry 5951 (class 2606 OID 79795)
-- Name: tags tags_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tags
    ADD CONSTRAINT tags_name_key UNIQUE (name);


--
-- TOC entry 5953 (class 2606 OID 79793)
-- Name: tags tags_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tags
    ADD CONSTRAINT tags_pkey PRIMARY KEY (id);


--
-- TOC entry 5852 (class 2606 OID 90117)
-- Name: users unique_email; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT unique_email UNIQUE (email);


--
-- TOC entry 5854 (class 2606 OID 122898)
-- Name: users users_openid_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_openid_key UNIQUE (openid);


--
-- TOC entry 5856 (class 2606 OID 79298)
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- TOC entry 5858 (class 2606 OID 122902)
-- Name: users users_unionid_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_unionid_key UNIQUE (unionid);


--
-- TOC entry 5860 (class 2606 OID 79300)
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- TOC entry 5956 (class 2606 OID 81929)
-- Name: voice_synthesis voice_synthesis_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.voice_synthesis
    ADD CONSTRAINT voice_synthesis_pkey PRIMARY KEY (id);


--
-- TOC entry 5919 (class 1259 OID 79561)
-- Name: idx_ai_conversations_conversation_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_ai_conversations_conversation_id ON public.ai_conversations USING btree (conversation_id);


--
-- TOC entry 5920 (class 1259 OID 79562)
-- Name: idx_ai_conversations_type; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_ai_conversations_type ON public.ai_conversations USING btree (conversation_type);


--
-- TOC entry 5921 (class 1259 OID 79560)
-- Name: idx_ai_conversations_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_ai_conversations_user_id ON public.ai_conversations USING btree (user_id);


--
-- TOC entry 5913 (class 1259 OID 79542)
-- Name: idx_announcements_status; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_announcements_status ON public.announcements USING btree (status);


--
-- TOC entry 5914 (class 1259 OID 79541)
-- Name: idx_announcements_type; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_announcements_type ON public.announcements USING btree (type);


--
-- TOC entry 5924 (class 1259 OID 79574)
-- Name: idx_communities_address; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_communities_address ON public.communities USING btree (address);


--
-- TOC entry 5925 (class 1259 OID 79573)
-- Name: idx_communities_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_communities_name ON public.communities USING btree (name);


--
-- TOC entry 5876 (class 1259 OID 79355)
-- Name: idx_deliverer_phone; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_deliverer_phone ON public.deliverer_profiles USING btree (phone);


--
-- TOC entry 5877 (class 1259 OID 79356)
-- Name: idx_deliverer_status; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_deliverer_status ON public.deliverer_profiles USING btree (status);


--
-- TOC entry 5895 (class 1259 OID 79435)
-- Name: idx_deliveries_deliverer_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_deliveries_deliverer_id ON public.deliveries USING btree (deliverer_id);


--
-- TOC entry 5896 (class 1259 OID 79434)
-- Name: idx_deliveries_order_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_deliveries_order_id ON public.deliveries USING btree (order_id);


--
-- TOC entry 5897 (class 1259 OID 79436)
-- Name: idx_deliveries_status; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_deliveries_status ON public.deliveries USING btree (status);


--
-- TOC entry 5865 (class 1259 OID 79320)
-- Name: idx_elderly_location; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_elderly_location ON public.elderly_profiles USING gist (location);


--
-- TOC entry 5866 (class 1259 OID 79321)
-- Name: idx_elderly_phone; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_elderly_phone ON public.elderly_profiles USING btree (phone);


--
-- TOC entry 5932 (class 1259 OID 79632)
-- Name: idx_emergency_calls_created_at; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_emergency_calls_created_at ON public.emergency_calls USING btree (created_at);


--
-- TOC entry 5933 (class 1259 OID 79629)
-- Name: idx_emergency_calls_elderly_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_emergency_calls_elderly_id ON public.emergency_calls USING btree (elderly_id);


--
-- TOC entry 5934 (class 1259 OID 79630)
-- Name: idx_emergency_calls_emergency_type; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_emergency_calls_emergency_type ON public.emergency_calls USING btree (emergency_type);


--
-- TOC entry 5935 (class 1259 OID 79631)
-- Name: idx_emergency_calls_response_status; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_emergency_calls_response_status ON public.emergency_calls USING btree (response_status);


--
-- TOC entry 5973 (class 1259 OID 155695)
-- Name: idx_favorites_meal_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_favorites_meal_id ON public.favorites USING btree (meal_id);


--
-- TOC entry 5974 (class 1259 OID 155694)
-- Name: idx_favorites_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_favorites_user_id ON public.favorites USING btree (user_id);


--
-- TOC entry 5975 (class 1259 OID 155696)
-- Name: idx_favorites_user_type; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_favorites_user_type ON public.favorites USING btree (user_type);


--
-- TOC entry 5928 (class 1259 OID 79595)
-- Name: idx_health_records_elderly_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_health_records_elderly_id ON public.health_records USING btree (elderly_id);


--
-- TOC entry 5929 (class 1259 OID 79596)
-- Name: idx_health_records_recorded_at; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_health_records_recorded_at ON public.health_records USING btree (recorded_at);


--
-- TOC entry 5878 (class 1259 OID 79371)
-- Name: idx_meals_special_tag; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_meals_special_tag ON public.meals USING btree (special_tag);


--
-- TOC entry 5879 (class 1259 OID 79370)
-- Name: idx_meals_status; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_meals_status ON public.meals USING btree (status);


--
-- TOC entry 5867 (class 1259 OID 79336)
-- Name: idx_member_phone; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_member_phone ON public.member_profiles USING btree (phone);


--
-- TOC entry 5887 (class 1259 OID 79412)
-- Name: idx_order_items_meal_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_order_items_meal_id ON public.order_items USING btree (meal_id);


--
-- TOC entry 5888 (class 1259 OID 79411)
-- Name: idx_order_items_order_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_order_items_order_id ON public.order_items USING btree (order_id);


--
-- TOC entry 5882 (class 1259 OID 79390)
-- Name: idx_orders_elderly_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_orders_elderly_id ON public.orders USING btree (elderly_id);


--
-- TOC entry 5883 (class 1259 OID 79392)
-- Name: idx_orders_payment_status; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_orders_payment_status ON public.orders USING btree (payment_status);


--
-- TOC entry 5884 (class 1259 OID 79391)
-- Name: idx_orders_status; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_orders_status ON public.orders USING btree (status);


--
-- TOC entry 5902 (class 1259 OID 79478)
-- Name: idx_relations_elder_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_relations_elder_id ON public.elder_member_relations USING btree (elder_id);


--
-- TOC entry 5903 (class 1259 OID 79479)
-- Name: idx_relations_member_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_relations_member_id ON public.elder_member_relations USING btree (member_id);


--
-- TOC entry 5904 (class 1259 OID 79504)
-- Name: idx_reviews_elderly_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_reviews_elderly_id ON public.reviews USING btree (elderly_id);


--
-- TOC entry 5905 (class 1259 OID 79503)
-- Name: idx_reviews_order_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_reviews_order_id ON public.reviews USING btree (order_id);


--
-- TOC entry 5906 (class 1259 OID 79505)
-- Name: idx_reviews_rating; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_reviews_rating ON public.reviews USING btree (rating);


--
-- TOC entry 5848 (class 1259 OID 79303)
-- Name: idx_users_status; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_users_status ON public.users USING btree (status);


--
-- TOC entry 5849 (class 1259 OID 79302)
-- Name: idx_users_user_type; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_users_user_type ON public.users USING btree (user_type);


--
-- TOC entry 5850 (class 1259 OID 79301)
-- Name: idx_users_username; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_users_username ON public.users USING btree (username);


--
-- TOC entry 5945 (class 1259 OID 79768)
-- Name: ix_exceptions_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_exceptions_id ON public.exceptions USING btree (id);


--
-- TOC entry 5938 (class 1259 OID 79738)
-- Name: ix_payments_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_payments_id ON public.payments USING btree (id);


--
-- TOC entry 5954 (class 1259 OID 81935)
-- Name: ix_voice_synthesis_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_voice_synthesis_id ON public.voice_synthesis USING btree (id);


--
-- TOC entry 6016 (class 2620 OID 79650)
-- Name: announcements trigger_update_announcements_timestamp; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_announcements_timestamp BEFORE UPDATE ON public.announcements FOR EACH ROW EXECUTE FUNCTION public.update_timestamp();


--
-- TOC entry 6017 (class 2620 OID 79651)
-- Name: communities trigger_update_communities_timestamp; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_communities_timestamp BEFORE UPDATE ON public.communities FOR EACH ROW EXECUTE FUNCTION public.update_timestamp();


--
-- TOC entry 6010 (class 2620 OID 79644)
-- Name: deliverer_profiles trigger_update_deliverer_profiles_timestamp; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_deliverer_profiles_timestamp BEFORE UPDATE ON public.deliverer_profiles FOR EACH ROW EXECUTE FUNCTION public.update_timestamp();


--
-- TOC entry 6013 (class 2620 OID 79647)
-- Name: deliveries trigger_update_deliveries_timestamp; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_deliveries_timestamp BEFORE UPDATE ON public.deliveries FOR EACH ROW EXECUTE FUNCTION public.update_timestamp();


--
-- TOC entry 6014 (class 2620 OID 79648)
-- Name: elder_member_relations trigger_update_elder_member_relations_timestamp; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_elder_member_relations_timestamp BEFORE UPDATE ON public.elder_member_relations FOR EACH ROW EXECUTE FUNCTION public.update_timestamp();


--
-- TOC entry 6008 (class 2620 OID 79642)
-- Name: elderly_profiles trigger_update_elderly_profiles_timestamp; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_elderly_profiles_timestamp BEFORE UPDATE ON public.elderly_profiles FOR EACH ROW EXECUTE FUNCTION public.update_timestamp();


--
-- TOC entry 6018 (class 2620 OID 79653)
-- Name: emergency_calls trigger_update_emergency_calls_timestamp; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_emergency_calls_timestamp BEFORE UPDATE ON public.emergency_calls FOR EACH ROW EXECUTE FUNCTION public.update_timestamp();


--
-- TOC entry 6011 (class 2620 OID 79645)
-- Name: meals trigger_update_meals_timestamp; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_meals_timestamp BEFORE UPDATE ON public.meals FOR EACH ROW EXECUTE FUNCTION public.update_timestamp();


--
-- TOC entry 6009 (class 2620 OID 79643)
-- Name: member_profiles trigger_update_member_profiles_timestamp; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_member_profiles_timestamp BEFORE UPDATE ON public.member_profiles FOR EACH ROW EXECUTE FUNCTION public.update_timestamp();


--
-- TOC entry 6012 (class 2620 OID 79646)
-- Name: orders trigger_update_orders_timestamp; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_orders_timestamp BEFORE UPDATE ON public.orders FOR EACH ROW EXECUTE FUNCTION public.update_timestamp();


--
-- TOC entry 6015 (class 2620 OID 79649)
-- Name: reviews trigger_update_reviews_timestamp; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_reviews_timestamp BEFORE UPDATE ON public.reviews FOR EACH ROW EXECUTE FUNCTION public.update_timestamp();


--
-- TOC entry 6007 (class 2620 OID 79641)
-- Name: users trigger_update_users_timestamp; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_update_users_timestamp BEFORE UPDATE ON public.users FOR EACH ROW EXECUTE FUNCTION public.update_timestamp();


--
-- TOC entry 5998 (class 2606 OID 79718)
-- Name: admin_profiles admin_profiles_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.admin_profiles
    ADD CONSTRAINT admin_profiles_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- TOC entry 5994 (class 2606 OID 79555)
-- Name: ai_conversations ai_conversations_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ai_conversations
    ADD CONSTRAINT ai_conversations_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- TOC entry 5980 (class 2606 OID 131084)
-- Name: deliverer_profiles deliverer_profiles_area_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.deliverer_profiles
    ADD CONSTRAINT deliverer_profiles_area_id_fkey FOREIGN KEY (area_id) REFERENCES public.delivery_areas(id);


--
-- TOC entry 5981 (class 2606 OID 79349)
-- Name: deliverer_profiles deliverer_profiles_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.deliverer_profiles
    ADD CONSTRAINT deliverer_profiles_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- TOC entry 5987 (class 2606 OID 79429)
-- Name: deliveries deliveries_deliverer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.deliveries
    ADD CONSTRAINT deliveries_deliverer_id_fkey FOREIGN KEY (deliverer_id) REFERENCES public.users(id);


--
-- TOC entry 5988 (class 2606 OID 79424)
-- Name: deliveries deliveries_order_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.deliveries
    ADD CONSTRAINT deliveries_order_id_fkey FOREIGN KEY (order_id) REFERENCES public.orders(id);


--
-- TOC entry 5989 (class 2606 OID 79468)
-- Name: elder_member_relations elder_member_relations_elder_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.elder_member_relations
    ADD CONSTRAINT elder_member_relations_elder_id_fkey FOREIGN KEY (elder_id) REFERENCES public.users(id);


--
-- TOC entry 5990 (class 2606 OID 79473)
-- Name: elder_member_relations elder_member_relations_member_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.elder_member_relations
    ADD CONSTRAINT elder_member_relations_member_id_fkey FOREIGN KEY (member_id) REFERENCES public.users(id);


--
-- TOC entry 5976 (class 2606 OID 106567)
-- Name: elderly_profiles elderly_profiles_health_tag_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.elderly_profiles
    ADD CONSTRAINT elderly_profiles_health_tag_id_fkey FOREIGN KEY (health_tag_id) REFERENCES public.health_tags(id);


--
-- TOC entry 5977 (class 2606 OID 79315)
-- Name: elderly_profiles elderly_profiles_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.elderly_profiles
    ADD CONSTRAINT elderly_profiles_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- TOC entry 5997 (class 2606 OID 79624)
-- Name: emergency_calls emergency_calls_elderly_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.emergency_calls
    ADD CONSTRAINT emergency_calls_elderly_id_fkey FOREIGN KEY (elderly_id) REFERENCES public.users(id);


--
-- TOC entry 6000 (class 2606 OID 79763)
-- Name: exceptions exceptions_delivery_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.exceptions
    ADD CONSTRAINT exceptions_delivery_id_fkey FOREIGN KEY (delivery_id) REFERENCES public.deliveries(id);


--
-- TOC entry 6005 (class 2606 OID 155689)
-- Name: favorites favorites_new_meal_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.favorites
    ADD CONSTRAINT favorites_new_meal_id_fkey FOREIGN KEY (meal_id) REFERENCES public.meals(id);


--
-- TOC entry 6006 (class 2606 OID 155684)
-- Name: favorites favorites_new_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.favorites
    ADD CONSTRAINT favorites_new_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- TOC entry 5978 (class 2606 OID 98304)
-- Name: elderly_profiles fk_elderly_community; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.elderly_profiles
    ADD CONSTRAINT fk_elderly_community FOREIGN KEY (community_id) REFERENCES public.communities(id);


--
-- TOC entry 5995 (class 2606 OID 79590)
-- Name: health_records health_records_created_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.health_records
    ADD CONSTRAINT health_records_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.users(id);


--
-- TOC entry 5996 (class 2606 OID 79585)
-- Name: health_records health_records_elderly_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.health_records
    ADD CONSTRAINT health_records_elderly_id_fkey FOREIGN KEY (elderly_id) REFERENCES public.users(id);


--
-- TOC entry 6002 (class 2606 OID 114706)
-- Name: health_reminders health_reminders_receiver_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.health_reminders
    ADD CONSTRAINT health_reminders_receiver_id_fkey FOREIGN KEY (receiver_id) REFERENCES public.users(id);


--
-- TOC entry 6003 (class 2606 OID 114701)
-- Name: health_reminders health_reminders_sender_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.health_reminders
    ADD CONSTRAINT health_reminders_sender_id_fkey FOREIGN KEY (sender_id) REFERENCES public.users(id);


--
-- TOC entry 5982 (class 2606 OID 79780)
-- Name: meals meals_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.meals
    ADD CONSTRAINT meals_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.categories(id);


--
-- TOC entry 5983 (class 2606 OID 79796)
-- Name: meals meals_tag_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.meals
    ADD CONSTRAINT meals_tag_id_fkey FOREIGN KEY (tag_id) REFERENCES public.tags(id);


--
-- TOC entry 5979 (class 2606 OID 79331)
-- Name: member_profiles member_profiles_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.member_profiles
    ADD CONSTRAINT member_profiles_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- TOC entry 5985 (class 2606 OID 79406)
-- Name: order_items order_items_meal_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT order_items_meal_id_fkey FOREIGN KEY (meal_id) REFERENCES public.meals(id);


--
-- TOC entry 5986 (class 2606 OID 79401)
-- Name: order_items order_items_order_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT order_items_order_id_fkey FOREIGN KEY (order_id) REFERENCES public.orders(id) ON DELETE CASCADE;


--
-- TOC entry 5984 (class 2606 OID 79385)
-- Name: orders orders_elderly_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_elderly_id_fkey FOREIGN KEY (elderly_id) REFERENCES public.users(id);


--
-- TOC entry 5999 (class 2606 OID 79733)
-- Name: payments payments_order_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.payments
    ADD CONSTRAINT payments_order_id_fkey FOREIGN KEY (order_id) REFERENCES public.orders(id);


--
-- TOC entry 5991 (class 2606 OID 131122)
-- Name: reviews reviews_deliverer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT reviews_deliverer_id_fkey FOREIGN KEY (deliverer_id) REFERENCES public.users(id);


--
-- TOC entry 5992 (class 2606 OID 79498)
-- Name: reviews reviews_elderly_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT reviews_elderly_id_fkey FOREIGN KEY (elderly_id) REFERENCES public.users(id);


--
-- TOC entry 5993 (class 2606 OID 79493)
-- Name: reviews reviews_order_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT reviews_order_id_fkey FOREIGN KEY (order_id) REFERENCES public.orders(id);


--
-- TOC entry 6004 (class 2606 OID 114758)
-- Name: staff_schedules staff_schedules_staff_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.staff_schedules
    ADD CONSTRAINT staff_schedules_staff_id_fkey FOREIGN KEY (staff_id) REFERENCES public.users(id);


--
-- TOC entry 6001 (class 2606 OID 81930)
-- Name: voice_synthesis voice_synthesis_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.voice_synthesis
    ADD CONSTRAINT voice_synthesis_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


-- Completed on 2026-04-13 15:34:59

--
-- PostgreSQL database dump complete
--

\unrestrict 9iuTt60GbbZu5pBx5Ra7sPASr1oA5BNSKX0b2NcPw1MkeSiY9JnsDfxZ2sV3qK7

