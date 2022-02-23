from pymongo import MongoClient


class MongoDBCOnnection:
    def __init__(self):
        self.connection = None

    def __enter__(self):
        self.connection = MongoClient(
            "mongodb+srv://akshayavhad89:<password>@cluster0.w9kab.mongodb.net/swarm_production?retryWrites=true&w=majority")

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()
