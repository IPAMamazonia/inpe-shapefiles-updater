DB_NAME = ''
HOST = ''
USER = ''
PW = ''
TABLE_NAME = ''
TERMINAL_COMMAND = 'cd {} && shp2pgsql -s 4326 {} {} | PGPASSWORD=' + \
    PW+' psql -h '+HOST+' -U postgres -d '+DB_NAME
