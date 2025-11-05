
class User:
    def __init__(self, user_id, username, password, watchlist=None, favorite_movies=None):
        self._user_id = user_id
        self._username = username
        self._password = password
        self._watchlist = watchlist
        self._favorite_movies = favorite_movies

    _watchlist = {}
    _favorite_movies = {}

    def set_user_id(self, user_id):
        """Users.json dosyasını kontrol ederek yeni kullanıcılara rastgele int id'ler atayan bir sistem tasarla."""
        _user_id = user_id
        pass
    
    def set_user_name(self, username):
        _username = username    # username daha önce alınmış ise ERROR!


    def set_password(self, password):
        _password = password    # password daha önce alınmış ise ERROR!


    def get_user_id(self):
        print(self._user_id)

    def get_user_name(self):
        print(self._username)

    def get_password(self):
        print(self._password)

    def add_to_watchlist(self):
        pass

    def remove_from_watchlist(self):
        pass

    def add_to_favorite_movies(self):
        pass

    def remove_from_favorite_movies(self):
        pass
        
        
# user = User(1, "testuser", "password123")
# user.get_user_id()