from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView
from .models import Product, Profile, Product_with_quantity
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
        quantity=request.POST.get('quantity','')
        
        prod_with_qu=Product_with_quantity(product_id=product_id,quantity=int(quantity))
        profile = Profile.objects.get(user=request.user)
        if list(profile.cart.filter(product_id=product_id))==[]:
            prod_with_qu.save()
            product = Product.objects.get(id=product_id)
            profile.cart.add(prod_with_qu)
        else:
            product= profile.cart.get(product_id=product_id)
            product.quantity+=int(quantity)
            product.save()

        q=request.POST.get('q','')
        url="../../app/searchresults/?q=" + q 
        return redirect(url)

def remove_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('RemoveButton', '')
        quantity=int(request.POST.get('quantity',''))
        profile = Profile.objects.get(user=request.user)
        product=profile.cart.get(product_id=product_id)

        if product.quantity-quantity<1:
            profile.cart.remove(product)
            product.delete()
        else:
            product.quantity-=quantity
            product.save()
        return redirect('cart')


def cart(request):
    profile = Profile.objects.get(user=request.user)
    cart=profile.cart.all()
    products=[]
    quantities=[]
    for prod in cart:
        products.append([Product.objects.get(id=prod.product_id),prod.quantity])
        
    supermarkets=set([x[0].supermarket for x in products ])
    total = 0
    for product in products:
        price = product[0].price
        price = str(price)
        price = price.replace(" ", "")
        total += int(price) * product[1]

    context = {
        'cart': products,
        'supermarkets':supermarkets,
        'sum' : total
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

