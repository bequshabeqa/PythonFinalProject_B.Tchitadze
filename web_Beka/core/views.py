# from django.http import HttpResponse
# from django.shortcuts import render, get_object_or_404
# from core.models import Films

# def home_view(request):
#     return render(
#         request,
#         'index.html',
#         {
#             'films': Films.objects.all()
#         }   
#     )

# def about_view(request):
#     return render(request, 'about.html')

# def product_view(request, pk):
#     return render(
#         request,
#         'product_detail.html', 
#         {
#         "pk": pk,
#         "product": get_object_or_404(Films, pk=pk)
#     })





from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.urls import reverse
from core.models import Category, Films, Comment
from django.views.generic import ListView
from .models import Category, Films



class HomeView(ListView):
    model = Films
    paginate_by = 6
    template_name = 'index.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.request.GET.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        
        category_id = self.request.GET.get('category')
        context['selected_category'] = int(category_id) if category_id and category_id.isdigit() else None
        
        if self.request.user.is_authenticated:
            context['liked_movies'] = self.request.user.liked_films.all()
            
        return context

def home_view(request):
    return render(
        request,
        'index.html',
        {
            'categories': Category.objects.all(),
            'films': Films.objects.all()
        }   
    )

def about_view(request):
    return render(request, 'about.html')

def product_view(request, pk):
    product = get_object_or_404(Films, pk=pk)

    comments = product.comments.all().order_by('-created_at')

    if request.method == "POST" and request.user.is_authenticated:
        comment_text = request.POST.get('comment_text')
        if comment_text:
            Comment.objects.create(
                film=product,
                author=request.user,
                text=comment_text
            )
            return redirect('product_detail', pk=pk)

    return render(
        request,
        'product_detail.html', 
        {
            "pk": pk,
            "product": product,
            "comments": comments 
        }
    )

def blog_view(request):
    films = Films.objects.prefetch_related('comments').all()
    
    if request.method == "POST":
        film_id = request.POST.get('film_id')
        text = request.POST.get('text')
        film = get_object_or_404(Films, id=film_id)
        Comment.objects.create(film=film, author=request.user, text=text)
        
        url = reverse('blog') 
        return redirect(f"{url}#comments-{film_id}")

    return render(request, 'blog.html', {'films': films})

def delete_comment(request, comment_id):
    # ვიღებთ კომენტარს, რომ წაშლამდე გავიგოთ რომელ ფილმს ეკუთვნის
    comment = get_object_or_404(Comment, id=comment_id)
    film_id = comment.film.id
    
    if request.user == comment.author:
        comment.delete()
    
    return redirect(f'/blog/#comments-{film_id}')

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    if comment.author == request.user:
        comment.delete()
        
    return redirect('product_detail', pk=comment.film.pk)


class FilmCreateView(ListView):
    model = Films
    fields = "__all__"
    template_name = 'film_create.html'
    success_url = '/'

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) 
            return redirect('blog') 
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user() 
            login(request, user)   
            return redirect('home') 
    else:
        form = AuthenticationForm()
        
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    from django.contrib.auth import logout
    logout(request)
    return redirect('home')

def contact_view(request):
    return render(request, 'contact.html')