from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone 
import datetime
import re
from validate_docbr import CPF
from .models import (
    Disponibilidade, Doencafisica, Endereco, Inscritocomunidade, 
    Inscritoconvenio, Medicamento, Motivoacompanhamento, Pcdsnd, Tipoterapia
)

# --- A "PONTE" PARA O JAVASCRIPT ---
class CommaSeparatedMultipleChoiceField(forms.MultipleChoiceField):
    def to_python(self, value):
        if not value:
            return []
        if isinstance(value, list):
            return value
        return [v for v in value.split(',') if v]

    def validate(self, value):
        super().validate(value)


ESTADO_CIVIL_CHOICES = [
    ('Solteiro', 'Solteiro'),
    ('Casado', 'Casado'),
    ('Divorciado', 'Divorciado'),
    ('Viúvo', 'Viúvo'),
    ('União Estável', 'União Estável'),
    ('Nenhum', 'Nenhum'),
    ('Outros', 'Outros'),
]

GENERO_CHOICES = [
    ('Masculino', 'Masculino'),
    ('Feminino', 'Feminino'),
    ('Não Binário', 'Não Binário'),
    ('Transgênero', 'Transgênero'),
    ('Outros', 'Outros'),
    ('Prefiro não dizer', 'Prefiro não dizer'),
]

ETNIA_CHOICES = [
    ('Branca', 'Branca'),
    ('Preta', 'Preta'),
    ('Parda', 'Parda'),
    ('Amarela', 'Amarela'),
    ('Indígena', 'Indígena'),
    ('Outras', 'Outras'),
]

RELIGIAO_CHOICES = [
    ('Católico', 'Católico'),
    ('Evangélico', 'Evangélico'),
    ('Budismo', 'Budismo'),
    ('Espirita', 'Espirita'),
    ('Hinduísmo', 'Hinduísmo'),
    ('Islamismo', 'Islamismo'),
    ('Judaismo', 'Judaismo'),
    ('Religião de Matriz Africana', 'Religião de Matriz Africana'),
    ('Sem religião', 'Sem religião'),
    ('Outros', 'Outros'),
]
# Este é novo, para o convenio.html (usando os values de lá)
ENCAMINHAMENTO_CHOICES = [
    ('caps', 'CAPS - Centro de Atenção Psicossocial'),
    ('cras', 'CRAS - Centro de Referência de Assistência Social'),
    ('creas', 'CREAS - Centro de Referência Especializado de Assistência Social'),
    ('deam', 'DEAM - Delegacia da Mulher'),
    ('dpdf', 'DPDF - Defensoria Pública do Distrito Federal'),
    ('mpdft', 'MPDFT - Ministério Público do Distrito Federal'),
    ('ses', 'SES - Secretaria de Saúde'),
    ('sejus', 'SEJUS - Secretaria de Justiça'),
    ('ubs', 'UBS - Unidade Básica de Saúde'),
    ('clinica_ana_lucia', 'Clínica Ana Lucia Chaves Fecury (Unieuro Asa Sul)'),
    ('outros', 'Outros'),
]

# (CHOICES comuns que já usam minúsculas)
MOTIVOS_CHOICES = [
    ('ansiedade', 'Ansiedade'), ('assediomoral', 'Assédio Moral'), ('depressao', 'Depressão'),
    ('dfaprendizagem', 'Dificuldade de Aprendizagem'), ('humorinstavel', 'Humor Instável'),
    ('insonia', 'Insônia'), ('isolasocial', 'Isolamento Social'), ('luto', 'Luto'),
    ('tristeza', 'Tristeza'), ('apatia', 'Apatia'), ('chorofc', 'Choro Frequente'),
    ('exaustao', 'Exaustão'), ('fadiga', 'Fadiga'), ('faltanimo', 'Falta de Ânimo'),
    ('vldt', 'Vazio/Invalidez'), ('assediosexual', 'Assédio Sexual'), ('outro', 'Outro')
] 
DOENCAS_CHOICES = [
    ('doencaresp', 'Doença Respiratória'),('cancer', 'Câncer'),('diabete', 'Diabetes'),
    ('disfusexual', 'Disfunção Sexual'),('doencadgt', 'Doença Digestiva'),('escleorosemlt', 'Esclerose Múltipla'),
    ('hcpt', 'Hipertensão'),('luposatm', 'Lúpus'),('obesidade', 'Obesidade'),
    ('pblmarenal', 'Problema Renal'),('outro', 'Outro'),('nenhum', 'Nenhum')
]
PCD_CHOICES = [
    ('tea', 'Autismo (TEA)'), ('tdah', 'TDAH'), ('dffs', 'Disfunção Fonoaudiológica'),
    ('dfv', 'Deficiência Visual'), ('dfa', 'Deficiência Auditiva'), ('ttap', 'Transtorno de Aprendizagem'),
    ('ahst', 'Altas Habilidades/Superdotação'), ('outro', 'Outro'), ('nenhum', 'Nenhum')
] 
MEDICAMENTOS_CHOICES = [
    ('ansiolitico', 'Ansiolítico'), ('antidepressivo', 'Antidepressivo'),
    ('antipsicotico', 'Antipsicótico'), ('estabhumor', 'Estabilizador de Humor'),
    ('memoriatct', 'Memória/Concentração'), ('outro', 'Outro'), ('nenhum', 'Nenhum')
]
TERAPIA_CHOICES_HTML = [
    ('infantil', 'Infantil (até 14 anos)'),
    ('adolescente', 'Adolescente (15 a 18 anos)'),
    ('adulto', 'Adulto (18 até 60 anos)'),
    ('idoso', 'Idoso (60+ anos)'),
    ('grupo', 'Em grupo'),
    ('casal', 'Casal'),
    ('familia', 'Família'),
]
DISPONIBILIDADE_CHOICES_HTML = [
    ('manha_semana', 'Manhã (Segunda a Sexta)'), ('tarde_semana', 'Tarde (Segunda a Sexta)'),
    ('noite_semana', 'Noite (Segunda a Sexta)'), ('sabado_manha', 'Sábado (Somente pela manhã, 8:30h às 12h)'),
]

# =======================================================================
# --- FORMULÁRIO BASE UNIVERSAL (Como você sugeriu) ---
# =======================================================================

class BaseInscritoForm(forms.ModelForm):
    
    # --- CAMPOS COMUNS (Agora herdados por todos) ---
    estadocivilinscrito = forms.ChoiceField(
        choices=ESTADO_CIVIL_CHOICES, required=True
    )
    identidadegenero = forms.ChoiceField(
        choices=GENERO_CHOICES, required=True
    )
    etnia = forms.ChoiceField(
        choices=ETNIA_CHOICES, required=True
    )
    religiao = forms.ChoiceField(
        choices=RELIGIAO_CHOICES, required=True
    )
    estadocivilresp = forms.ChoiceField(
        choices=ESTADO_CIVIL_CHOICES, required=False
    ) 
    motivos_acompanhamento = CommaSeparatedMultipleChoiceField(
        choices=MOTIVOS_CHOICES, required=False
    )
    doencas_fisicas = CommaSeparatedMultipleChoiceField(
        choices=DOENCAS_CHOICES, required=False
    )
    pcd_neurodivergente = CommaSeparatedMultipleChoiceField(
        choices=PCD_CHOICES, required=False
    )
    medicamentos_usados = CommaSeparatedMultipleChoiceField(
        choices=MEDICAMENTOS_CHOICES, required=False
    )
    tipo_terapias = forms.ChoiceField(
        choices=TERAPIA_CHOICES_HTML, required=True
    )
    disponibilidade_semana = forms.ChoiceField( 
        choices=DISPONIBILIDADE_CHOICES_HTML, required=True
    )
    cep = forms.CharField(max_length=9, label="CEP") # Alinhado com XXXXX-XXX
    cidade = forms.CharField(max_length=40, label="Cidade")
    bairro = forms.CharField(max_length=50, required=False, label="Bairro")
    rua = forms.CharField(max_length=100, label="Rua/Avenida")
    uf = forms.CharField(max_length=2, initial='DF', label="UF")

    # --- CAMPOS PARA CONTATOS DE EMERGÊNCIA (Múltiplos - Máx 3) ---
    nomecontatourgencia_1 = forms.CharField(
        max_length=50, required=True, label="Nome do 1º Contato de Emergência"
    )
    contatourgencia_1 = forms.CharField(
        max_length=15, required=True, label="Telefone do 1º Contato"
    )
    nomecontatourgencia_2 = forms.CharField(
        max_length=50, required=False, label="Nome do 2º Contato de Emergência"
    )
    contatourgencia_2 = forms.CharField(
        max_length=15, required=False, label="Telefone do 2º Contato"
    )
    nomecontatourgencia_3 = forms.CharField(
        max_length=50, required=False, label="Nome do 3º Contato de Emergência"
    )
    contatourgencia_3 = forms.CharField(
        max_length=15, required=False, label="Telefone do 3º Contato"
    )

    # --- MÉTODO SAVE (Comum) ---
    def save(self, commit=True):
        from .models import ContatoUrgencia
        
        inscrito = super().save(commit=False)
        
        # Limpar os contatos do modelo para evitar tentar salvar em campos que não existem mais
        inscrito.contatourgencia = ''
        inscrito.nomecontatourgencia = ''
        
        if commit:
            inscrito.save()
            fk_data = {self._fk_name: inscrito}

            def save_multiselect_fields(model, field_name, choices_list):
                obj = model(**fk_data)
                selected_values = self.cleaned_data.get(field_name, [])
                for key, _ in choices_list:
                    setattr(obj, key, key in selected_values)
                obj.save()

            save_multiselect_fields(Motivoacompanhamento, 'motivos_acompanhamento', MOTIVOS_CHOICES)
            save_multiselect_fields(Doencafisica, 'doencas_fisicas', DOENCAS_CHOICES)
            save_multiselect_fields(Pcdsnd, 'pcd_neurodivergente', PCD_CHOICES)
            save_multiselect_fields(Medicamento, 'medicamentos_usados', MEDICAMENTOS_CHOICES)
            
            disp_map = {
                'manha_semana': 'manha', 'tarde_semana': 'tarde',
                'noite_semana': 'noite', 'sabado_manha': 'sabado'
            }
            disponibilidade_obj = Disponibilidade(**fk_data)
            selected_disp = self.cleaned_data.get('disponibilidade_semana') 
            field_to_set = disp_map.get(selected_disp)
            if field_to_set:
                setattr(disponibilidade_obj, field_to_set, True)
            disponibilidade_obj.save()

            terapia_map = {
                'infantil': 'individualift',
                'adolescente': 'individualadt',
                'adulto': 'individualadto',
                'idoso': 'individualids',
                'grupo': 'grupo',
                'casal': 'casal', 
                'familia': 'familia'
            }
            terapia_obj = Tipoterapia(**fk_data)
            selected_terapia = self.cleaned_data.get('tipo_terapias')
            field_to_set_terapia = terapia_map.get(selected_terapia)
            if field_to_set_terapia:
                setattr(terapia_obj, field_to_set_terapia, True)
            terapia_obj.save()

            Endereco.objects.create(
                cidade=self.cleaned_data.get('cidade'),
                bairro=self.cleaned_data.get('bairro'),
                rua=self.cleaned_data.get('rua'),
                uf=self.cleaned_data.get('uf'),
                cep=self.cleaned_data.get('cep'),
                **fk_data
            )
            
            # --- CRIAR CONTATOS DE EMERGÊNCIA (Máx 3) ---
            for sequencia in range(1, 4):
                nome_key = f'nomecontatourgencia_{sequencia}'
                tel_key = f'contatourgencia_{sequencia}'
                
                nome = self.cleaned_data.get(nome_key)
                telefone = self.cleaned_data.get(tel_key)
                
                # Só criar se ambos nome e telefone forem preenchidos
                if nome and telefone:
                    ContatoUrgencia.objects.create(
                        **fk_data,
                        nomecontato=nome,
                        telefonecontato=telefone,
                        sequencia=sequencia
                    )
            
        return inscrito
        
    class Meta:
        abstract = True
        exclude = ['dthinscricao', 'status']

    # --- MÉTODOS DE VALIDAÇÃO (Comuns) ---
    def clean_dtnascimento(self):
        data_nascimento = self.cleaned_data.get('dtnascimento')
        if data_nascimento:
            today = timezone.now().date()
            if data_nascimento > today:
                raise ValidationError('A data de nascimento não pode ser no futuro.')
            if data_nascimento.year < 1899:
                raise ValidationError('O ano não pode ser anterior a 1899.')
        return data_nascimento

    def clean_cpfinscrito(self):
        cpf_str = self.cleaned_data.get('cpfinscrito')
        if cpf_str:
            cpf_validator = CPF()
            if not cpf_validator.validate(cpf_str):
                raise ValidationError('CPF inválido. Verifique os dígitos.')
        # Salva com máscara (requer max_length=14 no model)
        return cpf_str 

    def clean_cpfresp(self):
        cpf_str = self.cleaned_data.get('cpfresp')
        if cpf_str:
            cpf_validator = CPF()
            if not cpf_validator.validate(cpf_str):
                raise ValidationError('CPF do responsável inválido. Verifique os dígitos.')
        # Salva com máscara (requer max_length=14 no model)
        return cpf_str 

    def clean_cep(self):
        cep = self.cleaned_data.get('cep')
        if cep:
            if not re.fullmatch(r'\d{5}-\d{3}', cep):
                raise ValidationError('Formato de CEP inválido. O formato esperado é XXXXX-XXX')
        return cep

    def clean(self):
        cleaned_data = super().clean()
        cpfinscrito = cleaned_data.get('cpfinscrito')
        cpfresp = cleaned_data.get('cpfresp')
        data_nascimento = cleaned_data.get('dtnascimento')

        hoje = timezone.now().date()
        maior_de_idade = False
        if data_nascimento:
            maior_de_idade = (hoje.year - data_nascimento.year) - (
                (hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day)
            ) >= 18

        # Regra: para maior de idade, CPF do responsável não pode ser igual ao CPF do inscrito.
        if maior_de_idade and cpfinscrito and cpfresp and cpfinscrito == cpfresp:
            msg = 'O CPF do responsável não pode ser igual ao CPF do inscrito para maior de idade.'
            self.add_error('cpfinscrito', msg)
            self.add_error('cpfresp', msg)
        
        # --- VALIDAÇÃO DE CONTATOS DE EMERGÊNCIA (Máx 3) ---
        contatos_preenchidos = 0
        for sequencia in range(1, 4):
            nome_key = f'nomecontatourgencia_{sequencia}'
            tel_key = f'contatourgencia_{sequencia}'
            
            nome = cleaned_data.get(nome_key)
            telefone = cleaned_data.get(tel_key)
            
            # Se um dos dois for preenchido, ambos são obrigatórios
            if (nome and not telefone) or (telefone and not nome):
                if not nome:
                    self.add_error(
                        nome_key,
                        f'Preencha o nome do contato {sequencia}.'
                    )
                if not telefone:
                    self.add_error(
                        tel_key,
                        f'Preencha o telefone do contato {sequencia}.'
                    )
            
            # Contar quantos contatos foram preenchidos
            if nome and telefone:
                contatos_preenchidos += 1
        
        # Validar se pelo menos 1 contato foi preenchido
        if contatos_preenchidos == 0:
            self.add_error('nomecontatourgencia_1', 'Preencha pelo menos 1 contato de emergência.')
            self.add_error('contatourgencia_1', 'Preencha pelo menos 1 contato de emergência.')
        
        return cleaned_data


class InscritoComunidadeForm(BaseInscritoForm):
    _fk_name = 'idfichacomunidade'

    class Meta(BaseInscritoForm.Meta):
        model = Inscritocomunidade
        # Lista APENAS os campos do model que NÃO estão na BaseInscritoForm
        fields = [
            'nomeinscrito', 'dtnascimento', 'nomeresp', 'grauresp', 'cpfresp',
            'tellcellresp', 'emailresp', 'cpfinscrito', 'tellcellinscrito', 
            'emailinscrito', 'confirmlgpd',
            'estadocivilinscrito', 'identidadegenero', 'etnia', 'religiao', 'estadocivilresp'
        ]

class InscritoConvenioForm(BaseInscritoForm):
    _fk_name = 'idfichaconvenio'

    # Campo ADICIONAL que só existe no Convênio
    tipoencaminhamento = forms.ChoiceField(
        choices=ENCAMINHAMENTO_CHOICES, required=True
    )

    class Meta(BaseInscritoForm.Meta):
        model = Inscritoconvenio

        fields = [
            'nomeinscrito', 'dtnascimento', 
            'nomeresp', 'grauresp', 'cpfresp', 'tellcellresp',
            'emailresp', 'cpfinscrito', 'tellcellinscrito',
            'emailinscrito', 'confirmlgpd',
            # Campos herdados/adicionais que precisam constar no Meta para serem salvos
            'estadocivilinscrito', 'identidadegenero', 'etnia', 'religiao', 'estadocivilresp',
            'tipoencaminhamento'
        ]
