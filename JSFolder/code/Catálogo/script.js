let sect = document.getElementById('sec1')
let list = ['um', 'dois', 'três', 'quatro', 'cinco', 'seis', 'sete', 'oito', 'nove', 'dez', 'onze', 'doze', 'treze', 'catorze', 'quinze', 'dezesseis', 'dezessete', 'dezoito', 'dezenove', 'vinte', 'vinte e um']
sect.innerHTML = ""
for (let c=0;c<=list.length-1;c++) {
    let item = document.createElement('div')
    item.innerHTML = `${list[c]}`
    item.id = 'quad1'
    sect.appendChild(item)
}