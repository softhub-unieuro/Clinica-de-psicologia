// Função auxiliar para aplicar classes Bootstrap aos inputs do Django caso não venham do backend
document.addEventListener("DOMContentLoaded", function() {
    var inputs = document.querySelectorAll('input, select');
    inputs.forEach(function(input) {
        if (input.type !== 'checkbox' && input.type !== 'radio' && input.type !== 'submit') {
            input.classList.add('form-control');
        }
        if (input.tagName === 'SELECT') {
            input.classList.add('form-select');
            input.classList.remove('form-control'); // Select usa classe diferente no BS5
        }
    });
});

function selectProfile(profileValue) {
    // 1. Atualiza o Select oculto do Django
    const selectCargo = document.getElementById('id_cargo');
    if(selectCargo) selectCargo.value = profileValue;

    // 2. Gerencia a classe 'active' nos botões visuais
    const buttons = document.querySelectorAll('.btn-profile');
    buttons.forEach(btn => {
        // Limpa todos primeiro
        btn.classList.remove('active');
        
        // Ativa o clicado (verificação simples pelo texto do onclick)
        if (btn.getAttribute('onclick').includes("'" + profileValue + "'")) {
            btn.classList.add('active');
        }
    });

    // 3. Mostra/Esconde seções
    const sectionEstag = document.getElementById('section-ESTAG');
    const sectionPsi = document.getElementById('section-PSI');
    const labelMatricula = document.getElementById('label-matricula');

    // Reset (esconde tudo com animação suave se necessário, aqui display none)
    if(sectionEstag) sectionEstag.classList.remove('show');
    if(sectionPsi) sectionPsi.classList.remove('show');

    // Lógica de Exibição
    if (profileValue === 'ESTAG') {
        if(sectionEstag) sectionEstag.classList.add('show');
        if(labelMatricula) labelMatricula.innerText = "RA Acadêmico";
    } else if (['SUPER', 'COORD', 'RESP_TEC'].includes(profileValue)) {
        if(sectionPsi) sectionPsi.classList.add('show');
        if(labelMatricula) labelMatricula.innerText = "Matrícula Funcional";
    } else {
        // Secretária ou outros
        if(labelMatricula) labelMatricula.innerText = "Matrícula / Login";
    }
}

// Inicialização ao carregar a página
window.onload = function() {
    // Adiciona script para garantir estilização dos campos
    var inputs = document.querySelectorAll('input[type="text"], input[type="email"], input[type="password"], input[type="number"], select, input[type="file"]');
    inputs.forEach(function(el) {
        if(el.tagName === 'SELECT') el.classList.add('form-select');
        else el.classList.add('form-control');
    });

    // Verifica valor atual do cargo para manter estado em caso de erro de validação
    const cargoInput = document.getElementById('id_cargo');
    if (cargoInput && cargoInput.value) {
        selectProfile(cargoInput.value);
    } else {
        selectProfile('ESTAG'); // Padrão
    }
};
