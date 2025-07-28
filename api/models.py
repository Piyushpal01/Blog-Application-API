from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils.text import slugify
from django.utils import timezone

# Create your models here.
class CustomUser(AbstractUser):
    bio=models.TextField(blank=True, null=True)
    profile_pic=models.ImageField(upload_to="profile_img", blank=True, null=True)
    job_title = models.CharField(max_length=50, blank=True, null=True)
    
    # social media links
    facebook=models.URLField(max_length=255, blank=True, null=True)
    youtube=models.URLField(max_length=255, blank=True, null=True)
    instagram=models.URLField(max_length=255, blank=True, null=True)
    twitter=models.URLField(max_length=255, blank=True, null=True)
    linkedin=models.URLField(max_length=255, blank=True, null=True)
    github=models.URLField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.username

# Blogs
class Blog(models.Model):
    
    # left value is stored in DB and right value is displayed on panel/form.
    CATEGORY = (
        ('Frontend', 'Frontend'),
        ('Backend', 'Backend'),
        ('FullStack', 'FullStack'),
        ('Web3', 'Web3'),
        ('Healthcare', 'Healthcare'),
        ('Technology', 'Technology'),
        ('Economy', 'Economy'),
        ('Business', 'Business'),
        ('Sports', 'Sports'),
        ('Lifestyle', 'Lifestyle'),
    )

    title=models.CharField(max_length=255)
    slug=models.SlugField(unique=True, blank=True, max_length=255)
    content=models.TextField()
    # there can be multiple blogs for one user and one user can have multiple blogs, so one to many rs. 
    author=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name="blogs", null=True) # it's a foreign key rs to out user
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    published_at=models.DateTimeField(blank=True, null=True)
    is_draft=models.BooleanField(default=True)
    category=models.CharField(max_length=255, choices=CATEGORY, blank=False, null=False)
    featured_image=models.ImageField(upload_to="blog_img", blank=True, null=True)

    class Meta:
        # as to make the latest blog appear first than the other old blogs.
        ordering=["-published_at"]

    def __str__(self):
        return self.title
    
    # customizing save method
    def save(self, *args, **kwargs):
        # Step 1: Slugify the blog title (e.g., "My First Blog!" -> "my-first-blog")
        base_slug = slugify(self.title)  # title ko URL-friendly bana diya

        slug = base_slug  # initial slug same as base_slug
        num = 1  # number append karne ke liye counter

        # Step 2: Check if slug already exists in DB
        while Blog.objects.filter(slug=slug).exists():
            # If exists, append a number to make it unique (e.g., "my-first-blog-1")
            slug = f'{base_slug}-{num}'
            num += 1  # number badhate jao jab tak unique slug na mil jaye

        # Step 3: Set the unique slug to the object
        self.slug = slug

        # whenever is_draft is set to false it means the blog has published, Jab blog pehli baar publish ho (i.e., draft → publish), tabhi uska published_at set karo current time se.
        if not self.is_draft and self.published_at is None:
            self.published_at = timezone.now()
    
        super().save(*args, **kwargs)