from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from core.models import *
from userauths.models import ContactUs, Profile
from taggit.models import Tag
from django.db.models import Avg, Count
from core.forms import ProductReviewForm
from django.template.loader import render_to_string
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core import serializers
import calendar
from django.db.models.functions import ExtractMonth

from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm


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
    
    min_price = request.GET['min_price']
    max_price = request.GET['max_price']
    
    products = Product.objects.filter(product_status="publier").order_by("-id").distinct()
    products = products.filter(price__gte=min_price)
    products = products.filter(price__lte=max_price)
    
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

# cart functionality
def add_to_cart(request):
    cart_product = {}
    
    cart_product[str(request.GET['id'])]={
        'title':request.GET['title'],
        'qty': request.GET['qty'],
        'price':request.GET['price'],
        'image':request.GET['image'],
        'pid':request.GET['pid']
    }
    
    if "cart_data_obj" in request.session:
        if str(request.GET["id"]) in request.session["cart_data_obj"]:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = int(cart_product[str(request.GET['id'])]['qty'])
            cart_data.update(cart_data)
            request.session['cart_data_obj']=cart_data
        else:
            cart_data = request.session['cart_data_obj']
            cart_data.update(cart_product)
            request.session["cart_data_obj"] = cart_data
    
    else:
        request.session["cart_data_obj"] = cart_product
    return JsonResponse({
        'data':request.session['cart_data_obj'],
        'totalcartitems':len(request.session['cart_data_obj'])
    })
    

def cart_view(request):
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            # Clean up the price string by replacing non-breaking space with an empty string
            cleaned_price = item['price'].replace('\xa0', '')
            
            # Convert the cleaned price to float
            price_float = float(cleaned_price)
            
            item['total_price'] = int(item['qty']) * price_float
            # cart_total_amount += int(item['qty']) * price_float
            
            cart_total_amount += item['total_price']

        return render(request, 'core/cart.html', {
            'cart_data': request.session['cart_data_obj'],
            'totalcartitems': len(request.session['cart_data_obj']),
            'cart_total_amount': cart_total_amount
        })
    else:
        messages.warning(request, 'Votre panier est vide !')
        return redirect("core-index")


def delete_from_cart(request):
    product_id = str(request.GET['id'])
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            del request.session['cart_data_obj'][product_id]
            request.session['cart_data_obj'] = cart_data
            
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            # Clean up the price string by replacing non-breaking space with an empty string
            cleaned_price = item['price'].replace('\xa0', '')
            
            # Convert the cleaned price to float
            price_float = float(cleaned_price)
            
            item['total_price'] = int(item['qty']) * price_float
            # cart_total_amount += int(item['qty']) * price_float
            
            cart_total_amount += item['total_price']
            
    context = render_to_string("core/async/cart-list.html", {
            'cart_data': request.session['cart_data_obj'],
            'totalcartitems': len(request.session['cart_data_obj']),
            'cart_total_amount': cart_total_amount
        })
    return JsonResponse({
        "data":context,
        'totalcartitems': len(request.session['cart_data_obj']),
    })
    
    
def update_cart(request):
    product_id = str(request.GET['id'])
    product_qty = request.GET['qty']
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = product_qty
            request.session['cart_data_obj'] = cart_data
            
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            # Clean up the price string by replacing non-breaking space with an empty string
            cleaned_price = item['price'].replace('\xa0', '')
            
            # Convert the cleaned price to float
            price_float = float(cleaned_price)
            
            item['total_price'] = int(item['qty']) * price_float
            # cart_total_amount += int(item['qty']) * price_float
            
            cart_total_amount += item['total_price']
            
    context = render_to_string("core/async/cart-list.html", {
            'cart_data': request.session['cart_data_obj'],
            'totalcartitems': len(request.session['cart_data_obj']),
            'cart_total_amount': cart_total_amount
        })
    return JsonResponse({
        "data":context,
        'totalcartitems': len(request.session['cart_data_obj']),
    })
    
@login_required
def checkout_view(request):
    cart_total_amount = 0
    total_amount = 0
    
    # checking if cart_data_obj session exists
    if 'cart_data_obj' in request.session:
        
        # Getting total amount for paypal Amount
        for p_id, item in request.session['cart_data_obj'].items():
            # Clean up the price string by replacing non-breaking space with an empty string
            cleaned_price = item['price'].replace('\xa0', '')
            
            # Convert the cleaned price to float
            price_float = float(cleaned_price)
            
            item['total_price'] = int(item['qty']) * price_float
            # cart_total_amount += int(item['qty']) * price_float
            
            total_amount += item['total_price']

            # Create order object
            order = CartOrder.objects.create(
                user = request.user,
                price = total_amount
            )
        
            # Getting total amount for the cart
            for p_id, item in request.session['cart_data_obj'].items():
                # Clean up the price string by replacing non-breaking space with an empty string
                cleaned_price = item['price'].replace('\xa0', '')
                
                # Convert the cleaned price to float
                price_float = float(cleaned_price)
                
                item['total_price'] = int(item['qty']) * price_float
                # cart_total_amount += int(item['qty']) * price_float
                
                cart_total_amount += item['total_price']
                
                cart_order_products = CartOrderItems.objects.create(
                    order = order,
                    invoice_no = "Facture N°" + str(order.id),
                    item=item['title'],
                    image=item['image'],
                    price=cleaned_price,
                    qty=item['qty'],
                    total = int(item['qty']) * float(item['price'].replace('\xa0', '')),
                )
    
    
    host = request.get_host()
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': cart_total_amount ,
        'item_name': 'Commande-de-Article-n°-' + str(order.id),
        'invoice': 'FACTURE_N°'+ str(order.id),
        'currency_code': 'GNF',
        'notify_url':'http://{}{}'.format(host, reverse('paypal-ipn')),
        'return_url':'http://{}{}'.format(host, reverse('core-payment-completed')),
        'cancel_return':'http://{}{}'.format(host, reverse('core-payment-failed')),
    } 
    
    paypal_payment_button = PayPalPaymentsForm(initial=paypal_dict)
    
    # cart_total_amount = 0
    # if 'cart_data_obj' in request.session:
    #     for p_id, item in request.session['cart_data_obj'].items():
    #         # Clean up the price string by replacing non-breaking space with an empty string
    #         cleaned_price = item['price'].replace('\xa0', '')
            
    #         # Convert the cleaned price to float
    #         price_float = float(cleaned_price)
            
    #         item['total_price'] = int(item['qty']) * price_float
    #         # cart_total_amount += int(item['qty']) * price_float
            
    #         cart_total_amount += item['total_price']
            
    try:
        active_address = Address.objects.get(user=request.user, status=True)
    except:
        messages.warning(request, 'Il y a plusieurs adresses, une seule doit être activée.')
        active_address = None
        
        
        
        
    return render(request, 'core/checkout.html', {
        'cart_data': request.session['cart_data_obj'],
        'totalcartitems': len(request.session['cart_data_obj']),
        'cart_total_amount': cart_total_amount,
        'paypal_payment_button':paypal_payment_button,
        'active_address':active_address
    })
        
@login_required        
def payment_completed_view(request):
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            # Clean up the price string by replacing non-breaking space with an empty string
            cleaned_price = item['price'].replace('\xa0', '')
            
            # Convert the cleaned price to float
            price_float = float(cleaned_price)
            
            item['total_price'] = int(item['qty']) * price_float
            # cart_total_amount += int(item['qty']) * price_float
            
            cart_total_amount += item['total_price']
    return render(request, 'core/payment-completed.html', {
            'cart_data': request.session['cart_data_obj'],
            'totalcartitems': len(request.session['cart_data_obj']),
            'cart_total_amount': cart_total_amount,
        })

@login_required        
def payment_failed_view(request):
    return render(request, 'core/payment-failed.html')

@login_required  
def customer_dashboard(request):
    orders_list = CartOrder.objects.filter(user=request.user).order_by('-id')
    address = Address.objects.filter(user=request.user)
    
    
    orders = CartOrder.objects.annotate(month=ExtractMonth("order_date")).values("month").annotate(count=Count("id")).values("month", "count")
    month = []
    total_orders = []
    
    for i in orders:
        month.append(calendar.month_name[i['month']])
        total_orders.append(i['count'])
    
    if request.method == 'POST':
        address = request.POST.get('address')
        mobile = request.POST.get('mobile')
        
        new_address = Address.objects.create(
            user = request.user,
            address = address,
            mobile = mobile,
        )
        messages.success(request, 'Adresse ajoutée avec succès !')
        return redirect('core-dashboard')
    try:
        profile =  Profile.objects.get(user=request.user)
    except:
        profile = None
    
    
    context = {
        'profile':profile,
        'orders':orders,
        'orders_list':orders_list,
        'address':address,
        'month':month,
        'total_orders':total_orders,
    }
    return render(request, 'core/dashboard.html', context)

def order_detail(request, id):
    order = CartOrder.objects.get(user=request.user, id=id)
    order_items = CartOrderItems.objects.filter(order=order)
    context = {
        'order_items':order_items,
    }
    return render(request, 'core/order-detail.html', context)
    
def make_address_default(request):
    id = request.GET['id']
    Address.objects.update(status=False)
    Address.objects.filter(id=id).update(status=True)
    return JsonResponse({
        "boolean":True,
        
    })
    
@login_required    
def wishlistPage(request):
    try:
        wishlists = Wishlist.objects.filter(user=request.user)
    except:
        wishlists = None
    context = {
        'wishlists':wishlists
    }
    return render(request, 'core/wishlist.html', context)

def add_to_wishlist(request):
    product_id = request.GET['id']
    product = Product.objects.get(id=product_id)
    
    context = {}
    
    wishlist_count = Wishlist.objects.filter(product=product, user=request.user).count()
    print(wishlist_count)
    
    if wishlist_count > 0:
        context = {
            "bool":True
        }
    else:
        new_wishlist = Wishlist.objects.create(
        product = product,
        user = request.user,
        )
        context = {
            "bool":True
        }
    return JsonResponse(context)

def remove_wishlist(request):
    pid = request.GET['id']
    wishlists = Wishlist.objects.filter(user=request.user)
    
    wishlist_d = Wishlist.objects.get(id=pid)
    wishlist_d.delete()
    
    context = {
        "bool": True,
        "wishlists":wishlists
    }
    
    wishlist_json = serializers.serialize('json', wishlists)
    data = render_to_string("core/async/wishlist-list.html", context)
    return JsonResponse({
        "data":data,
        'wishlists':wishlist_json
    })


#=====Other Page=========
def contact(request):
    return render(request, 'core/contact.html')

def ajax_contact_form(request):
    full_name = request.GET['full_name']
    email = request.GET['email']
    phone = request.GET['phone']
    subject = request.GET['subject']
    message = request.GET['message']
    
    contact = ContactUs.objects.create(
        full_name=full_name,
        email=email,
        phone=phone,
        subject=subject,
        message = message
    )
    
    data = {
        'bool':True,
        'message': "Message sent successfully !"
    }
    
    return JsonResponse({
            "data":data
        })

def about_us(request):
    return render(request, 'core/about.html')

def purchase_guide(request):
    return render(request, 'core/purchase_guide.html')

def privacy_policy(request):
    return render(request, 'core/privacy_policy.html')

def terms_of_service(request):
    return render(request, 'core/terms_of_service.html')


