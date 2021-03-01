class AuthManager(object):
    def __init__(self):
        self.users = {}
    
    def register_user(self, user, pwd):
        if user in self.users:
            raise Exception("L'utilisateur '%s' existe deja." % user)
        self.users[user] = pwd
    
    def is_valid_user(self, user, pwd):
        if user not in self.users:
            return False
        if self.users[user] == pwd:
            return True
        
        return False