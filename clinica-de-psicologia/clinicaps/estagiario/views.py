from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.db.models import Q
from django.core.paginator import Paginator
from datetime import date
from formulario.models import Inscritocomunidade, Inscritoconvenio, Doencafisica, Medicamento, Disponibilidade, Endereco, Motivoacompanhamento
from coodernador.models import Prontuario, Evolucao
from usuarios.models import Usuario
from .forms import RelatoSessaoForm
from datetime import date, datetime

@login_required
def dashboard_estagiario(request):
    """
    Dashboard principal do Estagiário.
    Exibe seus pacientes vinculados e atendimentos da semana.
    """
    prontuarios = Prontuario.objects.filter(estagiario=request.user).select_related('paciente_comunidade', 'paciente_convenio')
    atendimentos = [
        {
            'paciente_nome': 'Maria Silva', 
            'status': 'Pendente', 
            'data': date(2025, 5, 14), 
            'acao_label': 'Aberto'
        },
        {
            'paciente_nome': 'Rafael Costa', 
            'status': 'Atendido', 
            'data': date(2025, 6, 10), 
            'acao_label': 'Fechado'
        },
    ]

    context = {
        'prontuarios': prontuarios,
        'atendimentos': atendimentos,
    }
    return render(request, 'DashboardEstagiario.html', context)

def get_label_terapia_optimized(inscrito, origem):
    """
    Versão otimizada que espera que os objetos relacionados já tenham sido carregados
    via prefetch_related ('tipoterapias' ou 'tipoterapia_set').
    """
    try:
        tipo_obj = None
        if origem == 'comunidade':
            tipos = list(getattr(inscrito, 'tipoterapias', []).all())
            tipo_obj = tipos[0] if tipos else None
        else:
            tipos = list(getattr(inscrito, 'tipoterapia_set', []).all())
            tipo_obj = tipos[0] if tipos else None
            
        if not tipo_obj:
            return "Não informado"
            
        labels = []
        if getattr(tipo_obj, 'individualift', False): labels.append("Infantil")
        if getattr(tipo_obj, 'individualadt', False): labels.append("Adolescente")
        if getattr(tipo_obj, 'individualadto', False): labels.append("Adulto")
        if getattr(tipo_obj, 'individualids', False): labels.append("Idoso")
        if getattr(tipo_obj, 'familia', False): labels.append("Família")
        if getattr(tipo_obj, 'grupo', False): labels.append("Grupo")
        if getattr(tipo_obj, 'casal', False): labels.append("Casal")
        
        return ", ".join(labels) if labels else "Não especificado"
    except Exception:
        return "Erro"

def transform_inscrito_dto(inscrito, origem):
    """
    Transforma um objeto de modelo em um dicionário (DTO) para a view,
    evitando injeção de atributos no objeto.
    """
    return {
        'pk': inscrito.pk,
        'nomeinscrito': inscrito.nomeinscrito,
        'dthinscricao': inscrito.dthinscricao,
        'tipo_origem': origem,
        'tipo_atendimento_label': get_label_terapia_optimized(inscrito, origem)
    }

@login_required
def consulta_inscritos(request):
    """
    Tela para consultar inscritos disponíveis e gerenciar os atribuídos.
    Refatorada para performance: Paginação real e Prefetch.
    """
    prontuarios_qs = Prontuario.objects.filter(estagiario=request.user)\
        .select_related('paciente_comunidade', 'paciente_convenio')\
        .prefetch_related(
            'paciente_comunidade__tipoterapias',
            'paciente_convenio__tipoterapia_set'
        )
    prontuarios_atribuidos = []
    for p in prontuarios_qs:
        if p.paciente_comunidade:
            p.tipo_atendimento_label = get_label_terapia_optimized(p.paciente_comunidade, 'comunidade')
        elif p.paciente_convenio:
            p.tipo_atendimento_label = get_label_terapia_optimized(p.paciente_convenio, 'convenio')
        else:
            p.tipo_atendimento_label = "-"
        prontuarios_atribuidos.append(p)
    ids_comunidade_vinculados = Prontuario.objects.filter(status_ativo=True).exclude(paciente_comunidade__isnull=True).values_list('paciente_comunidade_id', flat=True)
    ids_convenio_vinculados = Prontuario.objects.filter(status_ativo=True).exclude(paciente_convenio__isnull=True).values_list('paciente_convenio_id', flat=True)
    qs_comunidade = Inscritocomunidade.objects.exclude(idfichacomunidade__in=ids_comunidade_vinculados)\
        .order_by('dthinscricao')\
        .prefetch_related('tipoterapias')
        
    qs_convenio = Inscritoconvenio.objects.exclude(idfichaconvenio__in=ids_convenio_vinculados)\
        .order_by('dthinscricao')\
        .prefetch_related('tipoterapia_set')
    page_comunidade_num = request.GET.get('page_comunidade', 1)
    page_convenio_num = request.GET.get('page_convenio', 1)
    
    paginator_com = Paginator(qs_comunidade, 50) # 50 por página
    page_obj_com = paginator_com.get_page(page_comunidade_num)
    
    paginator_conv = Paginator(qs_convenio, 50) # 50 por página
    page_obj_conv = paginator_conv.get_page(page_convenio_num)
    lista_comunidade = [transform_inscrito_dto(i, 'comunidade') for i in page_obj_com]
    lista_convenio = [transform_inscrito_dto(i, 'convenio') for i in page_obj_conv]

    form_evolucao = RelatoSessaoForm()

    context = {
        'prontuarios_atribuidos': prontuarios_atribuidos,
        'lista_comunidade': lista_comunidade,
        'lista_convenio': lista_convenio,
        'page_obj_com': page_obj_com,
        'page_obj_conv': page_obj_conv,
        'form_evolucao': form_evolucao,
    }
    return render(request, 'consulta_inscritos.html', context)

@login_required
def vincular_paciente(request):
    if request.method == 'POST':
        tipo = request.POST.get('tipo')
        id_inscrito = request.POST.get('id')
        if not request.user.supervisor_vinculado:
            messages.error(request, "Você não possui um Supervisor vinculado. Contate a coordenação.")
            return redirect('estagiario:consulta_inscritos')

        coordenador = Usuario.objects.filter(cargo='COORD').first()
        if not coordenador:
            messages.error(request, "Não há Coordenador cadastrado no sistema para validar o vínculo.")
            return redirect('estagiario:consulta_inscritos')

        # Criar Prontuário
        try:
            with transaction.atomic():
                # Verificar limite de atendimentos do estagiário
                limite = 5 if request.user.nivel_estagio == 'AVANCADO' else 3
                qtd_atual = Prontuario.objects.filter(estagiario=request.user).count()
                
                if qtd_atual >= limite:
                    nivel_label = request.user.get_nivel_estagio_display() if request.user.nivel_estagio else 'Básico'
                    messages.error(request, f"Limite de atendimentos atingido ({limite}) para o nível {nivel_label}.")
                    return redirect('estagiario:consulta_inscritos')

                # Verificar se o paciente já está vinculado a ALGUÉM (não apenas ao usuário atual)
                if tipo == 'comunidade':
                    # Bloqueia o registro para evitar race condition
                    inscrito = get_object_or_404(Inscritocomunidade.objects.select_for_update(), idfichacomunidade=id_inscrito)
                    
                    if Prontuario.objects.filter(paciente_comunidade_id=id_inscrito).exists():
                        messages.error(request, "Este paciente já está vinculado a outro estagiário.")
                        return redirect('estagiario:consulta_inscritos')
                    
                elif tipo == 'convenio':
                    inscrito = get_object_or_404(Inscritoconvenio.objects.select_for_update(), idfichaconvenio=id_inscrito)

                    if Prontuario.objects.filter(paciente_convenio_id=id_inscrito).exists():
                        messages.error(request, "Este paciente já está vinculado a outro estagiário.")
                        return redirect('estagiario:consulta_inscritos')

                prontuario = Prontuario(
                    estagiario=request.user,
                    supervisor=request.user.supervisor_vinculado,
                    coordenador=coordenador
                )

                if tipo == 'comunidade':
                    prontuario.paciente_comunidade = inscrito
                elif tipo == 'convenio':
                    prontuario.paciente_convenio = inscrito
                
                prontuario.save()
                messages.success(request, f"Paciente {inscrito.nomeinscrito} vinculado com sucesso!")
            
        except Exception as e:
            messages.error(request, f"Erro ao vincular paciente: {str(e)}")

    return redirect('estagiario:consulta_inscritos')

@login_required
def adicionar_evolucao(request):
    if request.method == 'POST':
        id_prontuario = request.POST.get('idprontuario')
        data_atendimento = request.POST.get('data_atendimento')

        # ✅ TRATAMENTO CORRETO DA DATA
        if data_atendimento:
            try:
                data_atendimento = datetime.strptime(data_atendimento, '%Y-%m-%d').date()
            except ValueError:
                data_atendimento = date.today()
        else:
            data_atendimento = date.today()

        form = RelatoSessaoForm(request.POST)
        
        if form.is_valid():
            descricao = form.cleaned_data['descricao']

            prontuario = get_object_or_404(
                Prontuario, 
                idprontuario=id_prontuario, 
                estagiario=request.user
            )

            # 🚨 BLOQUEIO DE PRONTUÁRIO ARQUIVADO
            if not prontuario.status_ativo:
                messages.error(request, "Não é possível adicionar evolução a um prontuário arquivado.")
                return redirect('estagiario:consulta_inscritos')

            try:
                Evolucao.objects.create(
                    prontuario=prontuario,
                    data_atendimento=data_atendimento,
                    descricao=descricao
                )
                messages.success(request, "Evolução registrada com sucesso!")
            except Exception as e:
                messages.error(request, f"Erro ao registrar evolução: {str(e)}")
        else:
            messages.error(request, "Erro no formulário. Verifique os dados.")

    return redirect('estagiario:consulta_inscritos')

def get_boolean_labels(instance, field_map):
    """
    Helper para extrair labels de campos booleanos True.
    """
    labels = []
    if not instance:
        return labels
    
    for field_name, label in field_map.items():
        if getattr(instance, field_name, False):
            labels.append(label)
    return labels

@login_required
def dados_inscrito(request, pk):
    """
    Visualiza os dados detalhados de um inscrito vinculado (Prontuário).
    """
    prontuario = get_object_or_404(Prontuario, idprontuario=pk)
    
    # Verifica permissões: Estagiário dono, Supervisor vinculado, RT ou Coordenador
    has_permission = False
    if request.user.cargo in ['COORD', 'RESP_TEC']:
        has_permission = True
    elif request.user.cargo == 'SUPER':
        # Supervisor pode ver se for supervisor do estagiário do prontuário
        if prontuario.estagiario.supervisor_vinculado == request.user:
            has_permission = True
    elif prontuario.estagiario == request.user:
        has_permission = True
        
    if not has_permission:
         messages.error(request, "Você não tem permissão para visualizar este prontuário.")
         return redirect('estagiario:consulta_inscritos')
    
    paciente = prontuario.paciente_comunidade if prontuario.paciente_comunidade else prontuario.paciente_convenio
    tipo_origem = 'comunidade' if prontuario.paciente_comunidade else 'convenio'
    
    # Buscar dados complementares
    doencas_map = {
        'doencaresp': 'Doença Respiratória', 'cancer': 'Câncer', 'diabete': 'Diabetes',
        'disfusexual': 'Disfunção Sexual', 'doencadgt': 'Doença Digestiva', 'escleorosemlt': 'Esclerose Múltipla',
        'hcpt': 'Hipertensão/Hepatite', 'luposatm': 'Lúpus', 'obesidade': 'Obesidade',
        'pblmarenal': 'Problema Renal', 'outro': 'Outro'
    }
    medicamentos_map = {
        'ansiolitico': 'Ansiolítico', 'antidepressivo': 'Antidepressivo', 'antipsicotico': 'Antipsicótico',
        'estabhumor': 'Estabilizador de Humor', 'memoriatct': 'Memória/TCT', 'outro': 'Outro'
    }
    disponibilidade_map = {
        'manha': 'Manhã', 'tarde': 'Tarde', 'noite': 'Noite', 'sabado': 'Sábado'
    }
    motivo_map = {
        'ansiedade': 'Ansiedade', 'assediomoral': 'Assédio Moral', 'depressao': 'Depressão',
        'dfaprendizagem': 'Dificuldade de Aprendizagem', 'humorinstavel': 'Humor Instável',
        'insonia': 'Insônia', 'isolasocial': 'Isolamento Social', 'luto': 'Luto',
        'tristeza': 'Tristeza', 'apatia': 'Apatia', 'chorofc': 'Choro Fácil',
        'exaustao': 'Exaustão', 'fadiga': 'Fadiga', 'faltanimo': 'Falta de Ânimo',
        'vldt': 'Violência Doméstica', 'assediosexual': 'Assédio Sexual', 'outro': 'Outro'
    }

    if tipo_origem == 'comunidade':
        doencas = Doencafisica.objects.filter(idfichacomunidade=paciente).first()
        medicamentos = Medicamento.objects.filter(idfichacomunidade=paciente).first()
        disponibilidade = Disponibilidade.objects.filter(idfichacomunidade=paciente).first()
        endereco = Endereco.objects.filter(idfichacomunidade=paciente).first()
        motivo = Motivoacompanhamento.objects.filter(idfichacomunidade=paciente).first()
    else:
        doencas = Doencafisica.objects.filter(idfichaconvenio=paciente).first()
        medicamentos = Medicamento.objects.filter(idfichaconvenio=paciente).first()
        disponibilidade = Disponibilidade.objects.filter(idfichaconvenio=paciente).first()
        endereco = Endereco.objects.filter(idfichaconvenio=paciente).first()
        motivo = Motivoacompanhamento.objects.filter(idfichaconvenio=paciente).first()

    evolucoes = prontuario.evolucoes.all().order_by('-data_atendimento', '-dth_registro')

    context = {
        'paciente': paciente,
        'tipo_origem': tipo_origem,
        'prontuario': prontuario,
        'evolucoes': evolucoes,
        'endereco': endereco,
        'doencas_labels': get_boolean_labels(doencas, doencas_map),
        'medicamentos_labels': get_boolean_labels(medicamentos, medicamentos_map),
        'disponibilidade_labels': get_boolean_labels(disponibilidade, disponibilidade_map),
        'motivo_labels': get_boolean_labels(motivo, motivo_map),
    }
    return render(request, 'dados_inscrito.html', context)

@login_required
def dados_inscrito_detalhe(request, tipo, pk):
    """
    Visualiza os dados detalhados de um inscrito disponível (sem vínculo).
    """
    if tipo == 'comunidade':
        paciente = get_object_or_404(Inscritocomunidade, pk=pk)
        doencas = Doencafisica.objects.filter(idfichacomunidade=paciente).first()
        medicamentos = Medicamento.objects.filter(idfichacomunidade=paciente).first()
        disponibilidade = Disponibilidade.objects.filter(idfichacomunidade=paciente).first()
        endereco = Endereco.objects.filter(idfichacomunidade=paciente).first()
        motivo = Motivoacompanhamento.objects.filter(idfichacomunidade=paciente).first()
    elif tipo == 'convenio':
        paciente = get_object_or_404(Inscritoconvenio, pk=pk)
        doencas = Doencafisica.objects.filter(idfichaconvenio=paciente).first()
        medicamentos = Medicamento.objects.filter(idfichaconvenio=paciente).first()
        disponibilidade = Disponibilidade.objects.filter(idfichaconvenio=paciente).first()
        endereco = Endereco.objects.filter(idfichaconvenio=paciente).first()
        motivo = Motivoacompanhamento.objects.filter(idfichaconvenio=paciente).first()
    else:
        messages.error(request, "Tipo de inscrito inválido.")
        return redirect('estagiario:consulta_inscritos')
    
    # Mapas de labels
    doencas_map = {
        'doencaresp': 'Doença Respiratória', 'cancer': 'Câncer', 'diabete': 'Diabetes',
        'disfusexual': 'Disfunção Sexual', 'doencadgt': 'Doença Digestiva', 'escleorosemlt': 'Esclerose Múltipla',
        'hcpt': 'Hipertensão/Hepatite', 'luposatm': 'Lúpus', 'obesidade': 'Obesidade',
        'pblmarenal': 'Problema Renal', 'outro': 'Outro'
    }
    medicamentos_map = {
        'ansiolitico': 'Ansiolítico', 'antidepressivo': 'Antidepressivo', 'antipsicotico': 'Antipsicótico',
        'estabhumor': 'Estabilizador de Humor', 'memoriatct': 'Memória/TCT', 'outro': 'Outro'
    }
    disponibilidade_map = {
        'manha': 'Manhã', 'tarde': 'Tarde', 'noite': 'Noite', 'sabado': 'Sábado'
    }
    motivo_map = {
        'ansiedade': 'Ansiedade', 'assediomoral': 'Assédio Moral', 'depressao': 'Depressão',
        'dfaprendizagem': 'Dificuldade de Aprendizagem', 'humorinstavel': 'Humor Instável',
        'insonia': 'Insônia', 'isolasocial': 'Isolamento Social', 'luto': 'Luto',
        'tristeza': 'Tristeza', 'apatia': 'Apatia', 'chorofc': 'Choro Fácil',
        'exaustao': 'Exaustão', 'fadiga': 'Fadiga', 'faltanimo': 'Falta de Ânimo',
        'vldt': 'Violência Doméstica', 'assediosexual': 'Assédio Sexual', 'outro': 'Outro'
    }
        
    context = {
        'paciente': paciente,
        'tipo_origem': tipo,
        'prontuario': None,
        'endereco': endereco,
        'doencas_labels': get_boolean_labels(doencas, doencas_map),
        'medicamentos_labels': get_boolean_labels(medicamentos, medicamentos_map),
        'disponibilidade_labels': get_boolean_labels(disponibilidade, disponibilidade_map),
        'motivo_labels': get_boolean_labels(motivo, motivo_map),
    }
    return render(request, 'dados_inscrito.html', context)

@login_required
def nova_evolucao(request, pk):
    prontuario = get_object_or_404(Prontuario, idprontuario=pk)
    
    # 🔐 Permissão
    if prontuario.estagiario != request.user:
        messages.error(request, "Você não tem permissão para registrar evolução neste prontuário.")
        return redirect('estagiario:consulta_inscritos')

    # 🚨 BLOQUEIO DE ARQUIVADO
    if not prontuario.status_ativo:
        messages.error(request, "Este prontuário está arquivado e não pode receber evoluções.")
        return redirect('estagiario:consulta_inscritos')

    if request.method == 'POST':
        form = RelatoSessaoForm(request.POST)
        if form.is_valid():
            evolucao = form.save(commit=False)
            evolucao.prontuario = prontuario
            evolucao.data_atendimento = date.today()

            try:
                evolucao.save()
                messages.success(request, "Evolução registrada com sucesso!")
                return redirect('estagiario:dados_inscrito', pk=prontuario.pk)
            except Exception as e:
                messages.error(request, f"Erro ao salvar evolução: {str(e)}")
        else:
            messages.error(request, "Erro no formulário. Verifique os dados.")
    else:
        form = RelatoSessaoForm()

    paciente_nome = (
        prontuario.paciente_comunidade.nomeinscrito 
        if prontuario.paciente_comunidade 
        else prontuario.paciente_convenio.nomeinscrito
    )

    context = {
        'prontuario': prontuario,
        'paciente_nome': paciente_nome,
        'form': form,
        'data_hoje': date.today()
    }
    return render(request, 'DetalhesSessão.html', context)