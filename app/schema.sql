drop table if exists users;
drop table if exists transactions;

create table users (
  id integer primary key autoincrement,

  username text not null,
  password text not null,
  realname text not null,
  address text not null,
  email text not null,

  items_available text DEFAULT "",
  items_desired text DEFAULT "",

  points integer DEFAULT 0,
  num_given integer DEFAULT 0,
  num_bought integer DEFAULT 0,

  geo_x float Default 0,
  geo_y float Default 0,

  created_at timestamp DEFAULT CURRENT_TIMESTAMP
);

create table transactions (
  id integer primary key autoincrement,

  name_from text not null,
  name_to text not null,
  item text not null,
  price integer not null,

  created_at timestamp DEFAULT CURRENT_TIMESTAMP
);
