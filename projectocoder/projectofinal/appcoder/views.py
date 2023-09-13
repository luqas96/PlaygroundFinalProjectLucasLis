from django.shortcuts import render
from .models import Curso

from .forms import CursoFormulario, ProfesorFormulario
from .models import Curso, Profesor
# Create your views here.


from django.views.generic import ListView, CreateView, DeleteView, UpdateView, DetailView
from django.urls import reverse_lazy



def inicio_view(request):
    return render(request, "appcoder/inicio.html")


def cursos_view(request):
    if request.method == "GET":
        print("+" * 90) #  Imprimimos esto para ver por consola
        print("+" * 90) #  Imprimimos esto para ver por consola
        return render(
            request,
            "appcoder/curso_avanzado_formulario.html",
            {"form": CursoFormulario()}
        )
    else:
        print("*" * 90)     #  Imprimimos esto para ver por consola
        print(request.POST) #  Imprimimos esto para ver por consola
        print("*" * 90)     #  Imprimimos esto para ver por consola

        modelo = Curso(curso=request.POST["curso"], camada=request.POST["camada"])
        modelo.save()
        return render(
            request,
            "appcoder/inicio.html",
        )


def cursos_crud_read_view(request):
    cursos = Curso.objects.all()
    return render(request, "appcoder/cursos_lista.html", {"cursos": cursos})


def profesor_view(request):
    if request.method == "GET":
        return render(
            request,
            "appcoder/profesor_avanzado_formulario.html",
            {"form": ProfesorFormulario()}
        )
    else:
        formulario = ProfesorFormulario(request.POST)
        if formulario.is_valid():
            informacion = formulario.cleaned_data
            modelo = Profesor(
                nombre=informacion["nombre"],
                apellido=informacion["apellido"],
                email=informacion["email"],
                profesion=informacion["profesion"]
            )
            modelo.save()
        return render(
            request,
            "appcoder/inicio.html",
        )

def profesores_crud_read_view(request):
    profesores = Profesor.objects.all()
    return render(request, "appcoder/profesores_lista.html", {"profesores": profesores})


def profesores_crud_delete_view(request, profesor_email):
    profesor_a_eliminar = Profesor.objects.filter(email=profesor_email).first()
    profesor_a_eliminar.delete()
    return profesores_crud_read_view(request)


def profesores_crud_update_view(request, profesor_email):
    profesor = Profesor.objects.filter(email=profesor_email).first()
    if request.method == "GET":
        formulario = ProfesorFormulario(
            initial={
                "nombre": profesor.nombre,
                "apellido": profesor.apellido,
                "email": profesor.email,
                "profesion": profesor.profesion
            }
        )
        return render(request, "appcoder/profesores_formulario_edicion.html", {"form": formulario, "profesor": profesor})
    else:
        formulario = ProfesorFormulario(request.POST)
        if formulario.is_valid():
            informacion = formulario.cleaned_data
            profesor.nombre=informacion["nombre"]
            profesor.apellido=informacion["apellido"]
            profesor.email=informacion["email"]
            profesor.profesion=informacion["profesion"]
            profesor.save()
        return profesores_crud_read_view(request)



####################  ClassBasedViews (CBV)  - Vistas basadas en Clases #########################################

class CursoListView(ListView):
    model = Curso
    context_object_name = "cursos"
    template_name = "appcoder/cbv_curso_list.html"


class CursoDetail(DetailView):
    model = Curso
    template_name = "appcoder/cbv_curso_detail.html"


class CursoCreateView(CreateView):
    model = Curso
    template_name = "appcoder/cbv_curso_create.html"
    success_url = reverse_lazy("curso-list")
    fields = ["curso", "camada"]


class CursoUpdateView(UpdateView):
    model = Curso
    template_name = "appcoder/cbv_curso_update.html"
    success_url = reverse_lazy("curso-list")
    fields = ["curso"]

class CursoDeleteView(DeleteView):
    model = Curso
    template_name = "appcoder/cbv_curso_delete.html"
    success_url = reverse_lazy("curso-list")



from .forms import UserCreationFormulario, UserEditionFormulario
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin


def registro_view(request):

    if request.method == "GET":
        return render(
            request,
            "appcoder/registro.html",
            {"form": UserCreationFormulario()}
        )
    else:
        formulario = UserCreationFormulario(request.POST)
        if formulario.is_valid():
            informacion = formulario.cleaned_data
            usuario = informacion["username"]
            formulario.save()

            return render(
                request,
                "appcoder/inicio.html",
                {"mensaje": f"Usuario creado: {usuario}"}
            )
        else:
            return render(
                request,
                "appcoder/registro.html",
                {"form": formulario}
            )


            # Login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.contrib.auth import login, authenticate

def login_view(request):

    if request.user.is_authenticated:
        return render(
            request,
            "appcoder/inicio.html",
            {"mensaje": f"Ya estás autenticado: {request.user.username}"}
        )


    if request.method == "GET":
        return render(
            request,
            "appcoder/login.html",
            {"form": AuthenticationForm()}
        )
    else:
        formulario = AuthenticationForm(request, data=request.POST)
        if formulario.is_valid():
            informacion = formulario.cleaned_data
            usuario = informacion["username"]
            password = informacion["password"]
            modelo = authenticate(username=usuario, password=password)
            login(request, modelo)

        return render(
            request,
            "appcoder/inicio.html",
            {"mensaje": f"Bienvenido "}
        )

def logout_view(request):
    pass


from .forms import UserCreationFormulario, UserEditionFormulario
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin


def registro_view(request):

    if request.method == "GET":
        return render(
            request,
            "appcoder/registro.html",
            {"form": UserCreationFormulario()}
        )
    else:
        formulario = UserCreationFormulario(request.POST)
        if formulario.is_valid():
            informacion = formulario.cleaned_data
            usuario = informacion["username"]
            formulario.save()

            return render(
                request,
                "appcoder/inicio.html",
                {"mensaje": f"Usuario creado: {usuario}"}
            )
        else:
            return render(
                request,
                "appcoder/registro.html",
                {"form": formulario}
            )

def editar_usuario_view(request):


    if not request.user.is_authenticated:
        return render(
            request,
            "appcoder/login.html",
            {"form": AuthenticationForm()}
        )

    if request.method == "GET":
        return render(
            request,
            "appcoder/editar_usuario.html",
            {"form": UserEditionFormulario()}
        )
    else:
        formulario = UserEditionFormulario(request.POST)
        if formulario.is_valid():
            informacion = formulario.cleaned_data
            print(informacion)
            user = request.user
            user.email = informacion["email"]
            user.first_name = informacion["first_name"]
            user.last_name = informacion["last_name"]
            user.save()
            # formulario.save()

            return render(
                request,
                "appcoder/inicio.html",
                {"mensaje": f"Usuario creado"}
            )
        else:
            return render(
                request,
                "appcoder/editar-usuario.html",
                {"form": formulario}
            )


class CambiarContrasenia(LoginRequiredMixin, PasswordChangeView):
    template_name = "appcoder/cambiar_contrasenia.html"
    success_url = reverse_lazy("editar-usuario")