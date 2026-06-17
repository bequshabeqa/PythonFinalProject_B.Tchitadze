import sys
import importlib.util
import pkgutil

# 🛠️ Python 3.14 თავსებადობის პატჩი
if not hasattr(pkgutil, 'find_loader'):
    def _find_loader(fullname):
        try:
            spec = importlib.util.find_spec(fullname)
            return spec.loader if spec else None
        except Exception:
            return None
    pkgutil.find_loader = _find_loader

# ----------------------------------------------------------------
import random
from datetime import date
from django.core.management.base import BaseCommand
from imdb import Cinemagoer
from core.models import Films, Category

class Command(BaseCommand):
    help = 'IMDb-დან ან ლოკალური ბაზიდან ფილმების წამოღება'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('უკავშირდება IMDb-ს...'))
        
        ia = Cinemagoer()
        use_local_data = False
        top_movies = []

        # ადგილობრივი, გამზადებული ფილმების ბაზა IMDb-ის ბლოკირების შემთხვევისთვის 🛡️
        local_movies_pool = [
            {
                'title': 'The Shawshank Redemption', 'year': 1994, 'rating': 9.3, 'genre': 'Drama',
                'plot': 'Over the course of several years, two convicts form a friendship, seeking consolation and, eventually, redemption through basic compassion.'
            },
            {
                'title': 'The Godfather', 'year': 1972, 'rating': 9.2, 'genre': 'Drama',
                'plot': 'The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.'
            },
            {
                'title': 'The Dark Knight', 'year': 2008, 'rating': 9.0, 'genre': 'Action',
                'plot': 'When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.'
            },
            {
                'title': 'Inception', 'year': 2010, 'rating': 8.8, 'genre': 'Sci-Fi',
                'plot': 'A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.'
            },
            {
                'title': 'Pulp Fiction', 'year': 1994, 'rating': 8.9, 'genre': 'Thriller',
                'plot': 'The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption.'
            },
            {
                'title': 'Forrest Gump', 'year': 1994, 'rating': 8.8, 'genre': 'Comedy',
                'plot': 'The history of the United States from the 1950s to the 1970s unfolds from the perspective of an Alabama man with an IQ of 75, who yearns to be reunited with his childhood sweetheart.'
            },
            {
                'title': 'Interstellar', 'year': 2014, 'rating': 8.7, 'genre': 'Sci-Fi',
                'plot': 'When Earth becomes uninhabitable, a team of explorers travels through a wormhole in space in an attempt to ensure humanity\'s survival.'
            },
            {
                'title': 'Spirited Away', 'year': 2001, 'rating': 8.6, 'genre': 'Animation',
                'plot': 'During her family\'s move to the suburbs, a sullen 10-year-old girl wanders into a world ruled by gods, witches, and spirits, and where humans are changed into beasts.'
            }
        ]

        try:
            top_movies = ia.get_top250_movies()
        except Exception:
            top_movies = []

        # თუ IMDb-მ პირველივე რექვესთზე დაგვბლოკა
        if not top_movies:
            self.stdout.write(self.style.WARNING('IMDb-მ დაგვბლოკა. ავტომატურად გადავდივარ ადგილობრივ სარეზერვო ბაზაზე...'))
            use_local_data = True

        if use_local_data:
            # ვირჩევთ 5 შემთხვევით ფილმს ჩვენი ლოკალური სიიდან
            chosen_movies = random.sample(local_movies_pool, min(5, len(local_movies_pool)))
            
            for item in chosen_movies:
                title = item['title']
                if Films.objects.filter(title=title).exists():
                    self.stdout.write(f"ფილმი '{title}' უკვე არსებობს, ვტოვებ...")
                    continue
                
                category_obj, _ = Category.objects.get_or_create(
                    name=item['genre'],
                    defaults={'description': f'{item["genre"]} ფილმები'}
                )
                
                Films.objects.create(
                    title=title,
                    category=category_obj,
                    description=item['plot'],
                    release_date=date(item['year'], 1, 1),
                    rate=item['rating'],
                    comment="იმპორტირებულია სარეზერვო ბაზიდან.",
                    link="https://www.imdb.com/"
                )
                self.stdout.write(self.style.SUCCESS(f"  წარმატებით დაემატა (ლოკალური): {title} ({item['year']})"))
        
        else:
            # თუ IMDb-მ იმუშავა, ჩვეულებრივი ონლაინ რეჟიმი
            random_movies = random.sample(top_movies, 5)
            for movie_base in random_movies:
                try:
                    movie = ia.get_movie(movie_base.movieID)
                    title = movie.get('title')
                    
                    # თუ ონლაინ რეჟიმშიც ცარიელი სახელი მოვიდა ბლოკის გამო
                    if not title:
                        self.stdout.write(self.style.ERROR("IMDb-მ დეტალების წამოღება დაბლოკა."))
                        continue
                        
                    if Films.objects.filter(title=title).exists():
                        self.stdout.write(f"ფილმი '{title}' უკვე არსებობს, ვტოვებ...")
                        continue

                    year = movie.get('year', 2000)
                    rating = movie.get('rating', 8.0)
                    plot_list = movie.get('plot', ['აღწერა არ მოიძებნა'])
                    plot = plot_list[0].split('::')[0] if plot_list else 'აღწერა არ მოიძებნა'
                    genres = movie.get('genres', [])
                    
                    category_obj = None
                    if genres:
                        category_name = genres[0]
                        category_obj, _ = Category.objects.get_or_create(
                            name=category_name,
                            defaults={'description': f'IMDb {category_name} Movies'}
                        )

                    Films.objects.create(
                        title=title,
                        category=category_obj,
                        description=plot,
                        release_date=date(int(year), 1, 1),
                        rate=rating,
                        comment="ავტომატურად იმპორტირებულია IMDb-დან.",
                        link=f"https://www.imdb.com/title/tt{movie_base.movieID}/"
                    )
                    self.stdout.write(self.style.SUCCESS(f"  წარმატებით დაემატა: {title} ({year})"))
                    
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"შეცდომა ფილმის წამოღებისას: {e}"))

        self.stdout.write(self.style.SUCCESS('პროცესი დასრულდა!'))