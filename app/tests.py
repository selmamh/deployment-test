from django.test import TestCase, RequestFactory
from .models import *
from django.contrib.auth.models import AnonymousUser, User
from django.test import Client


# Create your tests here.

class ProductModelTests(TestCase):

    def test___str__(self):
        product = Product(product_name='tej', price=230, supermarket='spar', image_name='tej.jpg')
        result = product.__str__()
        self.assertEqual(product.price, 230)
        self.assertEqual(result, 'tej 230 spar tej.jpg')


class ProfileModelTests(TestCase):

    def test___str__(self):
        user1 = User.objects.create_user('user', 'user@gmail.com', 'pw')
        profile = Profile(user=user1)
        result = profile.__str__()
        self.assertEqual(result, 'user')


class CartModelTests(TestCase):
    def test___str__(self):
        user1 = User.objects.create_user('user4', 'user@gmail.com', 'pw', )
        user1.save()
        profile = Profile.objects.get(user_id=user1.id)
        product1 = profile.cart.create(product_id=15, quantity=2)
        product1.save()
        self.assertEqual(profile.cart.all()[0], product1)


class PageTests(TestCase):
    def setUp(self):
        # Create user

        self.user = User.objects.create_user(username='testuser', email='test@test.com', password='test1234')

        # Create Client

        self.c = Client()

        # Adding some dummy Products to the database

        product = Product(product_name='tej', price=230, supermarket='spar', image_name='tej.jpg')
        product.save()

    def test__login__(self):
        # Login Page available

        response = self.c.get('/app/login/')
        self.assertEqual(response.status_code, 200)

        # Login Page redirects with successful Login

        response = self.c.post('/app/login/', {'username': 'testuser', 'password': 'test1234'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain[-1][0], '/app/search/')

        # Login page doesn't redirect with wrong login 

        response = self.c.post('/app/login/', {'username': 'wronguser', 'password': 'test1234'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain, [])
        

    def test__search__(self):
        # Search Page avaiable

        response = self.c.get('/app/search/')
        self.assertEqual(response.status_code, 200)

    def test__searchresults__(self):
        # Searchresults Page available

        response = self.c.get('/app/searchresults/', {'q': 'tej'}, follow=True)
        self.assertEqual(response.status_code, 200)

        # Searchresults page gives back error without posted data
        with self.assertRaises(ValueError):
            response = self.c.get('/app/searchresults/')

        # Searchresults page shows Add to cart button if logged in

        self.c.force_login(self.user)
        response = self.c.get('/app/searchresults/', {'q': 'tej'}, follow=True)
        content = response.content.decode("utf-8")
        self.assertEqual('Add to cart' in content, True)

        # Searchresults page doesn't show Add to cart button when logged out
        self.c.logout()
        response = self.c.get('/app/searchresults/', {'q': 'tej'}, follow=True)
        content = response.content.decode("utf-8")
        self.assertEqual('Add to cart' in content, False)

    def test__cart__(self):
        # Cart page not available if logged out

        self.c.logout()
        with self.assertRaises(TypeError):
            response = self.c.get('/app/cart/')

        # Cart page available

        self.c.force_login(self.user)
        response = self.c.get('/app/cart/')
        self.assertEqual(response.status_code, 200)

        # Adding to cart

        response = self.c.post('/app/addcart/', {"AddButton": 1, "quantity":4}, follow=True)
        response = self.c.get('/app/cart/')
        content = response.content.decode("utf-8")
        self.assertEqual('Remove from Cart' in content, True)

        # Removing From Cart

        response = self.c.post('/app/removecart/', {'RemoveButton': 1, "quantity":4}, follow=True)
        content = response.content.decode("utf-8")
        self.assertEqual('Remove from Cart' in content, False)

    def test__register__(self):
        # Register page available:

        response = self.c.get('/app/register/')
        self.assertEqual(response.status_code, 200)