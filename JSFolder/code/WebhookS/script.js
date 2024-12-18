// Suprimindo avisos de segurança relacionados à desabilitação da verificação SSL não é possível em navegadores por razões de segurança
// Portanto, o URL deve usar um certificado SSL válido no lado do servidor.

function enviarSolicitacao(numeroSerie) {
    const url = "https://192.168.88.72:5000/neovero-receiver";
    const data = { numeroSerie: numeroSerie };

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data),
    })
    .then(response => {
        if (response.ok) {
            alert(`Sinal enviado com sucesso para ${url}: ${numeroSerie}.`);
        } else {
            alert(`Erro ao enviar sinal para ${url}: ${numeroSerie}. Status code: ${response.status}`);
        }
    })
    .catch(error => {
        alert(`Erro de Conexão: Não foi possível conectar ao servidor ${url}. Erro: ${error}`);
    });
}

// Manipulador de evento para o botão
document.getElementById('enviarButton').addEventListener('click', () => {
    const numeroSerie = document.getElementById('valorInput').value;

    if (numeroSerie) {
        enviarSolicitacao(numeroSerie);
    } else {
        alert("Por favor, insira um número de série.");
    }
});
