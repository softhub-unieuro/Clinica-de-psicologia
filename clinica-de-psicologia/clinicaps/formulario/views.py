from django.http import JsonResponse
from django.shortcuts import render
from .forms import InscritoComunidadeForm, InscritoConvenioForm
import json

def tela_inicial_view(request):
    return render(request, 'inicial.html')

def formulario_comunidade_view(request):
    # A view 'GET' apenas renderiza o seu template HTML
    if request.method == 'GET':
        return render(request, 'comunida_form.html')

    # A view 'POST' é o que seu JavaScript chama via 'fetch'
    if request.method == 'POST':
        try:
            # O JS envia JSON, então lemos o 'request.body'
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'erro', 'mensagem': 'JSON inválido.'}, status=400)
        form = InscritoComunidadeForm(data)

        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'sucesso', 'mensagem': 'Inscrição realizada com sucesso!'})
        else:
            erros_para_js = dict(form.errors)

            return JsonResponse({'status': 'erro_validacao', 'erros': erros_para_js}, status=400)

    # Se for outro método (PUT, etc.)
    return JsonResponse({'status': 'erro', 'mensagem': 'Método não permitido.'}, status=405)

def formulario_convenio_view(request):

    if request.method == 'GET':
        return render(request, 'convenio_form.html')

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'erro', 'mensagem': 'JSON inválido.'}, status=400)
        
        form = InscritoConvenioForm(data)

        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'sucesso', 'mensagem': 'Inscrição realizada com sucesso!'})
        else:
            erros_para_js = dict(form.errors)

            return JsonResponse({'status': 'erro_validacao', 'erros': erros_para_js}, status=400)

    return JsonResponse({'status': 'erro', 'mensagem': 'Método não permitido.'}, status=405)


def formulario_test_view(request):

    if request.method == 'GET':
        return render(request, 'convenio_form.html')

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'erro', 'mensagem': 'JSON inválido.'}, status=400)
        
        form = InscritoConvenioForm(data)

        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'sucesso', 'mensagem': 'Inscrição realizada com sucesso!'})
        else:
            erros_para_js = dict(form.errors)

            return JsonResponse({'status': 'erro_validacao', 'erros': erros_para_js}, status=400)

    return JsonResponse({'status': 'erro', 'mensagem': 'Método não permitido.'}, status=405)



