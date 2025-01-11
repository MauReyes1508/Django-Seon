from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q

from .models import Tercero
from .form import LoginForm, TerceroForm, UserRegistrationForm

# Registro de un usuario
@user_passes_test(lambda u: u.is_superuser)
def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirige a una página de éxito o el que prefieras
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})

# Verificación de creedenciales e inicio de sesión
def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Bienvenido, {user.username}!")
            return redirect('menu_rutinas')
        else:
            messages.error(request, "Credenciales inválidas.")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})



@login_required
def menu_rutinas(request):
    usuario = request.session.get('usuario', None)
    print(f"Usuario actual: {usuario}")
    return render(request, 'menu_rutinas.html', {'usuario': usuario})

@login_required
def logout_view(request):
    logout(request)
    print(request.session.items())
    messages.success(request, "Has cerrado sesión exitosamente.")
    return redirect('login') 


############## REGISTRO DE TERCEROS ###################################################################################

def registro_terceros(request):
    if request.method == 'POST':
        form = TerceroForm(request.POST)
        if form.is_valid():
            print("Formulario válido")
            form.save()  # Guarda el nuevo registro.
            messages.success(request, "Registro Guardado Correctamente")
            return redirect('registro_terceros')  # Redirige a la lista de registros.
        else:
            print("Errores en el formulario:", form.errors)
            # Aquí, pasamos los errores directamente a la plantilla
            return render(request, 'terceros/registro_terceros.html', {
                'form': form,
                'errors': form.errors
            })
    else:
        form = TerceroForm()  # Inicializa un formulario vacío para GET.

    return render(request, 'terceros/registro_terceros.html', {
        'form': form,
        'errors': form.errors if form.errors else None,
    })




def lista_terceros(request):
    # Obtener el término de búsqueda desde la URL
    query = request.GET.get('q', '')  # Captura el término de búsqueda desde el formulario.
    
    # Filtrar registros según el término de búsqueda
    if query:
        # Se filtran por código, nombre o número de cédula
        terceros = Tercero.objects.filter(
            Q(codter__icontains=query) |  # Búsqueda por código
            Q(nomter__icontains=query) |  # Búsqueda por nombre
            Q(nitter__icontains=query)    # Búsqueda por número de cédula
        )
    else:
        # Si no hay búsqueda, obtenemos todos los registros
        terceros = Tercero.objects.all().order_by('codter') # Se limitan los datos de busquedas para no sobrecargar el programa

    # Manejo de eliminación de registros
    if request.method == 'POST' and 'eliminar_id' in request.POST:
        tercero = get_object_or_404(Tercero, pk=request.POST.get('eliminar_id'))  # Obtiene el registro a eliminar.
        try:
            tercero.delete()  # Elimina el registro.
            messages.success(request, "Registro Eliminado Correctamente! 🧐")
        except Exception as e:
            messages.error(request, f"Error Al Eliminar Registro: {e}")
            
            return redirect('lista_terceros')  # Redirige a la lista.

    # Formulario vacío para edición (cuando no se está editando)
    form = TerceroForm()

    # Contexto para la plantilla
    context = {
        'terceros': terceros,  # Lista de terceros filtrados.
        'form': form,  # Formulario para editar.
        'query': query,  # Término de búsqueda actual.
    }
    return render(request, 'terceros/lista_terceros.html', context)



def actualizar_tercero(request):
    if request.method == 'POST':
        codter = request.POST.get('codter')
        
        # Verificar si el código fue recibido
        if not codter:
            messages.error(request, "No se proporcionó un código válido para actualizar.")
            return redirect('lista_terceros')

        print("Código recibido:", codter)  # Debugging

        # Intentar obtener el registro por el código
        tercero = get_object_or_404(Tercero, codter=codter)

        # Actualizar los datos del modelo con los valores del formulario
        campos = [
            'fecha_ini', 'nomter', 'papter', 'sapter', 'nomcter', 'tipper', 'nitter',
            'direle', 'celter', 'paister', 'ciuter', 'dirter', 'localidad', 'barrio', 'regimen_sim', 'excen_iva',
            'ter_origen', 'fecha_fin', 'cuptot', 'saldocup', 'descuento', 'zonater',
            'plazofac', 'vendedor', 'cta_banco', 'cod_banco', 'tipo_cta', 'categoria',
            'base_ret_fte', 'retfuente', 'base_ret_ica', 'retica', 'base_ret_iva',
            'retiva', 'lista_base', 'observa'
        ]

        for campo in campos:
            valor = request.POST.get(campo)
            if valor:
                setattr(tercero, campo, valor)
            else:
                setattr(tercero, campo, None)  # Asignar None si no hay valor

        print("Datos actualizados para guardar:", tercero.__dict__)  # Verificar el objeto antes de guardar
        tercero.save()

        # Mensaje de éxito
        messages.success(request, "Los cambios fueron guardados correctamente. 🥳")

        # Redirigir a la lista de terceros
        return redirect('lista_terceros')

    # Si no es un POST, redirigir a la lista
    messages.error(request, "Método no permitido.")
    return redirect('lista_terceros')



