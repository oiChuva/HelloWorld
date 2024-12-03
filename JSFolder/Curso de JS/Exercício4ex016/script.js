// // iniciar variáveis
// var ini = 0
// var fim = 0
// var pas = 0
// var res = document.getElementById('res')

// // colocar botão
// function contar(){
// // receber variáveis
//     var ini = document.getElementById('ini').value
//     var fim = document.getElementById('fim').value
//     var pas = document.getElementById('pas').value
//     // Converter para números
//     ini = Number(ini);
//     fim = Number(fim);
//     pas = Number(pas);
//     if (pas <= 0) {
//         alert("Passo inválido! Considerando passo 1.")
//         pas = 1;
//     }
//     res.innerHTML = (`${ini} `)
//     if (ini <= fim) {
//         if (ini >= 0 && fim >= ini++ && pas !=0) {
//             for (var i = ini; i <= fim; i += pas) {
//                 res.innerHTML += (`${i} `)
//             }
//         }
//     } else {
//         res.innerHTML = "Início maior que o fim!"
//     }
// }
function contar(){
    let ini = document.getElementById('ini')
    let fim = document.getElementById('fim')
    let passo = document.getElementById('pas')
    let res = document.getElementById('res')
    if (ini.value.length == 0 || fim.value.length == 0 || passo.value.length == 0){
        // window.alert('[ERRO] Faltam dados!')
        res.innerHTML = 'Impossível Contar.'
    } else {
        res.innerHTML = 'Contando: <br>'
        let i = Number(ini.value)
        let f = Number(fim.value)
        let p = Number(passo.value)
        if (p <= 0){
            window.alert('Passo inválido, considerando passo 1.')
            p = 1
        }
        if (i < f){
            // crescente
            for(let c = i; c <= f; c+= p){
                res.innerHTML += `${c} \u{27A1} `
            }
        } else {
            // regressiva
            for (let c = i; c >= f; c -= p){
                res.innerHTML += `${c} \u{27A1} `
            }
        } 
        res.innerHTML += `\u{1F4A5}`
    }
}