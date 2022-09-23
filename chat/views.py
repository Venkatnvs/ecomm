from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'chatapp/index.html')

def room(request, room_name):
    context = {
        'room_name': room_name
    }
    return render(request, 'chatapp/room.html', context)


# <script type="module">
#   // Import the functions you need from the SDKs you need
#   import { initializeApp } from "https://www.gstatic.com/firebasejs/9.9.3/firebase-app.js";
#   import { getAnalytics } from "https://www.gstatic.com/firebasejs/9.9.3/firebase-analytics.js";
#   // https://firebase.google.com/docs/web/setup#available-libraries

#   // Your web app's Firebase configuration
#   // For Firebase JS SDK v7.20.0 and later, measurementId is optional
#   const firebaseConfig = {
#     apiKey: "AIzaSyDVVBY6eU-ZXYUpmWOqrCjbndrwQUpdm2c",
#     authDomain: "nvshome-9d163.firebaseapp.com",
#     projectId: "nvshome-9d163",
#     storageBucket: "nvshome-9d163.appspot.com",
#     messagingSenderId: "772976899813",
#     appId: "1:772976899813:web:39caa29ca6633ee0dc460c",
#     measurementId: "G-M4G9K15CYR"
#   };

#   // Initialize Firebase
#   const app = initializeApp(firebaseConfig);
#   const analytics = getAnalytics(app);
# </script>
# zvcbeeeycnktkwho