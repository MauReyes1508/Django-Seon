from django import forms
from .models import Tercero
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm  

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise ValidationError("Las contraseñas no coinciden.")
        return cleaned_data

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=254, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Usuario'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}))

class TerceroForm(forms.ModelForm):
    class Meta:
        model = Tercero
        fields = "__all__" 

        widgets = {
            'fecha_ini': forms.DateInput(attrs={'type': 'date'}), 
            'fecha_fin': forms.DateInput(attrs={'type': 'date'}),
            'regimen_sim': forms.Select(attrs={'class': 'form-control'}),
            'excen_iva': forms.Select(attrs={'class': 'form-control'}),
            'ter_origen': forms.Select(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['tipper'].widget = forms.Select(choices=Tercero.TIPPER_CHOICES)
        self.fields['tipnit'].widget = forms.Select(choices=Tercero.TIPNIT_CHOICES)
        self.fields['tipper'].widget.choices = [("", "Seleccionar...")] + Tercero.TIPPER_CHOICES
        self.fields['tipnit'].choices = [("", "Seleccione el tipo de Persona")]
        self.fields['tipo_cta'].widget = forms.Select(choices=Tercero.TIPO_CTA_CHOICES)

        self.fields['regimen_sim'].required = False
        self.fields['excen_iva'].required = False
        self.fields['ter_origen'].required = False

        self.fields['tipnit'].widget.attrs.update({'class': 'form-select'})
        self.fields['tipper'].widget.attrs.update({'class': 'form-select'})
        self.fields['cuptot'].widget.attrs.update({'class': 'decimal-input'})
        self.fields['saldocup'].widget.attrs.update({'class': 'decimal-input'})
        self.fields['descuento'].widget.attrs.update({'class': 'percentage-input'})

        TIPNIT_CHOICES_NATURAL = [
            (0, 'Cédula de Ciudadanía'),
            (3, 'Tarjeta de Identidad'),
            (4, 'Registro Civil'),
            (2, 'Pasaporte'),
        ]

        TIPNIT_CHOICES_JURIDICA = [
            (1, 'NIT'),
        ]

        ## Tipo de persona ##
        tipper = self.initial.get("tipper", None) or self.data.get("tipper", None)

        # Persona Natural

        if tipper == "0":
            self.fields['tipnit'].choices += TIPNIT_CHOICES_NATURAL

        # Persona Jurídica

        elif tipper == "1":
            self.fields['tipnit'].choices += TIPNIT_CHOICES_JURIDICA
        else:
            self.fields['tipnit'].choices = []


    def clean(self):
        cleaned_data = super().clean()
        tipper = cleaned_data.get("tipper")
        tipnit = cleaned_data.get("tipnit")
        nitter = cleaned_data.get("nitter")

        # Validación para Persona Natural
        if tipper == "0":  # Persona Natural
            if tipnit not in [0, 2, 3, 4]:
                raise forms.ValidationError("Una persona NATURAL solo puede usar cédula, tarjeta de identidad o registro civil")

        # Validación para Persona Jurídica
        elif tipper == "1":  # Persona Jurídica
            if tipnit != 1:
                raise forms.ValidationError("Una persona JURÍDICA solo puede usar el documento de tipo NIT")

            # Validar que el NIT contenga solo números
            if not nitter or not nitter.strip().isdigit():
                raise forms.ValidationError("El NIT debe contener únicamente números para personas jurídicas")
            
            # Validar la longitud del NIT
            if not (5 <= len(nitter.strip()) <= 15):
                raise forms.ValidationError("El NIT o Documento debe contener entre 5 y 15 caracteres")

        return cleaned_data


    def clean_telter(self):
        tel = self.cleaned_data.get("telter")
        if tel:
            if not tel.isdigit() or len(tel) < 9 or len(tel) > 15:
                raise forms.ValidationError("El teléfono debe contener entre 9 y 15 dígitos, sin caracteres especiales.")
        return tel

    def clean_celter(self):
        cel = self.cleaned_data.get("celter")
        if cel:
            if not cel.isdigit() or len(cel) < 9 or len(cel) > 15:
                raise forms.ValidationError("El móvil debe contener entre 9 y 15 dígitos, sin caracteres especiales.")
        return cel
    
    def clean_excento_iva(self):
        excen_iva = self.cleaned_data.get('excen_iva')
        if excen_iva is None:  # Si el campo no tiene valor, lo dejamos como None (vacío)
            return None
        return excen_iva

    def clean_regimen_simplificado(self):
        regimen_sim = self.cleaned_data.get('regimen_sim')
        if regimen_sim is None:  # Si el campo no tiene valor, lo dejamos como None (vacío)
            return None
        return regimen_sim


