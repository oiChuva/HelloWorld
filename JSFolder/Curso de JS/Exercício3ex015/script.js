function verificar() {
    var data = new Date()
    var ano = data.getFullYear()
    var fano = document.getElementById('txtano')
    var res = document.querySelector('div#res')
    if (fano.value.length == 0 || Number(fano.value) > ano){
        window.alert('Verifique os dados e tente novamente')
    } else {
        var fsex = document.getElementsByName('radsex')
        var idade = ano - Number(fano.value)
        var gênero = ''
        var img = document.createElement('img')
        img.setAttribute('id', 'foto')
        if (fsex[0].checked){ 
            gênero = 'Homem'
            if (idade >= 0 && idade < 10){
                //Criança
                img.setAttribute('src', 'kid-m.jpg')

            } else if (idade < 21) {
                //jovem
                img.setAttribute('src', 'jovem-m.jpg')
            } else if (idade < 50){
                //adulto
                img.setAttribute('src', 'adulto-m.jpg')
            } else {
                //idoso
                img.setAttribute('src', 'idoso-m.jpg')
            }
        } else if (fsex[1].checked) {
            gênero = 'Mulher'
            if (idade >= 0 && idade < 10){
                //Criança
                img.setAttribute('src', 'kid-f.jpg')

            } else if (idade < 21) {
                //jovem
                img.setAttribute('src', 'jovem-f.jpg')
            } else if (idade < 50){
                //adulto
                img.setAttribute('src', 'adulto-f.jpg')
            } else {
                //idoso
                img.setAttribute('src', 'idosa-f.jpg')
            }
        } else {
            window.alert('Verifique os dados e tente novamente')
        }
        res.style.textAlign = 'center'
        res.innerHTML = `Detectamos ${gênero} com ${idade} anos`
        img.setAttribute("style","border-radius: 50%" )
        img.setAttribute("width", "250pt")
        img.setAttribute("height", "250pt")
        img.setAttribute("id", "photo")
        res.appendChild(img)
    }
}
