from django import forms

class MessageForm(forms.Form):
    mensagens = forms.CharField(
        max_length=255,
        label='Mensagem',
        widget=forms.Textarea(
            attrs={"rows": "5", "class": "form-control", "placeholder": "Digite sua mensagem aqui..."}
        )
    )
