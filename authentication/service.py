from authentication import serializers as auth_serializers
class AuthService:
    def handle_profile_view(user):
        serializers = auth_serializers.UserSerializer(user)
        return 200, serializers.data