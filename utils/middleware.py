from .models import UserView

class TrackUserViewsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # Get the UserView object for the current user or create one if it doesn't exist
            user_view, created = UserView.objects.get_or_create(user=request.user.customer)

            # Increment the view count for the user
            user_view.view_count += 1
            user_view.save()

        response = self.get_response(request)
        return response