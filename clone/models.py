from django.db import models
from django.contrib.auth.models import User
import datetime as dt
from cloudinary.models import CloudinaryField


# image model-image,name,caption,profile(foreign),likes,comments
# methods on image and profile models - save, del, update (caption in image model)


class Profile(models.Model):
    '''
    profile model and its methods
    '''
    profile_picture =CloudinaryField(blank = True, null = True) 
    about = models.TextField(max_length=50)
    user =models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile') 
    follower_user = models.IntegerField(blank=True , null=True)
    following_user = models.IntegerField(blank=True, null=True)

    def save_profile(self):
        '''save user profile'''
        self.save()

    def del_profile(self):
        '''delete user profile'''
        self.delete()

    @classmethod
    def get_profile_id(cls, id):
        profile = cls.objects.filter(id=id).all()
        return profile

    def update_profile(self, about):
        self.about = about
        self.save()
    
    @classmethod
    def search_by_profile(cls,search_term):
        profiles = cls.objects.filter(user__username__icontains=search_term)
        return profiles


class Image(models.Model):
    '''
    image model and its methods
    '''
    image =CloudinaryField(blank=True, null=True)
    image_name = models.CharField(max_length=40)
    image_caption = models.TextField(max_length=100, null=True, blank=True)
    date_uploaded = models.DateTimeField(auto_now_add=True, null=True)
    profile = models.ForeignKey(Profile, null=True, blank = True, on_delete=models.CASCADE)
    #user = models.ForeignKey(User, )

    class Meta:
        ordering = ['-date_uploaded']

    def save_image(self):
        '''save an image in database'''
        self.save()

    def delete_image(self):
        '''delete image from the database'''
        self.delete()

    def __str__(self):
        return self.image_name

    @classmethod
    def get_images(cls):
        '''
        query images posted from the database
        Returns:
            images: list of image post objects
        '''
        images = cls.objects.all()
        return images

    @classmethod
    def get_image_id(cls, id):
        img = cls.objects.filter(id=id).all()
        return img


class Comment(models.Model):
    '''
    comment model and its methods
    '''
    comment = models.CharField(max_length=30)
    image_id = models.ForeignKey(Image, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)