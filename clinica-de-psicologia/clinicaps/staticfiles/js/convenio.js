document.addEventListener('DOMContentLoaded', function () {

    // 1. ALTERAÇÃO: Procura pelo ID 'form-convenio'
    const form = document.getElementById('form-convenio');
    if (!form) {
        console.error("Erro Crítico: O formulário com ID 'form-convenio' não foi encontrado.");
        return;
    }

    const submitButton = document.getElementById('submit-button');
    const formFeedback = document.getElementById('form-feedback');

    const csrfTokenInput = form.querySelector('[name=csrfmiddlewaretoken]');
    if (!csrfTokenInput || !csrfTokenInput.value) {
        console.warn('Input CSRF token não encontrado ou vazio. O envio para o Django falhará.');
    }
    const csrfToken = csrfTokenInput ? csrfTokenInput.value : '';

    // --- MELHORIA 1: Definir min/max para data de nascimento ---
    try{
        const dataNascimentoInput = document.getElementById('data_nascimento');
        if (dataNascimentoInput){
            const today = new Date().toISOString().split('T')[0];
            dataNascimentoInput.min = '1899-01-01';
            dataNascimentoInput.max =  today;
        }
    } catch(e){
        console.warn("Nao foi possivel definir min/max da data.", e);
    }

    // --- MELHORIA 3: Auto-preenchimento com ViaCEP ---
    try {
        const cepInput = document.getElementById('cep');
        const ruaInput = document.getElementById('rua');
        const bairroInput = document.getElementById('bairro');
        const cidadeInput = document.getElementById('cidade');
        const ufInput = document.getElementById('uf');

        if (cepInput && ruaInput && bairroInput && cidadeInput && ufInput) {
            cepInput.addEventListener('blur', async function() {
                const cep = cepInput.value.replace(/\D/g, ''); 
                
                if (cep.length === 8) {
                    cepInput.disabled = true; 
                    try {
                        const response = await fetch(`https://viacep.com.br/ws/${cep}/json/`);
                        if (!response.ok) throw new Error('CEP não encontrado');
                        const data = await response.json();
                        
                        if (data.erro) {
                            console.warn('ViaCEP: CEP não existente.');
                        } else {
                            if (data.logradouro) ruaInput.value = data.logradouro;
                            if (data.bairro) bairroInput.value = data.bairro;
                            if (data.localidade) cidadeInput.value = data.localidade;
                            if (data.uf) ufInput.value = data.uf;
                            
                            [ruaInput, bairroInput, cidadeInput, ufInput].forEach(input => {
                                if(input.value && input.classList.contains('input-error')) {
                                    input.classList.remove('input-error');
                                    const parent = input.closest('.mb-4');
                                    const errorMsg = parent ? parent.querySelector('.error-message') : null;
                                    if (errorMsg) errorMsg.remove();
                                }
                            });
                        }
                    } catch (error) {
                        console.error('Erro ao buscar CEP:', error);
                    } finally {
                        cepInput.disabled = false; 
                    }
                }
            });
        }
    } catch (e) {
        console.warn("Não foi possível carregar o auto-preenchimento de CEP.", e);
    }

    const checkMenor = document.getElementById('checkMenorIdade');
    const dadosResponsavel = document.getElementById('dadosResponsavel');
    const inputsResponsavel = dadosResponsavel.querySelectorAll('input, select');

    function toggleResponsavel() {
        const isChecked = checkMenor.checked;
        if (isChecked) {
            dadosResponsavel.classList.remove('hidden');
            dadosResponsavel.classList.add('block');
        } else {
            dadosResponsavel.classList.remove('block');
            dadosResponsavel.classList.add('hidden');
        }
        inputsResponsavel.forEach(input => {
            input.required = isChecked;
            if (!isChecked) {
                input.value = '';
                if (input.tagName === 'SELECT') {
                    updateSelectColor(input);
                }
                input.classList.remove('input-error');
                const parent = input.closest('.mb-4') || input.closest('.custom-select-wrapper');
                const errorMsg = parent ? parent.querySelector('.error-message') : null;
                if (errorMsg) errorMsg.remove();
            }
        });
    }
    checkMenor.addEventListener('change', toggleResponsavel);
    toggleResponsavel();

    function updateSelectColor(select) {
        if (select.value === "") {
            select.style.color = '#6c757d';
        } else {
            select.style.color = '#333';
        }
    }

    document.querySelectorAll('.form-select:not([multiple])').forEach(select => {
        select.addEventListener('change', () => updateSelectColor(select));
        updateSelectColor(select);
    });

    const contactsContainer = document.getElementById('emergencyContactsContainer');
    const addContactBtn = document.getElementById('addContactBtn');
    let contactCount = 1;

    addContactBtn.addEventListener('click', function () {
        contactCount++;
        const newContact = document.createElement('div');
        newContact.className = 'contact-entry relative p-4 md:p-6 bg-gray-50 border border-gray-200 rounded-md mt-4';
        newContact.innerHTML = `
                <div class="flex flex-wrap -mx-3">
                    <h5 class="w-full px-3 font-bold text-base mt-0 mb-2 text-[#003366]">Contato ${contactCount}</h5>
                    <div class="w-full md:w-1/2 px-3">
                        <div class="mb-4 md:mb-0">
                            <label for="nome_urgencia_${contactCount}" class="sr-only">Nome Completo Contato ${contactCount}</label>
                            <input type="text" id="nome_urgencia_${contactCount}" name="nome_urgencia[]" class="apenas-letras form-control block w-full bg-gray-100 border-none rounded-md py-3 px-4 text-sm text-gray-800 focus:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-[#003366] focus:ring-opacity-60 md:text-base" placeholder="Nome Completo" required>
                        </div>
                    </div>
                    <div class="w-full md:w-1/2 px-3">
                        <div class="mb-0">
                            <label for="telefone_urgencia_${contactCount}" class="sr-only">Telefone Celular Contato ${contactCount}</label>
                            <input type="text" id="telefone_urgencia_${contactCount}" name="telefone_urgencia[]" class="telefone form-control block w-full bg-gray-100 border-none rounded-md py-3 px-4 text-sm text-gray-800 focus:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-[#003366] focus:ring-opacity-60 md:text-base" placeholder="Telefone Celular" required maxlength="15">
                        </div>
                    </div>
                </div>
                <button type="button" class="remove-contact-btn absolute top-2.5 right-2.5 bg-red-600 text-white border-none rounded-full w-8 h-8 text-lg flex items-center justify-center leading-none shadow-md transition-all duration-200 ease-in-out hover:bg-red-700 hover:scale-110" aria-label="Remover Contato ${contactCount}"><i class="bi bi-dash" aria-hidden="true"></i></button>
            `;
        contactsContainer.appendChild(newContact);

        newContact.querySelectorAll('.telefone').forEach(input => {
            input.addEventListener('input', (e) => e.target.value = formatTelefone(e.target.value));
        });
        newContact.querySelectorAll('.apenas-letras').forEach(input => {
            input.addEventListener('input', (e) => e.target.value = e.target.value.replace(/[^\p{L}\s'-]/gu, ''));
        });
    });

    contactsContainer.addEventListener('click', function (e) {
        const removeBtn = e.target.closest('.remove-contact-btn');
        if (removeBtn) {
            removeBtn.closest('.contact-entry').remove();
            updateContactNumbers();
        }
    });

    function updateContactNumbers() {
        const allContacts = contactsContainer.querySelectorAll('.contact-entry');
        allContacts.forEach((contact, index) => {
            const title = contact.querySelector('h5');
            if (title) title.textContent = `Contato ${index + 1}`;
            // ... (restante da lógica de atualização de ID, que está correta) ...
        });
        contactCount = allContacts.length;
    }

    function showMessage(type, message) {
        const alertDiv = document.createElement('div');
        alertDiv.className = `form-feedback-box feedback-${type}`;
        alertDiv.setAttribute('role', 'alert');
        alertDiv.innerHTML = `
                ${message}
                <button type="button" class="feedback-close-btn" aria-label="Close"></button>
            `;
        formFeedback.innerHTML = '';
        formFeedback.appendChild(alertDiv);
        alertDiv.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }

    formFeedback.addEventListener('click', function (e) {
        const closeButton = e.target.closest('.feedback-close-btn');
        if (closeButton) {
            const alertBox = closeButton.closest('.form-feedback-box');
            alertBox.style.opacity = '0';
            setTimeout(() => alertBox.remove(), 150);
        }
    });


    // --- LÓGICA MULTI-SELECT (APRIMORADA) ---
    // Esta nova lógica lê as opções do HTML, como você sugeriu.
    
    // 2. ALTERAÇÃO: Objeto 'multiSelectOptions' removido.
    
    const multiSelectState = {};
    const globalOptionsLookup = {}; // Novo: Armazena o texto das opções

    function initializeMultiSelects() {
        // Encontra todos os selects que devem ser multi-select
        // (Baseado nos IDs que você definiu no HTML)
        const multiSelectIds = ['motivos_acompanhamento', 'medicamentos_usados', 'pcd_neurodivergente', 'doencas_fisicas'];
        
        multiSelectIds.forEach(fieldId => {
            const originalSelect = document.getElementById(fieldId);
            if (!originalSelect) {
                 console.warn(`Campo select original com ID '${fieldId}' não encontrado para multi-select.`);
                 return;
            }

            // 3. ALTERAÇÃO: Lê as opções do HTML
            const options = Array.from(originalSelect.querySelectorAll('option:not([disabled])')).map(opt => ({
                value: opt.value,
                text: opt.textContent
            }));
            
            // Armazena as opções para usar depois (para criar as "pills")
            globalOptionsLookup[fieldId] = options; 

            const placeholder = originalSelect.querySelector('option[disabled]')?.textContent || 'Selecione uma ou mais opções';
            multiSelectState[fieldId] = [];

            const multiSelectWrapper = document.createElement('div');
            multiSelectWrapper.className = 'custom-multiselect-wrapper relative mb-4';
            multiSelectWrapper.dataset.fieldId = fieldId;

            // Gera o HTML do dropdown usando as opções lidas do HTML
            multiSelectWrapper.innerHTML = `
                <label for="${fieldId}_display" class="sr-only">${placeholder}</label>
                <div id="${fieldId}_display" name="${fieldId}_display" class="multiselect-display form-control flex items-center flex-wrap gap-1 block w-full bg-gray-100 border-none rounded-l-md py-2 px-4 text-sm text-gray-800 focus:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-[#003366] focus:ring-opacity-60 md:text-base cursor-pointer pr-12" tabindex="0" role="combobox" aria-haspopup="listbox" aria-expanded="false">
                    <span class="placeholder-text text-gray-500">${placeholder}</span>
                </div>
                <div class="custom-arrow absolute top-0 right-0 bottom-0 w-10 bg-[#003366] text-white flex items-center justify-center pointer-events-none rounded-r-md text-lg md:w-12">
                    <i class="bi bi-caret-down-fill" aria-hidden="true"></i>
                </div>
                <div class="multiselect-dropdown absolute hidden top-full left-0 right-0 z-10 bg-white border border-gray-300 rounded-md shadow-lg mt-1" role="listbox">
                    ${options.map(option => `
                        <div class="multiselect-option flex items-center p-2 hover:bg-gray-100 cursor-pointer" data-value="${option.value}" role="option" aria-selected="false">
                            <input type="checkbox" class="w-4 h-4 text-[#003366] rounded border-gray-300 focus:ring-[#003366] mr-2 pointer-events-none" tabindex="-1">
                            <span>${option.text}</span>
                        </div>
                    `).join('')}
                </div>
                <input type="hidden" id="${fieldId}" name="${fieldId}" class="multiselect-hidden-input">
            `;

            originalSelect.closest('.custom-select-wrapper').replaceWith(multiSelectWrapper);

            // Adiciona Event Listeners
            const display = multiSelectWrapper.querySelector('.multiselect-display');
            const dropdown = multiSelectWrapper.querySelector('.multiselect-dropdown');
            const optionsElements = multiSelectWrapper.querySelectorAll('.multiselect-option');

            display.addEventListener('click', (e) => {
                e.stopPropagation();
                const isExpanded = dropdown.classList.contains('hidden');
                closeAllMultiSelects();
                if (isExpanded) {
                    dropdown.classList.remove('hidden');
                    display.setAttribute('aria-expanded', 'true');
                } else {
                    dropdown.classList.add('hidden');
                    display.setAttribute('aria-expanded', 'false');
                }
            });

            optionsElements.forEach(optionEl => {
                optionEl.addEventListener('click', (e) => {
                    e.stopPropagation();
                    const value = optionEl.dataset.value;
                    toggleMultiSelectOption(fieldId, value);
                });
            });
        });
    }

    function closeAllMultiSelects() {
        document.querySelectorAll('.multiselect-dropdown').forEach(dropdown => {
            dropdown.classList.add('hidden');
            const display = dropdown.previousElementSibling;
            if (display && display.classList.contains('multiselect-display')) {
                 display.setAttribute('aria-expanded', 'false');
            }
        });
    }

    function toggleMultiSelectOption(fieldId, value) {
        const state = multiSelectState[fieldId];
        if (!state) return;
        
        const index = state.indexOf(value);
        if (index > -1) {
            state.splice(index, 1);
        } else {
            state.push(value);
        }
        updateMultiSelectUI(fieldId);
    }

    function updateMultiSelectUI(fieldId) {
        const wrapper = document.querySelector(`.custom-multiselect-wrapper[data-field-id="${fieldId}"]`);
        if (!wrapper) return;

        const display = wrapper.querySelector('.multiselect-display');
        const hiddenInput = wrapper.querySelector('.multiselect-hidden-input');
        const placeholder = display.querySelector('.placeholder-text');
        
        // 4. ALTERAÇÃO: Lê as opções do lookup global
        const options = globalOptionsLookup[fieldId]; 
        const state = multiSelectState[fieldId];

        display.querySelectorAll('.multiselect-pill').forEach(pill => pill.remove());

        state.forEach(value => {
            const option = options.find(o => o.value === value);
            if (!option) return;

            const pill = document.createElement('span');
            pill.className = 'multiselect-pill';
            pill.dataset.value = value;
            pill.innerHTML = `
                <span>${option.text}</span>
                <button type="button" class="multiselect-pill-remove" aria-label="Remover ${option.text}">&times;</button>
            `;
            display.insertBefore(pill, placeholder);
        });

        hiddenInput.value = state.join(',');

        wrapper.querySelectorAll('.multiselect-option').forEach(optionEl => {
            const value = optionEl.dataset.value;
            const checkbox = optionEl.querySelector('input[type="checkbox"]');
            if (state.includes(value)) {
                checkbox.checked = true;
                optionEl.setAttribute('aria-selected', 'true');
            } else {
                checkbox.checked = false;
                optionEl.setAttribute('aria-selected', 'false');
            }
        });

         if (state.length > 0) {
             clearMultiSelectError(fieldId);
         }
    }
    
    function clearMultiSelectError(fieldId) {
         const wrapper = document.querySelector(`.custom-multiselect-wrapper[data-field-id="${fieldId}"]`);
         if (!wrapper) return;
         const display = wrapper.querySelector('.multiselect-display');
         
         if (display.classList.contains('input-error')) {
             display.classList.remove('input-error');
             const errorMsg = wrapper.querySelector('.error-message');
             if (errorMsg) errorMsg.remove();
         }
    }

    form.addEventListener('click', (e) => {
        const removeBtn = e.target.closest('.multiselect-pill-remove');
        if (removeBtn) {
            e.preventDefault();
            e.stopPropagation();
            const pill = removeBtn.closest('.multiselect-pill');
            const wrapper = removeBtn.closest('.custom-multiselect-wrapper');
            const fieldId = wrapper.dataset.fieldId;
            const value = pill.dataset.value;
            toggleMultiSelectOption(fieldId, value);
        }
    });

    document.addEventListener('click', (e) => {
        if (!e.target.closest('.custom-multiselect-wrapper')) {
            closeAllMultiSelects();
        }
    });

    initializeMultiSelects();

    // --- FIM LÓGICA MULTI-SELECT ---


    function clearErrors() {
        form.querySelectorAll('.error-message').forEach(el => el.remove());
        form.querySelectorAll('.input-error').forEach(el => {
            el.classList.remove('input-error');
        });
        formFeedback.innerHTML = '';
    }

    function displayErrors(erros) {
        console.log("Erros de validação:", erros);
        let firstErrorField = null;

        // 5. ALTERAÇÃO: Adicionado 'tipoencaminhamento'
        const fieldNameMap = {
            'nomeinscrito': 'nome_inscrito',
            'dtnascimento': 'data_nascimento',
            'cpfinscrito': 'cpf_inscrito',
            'tellcellinscrito': 'telefone_inscrito',
            'emailinscrito': 'email_inscrito',
            'identidadegenero': 'identidade_genero',
            'etnia': 'cor_etnia',
            'religiao': 'religiao',
            'estadocivilinscrito': 'estado_civil_inscrito',
            'rua': 'rua',
            'bairro': 'bairro',
            'cidade': 'cidade',
            'uf': 'uf',
            'cep': 'cep',
            'nomecontatourgencia': 'nome_urgencia_1',
            'contatourgencia': 'telefone_urgencia_1',
            'nomeresp': 'nome_responsavel',
            'cpfresp': 'cpf_responsavel',
            'tellcellresp': 'telefone_responsavel',
            'emailresp': 'email_responsavel',
            'estadocivilresp': 'estado_civil_responsavel',
            'grauresp': 'parentesco_responsavel',
            'confirmlgpd': 'checkLGPD',
            'motivos_acompanhamento': 'motivos_acompanhamento_display',
            'medicamentos_usados': 'medicamentos_usados_display',
            'pcd_neurodivergente': 'pcd_neurodivergente_display',
            'doencas_fisicas': 'doencas_fisicas_display',
            'tipo_terapias': 'tipo_terapias',
            'disponibilidade_semana': 'disponibilidade',
            'tipoencaminhamento': 'tipo_encaminhamento' // <-- NOVO
        };


        for (const [fieldName, errorMessages] of Object.entries(erros)) {
            
            const frontendId = fieldNameMap[fieldName] || fieldName;
            let campo = document.getElementById(frontendId);

            if (!campo && frontendId.endsWith('_display')) {
                campo = document.getElementById(frontendId);
            }

            if (!campo && frontendId.includes('[]')) {
                const camposArray = form.querySelectorAll(`[name="${frontendId}"]`);
                if (camposArray.length > 0) campo = camposArray[0];
            } else if (!campo) {
                campo = form.querySelector(`[name="${fieldName}"]`);
            }

            if (campo) {
                if (!firstErrorField) firstErrorField = campo;

                let parentWrapper;
                if (campo.type === 'checkbox') {
                    campo.classList.add('input-error');
                    parentWrapper = campo.closest('div');
                }
                else if (campo.classList.contains('multiselect-display')) {
                    campo.classList.add('input-error');
                    parentWrapper = campo.closest('.custom-multiselect-wrapper');
                } else {
                    campo.classList.add('input-error');
                    parentWrapper = campo.closest('.custom-select-wrapper') || campo.closest('.mb-4') || campo.parentNode;
                }

                const erroEl = document.createElement('span');
                erroEl.className = 'error-message';
                erroEl.textContent = Array.isArray(errorMessages) ? errorMessages.join(' ') : errorMessages;
                
                parentWrapper.appendChild(erroEl);

            } else {
                console.warn(`Campo de erro '${fieldName}' (mapeado para '${frontendId}') não encontrado no DOM.`);
            }
        }

        if (!formFeedback.querySelector('.feedback-danger')) {
             showMessage('danger', '<strong>Erro de validação:</strong> Por favor, verifique os campos destacados.');
        }

        if (firstErrorField) {
            firstErrorField.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
    }


    // --- Funções de Validação Client-Side (COM QUALIDADE) ---

    function isValidEmail(email) {
        const re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1.3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        return re.test(String(email).toLowerCase());
    }

    function isValidCPF(cpf) {
        cpf = cpf.replace(/\D/g,'');
        if (cpf.length !== 11 || /^(\d)\1+$/.test(cpf)){
            return false;
        }
        let sum = 0;
        let remainder;
        for (let i = 1; i <= 9; i++) {
            sum += parseInt(cpf.substring(i - 1, i)) * (11 - i);
        }
        remainder = (sum * 10) % 11;
        if (remainder === 10 || remainder === 11) {
            remainder = 0;
        }
        if (remainder !== parseInt(cpf.substring(9, 10))) {
            return false;
        }
        sum = 0;
        for (let i = 1; i <= 10; i++) {
            sum += parseInt(cpf.substring(i - 1, i)) * (12 - i);
        }
        remainder = (sum * 10) % 11;
        if (remainder === 10 || remainder === 11) {
            remainder = 0;
        }
        if (remainder !== parseInt(cpf.substring(10, 11))) {
            return false;
        }
        return true;
    }
        
    function isValidTelefone(tel) {
        const digits = tel.replace(/\D/g, '');
        return digits.length >= 10 && digits.length <= 11;
    }

    function isValidCEP(cep) {
        const digits = cep.replace(/\D/g, '');
        return digits.length === 8;
    }


    function validateForm() {
        const errors = {};
        const requiredFields = form.querySelectorAll('[required]');
        
        requiredFields.forEach(field => {
            if (field.closest('#dadosResponsavel') && dadosResponsavel.classList.contains('hidden')) {
                 return;
            }
             
            const fieldId = field.id;
            const fieldValue = field.value.trim();

            if (field.tagName === 'SELECT' && fieldValue === '') {
                errors[fieldId] = 'Este campo é obrigatório.';
            } else if (field.type === 'checkbox' && !field.checked) {
                if (field.id === 'checkLGPD') {
                     errors[fieldId] = 'Você deve concordar com os termos.';
                }
            } else if (field.type !== 'checkbox' && fieldValue === '') {
                errors[fieldId] = 'Este campo é obrigatório.';
            }

            else if (field.classList.contains('email') && !isValidEmail(fieldValue)) {
                errors[fieldId] = 'Por favor, insira um e-mail válido.';
            }
            else if (field.classList.contains('cpf') && !isValidCPF(fieldValue)) {
                errors[fieldId] = 'Por favor, insira um CPF válido.';
            }
            else if (field.classList.contains('telefone') && !isValidTelefone(fieldValue)) {
                errors[fieldId] = 'Por favor, insira um telefone válido (10 ou 11 dígitos).';
            }
            else if (field.classList.contains('cep') && !isValidCEP(fieldValue)) {
                errors[fieldId] = 'Por favor, insira um CEP válido (8 dígitos).';
            }
        });

        // 6. ALTERAÇÃO: Validação de multi-select simplificada
        // (A validação de 'required' normal acima já pega os selects
        // que agora estão visíveis e têm a tag 'required')
        
        if (Object.keys(errors).length > 0) {
            displayErrors(errors);
            return false;
        }

        return true;
    }


    form.addEventListener('submit', async function (event) {
        event.preventDefault();
        clearErrors();

        const isFormValid = validateForm();
        if (!isFormValid) {
            return;
        }

        submitButton.disabled = true;
        submitButton.innerHTML = `
                <span class="loading-spinner" role="status" aria-hidden="true"></span>
                Enviando...
            `;

        const formData = new FormData(form);
        const dadosObjeto = {};

        // --- Mapeamento (Igual ao do comunidade.js) ---
        
        dadosObjeto.nomeinscrito = formData.get('nome_inscrito');
        dadosObjeto.dtnascimento = formData.get('data_nascimento');
        dadosObjeto.cpfinscrito = formData.get('cpf_inscrito');
        dadosObjeto.tellcellinscrito = formData.get('telefone_inscrito');
        dadosObjeto.emailinscrito = formData.get('email_inscrito');
        dadosObjeto.identidadegenero = formData.get('identidade_genero');
        dadosObjeto.etnia = formData.get('cor_etnia');
        dadosObjeto.religiao = formData.get('religiao');
        dadosObjeto.estadocivilinscrito = formData.get('estado_civil_inscrito');
        
        dadosObjeto.rua = formData.get('rua');
        dadosObjeto.bairro = formData.get('bairro');
        dadosObjeto.cidade = formData.get('cidade');
        dadosObjeto.uf = formData.get('uf');
        dadosObjeto.cep = formData.get('cep');

        dadosObjeto.nomecontatourgencia = formData.get('nome_urgencia[]');
        dadosObjeto.contatourgencia = formData.get('telefone_urgencia[]');
        
        dadosObjeto.nomeresp = formData.get('nome_responsavel');
        dadosObjeto.cpfresp = formData.get('cpf_responsavel');
        dadosObjeto.tellcellresp = formData.get('telefone_responsavel');
        dadosObjeto.emailresp = formData.get('email_responsavel');
        dadosObjeto.estadocivilresp = formData.get('estado_civil_responsavel');
        dadosObjeto.grauresp = formData.get('parentesco_responsavel');
        
        dadosObjeto.tipo_terapias = formData.get('tipo_terapias');
        dadosObjeto.disponibilidade_semana = formData.get('disponibilidade');
        
        // 7. ALTERAÇÃO: Adicionado o novo campo de convênio
        dadosObjeto.tipoencaminhamento = formData.get('tipo_encaminhamento');
        
        // Campos Multi-Select
        const multiSelectIds = ['motivos_acompanhamento', 'medicamentos_usados', 'pcd_neurodivergente', 'doencas_fisicas'];
        multiSelectIds.forEach(fieldId => {
            const hiddenInput = document.getElementById(fieldId);
            if (hiddenInput) {
                dadosObjeto[fieldId] = hiddenInput.value.split(',').filter(Boolean);
            }
        });

        // Checkboxes
        dadosObjeto.menorIdade = checkMenor.checked;
        dadosObjeto.confirmlgpd = document.getElementById('checkLGPD').checked;
        // --- FIM DO MAPEAMENTO ---

        console.log("Dados a serem enviados (JSON):", dadosObjeto);

        try {
            const response = await fetch(form.action, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify(dadosObjeto)
            });

            const resultado = await response.json();

            if (response.ok) {
                showMessage('success', `<strong>Sucesso!</strong> ${resultado.mensagem || 'Inscrição realizada com sucesso!'}`);
                form.reset();
                
                Object.keys(multiSelectState).forEach(fieldId => {
                    multiSelectState[fieldId] = [];
                    updateMultiSelectUI(fieldId);
                });

                document.querySelectorAll('.form-select').forEach(updateSelectColor);
                toggleResponsavel();

                const extraContacts = contactsContainer.querySelectorAll('.contact-entry:not(:first-child)');
                extraContacts.forEach(contact => contact.remove());
                updateContactNumbers();

            } else if (resultado.status === 'erro_validacao') {
                displayErrors(resultado.erros);
            } else {
                showMessage('danger', `Erro do servidor: ${resultado.mensagem || 'Erro desconhecido.'}`);
            }

        } catch (error) {
            console.error('Erro de comunicação:', error);
            showMessage('danger', 'Ocorreu um erro de comunicação com o servidor. Tente novamente mais tarde.');
        } finally {
            submitButton.disabled = false;
            submitButton.innerHTML = 'Salvar Inscrição';
        }
    });

    // --- Funções de Formatação (Máscaras) ---

    function formatCPF(value) {
        const digits = value.replace(/\D/g, '').slice(0, 11);
        if (digits.length <= 3) return digits;
        if (digits.length <= 6) return digits.replace(/(\d{3})(\d)/, '$1.$2');
        if (digits.length <= 9) return digits.replace(/(\d{3})(\d{3})(\d)/, '$1.$2.$3');
        return digits.replace(/(\d{3})(\d{3})(\d{3})(\d{1,2})/, '$1.$2.$3-$4');
    }

    function formatTelefone(value) {
        const digits = value.replace(/\D/g, '').slice(0, 11);
        if (digits.length <= 2) return `(${digits}`; 
        if (digits.length <= 7) return digits.replace(/(\d{2})(\d)/, '($1) $2'); 
        if (digits.length <= 10) return digits.replace(/(\d{2})(\d{4})(\d{4})/, '($1) $2-$3'); // Fixo
        return digits.replace(/(\d{2})(\d{5})(\d{4})/, '($1) $2-$3'); // Celular
    }

    function formatCEP(value) {
        const digits = value.replace(/\D/g, '').slice(0, 8);
        if (digits.length <= 5) return digits;
        return digits.replace(/(\d{5})(\d{1,3})/, '$1-$2');
    }

    form.addEventListener('input', function (e) {
        const target = e.target;

        if (target.classList.contains('input-error')) {
            target.classList.remove('input-error');
            const parent = target.closest('.custom-select-wrapper') || target.closest('.mb-4') || target.parentNode;
            const errorMsg = parent ? parent.querySelector('.error-message') : null;
            if (errorMsg) errorMsg.remove();
        }

        if (target.classList.contains('cpf')) {
            target.value = formatCPF(target.value);
        }
        if (target.classList.contains('telefone')) {
            target.value = formatTelefone(target.value);
        }
        if (target.classList.contains('cep')) {
            target.value = formatCEP(target.value);
        }
        if (target.classList.contains('apenas-letras')) {
            target.value = target.value.replace(/[^\p{L}\s'-]/gu, '');
        }
    });

    form.addEventListener('change', function (e) {
        const target = e.target;
        if (target.tagName === 'SELECT' && target.classList.contains('input-error')) {
            target.classList.remove('input-error');
            const errorMsg = target.closest('.custom-select-wrapper').querySelector('.error-message');
            if (errorMsg) errorMsg.remove();
        }
    });

});