from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def icon(self):
        genre_icons = {
            'Action': '💥',
            'Comedy': '😂',
            'კომედია': '😂',
            'Drama': '🎭',
            'Horror': '👻',
            'Sci-Fi': '👽',
            'Romance': '❤️',
            'Thriller': '🤫',
            'Fantasy': '🦄',
            'Animation': '🧸',
            'Documentary': '🎥',
        }
        return genre_icons.get(self.name, '🍿')


class Films(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='films')
    description = models.TextField()
    release_date = models.DateField()
    rate = models.DecimalField(
        max_digits=3,      
        decimal_places=1,   
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)]
    )
    link = models.URLField(null=True, blank=True)

    # 🌟 ახალი ველი მოწონებული ფილმებისთვის (Many-to-Many კავშირი)
    likes = models.ManyToManyField(User, related_name='liked_films', blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f"/product/{self.pk}/"


class Comment(models.Model):
    # 'film' არის კავშირი Films მოდელთან
    film = models.ForeignKey('Films', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username} - {self.text[:20]}"








# from django.db import models
# from django.core.validators import MinValueValidator, MaxValueValidator
# from django.contrib.auth.models import User



# class Movie(models.Model):
#     title = models.CharField(max_length=255)
#     rate = models.FloatField()
#     description = models.TextField(blank=True, null=True)

#     def __str__(self):
#         return self.title
    
# class Category(models.Model):
#     name = models.CharField(max_length=100)
#     description = models.TextField(null=True, blank=True)

#     def __str__(self):
#         return self.name

#     @property
#     def icon(self):
#         genre_icons = {
#             'Action': '💥',
#             'Comedy': '😂',
#             'კომედია': '😂',
#             'Drama': '🎭',
#             'Horror': '👻',
#             'Sci-Fi': '👽',
#             'Romance': '❤️',
#             'Thriller': '🤫',
#             'Fantasy': '🦄',
#             'Animation': '🧸',
#             'Documentary': '🎥',
#         }
#         return genre_icons.get(self.name, '🍿')


# class Films(models.Model):
#     title = models.CharField(max_length=200)
#     category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='films')
#     description = models.TextField()
#     release_date = models.DateField()
#     rate = models.DecimalField(
#         max_digits=3,      
#         decimal_places=1,   
#         validators=[MinValueValidator(0.0), MaxValueValidator(10.0)]
#     )
#     comment = models.TextField()
#     link = models.URLField(null=True, blank=True)

#     # 🌟 ახალი ველი მოწონებული ფილმებისთვის (Many-to-Many კავშირი)
#     likes = models.ManyToManyField(User, related_name='liked_films', blank=True)

#     def __str__(self):
#         return self.title

#     def get_absolute_url(self):
#         return f"/product/{self.pk}/"


# class Comment(models.Model):
#     # 'film' არის კავშირი Films მოდელთან
#     film = models.ForeignKey('Films', on_delete=models.CASCADE, related_name='comments')
#     author = models.ForeignKey(User, on_delete=models.CASCADE)
#     text = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.author.username} - {self.text[:20]}"