from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario


class RegistroForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        help_text="Ingresa un correo válido 💌"
    )

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'password1', 'password2']

    # 🔥 VALIDAR USERNAME ÚNICO
    def clean_username(self):
        username = self.cleaned_data.get('username')

        if Usuario.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("Este nombre de usuario ya está registrado 😢")

        return username

    # 🔥 VALIDAR EMAIL ÚNICO
    def clean_email(self):
        email = self.cleaned_data.get('email')

        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo ya está registrado 😢")

        return email

    # 💾 GUARDAR USUARIO
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user