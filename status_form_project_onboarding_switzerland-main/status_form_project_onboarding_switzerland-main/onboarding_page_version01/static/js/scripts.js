document.addEventListener("DOMContentLoaded", function() {
    fetchBankers();  // carrega a lista de bankers quando a página é aberta
});

function fetchBankers() {
    fetch('/get_bankers')
        .then(response => response.json())
        .then(bankers => {
            const bankerSelect = document.getElementById('banker');
            bankerSelect.innerHTML = '<option value="">Select Banker</option>'; // clear nas opções existentes
            bankers.forEach(banker => {
                let option = document.createElement('option');
                option.value = banker.id;
                option.text = banker.name;
                bankerSelect.appendChild(option);
            });
        });
}

function fetchClients() {
    const bankerId = document.getElementById('banker').value;
    const clientSelect = document.getElementById('client');
    clientSelect.innerHTML = '<option value="">Select Client</option>'; // reset no campo client

    if (bankerId) {
        clientSelect.disabled = false; // habilita o campo de Client
        fetch(`/get_clients?banker_id=${encodeURIComponent(bankerId)}`)
            .then(response => response.json())
            .then(clients => {
                clients.forEach(client => {
                    let option = document.createElement('option');
                    option.value = client.id;
                    option.text = client.name;
                    clientSelect.appendChild(option);
                });
            });
    } else {
        clientSelect.disabled = true; // desabilita o campo de Client if nenhum banker for selecionado
        document.getElementById('error-message').classList.add('hidden'); // oculta a mensagem de erro
    }
}

function getStatus() {
    const clientTitle = document.getElementById('client').value;
    if (clientTitle) {
        fetch(`/get_status?card_title=${encodeURIComponent(clientTitle)}`)
            .then(response => response.json())
            .then(statuses => {
                // filtro nos dados para remover qualquer informação do banker
                const filteredStatuses = filterBankerData(statuses);
                displayStatuses(filteredStatuses);
            })
            .catch(error => {
                console.error('Erro ao buscar status:', error);
            });
    }
}

// função para filtro nos dados do banker
function filterBankerData(statuses) {
    return statuses.filter(status => {
        return !status.form.includes("Banker"); // filtro
    });
}

// função para show nos dados na table
function displayStatuses(statuses) {
    const statusTableBody = document.getElementById('status-table').querySelector('tbody');
    statusTableBody.innerHTML = '';
    statuses.forEach(status => {
        let row = statusTableBody.insertRow();
        let cellForm = row.insertCell(0);
        let cellStatus = row.insertCell(1);

        if (status.url) {
            let link = document.createElement('a');
            link.href = status.url;
            link.textContent = status.form;
            link.target = '_blank';
            cellForm.appendChild(link);
        } else {
            cellForm.textContent = status.form;
        }

        cellStatus.textContent = status.status;
    });
}

// exibe msg de erro se o filtro de Client for clicado sem selecionar um Banker (test)
document.getElementById('client').addEventListener('click', function(event) {
    if (!document.getElementById('banker').value) {
        document.getElementById('error-message').classList.remove('hidden');
        event.preventDefault();
    }
});