from django import forms
from coodernador.models import Evolucao

class RelatoSessaoForm(forms.ModelForm):
    class Meta:
        model = Evolucao
        fields = ['descricao']
        widgets = {
            'descricao': forms.Textarea(attrs={
                'class': 'form-control w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all resize-none',
                'rows': 5,
                'maxlength': '500',  # Bloqueia no front
                'placeholder': 'Descreva de forma objetiva: Humor, Tópico Central, Intervenção e Desfecho.',
                'id': 'descricao'
            }),
        }
