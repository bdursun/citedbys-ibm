from databases.alchemy import  DatabaseAlc
class CustomException(Exception):
    def __init__(self, message,id):
        self.message = message
        self.id = id
        super().__init__(self.message)
        self.save_to_database()

    def save_to_database(self):
        db = DatabaseAlc('orchestrator/db/citedbys.db')
        db.insert_exception(self.id, self.message)