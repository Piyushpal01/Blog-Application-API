from rest_framework import serializers
from django.contrib.auth import get_user_model  # good way to use default User model
from .models import Blog

# this seralizer enables user to create account
class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        # get_user_model() -> Django ka function hai jo currently active User model ko return karta hai — chahe wo default ho ya custom.
        model = get_user_model()
        fields = ["id", "email", "username", "first_name", "last_name", "password"]
        extra_kwargs = {
            'password':{'write_only':True} # this line say that our password can be only write, it's hidden not cannot be seen
        }

    # Create method
    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        password = validated_data['password']

        # this simply helps to get user model we are using currently we're using customuser model, it's best practice.
        user = get_user_model() 
        new_user = user.objects.create(username=username, email=email, first_name=first_name, last_name=last_name)

        # setting password for new user
        new_user.set_password(password)
        new_user.save()
        return new_user
    
# to return author object not just author's id.
class SimpleAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model=get_user_model()
        fields=["id", "username", "first_name", "last_name", "profile_pic"]

class BlogSerializer(serializers.ModelSerializer):
    author = SimpleAuthorSerializer(read_only=True) # serializing the author object here

    class Meta:
        model=Blog
        fields="__all__"

# for updating user profile
class UpdateUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["id", "email", "username", "first_name", "last_name", "bio", "profile_pic", "job_title", "facebook", "youtube", "instagram", "twitter", "linkedin", "github"]
        
        
# for serializing user info
class UserInfoSerializer(serializers.ModelSerializer):
    author_posts = serializers.SerializerMethodField()  # SerializerMethodField ek special field hai jo automatically model me nahi hota.Iska use hum custom data ko serializer me add karne ke liye karte hain, jo directly model field nahi hota. ye apne corresponding get_<fieldname>() method ko call karke custom data provide karta hai.

    class Meta:
        model = get_user_model()
        fields = ["id", "email", "username", "first_name", "last_name", "bio", "profile_pic", "job_title", "facebook", "youtube", "instagram", "twitter", "linkedin", "github", "author_posts"]

    def get_author_posts(self, user):
        blogs = Blog.objects.filter(author=user)[:9]
        serializer = BlogSerializer(blogs, many=True)
        return serializer.data