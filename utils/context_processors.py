from django.conf import settings
from store.utilitys import GetSubAndMainCate

def ecommdetails(request):
    context = {
        'site_name':settings.SITE_NAME,
        'categories':GetSubAndMainCate(request)['categories_list'],
        'animations':settings.SHOW_ANIMATIONS,
    }
    return context