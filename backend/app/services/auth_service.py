from app.config import firebase_auth


class AuthService:

    def verify_admin(self, token):
        decoded = firebase_auth.verify_token(token)

        if not decoded:
            raise ValueError("Invalid token")

        return decoded
