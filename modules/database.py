from tinydb import TinyDB, Query
from tinydb.operations import set as dset

class DB:
    __message__ = 'Ошибка при работе с TinyDB: '

    def __init__(self, db_name):
        try:
            self.db_ = TinyDB(db_name)
            if len(self.db_.tables()) == 0:
                banwords = self.db_.table('banwords')
                banwords.insert({'word': ''})
                self.db_.table('vault')
                self.db_.table('notes')
                self.db_.table('allowed')
                self.db_.table('modes')

        except Exception as error:
            print(self.__message__, error)


    #note functions
    def save(self, name, id, table):
        try:
            notes = self.db_.table(table)
            notes.insert({'name': name, 'msg_id': id})
            return True
        except Exception as error:
            print(self.__message__, error)
            return False


    def get(self, name, table):
        try:
            note = Query()
            notes = self.db_.table(table)
            res = notes.get(note.name == name)
            if res is not None:
                return res['msg_id']
            else:
                return None
        except Exception as error:
            print(self.__message__, error)
            return None
    
    def get_all(self, table):
        try:
            notes = self.db_.table(table)
            return notes.all()
        except Exception as error:
            print(self.__message__, error)
            return None
    
    def noted(self, name, table):
        note = Query()
        notes = self.db_.table(table)
        res = notes.get(note.name == name)
        if res is None:
            return False
        else:
            return True
    

    def deln(self, name, table):
        try:
            note = Query()
            notes = self.db_.table(table)
            res = notes.remove(note.name == name)
            if len(res) > 0:
                return True
            else:
                return False
        except Exception as error:
            print(self.__message__, error)
            return False


    def del_all(self, table):
        try:
            notes = self.db_.table(table)
            notes.truncate()
            return True
        except Exception as error:
            print(self.__message__, error)
            return False
    

    def add_user(self, id):
        try:
            allowed = self.db_.table('allowed')
            allowed.insert({'id': id})
            return True
        except Exception as error:
            print(self.__message__, error)
            return False
    
    def all_users(self):
        try:
            allowed = self.db_.table('allowed')
            return allowed.all()
        except Exception as error:
            print(self.__message__, error)
            return False
    

    def del_user(self, id):
        try:
            user = Query()
            allowed = self.db_.table('allowed')
            res = allowed.remove(user.id == id)
            if res is None:
                return False
            else:
                return True
        except Exception as error:
            print(self.__message__, error)
            return False
    

    def allowed(self, id):
        user = Query()
        allowed = self.db_.table('allowed')
        res = allowed.get(user.id == id)
        if res is None:
            return False
        else:
            return res['id']


    def addword(self, word):
        try:
            words = self.db_.table('banwords')
            words.insert({'word': word})
            return True
        except Exception as error:
            print(self.__message__, error)
            return False
    
    
    def delword(self, word):
        try:
            words = Query()
            wordst = self.db_.table('banwords')
            res = wordst.remove(words.word == word)
            if len(res) > 0:
                return True
            else:
                return False
        except Exception as error:
            print(self.__message__, error)
            return False
    
    
    def checkword(self, word):
        words = Query()
        wordst = self.db_.table('banwords')
        res = wordst.get(words.word == word)
        if res is None:
            return False
        else:
            return True
    
    
    def getwords(self):
        try:
            words = self.db_.table('banwords')
            return [el['word'] for el in words.all()]
        except Exception as error:
            print(self.__message__, error)
            return False
    
    
    def checkmode(self, chat_id, mode_name):
        mode = Query()
        modes = self.db_.table('modes')
        res = modes.get((mode[mode_name] == True) & (mode.chat_id == chat_id))
        if res is None:
            return False
        else:
            return True
    
    
    def checkchat(self, chat_id):
        mode = Query()
        modes = self.db_.table('modes')
        res = modes.get(mode.chat_id == chat_id)
        if res is None:
            return False
        else:
            return True
        
    
    def addmode(self, chat_id, mode_name, state):
        try:
            mode = Query()
            modes = self.db_.table('modes')
            res = modes.search(mode[mode_name].exists())
            if res is None:
                return False
            
            modes.upsert({'chat_id': chat_id, 'nopolitics': False, 'mutepolitics': False, 'autoban': False, 'autowarn': False}, mode.chat_id == chat_id)
            
            modes.update(dset(mode_name, state), mode.chat_id == chat_id)
            return True
        except Exception as error:
            print(self.__message__, error)
            return False
    
    
    def getmodes(self, chat_id):
        try:
            mode = Query()
            modes = self.db_.table('modes')
            return modes.get(mode.chat_id == chat_id)
        except Exception as error:
            print(self.__message__, error)
            return False
