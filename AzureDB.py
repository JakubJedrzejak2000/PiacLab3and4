import pypyodbc
import azurecred


class AzureDB:
    dsn = 'DRIVER=' + azurecred.AZDBDRIVER + ';SERVER=' + azurecred.AZDBSERVER + ';PORT=1433;DATABASE=' + azurecred.AZDBNAME + ';UID=' + azurecred.AZDBUSER + ';PWD=' + azurecred.AZDBPW

    def __init__(self):
        self.conn = pypyodbc.connect(self.dsn)
        self.cursor = self.conn.cursor()

    def finalize(self):
        if self.conn:
            self.conn.close()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.finalize()

    def __enter__(self):
        return self

    def azureGetData(self):
        try:
            self.cursor.execute("SELECT * from data")
            data = self.cursor.fetchall()
            return data
        except pypyodbc.DatabaseError as exception:
            print("Failed to execute query")
            print(exception)
            exit(1)

    def azureGetParticularDate(self, id):
        try:
            self.cursor.execute("SELECT * from data WHERE id=" + id)
            data = self.cursor.fetchall()
            return data
        except pypyodbc.DatabaseError as exception:
            print("Failed to execute query")
            print(exception)
            exit(1)

    def azureAddData(self, name, text, data):
        self.cursor.execute(
            "INSERT into data (name, text, date) values ('" + name + "', '" + text + "', '" + data + "')")
        self.conn.commit()

    def azureDeleteData(self, id):
        self.cursor.execute("DELETE FROM data WHERE id=" + id)
        self.conn.commit()

    def azureUpdateData(self, id, name, text, data):
        self.cursor.execute(
            "UPDATE data SET name='" + name + "', text='" + text + "', date='" + data + "' WHERE id=" + id
        )
        self.conn.commit()
