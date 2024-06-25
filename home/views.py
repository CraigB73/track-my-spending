from django.shortcuts import render, redirect
from allauth.account.forms import LoginForm

# Create your views here.
def home_view(request):
    """
    Renders the Home page
    """
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            return redirect("home/home.html")
    else:
        form = LoginForm()
    return render(request, "home/home.html", { "form": form})