from django.shortcuts import get_object_or_404
from .models import Blog
from .serializers import UserRegistrationSerializer, BlogSerializer, UpdateUserProfileSerializer, UserInfoSerializer, SimpleAuthorSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth import get_user_model


# Create your views here.

# pagination class for listing 3 blogs per page
class BlogListPagination(PageNumberPagination):
    page_size = 3 # Number of blog articles per page


# listing blogs and paginating it, having 3 blog articles per page
@api_view(['GET'])
def blog_list(req):
    # Only get blogs that are not drafts and order by published date (newest first)
    blogs = Blog.objects.filter(is_draft=False).order_by('-published_at')    #  Force newest published first
    
    # Filter by category if provided in query params
    category = req.query_params.get('category')
    if category:
        blogs = blogs.filter(category__iexact=category)

    # Paginate the (filtered) blogs
    paginator = BlogListPagination()    # Initialize custom pagination class
    paginated_blogs = paginator.paginate_queryset(blogs, req)   # Apply pagination to the blog queryset using request
    
    serializer = BlogSerializer(paginated_blogs, many=True)
    return paginator.get_paginated_response(serializer.data)    # Returning paginated response with serialized data

# get particular blog based on slug for user-friendly.
@api_view(['GET'])
def get_blog(req, slug):
    blog = get_object_or_404(Blog, slug=slug)
    serializer = BlogSerializer(blog)
    return Response(serializer.data)

# Registering new users. -> supports post req only as for registering.
@api_view(["POST"])
def register_user(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# blog can only be create if user is logged in
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_blog(req):
    user = req.user
    serializer = BlogSerializer(data=req.data)
    if serializer.is_valid():
        serializer.save(author=user) # author=user means -> “Jo blog create ho raha hai, uska author wo user ho jo abhi authenticated hai (i.e. login hai).”
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Updating blog
@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated]) # user can only update if he is authenticated and has to update his blog not others.
def update_blog(req, pk):
    user = req.user # get logged in user
    blog = Blog.objects.get(id=pk)
    
    # if current blog author is not equal to logged in user he must not update.
    if blog.author != user:
        return Response({'error':'You are not the author of this blog!'}, status=status.HTTP_403_FORBIDDEN)
    
    serializer = BlogSerializer(blog, data=req.data, partial=(req.method == 'PATCH'))
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# Deleting Blog
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_blog(req, pk):
    blog = Blog.objects.get(id=pk)
    user = req.user
    
    if blog.author != user:
        return Response({'error':'You are not the author of this blog!'}, status=status.HTTP_403_FORBIDDEN)
    
    blog.delete()
    return Response({'message':'Blog delete successfully'}, status=status.HTTP_204_NO_CONTENT)

# view for updating user profile, serialzier
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user_profile(req):
    # print(req.data)
    user = req.user
    serializer = UpdateUserProfileSerializer(user, data=req.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# get user's username
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_username(req):
    user = req.user
    # print(user)
    username = user.username
    return Response({"username": username})

# get user's userinfo
@api_view(['GET'])
def get_userinfo(req, username):
    User = get_user_model()
    user = get_object_or_404(User, username=username)
    serializer = UserInfoSerializer(user)
    return Response(serializer.data)

# get user
@api_view(['GET'])
def get_user(req, pk):
    User = get_user_model()
    try:
        existing_user = User.objects.get(pk=pk)
        serializer = SimpleAuthorSerializer(existing_user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)