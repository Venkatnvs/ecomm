from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import UserPassesTestMixin

def Dashboard(request):
    return render(request,'blog/admin/dashboard.html')

class BlogCreate(UserPassesTestMixin,View):
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
            is_by_seller=False
        elif user_type=='Seller':
            is_by_seller=True
        context = {
            'is_by_seller':is_by_seller,
        }
        return render(request, 'blog/admin/blog_create.html', context)
