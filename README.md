createdb -h localhost -p 5432 -U postgres SNCB

psql -h localhost -p 5432 -U postgres -d SNCB -c 'CREATE EXTENSION PostGIS';

