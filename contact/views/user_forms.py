from contact.forms import RegisterForm, RegisterUpdateForm
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render


def register(request):
    form = RegisterForm()





    if request.method== "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Usuário Registrado")
            return redirect('contact:index')
            

    return render(
        request, 
        "contact/register.html",
        {
            "form": form
        }
    )

def login_view(request):

    if request.user.is_authenticated:
        return redirect("contact:index")

    form = AuthenticationForm(request)

    if request.method == "POST":
        form = AuthenticationForm(request, data = request.POST)

        if form.is_valid():
            user = form.get_user()
            messages.success(request, f"Bem vindo {user.username}")
            auth.login(request, user)
            return redirect("contact:index")
        messages.error(request, "Usuário ou senha inválidos")

    return render(
        request,
        "contact/login.html",
        {
            "form": form
        }
    )

@login_required(login_url="contact:login")
def logout_view(request):

    auth.logout(request)
    return redirect("contact:login")

@login_required(login_url="contact:login")
def user_update(request):

    form = RegisterUpdateForm(instance=request.user)

    if request.method != "POST":
        return render(
            request,
            "contact/user_update.html",
            {
                "form": form
            }
        )

    form = RegisterUpdateForm(data = request.POST, instance=request.user)

    if not form.is_valid():
        return render(
        request,
        "contact/user_update.html",
        {
            "form": form
        }
        )
    
    form.save()
    messages.success(request, "Usuário Atualizado")
    return redirect("contact:user_update")
