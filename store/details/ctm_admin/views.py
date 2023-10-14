from django.shortcuts import render
from django.shortcuts import HttpResponse, render
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from clients.models import Customer, EditorType
from store.models import *
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.db.models import Q
from django.conf import settings
import os
import json
from django.views import View
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin
from .models import *
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.core.serializers.json import DjangoJSONEncoder
from .dashboard import GetCounts,unique_visitors_data,device_type_data_last_30_days

@login_required
@user_passes_test(lambda u: u.is_superuser)
def main(request):
    user_data = User.objects.annotate(day=TruncDate('date_joined')).values('day').annotate(count=Count('id'))
    product_data = Product.objects.filter(
        is_active=True,
        subcategories__category__is_active=True,
        subcategories__is_active=True,
    ).annotate(day=TruncDate('created_at')).values('day').annotate(count=Count('id'))
    user_data_list = list(user_data)
    product_data_list = list(product_data)

    dates ,counts = unique_visitors_data()
    data = {'labels':json.dumps(dates,cls=DjangoJSONEncoder), 'data':json.dumps(counts,cls=DjangoJSONEncoder)}

    device_types, counts_dev = device_type_data_last_30_days()
    data_d = {'labels':json.dumps(device_types,cls=DjangoJSONEncoder), 'data':json.dumps(counts_dev,cls=DjangoJSONEncoder)}
    context = {
        'user_data': json.dumps(user_data_list, cls=DjangoJSONEncoder),
        'product_data':json.dumps(product_data_list, cls=DjangoJSONEncoder),
        "user_act_cnt": GetCounts(request)['users'],
        "order_cmp_cnt": GetCounts(request)['orders_comp'],
        "order_ncmp_cnt": GetCounts(request)['orders_ncomp'],
        "prod_cmp_cnt": GetCounts(request)['products'],
        "data":data,
        "devices_d":data_d
        # "data":json.dumps(data, cls=DjangoJSONEncoder)
    }
    return render(request, 'ctm_admin/index.html',context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def ckeditor(request):
    return render(request, 'ctm_admin/ckeditor.html')

class CategoryListview(UserPassesTestMixin,ListView):
    model = Category
    template_name = 'ctm_admin/categorylistview.html'
    paginate_by = 4

    def test_func(self):
        try:
            return self.request.user.is_superuser
        except Exception as e:
            return False

    def get_queryset(self):
        filter_val = self.request.GET.get('filter','')
        order_by = self.request.GET.get('order_by','id')
        if filter_val != "":
            cagr = Category.objects.filter(Q(name__contains=filter_val) | Q(description__contains=filter_val)).order_by(order_by)
        else:
            cagr = Category.objects.all().order_by(order_by)
        return cagr

    def get_context_data(self, **kwargs):
        context = super(CategoryListview, self).get_context_data(**kwargs)
        context['filter']=self.request.GET.get('filter','')
        context['order_by']=self.request.GET.get('order_by','id')
        context['all_table_data']=Category._meta.get_fields()
        return context

class CategoryRequestListview(UserPassesTestMixin,ListView):
    model = RequestCategory
    template_name = 'ctm_admin/categoryrequests.html'
    paginate_by = 4

    def test_func(self):
        try:
            return self.request.user.is_superuser
        except Exception as e:
            return False

    def get_queryset(self):
        filter_val = self.request.GET.get('filter','')
        order_by = self.request.GET.get('order_by','id')
        if filter_val != "":
            cagr = RequestCategory.objects.filter(Q(category__name__contains=filter_val) | Q(category__description__contains=filter_val)).order_by(order_by)
        else:
            cagr = RequestCategory.objects.all().order_by(order_by)
        return cagr

    def get_context_data(self, **kwargs):
        context = {'requestcategory_list':RequestCategory.objects.filter(is_completed=False,is_active=True)}
        context['filter']=self.request.GET.get('filter','')
        context['order_by']=self.request.GET.get('order_by','id')
        context['all_table_data']=RequestCategory._meta.get_fields()
        return context

class CategoryCreate(UserPassesTestMixin,SuccessMessageMixin, CreateView):
    model = Category
    success_message = 'Category created successfuly'
    fields = '__all__'
    template_name = 'ctm_admin/categorycreate.html'

    def test_func(self):
        try:
            return self.request.user.is_superuser
        except Exception as e:
            return False

class CategoryUpdate(UserPassesTestMixin,SuccessMessageMixin, UpdateView):
    model = Category
    success_message = 'Category updated successfuly'
    fields = '__all__'
    template_name = 'ctm_admin/categoryupdate.html'

    def test_func(self):
        try:
            return self.request.user.is_superuser
        except Exception as e:
            return False

class CategoryRequestUpdate(UserPassesTestMixin,SuccessMessageMixin, UpdateView):
    model = Category
    success_message = 'Requested Category added successfuly'
    fields = '__all__'
    template_name = 'ctm_admin/categoryrequestupdate.html'

    def form_valid(self, form):
        cate=form.save(commit=False)
        cate.is_active = True
        cate.save()
        reqcate = RequestCategory.objects.get(category=cate)
        reqcate.is_completed = True
        reqcate.save()
        messages.success(self.request, 'Requested Category added successfuly')
        return redirect('admin-categoryrequest')

    def test_func(self):
        try:
            return self.request.user.is_superuser
        except Exception as e:
            return False

class SubCategoryListview(UserPassesTestMixin,ListView):
    model = SubCategory
    template_name = 'ctm_admin/subcategorylistview.html'
    paginate_by = 4

    def test_func(self):
        try:
            return self.request.user.is_superuser
        except Exception as e:
            return False

    def get_queryset(self):
        filter_val = self.request.GET.get('filter','')
        order_by = self.request.GET.get('order_by','id')
        if filter_val != "":
            cagr = SubCategory.objects.filter(Q(name__contains=filter_val) | Q(description__contains=filter_val)).order_by(order_by)
        else:
            cagr = SubCategory.objects.all().order_by(order_by)
        return cagr

    def get_context_data(self, **kwargs):
        context = super(SubCategoryListview, self).get_context_data(**kwargs)
        context['filter']=self.request.GET.get('filter','')
        context['order_by']=self.request.GET.get('order_by','id')
        context['all_table_data']=SubCategory._meta.get_fields()
        return context

class SubCategoryCreate(UserPassesTestMixin,SuccessMessageMixin, CreateView):
    model = SubCategory
    success_message = 'Subcategory created successfuly'
    fields = '__all__'
    template_name = 'ctm_admin/subcategorycreate.html'

    def test_func(self):
        try:
            return self.request.user.is_superuser
        except Exception as e:
            return False

class SubCategoryUpdate(UserPassesTestMixin,SuccessMessageMixin, UpdateView):
    model = SubCategory
    success_message = 'Subcategory updated successfuly'
    fields = '__all__'
    template_name = 'ctm_admin/subcategoryupdate.html'

    def test_func(self):
        try:
            return self.request.user.is_superuser
        except Exception as e:
            return False

class SellerUserListview(UserPassesTestMixin,ListView):
    model = SellerUser
    template_name = 'ctm_admin/seller-user_listview.html'
    paginate_by = 4

    def test_func(self):
        try:
            return self.request.user.is_superuser
        except Exception as e:
            return False

    def get_queryset(self):
        filter_val = self.request.GET.get('filter','')
        order_by = self.request.GET.get('order_by','id')
        if filter_val != "":
            cagr = SellerUser.objects.filter(Q(company_name__contains=filter_val) | Q(gst_details__contains=filter_val) | Q(address__contains=filter_val)).order_by(order_by)
        else:
            cagr = SellerUser.objects.all().order_by(order_by)
        return cagr

    def get_context_data(self, **kwargs):
        context = super(SellerUserListview, self).get_context_data(**kwargs)
        context['filter']=self.request.GET.get('filter','')
        context['order_by']=self.request.GET.get('order_by','id')
        context['all_table_data']=SellerUser._meta.get_fields()
        return context

class SellerUserCreate(UserPassesTestMixin,SuccessMessageMixin, CreateView):
    model = User
    success_message = 'Seller created successfuly'
    fields = ['first_name', 'last_name', 'email', 'username', 'password']
    template_name = 'ctm_admin/Seller-usercreate.html'

    def test_func(self):
        try:
            return self.request.user.is_superuser
        except Exception as e:
            return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        states_data = []
        file_path = os.path.join(settings.BASE_DIR, 'data_files/states_dist.json')
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
            for values in data:
                states_data.append(values['state'])
        context['data']=states_data
        return context

    def form_valid(self, form):
        user=form.save(commit=False)
        check_email = User.objects.filter(email=user.email)
        if check_email.exists():
            messages.error(self.request, 'Email already exists')
            return redirect('admin-seller-usercreate')
        user.is_active=True
        user.set_password(form.cleaned_data['password'])
        user.save()
        customer = Customer.objects.create(user=user, customer_type="Seller")
        customer.save()

        profile_pic = self.request.FILES['profile_pic']
        by_admin = False
        if self.request.POST.get('by_admin')=='on':
            by_admin = True
        
        customer.selleruser.profile_pic=profile_pic
        customer.selleruser.company_name=self.request.POST.get('company_name')
        customer.selleruser.gst_details=self.request.POST.get('gst_details')
        customer.selleruser.address=self.request.POST.get('address')
        customer.selleruser.state=self.request.POST.get('state')
        customer.selleruser.city=self.request.POST.get('city')
        customer.selleruser.zip=self.request.POST.get('zip')
        customer.selleruser.by_admin=by_admin
        customer.selleruser.save()
        messages.success(self.request, 'SellerUser Created Successfully')
        return redirect('admin-seller-userlist')


class SellerUserUpdate(UserPassesTestMixin,SuccessMessageMixin, UpdateView):
    model = User
    success_message = 'Seller created successfuly'
    fields = ['first_name', 'last_name', 'email', 'username']
    template_name = 'ctm_admin/Seller-user_update.html'

    def test_func(self):
        try:
            return self.request.user.is_superuser
        except Exception as e:
            return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selleruser']=SellerUser.objects.get(user_type=self.object.customer.pk)
        chs = context['selleruser'].state
        states_data = []
        data_dist = None
        file_path = os.path.join(settings.BASE_DIR, 'data_files/states_dist.json')
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
            for value in data:
                states_data.append(value['state'])
                x = value['state']
                if x == chs:
                    data_dist = value['districts']
        context['data']=states_data
        context['data_a']=data_dist
        return context

    def form_valid(self, form):
        user=form.save(commit=False)
        user.save()
        customer = Customer.objects.get(user=user)

        if self.request.FILES.get('profile_pic',False):
            profile_pic = self.request.FILES['profile_pic']
            customer.selleruser.profile_pic=profile_pic
        
        by_admin = False
        if self.request.POST.get('by_admin')=='on':
            by_admin = True
        
        customer.selleruser.company_name=self.request.POST.get('company_name')
        customer.selleruser.gst_details=self.request.POST.get('gst_details')
        customer.selleruser.address=self.request.POST.get('address')
        customer.selleruser.state=self.request.POST.get('state')
        customer.selleruser.city=self.request.POST.get('city')
        customer.selleruser.zip=self.request.POST.get('zip')
        customer.selleruser.by_admin=by_admin
        customer.selleruser.save()
        messages.success(self.request, 'SellerUser Updated Successfully')
        return redirect('admin-seller-userlist')

class ProductCreateView(UserPassesTestMixin,View):
    def test_func(self):
        try:
            return self.request.user.is_superuser
        except Exception as e:
            return False
    
    def get(self, request):
        seller = SellerUser.objects.filter(user_type__user__is_active=True)
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
        return render(request, 'ctm_admin/products_create.html', context)

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
        p_is_bestselling = request.POST.get('is_bestselling','')
        p_is_featured = request.POST.get('is_featured','')
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
        a_seller = SellerUser.objects.get(id=p_seller)


        b_is_active = None
        b_is_bestselling = None
        b_is_featured = None
        b_is_digital = None
        b_return_allowed = None
        if p_is_active == 'on':
            b_is_active=True
        else:
            b_is_active=False

        if p_is_bestselling == 'on':
            b_is_bestselling=True
        else:
            b_is_bestselling=False

        if p_is_featured == 'on':
            b_is_featured=True
        else:
            b_is_featured=False

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
            is_bestselling=b_is_bestselling,
            is_featured=b_is_featured,
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
    
# The ProductsListview class is a subclass of ListView.
class ProductsListview(UserPassesTestMixin,ListView):
    model = Product
    template_name = 'ctm_admin/productslistview.html'
    paginate_by = 4

    def test_func(self):
        try:
            return self.request.user.is_superuser
        except Exception as e:
            return False

    def get_queryset(self):
        filter_val = self.request.GET.get('filter','')
        order_by = self.request.GET.get('order_by','id')
        if filter_val != "":
            prod = Product.objects.filter(
                Q(name__contains=filter_val) | 
                Q(description__contains=filter_val) | 
                Q(brand__contains = filter_val) | 
                Q(subcategories__name__contains = filter_val) |
                Q(subcategories__category__name__contains = filter_val)
            ).order_by(order_by)
        else:
            prod = Product.objects.filter().order_by(order_by)
        return prod

    def get_context_data(self, **kwargs):
        context = super(ProductsListview, self).get_context_data(**kwargs)
        context['filter']=self.request.GET.get('filter','')
        context['order_by']=self.request.GET.get('order_by','id')
        context['all_table_data']=Product._meta.get_fields()
        return context

class ProductsUpdate(UserPassesTestMixin,SuccessMessageMixin, UpdateView):
    model = Product
    success_message = 'Products updated successfuly'
    fields = '__all__'
    template_name = 'ctm_admin/productupdate.html'

    def test_func(self):
        try:
            return self.request.user.is_superuser
        except Exception as e:
            return False