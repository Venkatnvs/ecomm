from django.shortcuts import render
from django.contrib.auth.decorators import login_required,user_passes_test
from store.models import Category
from django.views.generic import ListView,CreateView, UpdateView, DetailView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Q
from django.contrib.messages.views import SuccessMessageMixin
from clients.models import Customer,SellerUser
from store.details.ctm_admin.models import RequestCategory
from django.contrib import messages
from django.shortcuts import redirect

@login_required
@user_passes_test(lambda u: True if((u.customer.customer_type == 'Admin') or (u.customer.customer_type == 'Seller')) else False)
def main(request):
    return render(request,'ctm_seller/index.html')


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