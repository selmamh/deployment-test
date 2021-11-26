from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView
from .models import Product, Profile
from django.db.models import Q
from .forms import NewUserForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import views as auth_views


# Create your views here.
def home(request):
    # with context we pass the data to the template
    context = {}
    return render(request, 'app/home.html', context)


def add_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('AddButton', '')
        product = Product.objects.get(id=product_id)
        profile = Profile.objects.get(user=request.user)
        profile.cart.add(product)
        return redirect('search')

def remove_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('RemoveButton', '')
        product = Product.objects.get(id=product_id)
        profile = Profile.objects.get(user=request.user)
        profile.cart.remove(product)
        return redirect('cart')


def cart(request):
    profile = Profile.objects.get(user=request.user)

    cart=profile.cart.all()
    supermarkets=set([x.supermarket for x in cart ])


    context = {
        'cart': profile.cart.all(),
        'supermarkets':supermarkets
    }
    return render(request, 'app/cart.html', context)


class Search(TemplateView):
    template_name = 'app/search.html'


class SearchResultsView(ListView):
    model = Product
    template_name = 'app/searchresults.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Product.objects.filter(
            Q(product_name__icontains=query)
        )
        return object_list


def register_request(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('search')
    else:
        form = UserCreationForm()
    return render(request, 'app/register.html', {'form': form})

def login_user(request, template_name='app/login.html', extra_context=None):  
    response = auth_views.login(request, template_name)  
    if request.POST.has_key('remember_me'):    
        request.session.set_expiry(1209600)
