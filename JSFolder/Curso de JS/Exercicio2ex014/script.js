function carregar(){
    var msg = window.document.getElementById('msg')
    var img = window.document.getElementById('imagem1')
    var data = new Date()
    var hora = 22//data.getHours()
    
    msg.innerHTML = `Agora são ${hora} horas.`
    if (hora >= 0 && hora < 12){
        //BOM DIA
        img.src = 'manha.jpg'
        document.body.style.background = '#f5dd95'
        document.getElementById('headerr').style.color = '#000000'
        document.getElementById('footerr').style.color = '#000000'
    } else if (hora >= 12 && hora < 18) {
        //Boa tarde
        img.src = 'chatarde.jpg'
        document.body.style.background = '#637cd4'

    } else {
        //Boa Noite
        img.src = 'noite.jpg'
        document.body.style.background = '#3f3063'
    }
}