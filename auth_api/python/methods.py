import jwt
import mysql.connector
import hashlib

class Token:

    def generate_token(self, username, password):
        if DBConnector().isValid(username,password) is True:
            role = DBConnector().getRole(username,password)

        encodedJWT = jwt.encode({"Role": role}, 'my2w7wjd7yXF64FIADfJxNs1oupTGAuW', algorithm="HS256")
        return encodedJWT


class Restricted:

    def access_data(self, authorization):       
         
        return jwt.decode(authorization, 'my2w7wjd7yXF64FIADfJxNs1oupTGAuW', algorithms=['HS256'])
class DBConnector:
    
    def isValid(self, username, password):

        try:
            connection = mysql.connector.connect(host='sre-bootcamp-selection-challenge.cabf3yhjqvmq.us-east-1.rds.amazonaws.com',
                                                database='bootcamp_tht',
                                                user='secret',
                                                password='jOdznoyH6swQB9sTGdLUeeSrtejWkcw')

            cursor = connection.cursor()
            sql_select_Query = "SELECT password, salt FROM users WHERE username = %s"
            cursor.execute(sql_select_Query, (username,))
            records = cursor.fetchall()

            for row in records:
                storedPwd = row[0]
                salt= row[1]

            hashPwd = hashlib.sha512( str(password+salt ).encode("utf-8") ).hexdigest()
          

            return hashPwd == storedPwd

        except mysql.connector.Error as e:
            print("Error reading data from MySQL table", e)
        finally:
            if connection.is_connected():
                connection.close()
                cursor.close()


    def getRole(self, username, password):
        try:
            connection = mysql.connector.connect(host='sre-bootcamp-selection-challenge.cabf3yhjqvmq.us-east-1.rds.amazonaws.com',
                                                database='bootcamp_tht',
                                                user='secret',
                                                password='jOdznoyH6swQB9sTGdLUeeSrtejWkcw')

            cursor = connection.cursor()
            sql_select_Query = "SELECT role FROM users WHERE username = %s"
            cursor.execute(sql_select_Query, (username,))
            records = cursor.fetchall()

            for row in records:
                role = row[0]

            return role
        except mysql.connector.Error as e:
            print("Error reading data from MySQL table", e)
        finally:
            if connection.is_connected():
                connection.close()
                cursor.close()