document.getElementById("sendButton").addEventListener("click", function () {
    // Captura os valores dos campos de entrada
    const codItem = document.getElementById("codItem").value.trim();
    const quantidade = document.getElementById("quantidade").value.trim();

    // Valida os campos
    if (!codItem || !quantidade) {
        alert("Por favor, preencha todos os campos!");
        return;
    }

    // Cria o payload para a requisição
    const payload = {
        codItem: codItem,
        qtde: parseInt(quantidade, 10)
    };

    // Envia a requisição para a API
    fetch("https://192.168.88.72:5000/RequisicaoInclusaoCompra", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`Erro na requisição: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        // Exibe a resposta da API
        alert(`Requisição enviada com sucesso! Código gerado: ${data.codIntReqCompra}`);
    })
    .catch(error => {
        // Trata erros na requisição
        console.error("Erro:", error);
        alert("Ocorreu um erro ao enviar a requisição. Verifique os dados e tente novamente.");
    });
});