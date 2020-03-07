from django.db import models
from django.contrib.auth.models import User
import datetime as dt

# image model-image,name,caption,profile(foreign),likes,comments
# methods on image and profile models - save, del, update (caption in image model)


class Tag(models.Model):
    """ class to indicate the category of the image"""
    name = models.CharField(max_length=30)

class Image(models.model):
    image = models.ImageField(uploadto='photos/', null=True)
    image_name = models.CharField(max_length=40)
    image_caption = models.TextField(max_length=100, null=True, blank=True)
    likes = models.IntegerField(null=True, blank=True)
    date_uploaded = models.DateTimeField(auto_now_add=True, null=True)
    caption = models.ForeignKey(Tag,blank = True, on_delete=models.CASCADE )
    #profile = models.ForeignKey(Profile, null=True, blank = True, on_delete=models.CASCADE)
    #user = models.ForeignKey(User)

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
        images = Image.objects.all()
        return images
