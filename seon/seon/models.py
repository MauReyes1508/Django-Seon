from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator


def validate_phone(value):
    if not value.isdigit() or not (9 <= len(value) <= 15):
        raise ValidationError("El número de teléfono debe contener entre 9 y 15 dígitos y solo puede incluir números.")
  
    
def validar_nit(nit):
    if not nit:
        raise ValidationError("El NIT no puede estar vacío.")
    
    
    nit = nit.replace(" ", "").strip()
    if "-" in nit:
        partes = nit.split("-")
        if len(partes) != 2:
            raise ValidationError("El NIT solo puede tener un guion entre el número principal y el dígito de verificación.")
        
        numero, digito_verificacion = partes
        if not numero.isdigit() or not digito_verificacion.isdigit():
            raise ValidationError("El NIT debe contener solo números antes y después del guion.")
    else:
        numero = nit
        digito_verificacion = numero[-1]
        numero = numero[:-1]
    
    if not numero.isdigit():
        raise ValidationError("El NIT debe contener solo números en su parte principal.")
    
    if len(numero) < 4 or len(numero) > 15:
        raise ValidationError("El número del NIT debe tener entre 4 y 15 dígitos.")
    
    return nit






class Tercero(models.Model):
    # Opciones para los campos de elección
    TIPPER_CHOICES = [
        (0, 'Natural'),
        (1, 'Jurídica'),
    ]
 
    TIPNIT_CHOICES = [
        (1,'NIT'),
        (0, 'Cédula de Ciudadanía'),
        (3, 'Tarjeta de Identidad'),
        (4, 'Registro Civil'),
        (2, 'Pasaporte'),
    ]

    EXCEN_IVA_CHOICES = [
        ('V', 'Si Aplica'),
        ('F', 'No Aplica'),
    ]

    REGIMEN_SIM_CHOICES = [
        ('V', 'Si Aplica'),
        ('F', 'No Aplica'),
    ]

    TIPO_CTA_CHOICES = [
        (0, 'Corriente'),
        (1, 'Ahorros'),
    ]

    TIPTER_CHOICES = [
        (0, 'Cliente'),
        (1,'Proveedor'),
        (2, 'Empleado'),
        (3, 'Inactivos'),
        (4, 'Otros'),
    ]

    TER_ORIGEN_CHOICES = [
        (0, 'Comercial'),
        (1, 'Internet'),
        (2, 'Recomendación'),
        (3, 'Cursos'),
        (4, 'Publicidad'),
    ]

    # Validaciones comunes
    PHONE_VALIDATOR = RegexValidator(
        regex=r'^\+?\d{9,15}$',
        message="El número de teléfono debe tener entre 9 y 15 dígitos y puede comenzar con '+'"
    )

    # Identificación
    codter = models.AutoField(primary_key=True, verbose_name="Código del Tercero")
    tipper = models.SmallIntegerField(choices=TIPPER_CHOICES, verbose_name="Tipo de Persona")  # Tipo de persona
    nomter = models.CharField(max_length=100, null=True, blank=True, verbose_name="Nombre/Razón social")
    papter = models.CharField(max_length=50, null=True, blank=True, verbose_name="Primer apellido")
    sapter = models.CharField(max_length=50, null=True, blank=True, verbose_name="Segundo apellido")
    nomcter = models.CharField(max_length=100, null=True, blank=True, verbose_name="Nombre comercial")
    tipnit = models.SmallIntegerField(choices=TIPNIT_CHOICES) # Tipo de Nit
    nitter = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="NIT/Cédula",
        validators=[validar_nit],
        help_text="(Ingrese el NIT o la cédula sin puntos ni guiones)."
    )

    ########################################################################################################

    # Identificación 2
    tipter = models.SmallIntegerField(choices=TIPTER_CHOICES) # Tipo de tercero
    contacto = models.CharField(max_length=100, null=True, blank=True, verbose_name="Persona de contacto")
    cgo_contac = models.CharField(max_length=50, null=True, blank=True, verbose_name="Cargo del contacto")
    regimen_sim = models.CharField(max_length=1, choices=REGIMEN_SIM_CHOICES, null=True, blank=True, verbose_name="Régimen Simplificado")
    excen_iva = models.CharField(max_length=1, choices=EXCEN_IVA_CHOICES, null=True, blank=True, verbose_name="Exento de IVA")

    ##########################################################################################################

    # Ubicación
    paister = models.CharField(max_length=50, null=True, blank=True, verbose_name="País de residencia", default="Colombia")
    ciuter = models.CharField(max_length=50, null=True, blank=True, verbose_name="Ciudad", default="Bogotá D.C")
    dirter = models.CharField(max_length=150, null=True, blank=True, verbose_name="Dirección")
    direle = models.EmailField(
        max_length=100, 
        null=True, 
        blank=True, 
        verbose_name="Correo electrónico",
    )
    rutater = models.CharField(max_length=20, null=True, blank=True, verbose_name="Ruta")
    telter = models.CharField(
        max_length=20, null=True, blank=True, validators=[validate_phone], verbose_name="Teléfono fijo"
    )
    celter = models.CharField(
        max_length=20, null=True, blank=True, validators=[validate_phone], verbose_name="Teléfono móvil"
    )

    #########################################################################################################

    # Financieros
    cuptot = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True, verbose_name="Cupo total",
        validators=[MinValueValidator(0)]
    )
    saldocup = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True, verbose_name="Saldo del cupo",
        validators=[MinValueValidator(0)]
    )
    descuento = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Descuento (%)",
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    zonater = models.CharField(max_length=50, null=True, blank=True, verbose_name="Zona")
    fecha_ini = models.DateField(null=True, blank=True, verbose_name="Fecha de inicio")
    fecha_fin = models.DateField(null=True, blank=True, verbose_name="Fecha de fin")
    #lispre = models.SmallIntegerField(null=True, blank=True, verbose_name="Lista de precios")

    ###################################################################################################
    
    # Vendedor
    plazofac = models.SmallIntegerField(null=True, blank=True, verbose_name="Plazo de facturación")
    vendedor = models.SmallIntegerField(null=True, blank=True, verbose_name="Código del vendedor")
    cta_banco = models.CharField(max_length=50, null=True, blank=True, verbose_name="Cuenta bancaria")
    cod_banco = models.CharField(max_length=20, null=True, blank=True, verbose_name="Código del banco")
    tipo_cta = models.SmallIntegerField(
        choices=TIPO_CTA_CHOICES, null=True, blank=True, verbose_name="Tipo de cuenta bancaria"
    )
    categoria = models.CharField(max_length=50, null=True, blank=True, verbose_name="Categoría")

    #########################################################################################################

    # Otros
    retfuente = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Retención fuente")
    retica = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Retención ICA")
    retiva = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Retención IVA")
    base_ret_fte = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, verbose_name="Base Retención Fuente")
    base_ret_ica = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, verbose_name="Base Retención ICA")
    base_ret_iva = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, verbose_name="Base Retención IVA")
    lista_base = models.SmallIntegerField(null=True, blank=True, verbose_name="Lista base")
    observa = models.TextField(null=True, blank=True, verbose_name="Observaciones")
    ter_origen = models.SmallIntegerField(null=True, blank=True, verbose_name="Origen del cliente", choices=TER_ORIGEN_CHOICES)
    localidad = models.CharField(max_length=50, null=True, blank=True, verbose_name="Localidad")
    barrio = models.CharField(max_length=50, null=True, blank=True, verbose_name="Barrio")

    #####################################################################################################################################

   
    """ descuento_2 = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Descuento adicional (%)",
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    lisvar = models.SmallIntegerField(null=True, blank=True, verbose_name="Lista variable")
    codalter = models.IntegerField(null=True, blank=True, verbose_name="Código alternativo")
    
    des_origen = models.CharField(max_length=50, null=True, blank=True, verbose_name="Descripción del origen") """
    


    # Métodos útiles
    def __str__(self):
        return f"{self.get_tipnit_display()} - {self.nomter or self.nomcter}"

    def get_tipo_persona_display(self):
        return self.get_tipper_display()

    def get_tipo_nit_display(self):
        return self.get_tipnit_display()

    def get_tipo_tercero_display(self):
        return self.get_tipter_display()
    
    def get_regimen_simpli_display(self):
        return self.get_regimen_sim_display()
    
    def get_excento_iva_display(self):
        return self.get_excen_iva_display()
    
    def get_tipo_cuenta_display(self):
        return self.get_tipo_cta_display()
    
    def get_tercero_orgien_display(self):
        return self.get_ter_origen_display()
    
    



    class Meta:
        verbose_name = "Tercero"
        verbose_name_plural = "Terceros"
        ordering = ['nomter']
        managed = False
        db_table = 'TERCEROS'
