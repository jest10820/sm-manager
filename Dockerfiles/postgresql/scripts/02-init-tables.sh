#!/bin/bash

##### MISSING STATS TABLE

set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" supermanager <<-EOSQL

CREATE SEQUENCE IF NOT EXISTS custom_position_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE custom_position_id_seq OWNER TO manager;

CREATE TABLE IF NOT EXISTS custom_position (
    id integer DEFAULT nextval('custom_position_id_seq'::regclass) NOT NULL,
    pos_id integer NOT NULL,
    description text NOT NULL
);


ALTER TABLE custom_position OWNER TO manager;
COMMENT ON TABLE custom_position IS 'Define custom positions for players';

CREATE SEQUENCE IF NOT EXISTS game_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE game_id_seq OWNER TO manager;

CREATE TABLE IF NOT EXISTS game (
    id integer DEFAULT nextval('game_id_seq'::regclass) NOT NULL,
    local_team_id integer NOT NULL,
    visiting_team_id integer NOT NULL,
    local_points integer,
    visiting_points integer,
    game_type_id integer NOT NULL,
    jornada integer DEFAULT 0 NOT NULL,
    date date NOT NULL,
    neutral_court boolean DEFAULT false NOT NULL
);


ALTER TABLE game OWNER TO manager;
COMMENT ON TABLE game IS 'List of all games';


CREATE SEQUENCE IF NOT EXISTS game_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE game_type_id_seq OWNER TO manager;

CREATE TABLE IF NOT EXISTS game_type (
    id integer DEFAULT nextval('game_type_id_seq'::regclass) NOT NULL,
    type text NOT NULL
);


ALTER TABLE game_type OWNER TO manager;
COMMENT ON TABLE game_type IS 'List of type of game played';

CREATE SEQUENCE IF NOT EXISTS nationality_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE nationality_id_seq OWNER TO manager;

CREATE TABLE IF NOT EXISTS nationality (
    id integer DEFAULT nextval('nationality_id_seq'::regclass) NOT NULL,
    description text NOT NULL
);


ALTER TABLE nationality OWNER TO manager;
COMMENT ON TABLE nationality IS 'List of players'' nationality';


CREATE SEQUENCE IF NOT EXISTS player_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE player_id_seq OWNER TO manager;

CREATE TABLE IF NOT EXISTS player (
    initial_prize integer NOT NULL,
    custom_pos_id integer NOT NULL,
    id integer DEFAULT nextval('player_id_seq'::regclass) NOT NULL,
    name text NOT NULL,
    nationality_id integer NOT NULL,
    team_id integer NOT NULL
);


ALTER TABLE player OWNER TO manager;
COMMENT ON TABLE player IS 'List of all players';


CREATE SEQUENCE IF NOT EXISTS position_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE position_id_seq OWNER TO manager;

CREATE TABLE IF NOT EXISTS postition (
    id integer DEFAULT nextval('position_id_seq'::regclass) NOT NULL,
    type text NOT NULL
);


ALTER TABLE postition OWNER TO manager;
COMMENT ON TABLE postition IS 'Player position according to supermanager';


CREATE SEQUENCE IF NOT EXISTS team_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE team_id_seq OWNER TO manager;

CREATE TABLE IF NOT EXISTS team (
    id integer DEFAULT nextval('team_id_seq'::regclass) NOT NULL,
    name text NOT NULL
);


ALTER TABLE team OWNER TO manager;

COMMENT ON TABLE team IS 'Table with all the teams';

ALTER TABLE ONLY custom_position
    ADD CONSTRAINT custom_position_pkey PRIMARY KEY (id);

ALTER TABLE ONLY game
    ADD CONSTRAINT game_pkey PRIMARY KEY (id);

ALTER TABLE ONLY game_type
    ADD CONSTRAINT game_type_pkey PRIMARY KEY (id);

ALTER TABLE ONLY nationality
    ADD CONSTRAINT nationality_pkey PRIMARY KEY (id);

ALTER TABLE ONLY player
    ADD CONSTRAINT player_pkey PRIMARY KEY (id);

ALTER TABLE ONLY postition
    ADD CONSTRAINT postition_pkey PRIMARY KEY (id);

ALTER TABLE ONLY team
    ADD CONSTRAINT team_pkey PRIMARY KEY (id);

CREATE INDEX IF NOT EXISTS fki_fk_custom_pos_id ON player USING btree (custom_pos_id);
CREATE INDEX IF NOT EXISTS fki_fk_game_type_id ON game USING btree (game_type_id);
CREATE INDEX IF NOT EXISTS fki_fk_nationality_id ON player USING btree (nationality_id);
CREATE INDEX IF NOT EXISTS fki_fk_pos_id ON custom_position USING btree (pos_id);
CREATE INDEX IF NOT EXISTS fki_fk_team_id ON player USING btree (team_id);
CREATE INDEX IF NOT EXISTS fki_fk_visiting_team_id ON game USING btree (visiting_team_id);

ALTER TABLE ONLY player
    ADD CONSTRAINT fk_custom_pos_id FOREIGN KEY (custom_pos_id) REFERENCES custom_position(id) ON UPDATE CASCADE;

ALTER TABLE ONLY game
    ADD CONSTRAINT fk_game_type_id FOREIGN KEY (game_type_id) REFERENCES game_type(id) ON UPDATE CASCADE;

ALTER TABLE ONLY game
    ADD CONSTRAINT fk_local_team_id FOREIGN KEY (local_team_id) REFERENCES team(id) ON UPDATE CASCADE;

ALTER TABLE ONLY player
    ADD CONSTRAINT fk_nationality_id FOREIGN KEY (nationality_id) REFERENCES nationality(id) ON UPDATE CASCADE;

ALTER TABLE ONLY custom_position
    ADD CONSTRAINT fk_pos_id FOREIGN KEY (pos_id) REFERENCES postition(id) ON UPDATE CASCADE;

ALTER TABLE ONLY player
    ADD CONSTRAINT fk_team_id FOREIGN KEY (team_id) REFERENCES team(id) ON UPDATE CASCADE;

ALTER TABLE ONLY game
    ADD CONSTRAINT fk_visiting_team_id FOREIGN KEY (visiting_team_id) REFERENCES team(id) ON UPDATE CASCADE;

EOSQL
