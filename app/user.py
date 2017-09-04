from flask import jsonify

class User:

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def to_json(self):
        return jsonify({
            "email": self.email,
            "link": "/users/" + self.username
        })
