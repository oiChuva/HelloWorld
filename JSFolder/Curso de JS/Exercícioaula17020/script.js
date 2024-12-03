let num = document.getElementById('txtn')
let nlist = document.getElementById('sellist')
let res = document.querySelector('div#res')
let numlist = []

function isNumero(n) {
    if(Number(n) >= 1 && Number(n) <= 100){
        return true
    } else {
        return false
    }
}
function inLista(n, l) {
    if(l.indexOf(Number(n)) != -1) {
        return true
    } else {
        return false
    }
}

function adece(){
    if (isNumero(num.value) && !inLista(num.value, numlist)) {
        numlist.push(Number(num.value))
        let item =  document.createElement('option')
        item.text = `Valor ${num.value} adicionado.`
        nlist.appendChild(item)
        res.innerHTML = ''
    } else {
        window.alert('Valor inválido ou já encontrado na lista.')
    }
    num.value = ''
    num.focus()
}

function final() {
    if (numlist.length == 0) {
        window.alert('Insira valores antes de finalizar.')
    } else {
        let tot = numlist.length
        let maior = numlist[0]
        let menor = numlist[0]
        let soma = 0
        let media = 0
        for(let pos in numlist){
            soma += numlist[pos]
            if (numlist[pos] > maior)
                maior = numlist[pos]
            if (numlist[pos] < menor)
                menor = numlist[pos]
        }
        media = soma / tot
        res.innerHTML = ''
        res.innerHTML += `<p>Ao todo, temos ${tot} números cadastrados.</p>`
        res.innerHTML += `<p>O maior valor informado foi ${maior}.</p>`
        res.innerHTML += `<p>O menor valor informado foi ${menor}.</p>`
        res.innerHTML += `<p>Somando todos os valores, temos ${soma}.</p>`
        res.innerHTML += `<p>A média dos valores digitados é ${media}.</p>`
    }
}