from django.contrib import admin
from .models import *

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Product)
admin.site.register(ProductMedia)
admin.site.register(ProductTransaction)
admin.site.register(ProductDetails)
admin.site.register(ProductAbout)
admin.site.register(ProductTags)
admin.site.register(ProductQuestions)
admin.site.register(ProductReviews)
admin.site.register(ProductReviewsVoting)
admin.site.register(ProductVarient)
admin.site.register(ProductVarientItems)