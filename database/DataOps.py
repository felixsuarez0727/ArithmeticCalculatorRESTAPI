import sqlite3
from datetime import datetime
from models.OperationRecord import OperationRecord

class DataOps:
    database='db.db'
    
    def ValidateUser(self, _user, _pass):
        try:
            with sqlite3.connect(self.database) as conn:
                cursor = conn.cursor()
                query = 'SELECT * FROM User where username = ? and password = ?'
                
                cursor.execute(query, (_user, _pass))
                rows = cursor.fetchall() 
                return rows
        except Exception as e:
            raise Exception('Error retrieving data: ' + str(e))
    
    def SaveToken(self, _user, _token):
        try:
            with sqlite3.connect(self.database) as conn:
                cursor = conn.cursor()
                query = '''
                    INSERT INTO ACCESSTOKEN
                    (username,accesstoken,issuedate)
                    VALUES (?,?,?)
                '''
                now = datetime.now()
                cursor.execute(query, (_user, _token, now.strftime("%Y-%m-%d %H:%M:%S") ))
                # Confirmar los cambios
                conn.commit()
                return True
        except Exception as e:
            raise Exception('Error retrieving data: ' + str(e))
    
    def RevokeToken(self, _token):
        try:
            with sqlite3.connect(self.database) as conn:
                cursor = conn.cursor()


                query = 'SELECT * FROM ACCESSTOKEN where accesstoken = ? and revokedate is null'
                
                cursor.execute(query, (_token,))
                rows = cursor.fetchall() 

                if not rows:
                    raise Exception('Token has not been found!')

                query = '''
                    UPDATE ACCESSTOKEN
                    SET
                    REVOKEDATE = ?
                    WHERE ACCESSTOKEN = ?
                '''
                now = datetime.now()
                cursor.execute(query, (now.strftime("%Y-%m-%d %H:%M:%S"), _token ))
                # Confirmar los cambios
                conn.commit()
                return "Logout completed!"
        except Exception as e:
            raise Exception('Error retrieving data: ' + str(e))
    
    def ValidateToken(self, _token):
        try:
            with sqlite3.connect(self.database) as conn:
                cursor = conn.cursor()


                query = 'SELECT accesstoken FROM ACCESSTOKEN where accesstoken = ? and revokedate is null'
                
                cursor.execute(query, (_token,))
                rows = cursor.fetchall() 

                if not rows:
                    raise Exception('Token not found or revoked!')
                
                tk = rows[0]
                return str(tk[0])
        except Exception as e:
            raise Exception('Error retrieving data: ' + str(e))

    def SaveOperationRecord(self, operation, user, amount, balance, operation_response):
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        try:
            # Iniciar una transacción
            conn.execute('BEGIN TRANSACTION;')
             
            #INSERT OPERATION
            
            query = 'SELECT * FROM User where username = ? '
                
            cursor.execute(query, (user,))
            rows = cursor.fetchone() 
            if not rows:
                raise Exception('User not found!')
               
            user_id = rows[0]
                               
            #INSERT OPERATION
            query = '''
                INSERT INTO operation
                (type, cost)
                VALUES (?, ?);
            '''
                
            cursor.execute(query, (operation,1))
            last_id  = cursor.lastrowid

            
            #INSERT RECORD
            query = '''
                INSERT INTO RECORD
                (operation_id, user_id, amount, 
                user_balance, operation_response, date)
                VALUES (?, ?, ?, ?, ?, ?);
                '''
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            cursor.execute(query, 
                           (last_id, user_id, amount,
                           balance, operation_response, now))               
            conn.commit()               
            return True            
                           
        except Exception as e:
            conn.rollback()
            raise Exception('Error saving record: ' + str(e))
        finally:            
            conn.close()

    def OperationRecords(
        self,
        user: str = "dev",
        page: int = 1,
        per_page: int = 10,
        sort_by: str = 'date',
        sort_order: str = 'asc',
        search: str = ''
    ):
        with sqlite3.connect(self.database) as conn:
            conn.row_factory = sqlite3.Row 
            cursor = conn.cursor()

            query = 'SELECT id FROM User where username = ? '
                    
            cursor.execute(query, (user,))
            rows = cursor.fetchone() 
            if not rows:
                raise Exception('User not found!')
                
            user_id = rows[0]
         
            if sort_by == 'id':
                sort_by='r.'+sort_by

            # Construir la consulta SQL con búsqueda, orden y paginación
            query = f"""
            SELECT r.id, r.operation_id, r.user_id, r.amount, r.user_balance, r.operation_response, r.date, r.deleted_at, o.type FROM record r
            inner join operation o
            on o.id = r.operation_id 
            WHERE r.user_id = ? AND r.deleted_at is null AND (o.type LIKE ? OR r.operation_response LIKE ? OR r.amount LIKE ? OR CAST(r.id AS TEXT) LIKE ? )

            ORDER BY {sort_by} {sort_order}
            LIMIT ? OFFSET ?
            """
            
            
            # Cálculo del offset
            offset = (page - 1) * per_page
            
            

            # Ejecutar la consulta
            cursor.execute(query, (user_id, f'%{search}%', f'%{search}%', f'%{search}%',f'{search}%', per_page, offset))
            rows = cursor.fetchall()
             
            # Manejar el caso donde no hay resultados
            if not rows:
                return []
                
            try:
                records = [OperationRecord(
                    id= int(row['id']),
                    operation_id = int(row['operation_id']),
                    user_id = int(row['user_id']),
                    amount = str(row['amount']),
                    user_balance = float(row['user_balance']),
                    operation_response = str(row['operation_response']),
                    date = str(row['date']),
                    deleted_at = row['deleted_at'],
                    type = str(row['type'])
                ) for row in rows]
                          
                return records
            except Exception as e:
                return str(e)

    def SoftDelete(self, user, id_record):
        try:
            with sqlite3.connect(self.database) as conn:
                cursor = conn.cursor()

                query = 'SELECT id FROM User where username = ? '
                    
                cursor.execute(query, (user,))
                rows = cursor.fetchone() 
                if not rows:
                    raise Exception('User not found!')
                    
                user_id = rows[0]
                if not rows:
                    raise Exception('User not found!')

                
                query = 'SELECT * FROM record where id = ? and user_id= ? and deleted_at is null'
               
                cursor.execute(query, (id_record, user_id))
                rows = cursor.fetchall() 

               
                if not rows:
                    raise Exception('Record not found, does not belong to User or has been deleted before!')

                query = '''
                    UPDATE record
                    SET
                    deleted_at = ?
                    WHERE id = ?
                '''
                now = datetime.now()
                cursor.execute(query, (now.strftime("%Y-%m-%d %H:%M:%S"), id_record ))
                # Confirmar los cambios
                conn.commit()
                return "Process is done!"
        except Exception as e:
            raise Exception('Error retrieving data: ' + str(e))
