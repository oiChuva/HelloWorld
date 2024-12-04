// Função para consultar o estoque
function consultarEstoque() {
    const resultadoDiv = document.getElementById("res");
    const formDiv = document.getElementById("form");
    const outsection = document.getElementById("outsection");
    const url = 'https://192.168.88.72:5000/LerEst'; // Endpoint da API

    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro na resposta da API');
            }
            return response.json();
        })
        .then(data => {
            // Remove o botão de "Consultar Estoque"
            const consultarButton = document.getElementById("botaoGetApi");
            if (consultarButton) {
                consultarButton.remove();
            }

            resultadoDiv.innerHTML = '<h2>Resultado da Consulta</h2>';

            if (data.length > 0) {
                // Criação do campo de busca com datalist
                const input = document.createElement("input");
                input.type = "text";
                input.id = "itemSearch";
                input.setAttribute("list", "itemsList");
                input.placeholder = "Digite o nome ou código do item";

                const dataList = document.createElement("datalist");
                dataList.id = "itemsList";

                // Preenchendo o datalist com os dados retornados pela API
                data.forEach(item => {
                    const option = document.createElement("option");
                    option.value = `${item.cDescricao} | ${item.cCodigo}`;
                    option.setAttribute("data-saldo", item.nSaldo);
                    dataList.appendChild(option);
                });

                // Exibição do saldo do item selecionado
                const saldoDisplay = document.createElement("p");
                saldoDisplay.id = "saldoDisplay";
                saldoDisplay.innerHTML = "Saldo do item selecionado: ";

                resultadoDiv.appendChild(input);
                resultadoDiv.appendChild(dataList);
                resultadoDiv.appendChild(saldoDisplay);

                input.addEventListener("change", () => {
                    const selectedItem = input.value;
                    const option = Array.from(dataList.options).find(opt => opt.value === selectedItem);

                    if (option) {
                        const selectedSaldo = option.getAttribute("data-saldo");
                        saldoDisplay.innerHTML = `Saldo do item selecionado: ${selectedSaldo}`;

                        verificarCampos();
                    } else {
                        saldoDisplay.innerHTML = "Item inválido.";
                    }
                });

                // Ajustar a largura da seção
                const sec = document.getElementById("section1");
                if (sec) {
                    sec.style.width = "70%";
                    sec.style.height = "96%"
                }
            } else {
                resultadoDiv.innerHTML += '<p>Nenhum produto encontrado no estoque.</p>';
            }
        })
        .catch(error => {
            console.error('Erro:', error);
            resultadoDiv.innerHTML = '<p>Erro ao consultar o estoque.</p>';
        });
}

// Verificar se todos os campos estão preenchidos antes de exibir o botão
function verificarCampos() {
    const input = document.getElementById("itemSearch").value;
    const solicitante = document.getElementById("Solicitante").value;
    const motivoOS = document.getElementById("MotivoOS").value;
    const quantidadeNum = document.getElementById("quantNum").value;
    const data = document.getElementById("Data").value;
    const saldoDisplay = document.getElementById("saldoDisplay").innerText;

    const outsection = document.getElementById("outsection");

    // Se todos os campos estão preenchidos e o saldo é válido
    if (input && solicitante && motivoOS && quantidadeNum && data && saldoDisplay.includes("Saldo do item selecionado")) {
        // Remove botão "Enviar" anterior, se existir
        const existingButton = document.getElementById("sendButton");
        if (!existingButton) {
            const sendButton = document.createElement("button");
            sendButton.id = "sendButton";
            sendButton.textContent = "➤";
            outsection.appendChild(sendButton);

            // Adiciona evento de clique no botão "Enviar"
            sendButton.addEventListener("click", () => {
                const ht_mail = `
                    <p><b>Item selecionado:</b> ${input}</p>
                    <p><b>Saldo:</b> ${saldoDisplay.split(": ")[1]}</p>
                    <p><b>Quantidade:</b> ${quantidadeNum}</p>
                    <p><b>Solicitante:</b> ${solicitante}</p>
                    <p><b>Motivo ou OS:</b> ${motivoOS}</p>
                    <p><b>Data:</b> ${data}</p>
                `;
                enviarDados(ht_mail);
            });
        }
    } else {
        // Remove botão "Enviar" se algum campo estiver vazio
        const existingButton = document.getElementById("sendButton");
        if (existingButton) {
            existingButton.remove();
        }
    }
}

// Função para enviar os dados
function enviarDados(ht_mail) {
    const url = 'https://192.168.88.72:5000/sendmail'; // Endpoint para envio

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ ht_mail }),
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro ao enviar os dados');
            }
            return response.json();
        })
        .then(data => {
            document.body.innerHTML = 'Solicitação Enviada.';
            const F5_Button = document.createElement("button");
            F5_Button.id = "sendButton";
            F5_Button.textContent = "↺";
            console.log("Resposta do servidor:", data);
            document.body.appendChild(F5_Button);
            F5_Button.style.position = "absolute";
            F5_Button.style.top = "50%";
            F5_Button.style.left = "50%";
            F5_Button.style.transform = "translate(-50%, -50%)";
            F5_Button.style.backgroundColor = "#282828";
            F5_Button.addEventListener("click", () => {
                window.location.href = "https://requisicao.arcocirurgico.com.br/";
            });
        })
        .catch(error => {
            console.error('Erro:', error);
            alert("Erro ao enviar os dados.");
        });
}

// Adicionar eventos de mudança aos campos para verificar preenchimento
document.querySelectorAll("#Solicitante, #MotivoOS, #quantNum, #Data").forEach(field => {
    field.addEventListener("input", verificarCampos);
});
