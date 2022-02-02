CREATE TABLE address_portfolio (
    address text PRIMARY KEY,
    assets_value real,
    deposited_value real,
    borrowed_value real,
    locked_value real,
    staked_value real,
    total_value real,
    updated_at timestamp without time zone DEFAULT now() NOT NULL
);


CREATE TABLE params (
    name text PRIMARY KEY,
    value text NOT NULL,
    updated_at timestamp without time zone DEFAULT now() NOT NULL
);


CREATE TABLE status (
    id SEQUENCE PRIMARY KEY,
    author_address text NOT NULL,
    text text NOT NULL,
    block_number integer NOT NULL
);

