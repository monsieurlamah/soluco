from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from core.models import *
from taggit.models import Tag
from django.db.models import Avg
from core.forms import ProductReviewForm
from django.template.loader import render_to_string

def index(request):
    products = Product.objects.filter(product_status="publier").order_by("-id")[:8]
    product_featureds = Product.objects.filter(featured=True, product_status="publier").order_by("-id")[:8]
    new_products = Product.objects.filter(featured=True, product_status="publier").order_by("-id")
    categories = Category.objects.all()
    context = {
        'products':products,
        'product_featureds':product_featureds,
        'new_products':new_products,
        'categories':categories
    }
    return render(request, 'core/index.html', context)

def product_list_view(request):
    products = Product.objects.filter(product_status="publier").order_by("-id")
    categories = Category.objects.all()
    vendors = Vendor.objects.all()
    
    context = {
        'products':products,
        'categories':categories,
        'vendors':vendors,
    }
    return render(request, 'core/product-list.html', context)

def category_list_view(request):
    categories = Category.objects.all()
    context = {
        'categories':categories
    }
    return render(request, 'core/category-list.html', context)


def category_product_list(request, cid):
    category = Category.objects.get(cid=cid)
    products = Product.objects.filter(product_status="publier", category=category)
    categories = Category.objects.all()
    context = {
        'category':category,
        'products':products,
        'categories':categories
    }
    
    return render(request, 'core/product-category.html', context)


def vendor_list_view(request):
    vendors = Vendor.objects.all()
    context = {
        'vendors': vendors
    }
    return render(request, 'core/vendor-list.html', context)


def vendor_detail_view(request, vid):
    vendor = Vendor.objects.get(vid=vid)
    products = Product.objects.filter(product_status="publier", vendor=vendor)
    categories = Category.objects.all()
    context = {
        'vendor':vendor,
        'products':products,
        'categories':categories
    }
    return render(request, 'core/vendor-detail.html', context)

def product_detail_view(request, pid):
    product = Product.objects.get(pid=pid)
    p_image = product.p_images.all()
    related_products= Product.objects.filter(category=product.category).exclude(pid=pid)
    new_products= Product.objects.filter(category=product.category, product_status="publier").order_by("-id").exclude(pid=pid)[:3]
    
    # Getting all reviews related to a product
    reviews = ProductReview.objects.filter(product=product).order_by("-date")
    
    # Getting average review
    average_rating = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))
    
    #Product Review form
    review_form = ProductReviewForm()
    
    make_review = True
    if request.user.is_authenticated:
        user_review_count = ProductReview.objects.filter(user=request.user, product=product).count()
        if user_review_count > 0:
            make_review = False
    
    context = {
        'product':product,
        'p_image':p_image,
        'make_review':make_review,
        'average_rating':average_rating,
        'related_products':related_products,
        'new_products':new_products,
        'reviews':reviews,
        'review_form':review_form,
    }
    return render(request, 'core/product-detail.html', context)


def tag_list(request, tag_slug=None):
    products = Product.objects.filter(product_status="publier").order_by("-id")
    
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        products = products.filter(tags__in=[tag])
    context = {
        'products':products,
        'tag':tag,
    }
    return render(request, 'core/tag.html', context)


def ajax_add_review(request, pid):
    product = Product.objects.get(pid=pid)
    user = request.user
    
    review = ProductReview.objects.create(
        user=user,
        product=product,
        review=request.POST['review'],
        rating=request.POST['rating'],
    )
    
    context = {
        'user': user.username,
        'review':request.POST['review'],
        'rating':request.POST['rating'],
    }
    
    average_reviews = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))
    
    return JsonResponse(
       {
        'bool': True,
        'context': context,
        'average_reviews' : average_reviews
       }
    )
    
def sarch_view(request):
    query = request.GET.get('q')
    products = Product.objects.filter(title__icontains=query).order_by('-date')
    context = {
        'query':query,
        'products':products
    }
    return render(request, 'core/search.html', context)


def filter_product(request):
    categories = request.GET.getlist("category[]")
    vendors = request.GET.getlist("vendor[]")
    
    products = Product.objects.filter(product_status="publier").order_by("-id").distinct()
    
    if len(categories) > 0:
        products = products.filter(category__id__in=categories).distinct()
        
    if len(vendors) > 0:
        products = products.filter(vendor__id__in=vendors).distinct()
    context = {
        'products':products
    }
    data = render_to_string('core/async/product-list.html', context)
    return JsonResponse({
        'data':data
    })