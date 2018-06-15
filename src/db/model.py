import psycopg2
from configs import DB_NAME, PW, HOST, USER, TABLE_NAME


class DB_Model:

    def __init__(self):
        self.con = psycopg2.connect(
            host=HOST, database=DB_NAME,user=USER, password=PW)
        self.cur = self.con.cursor()

    def calculate(self):
        print 'Calculando...'
        self.cur.execute('''
            INSERT INTO queimadas_tis (id, data, geom)
                    SELECT 
                        p.id as id,
                        to_date(to_char(date(r.datahora), 'YYYY-MM-DD'), 'YYYY-MM-DD') as date,
                        (ST_Dump(r.geom)).geom AS geom
                    FROM 
                        {} as r,
                        (SELECT id, geom FROM terras_indigenas) as p
                    WHERE
                        ST_intersects(r.geom, p.geom)
                        AND NOT EXISTS (
                            SELECT * FROM queimadas_tis as q 
                                WHERE q.id = p.id 
                                AND q.data = to_date(to_char(date(r.datahora), 'YYYY-MM-DD'), 'YYYY-MM-DD') 
                                AND q.geom = r.geom
                        )
        '''.format(TABLE_NAME))
        self.cur.execute('''
            INSERT INTO queimadas_tis_buffer (id, data, geom)
                    SELECT 
                        p.id as id,
                        to_date(to_char(date(r.datahora), 'YYYY-MM-DD'), 'YYYY-MM-DD') as date,
                        (ST_Dump(r.geom)).geom AS geom
                    FROM 
                        {} as r,
                        (SELECT id, geom FROM terras_indigenas_buffer_10km) as p
                    WHERE
                        ST_intersects(r.geom, p.geom)
                        AND NOT EXISTS (
                            SELECT * FROM queimadas_tis as q 
                                WHERE q.id = p.id 
                                AND q.data = to_date(to_char(date(r.datahora), 'YYYY-MM-DD'), 'YYYY-MM-DD') 
                                AND q.geom = r.geom
                        )
        '''.format(TABLE_NAME))
        self.con.commit()
        print "Calculo concluido"

    def check_if_table_exists(self):

        self.cur.execute('''
        SELECT EXISTS (
   SELECT 1
   FROM   information_schema.tables 
   WHERE  table_schema = 'public'
   AND    table_name = '{}'
   );
'''.format(TABLE_NAME))
        exists = self.cur.fetchone()[0]    
        print exists

        return exists


    def drop_table(self):
        self.cur.execute('''
        DROP TABLE {};
        '''.format(TABLE_NAME))
        self.con.commit()
        print "Table dropada"
    def close_conn(self):
        self.con.close()

    # def select(self):
    #     self.cur.execute('select * from imazon_sad_desmatamento')
    #     print self.cur.fetchall()
    def database_calculate_and_drop_table(self):

        self.calculate()
        self.drop_table()
        self.close_conn()
# db = DB_Model()
# db.drop_table()
# db.close_conn()
