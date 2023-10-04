from django.shortcuts import render
from django.contrib.auth.decorators import login_required,user_passes_test
from store.models import *
from django.views.generic import ListView,CreateView, UpdateView, DetailView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Q
from django.contrib.messages.views import SuccessMessageMixin
from clients.models import *
from store.details.ctm_admin.models import RequestCategory
from django.contrib import messages
from django.shortcuts import redirect
from .models import *
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from clients.utils import token_generater
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from decouple import config
from django.urls import reverse
from django.template.loader import get_template
import threading
from django.http import HttpResponseForbidden,HttpResponse
from django.views import View
from django.conf import settings

class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send(fail_silently=False)

@login_required
@user_passes_test(lambda u: True if((u.customer.customer_type == 'Admin') or (u.customer.customer_type == 'Seller')) else False)
def main(request):
    return render(request,'ctm_seller/index.html')


@login_required
@user_passes_test(lambda u: True if(u.customer.customer_type == 'Admin') else False)
def SelectSeller(request):
    if request.method == 'GET':
        sell = SellerUser.objects.all()
        context = {
            'sellers':sell
        }
        return render(request,'ctm_seller/admin_sel_seller.html',context)
    if request.method == 'POST':
        seller_usr = request.POST.get("sell_usr",False)
        get_next = request.GET.get('next',False)
        if seller_usr:
            request.session['admin_seller_sel'] = seller_usr
        else:
            return HttpResponseForbidden()
        if get_next:
            return redirect(get_next)
        else:
            return redirect('seller-index')

class CategoryListview(UserPassesTestMixin,ListView):
    model = Category
    template_name = 'ctm_seller/categorylistview.html'
    paginate_by = 4

    def test_func(self):
        try:
            user_type = self.request.user.customer.customer_type
            if user_type == 'Admin' or user_type=='Seller':
                return True
            else:
                return False
        except Exception as e:
            return False

    def get_queryset(self):
        filter_val = self.request.GET.get('filter','')
        order_by = self.request.GET.get('order_by','id')
        if filter_val != "":
            cagr = Category.objects.filter(
                Q(name__contains=filter_val) | 
                Q(description__contains=filter_val) |
                Q(is_active = True)
                ).order_by(order_by)
        else:
            cagr = Category.objects.filter(is_active=True).order_by(order_by)
        return cagr

    def get_context_data(self, **kwargs):
        context = super(CategoryListview, self).get_context_data(**kwargs)
        context['filter']=self.request.GET.get('filter','')
        context['order_by']=self.request.GET.get('order_by','id')
        context['all_table_data']=Category._meta.get_fields()
        return context
    
class CategoryRequest(UserPassesTestMixin,SuccessMessageMixin, CreateView):
    model = Category
    success_message = 'Category requested successfuly'
    fields = '__all__'
    template_name = 'ctm_seller/categorycreate.html'

    def test_func(self):
        try:
            user_type = self.request.user.customer.customer_type
            if user_type == 'Admin' or user_type=='Seller':
                return True
            else:
                return False
        except Exception as e:
            return False
        
    def form_valid(self, form):
        cate=form.save(commit=False)
        cate.is_active=False
        cate.save()
        reqcate = RequestCategory.objects.create(category=cate,user=self.request.user.customer)
        reqcate.save()
        messages.success(self.request, 'Category Requested Successfully')
        return redirect('seller-categoryrequest')
    
class StaffUserListview(UserPassesTestMixin,ListView):
    model = SellerStaff
    template_name = 'ctm_seller/staff_user_listview.html'
    paginate_by = 4

    def test_func(self):
        try:
            user_type = self.request.user.customer.customer_type
            if user_type == 'Admin' or user_type=='Seller':
                return True
            else:
                return False
        except Exception as e:
            return False

    def get_queryset(self):
        filter_val = self.request.GET.get('filter','')
        order_by = self.request.GET.get('order_by','id')
        user_type = self.request.user.customer.customer_type
        if user_type == "Admin":
            if filter_val != "":
                cagr = SellerStaff.objects.filter(Q(user__contains=filter_val)).order_by(order_by)
            else:
                cagr = SellerStaff.objects.all().order_by(order_by)
        else:
            if filter_val != "":
                cagr = SellerStaff.objects.filter(Q(seller=self.request.user.customer.selleruser) & Q(user__username__contains=filter_val)).order_by(order_by)
            else:
                cagr = SellerStaff.objects.filter(Q(seller=self.request.user.customer.selleruser)).order_by(order_by)
        return cagr
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter']=self.request.GET.get('filter','')
        context['order_by']=self.request.GET.get('order_by','id')
        context['all_table_data']=SellerStaff._meta.get_fields()
        return context

class StaffUserCreate(UserPassesTestMixin,SuccessMessageMixin, CreateView):
    model = SellerStaff
    success_message = 'Staff created successfuly'
    fields = '__all__'
    template_name = 'ctm_seller/staff_user_create.html'

    def test_func(self):
        try:
            user_type = self.request.user.customer.customer_type
            if user_type == 'Admin' or user_type=='Seller':
                return True
            else:
                return False
        except Exception as e:
            return False
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_type = self.request.user.customer.customer_type
        if user_type == 'Admin':
            context['is_by_seller']=False
        elif user_type=='Seller':
            context['is_by_seller']=True
        return context

    def form_valid(self, form):
        user_type = self.request.user.customer.customer_type
        data = self.request.POST
        selleruser = self.request.user
        sellerusr_id = data['seller']
        seller = SellerUser.objects.get(id=sellerusr_id)
        slruser = data['username']
        if user_type == 'Admin':
            stusrname = f'{seller}222{slruser}'
        elif user_type == 'Seller':
            stusrname = f'{selleruser}222{slruser}'
        else:
            return HttpResponseForbidden()
        password = data['password']
        email = data['email']
        firstname = data['first_name']
        lastname = data['last_name']
        profile_pic = self.request.FILES['profile_pic']
        customer_type = data['customer_type']
        pst_is_active = data['is_active']
        if pst_is_active == 'on':
            bst_is_active=True
        else:
            bst_is_active=False
        context = {
            'FieldValues':self.request.POST
        }
        if not User.objects.filter(username=stusrname).exists():
            if not User.objects.filter(email=email).exists():
                if len(password)<6:
                    messages.error(self.request, 'Password too short')
                    return render(self.request, 'ctm_seller/staff_user_create.html', context)

                user = User.objects.create_user(username=stusrname, email=email, first_name=firstname,last_name=lastname)
                user.set_password(password)
                user.is_active=False
                user.save()

                sellstf = SellerStaff.objects.create(user=user,seller=seller,profile_pic=profile_pic,customer_type=customer_type,is_active=bst_is_active)
                sellstf.save()
                email_tmp_path = 'emails/auth/email_verification.html'
                domain = get_current_site(self.request).domain
                request_main = config('REQUEST')
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                link = reverse('activate', kwargs={'uidb64':uidb64, 'token':token_generater.make_token(user)})
                from_mail = config('FROM_MAIL')
                activate_url = request_main+domain+link
                context_email_data = {
                    'title':settings.SITE_NAME,
                    'baseurl':domain+request_main,
                    'activate_url':activate_url,
                    'user_name':user.username,
                    'user_email':user.email,
                }
                email_body = get_template(email_tmp_path).render(context_email_data)
                email_subject = f'Activate your account | {settings.SITE_NAME}'
                email = EmailMessage(
                    email_subject,
                    email_body,
                    from_mail,
                    [email],
                )
                email.content_subtype = 'html'
                EmailThread(email).start()
                messages.info(self.request, 'A Verification email have been sent')
                messages.success(self.request, 'StaffUser Account Created Successfully')
                return redirect('seller-staff-userlist')
            
            messages.error(self.request, 'Email already in Use.Try Again')
            return render(self.request,'ctm_seller/staff_user_create.html',context)
        
        messages.error(self.request, 'Username already in Use.Try Again')
        return render(self.request,'ctm_seller/staff_user_create.html',context)
    
class ProductsListview(UserPassesTestMixin,ListView):
    model = Product
    template_name = 'ctm_seller/productslistview.html'
    paginate_by = 4

    def get(self,request, *args, **kwargs):
        user_type = self.request.user.customer.customer_type
        if user_type == 'Admin':
            if 'admin_seller_sel' in self.request.session:
                admin_sel_sell = self.request.session['admin_seller_sel']
                self.user_to_get = SellerUser.objects.filter(id=admin_sel_sell).first()
                self.user_to_get = self.user_to_get.user_type.user
            else:
                return redirect('seller-sel-seller')
        else:
            self.user_to_get = self.request.user
        response = super().get(request, *args, **kwargs)
        return response

    def test_func(self):
        try:
            user_type = self.request.user.customer.customer_type
            if user_type == 'Admin':
                return True
            elif user_type=='Seller':
                return True
            else:
                return False
        except Exception as e:
            return False

    def get_queryset(self):
        filter_val = self.request.GET.get('filter','')
        order_by = self.request.GET.get('order_by','id')
        user_to_get = self.user_to_get
        if filter_val != "":
            print(user_to_get)
            prod = Product.objects.filter(
                Q(subcategories__category__is_active=True) &
                Q(subcategories__is_active=True)&
                Q(by_seller__user_type__user = user_to_get) &
                Q(name__contains=filter_val) | 
                Q(description__contains=filter_val) | 
                Q(brand__contains = filter_val) | 
                Q(subcategories__name__contains = filter_val) |
                Q(subcategories__category__name__contains = filter_val)
            ).order_by(order_by)
        else:
            prod = Product.objects.filter(by_seller__user_type__user = user_to_get, is_active=True,subcategories__category__is_active=True,subcategories__is_active=True).order_by(order_by)
        return prod

    def get_context_data(self, **kwargs):
        context = super(ProductsListview, self).get_context_data(**kwargs)
        context['filter']=self.request.GET.get('filter','')
        context['order_by']=self.request.GET.get('order_by','id')
        context['all_table_data']=Product._meta.get_fields()
        return context
    
class ProductCreateView(UserPassesTestMixin,View):
    def test_func(self):
        try:
            user_type = self.request.user.customer.customer_type
            if user_type == 'Admin' or user_type=='Seller':
                return True
            else:
                return False
        except Exception as e:
            return False
    
    def get(self, request):
        user_type = self.request.user.customer.customer_type
        if user_type == 'Admin':
            if 'admin_seller_sel' in self.request.session:
                admin_sel_sell = self.request.session['admin_seller_sel']
                seller = SellerUser.objects.filter(id=admin_sel_sell).first()
                seller = seller.user_type.user
            else:
                return redirect('seller-sel-seller')
        else:
            seller = self.request.user
        editor, created = EditorType.objects.get_or_create()
        categories = Category.objects.filter(is_active=True)
        categories_list = []
        for value in categories:
            sub_categories = SubCategory.objects.filter(is_active=True, category=value.id)
            categories_list.append({'category':value, 'subcategory':sub_categories})
        context = {
            'title':'Add Product',
            'data': categories_list,
            'editor': editor,
            'seller': seller
        }
        return render(request, 'ctm_seller/product_createview.html', context)

    def post(self, request):
        p_name = request.POST.get('name')
        p_slug = request.POST.get('slug')
        p_brand = request.POST.get('brand')
        p_subcategory = request.POST.get('subcategory')
        p_sku = request.POST.get('sku')
        p_seller = request.POST.get('seller')
        p_quantity = request.POST.get('quantity')
        p_old_price = request.POST.get('old_price')
        p_offer = request.POST.get('offer')
        p_new_price = request.POST.get('new_price')
        p_short_description = request.POST.get('product_short_description')
        p_is_active = request.POST.get('is_active','on')
        p_is_digital = request.POST.get('is_digital','')
        p_return_allowed = request.POST.get('return_allowed','')
        p_media_type_l = request.POST.getlist('media_type[]')
        p_media_content_l = request.FILES.getlist('select_media[]')
        p_detail_title_l = request.POST.getlist('detail_title[]')
        p_details_detail_l = request.POST.getlist('details_detail[]')
        p_details_active_l = request.POST.getlist('details_active[]')
        p_about_title_l = request.POST.getlist('about_title[]')
        p_about_active_l = request.POST.getlist('about_active[]')
        p_product_tags = request.POST.get('product_tags')
        p_long_desc = request.POST.get('long_desc')

        a_subcategory = SubCategory.objects.get(id=p_subcategory)

        user_type = self.request.user.customer.customer_type
        if user_type == 'Admin':
            if 'admin_seller_sel' in self.request.session:
                admin_sel_sell = self.request.session['admin_seller_sel']
                a_seller = SellerUser.objects.filter(id=admin_sel_sell).first()
            else:
                return redirect('seller-sel-seller')
        else:
            a_seller = SellerUser.objects.filter(user_type__user=self.request.user).first()


        b_is_active = None
        b_is_digital = None
        b_return_allowed = None
        if p_is_active == 'on':
            b_is_active=True
        else:
            b_is_active=False
        if p_is_digital == 'on':
            b_is_digital=True
        else:
            b_is_digital=False

        if p_return_allowed == 'on':
            b_return_allowed=True
        else:
            b_return_allowed=False
        
        a_product = Product(
            name=p_name,
            slug=p_slug,
            brand=p_brand,
            subcategories=a_subcategory,
            sku=p_sku,
            old_price=p_old_price,
            offer=p_offer,
            new_price=p_new_price,
            quantity=p_quantity,
            description=p_short_description,
            long_description=p_long_desc,
            by_seller=a_seller,
            is_active=b_is_active,
            is_digital=b_is_digital,
            return_allowed=b_return_allowed,
            meta_keywords=p_name,
            meta_description=p_short_description)
        a_product.save()

        a_i=0
        for media in p_media_content_l:
            a_media = ProductMedia(
                product=a_product,
                type = p_media_type_l[a_i],
                content = media
            )
            a_media.save()
            a_i+=1

        a_j=0
        for title in p_detail_title_l:
            detail_active = None
            if p_details_active_l[a_j] == 'on':
                detail_active=True
            else:
                detail_active=False
            a_details = ProductDetails(
                product=a_product,
                title=title,
                details=p_details_detail_l[a_j],
                is_active=detail_active
            )
            a_details.save()
            a_j+=1

        a_n=0
        for about in p_about_title_l:
            about_active = None
            if p_about_active_l[a_n] == 'on':
                about_active=True
            else:
                about_active=False
            a_about=ProductAbout(
                product=a_product,
                title=about,
                is_active=about_active
            )
            a_about.save()
            a_n+=1
        
        product_tags_l = p_product_tags.split(',')
        for tag in product_tags_l:
            a_tags = ProductTags(
                product=a_product,
                title=tag
            )
            a_tags.save()

        a_transaction = ProductTransaction(
            product=a_product,
            type = 1,
            count = p_quantity,
            description = str(p_quantity)+' items added to stock'
        )
        a_transaction.save()
        return HttpResponse('form submited')