function consultarEstoque() {
    const resultadoDiv = document.getElementById("res");
    const url = 'https://192.168.88.72:5000/LerEst'; // Endpoint da API

    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro na resposta da API');
            }
            return response.json();
        })
        .then(data => {
            resultadoDiv.innerHTML = '</br>';

            if (data.length > 0) {
                // Criar container para input e saldo
                const container = document.createElement("div");
                container.className = "input-container"; // Aplicar flexbox

                // Criar input de pesquisa
                const input = document.createElement("input");
                input.type = "text";
                input.id = "itemSearch";
                input.setAttribute("list", "itemsList");
                input.placeholder = "Digite o nome ou código do item";
                input.className = "input";

                const dataList = document.createElement("datalist");
                dataList.id = "itemsList";

                // Preencher o datalist com os itens retornados
                data.forEach(item => {
                    const option = document.createElement("option");
                    option.value = `${item.cDescricao} | ${item.cCodigo}`;
                    option.setAttribute("data-saldo", item.nSaldo);
                    dataList.appendChild(option);
                });

                // Criar saldoDisplay para exibir o saldo
                const saldoDisplay = document.createElement("div");
                saldoDisplay.id = "saldoDisplay";
                saldoDisplay.className = "quantidade";
                saldoDisplay.innerHTML = "Saldo";

                // Adicionar input e saldo ao container
                container.appendChild(input);
                container.appendChild(saldoDisplay);

                // Adicionar elementos ao resultadoDiv
                resultadoDiv.appendChild(container);
                resultadoDiv.appendChild(dataList);

                // Atualizar saldo ao selecionar item
                input.addEventListener("input", () => {
                    const selectedItem = input.value;
                    const option = Array.from(dataList.options).find(opt => opt.value === selectedItem);

                    if (option) {
                        saldoDisplay.innerHTML = `${option.getAttribute("data-saldo")}`;
                    } else {
                        saldoDisplay.innerHTML = "Item inválido.";
                    }
                });
            } else {
                resultadoDiv.innerHTML += '<p>Nenhum produto encontrado no estoque.</p>';
            }
        })
        .catch(error => {
            console.error('Erro:', error);
            resultadoDiv.innerHTML = '<p>Erro ao consultar o estoque.</p>';
        });
}



function verificarCampos() {
    const input = document.getElementById("itemSearch").value.trim();
    const solicitante = document.getElementById("Solicitante").value.trim();
    const motivoOS = document.getElementById("MotivoOS").value.trim();
    const quantidadeNum = document.getElementById("quantNum").value.trim();
    const data = document.getElementById("Data").value.trim();
    const saldoDisplay = document.getElementById("saldoDisplay").innerText.trim();
    const sendButton = document.getElementById("sendButton");

    // Verifica se saldoDisplay é um número válido
    const saldoValido = !isNaN(parseFloat(saldoDisplay)) && isFinite(saldoDisplay);

    if (input && solicitante && motivoOS && quantidadeNum && data && saldoValido) {
        sendButton.onclick = () => {
            const ht_mail = `
                <p><b>Item selecionado:</b> ${input}</p>
                <p><b>Saldo:</b> ${saldoDisplay}</p>
                <p><b>Quantidade:</b> ${quantidadeNum}</p>
                <p><b>Solicitante:</b> ${solicitante}</p>
                <p><b>Motivo ou OS:</b> ${motivoOS}</p>
                <p><b>Data:</b> ${data}</p>
            `;
            enviarDados(ht_mail);
        };
    } else {
        console.log("Erro na identificação. Verifique se todos os campos foram preenchidos corretamente.");
    }
}

function enviarDados(ht_mail) {
    const url = 'https://192.168.88.72:5000/sendmail';

    fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ht_mail }),
    })
        .then(response => {
            if (!response.ok) throw new Error('Erro ao enviar os dados');
            return response.json();
        })
        .then(() => {
            window.location.href = "response.html"
        })
        .catch(error => {
            console.error('Erro:', error);
            alert("Erro ao enviar os dados.");
        });
}

document.querySelectorAll("#Solicitante, #MotivoOS, #quantNum, #Data").forEach(field => {
    field.addEventListener("input", verificarCampos);
});