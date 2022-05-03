from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class MainMenu(models.Model):
    item = models.CharField(max_length=200, unique=True)
    link = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.item


class Book(models.Model):
    name = models.CharField(max_length=200)
    web = models.URLField(max_length=200)
    price = models.DecimalField(decimal_places=2, max_digits=8)
    publishdate = models.DateField(auto_now=True)
    picture = models.FileField(upload_to='bookEx/static/uploads')
    pic_path = models.CharField(max_length=300, editable=False, blank=True)
    username = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    shopping_cart = models.BooleanField(default=False)
    favorites = models.ManyToManyField(User, related_name='favorite', default=None, blank=True)

    def __str__(self):
        return str(self.id)


# Shopping Cart Models
class OrderBook(models.Model):
    product = models.OneToOneField(Book, on_delete=models.SET_NULL, null=True)
    is_ordered = models.BooleanField(default=False)
    date_added = models.DateField(auto_now=True)

    def __str__(self):
        return self.product


class Order(models.Model):
    ordered_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    order_id = models.CharField(max_length=20)
    books = models.ManyToManyField(OrderBook)
    is_ordered = models.BooleanField(default=False)
    date_purchased = models.DateField(auto_now=True)

    def getTotalItems(self):
        return self.books.all()

    def getTotalCost(self):
        return sum([book.product.price for book in self.books.all()])

    def __str__(self):
        return '{0} - {1}'.format(self.ordered_by, self.order_id)



STATUS = (
    (0, "Draft"),
    (1, "Publish")
)


class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)
