CREATE TABLE config (
    config text NOT NULL
);

CREATE TABLE logs (
    type text NOT NULL,
    device text NOT NULL,
    time text NOT NULL,
    date text NOT NULL,
    location text NOT NULL,
    label text NULL
);

insert into config ('config') values ('{}');