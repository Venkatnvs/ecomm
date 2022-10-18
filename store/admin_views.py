from django.shortcuts import HttpResponse, render
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from clients.models import Customer, EditorType
from .models import *
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect
from django.db.models import Q
from django.conf import settings
import os
import json
from django.views import View

@login_required()
def main(request):
    return render(request, 'ctm_admin/index.html')

def ckeditor(request):
    return render(request, 'ctm_admin/ckeditor.html')

class CategoryListview(ListView):
    model = Category
    template_name = 'ctm_admin/categorylistview.html'
    paginate_by = 4

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

class CategoryCreate(SuccessMessageMixin, CreateView):
    model = Category
    success_message = 'Category created successfuly'
    fields = '__all__'
    template_name = 'ctm_admin/categorycreate.html'

class CategoryUpdate(SuccessMessageMixin, UpdateView):
    model = Category
    success_message = 'Category updated successfuly'
    fields = '__all__'
    template_name = 'ctm_admin/categoryupdate.html'

class SubCategoryListview(ListView):
    model = SubCategory
    template_name = 'ctm_admin/subcategorylistview.html'
    paginate_by = 4

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

class SubCategoryCreate(SuccessMessageMixin, CreateView):
    model = SubCategory
    success_message = 'Subcategory created successfuly'
    fields = '__all__'
    template_name = 'ctm_admin/subcategorycreate.html'

class SubCategoryUpdate(SuccessMessageMixin, UpdateView):
    model = SubCategory
    success_message = 'Subcategory updated successfuly'
    fields = '__all__'
    template_name = 'ctm_admin/subcategoryupdate.html'

class SellerUserListview(ListView):
    model = SellerUser
    template_name = 'ctm_admin/seller-user_listview.html'
    paginate_by = 4

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

class SellerUserCreate(SuccessMessageMixin, CreateView):
    model = User
    success_message = 'Seller created successfuly'
    fields = ['first_name', 'last_name', 'email', 'username', 'password']
    template_name = 'ctm_admin/Seller-usercreate.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        states_data = []
        file_path = os.path.join(settings.BASE_DIR, 'states_dist.json')
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


class SellerUserUpdate(SuccessMessageMixin, UpdateView):
    model = User
    success_message = 'Seller created successfuly'
    fields = ['first_name', 'last_name', 'email', 'username']
    template_name = 'ctm_admin/Seller-user_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selleruser']=SellerUser.objects.get(user_type=self.object.customer.pk)
        chs = context['selleruser'].state
        states_data = []
        data_dist = None
        file_path = os.path.join(settings.BASE_DIR, 'states_dist.json')
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

class ProductCreateView(View):
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
        print(request.POST)
        return HttpResponse('form submited')