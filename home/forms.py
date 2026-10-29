from django import forms


class ContactoForm(forms.Form):
    nombre_completo = forms.CharField(
        label="Nombre completo",
        max_length=150,
        widget=forms.TextInput(attrs={"autocomplete": "name", "placeholder": "Escribe tu nombre completo"}),
    )
    telefono = forms.CharField(
        label="Teléfono",
        max_length=20,
        widget=forms.TextInput(attrs={"autocomplete": "tel", "inputmode": "tel", "placeholder": "Número de teléfono"}),
    )
    municipio = forms.CharField(
        label="Municipio",
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder": "Escribe tu municipio"}),
    )
    correo = forms.EmailField(
        label="Correo electrónico",
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email", "placeholder": "correo@ejemplo.com"}),
    )
    mensaje = forms.CharField(
        label="Descripción del mensaje",
        max_length=5000,
        widget=forms.Textarea(attrs={"rows": 6, "placeholder": "Describe cómo podemos ayudarte"}),
    )
    consentimiento = forms.BooleanField(
        required=True,
        label="He leído el Aviso de Privacidad y entiendo el tratamiento de mis datos personales.",
        error_messages={"required": "Debes aceptar esta declaración para enviar el formulario."},
    )

    def clean_telefono(self):
        telefono = self.cleaned_data["telefono"].strip()
        digits = "".join(character for character in telefono if character.isdigit())
        if len(digits) < 10 or len(digits) > 15:
            raise forms.ValidationError("Escribe un teléfono válido (de 10 a 15 dígitos).")
        return telefono
