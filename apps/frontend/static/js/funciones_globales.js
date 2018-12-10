
function formatearNumeros(input)
{
    var num = input.value.replace(/\./g,'');
    if(!isNaN(num)){
        num = num.toString().split('').reverse().join('').replace(/(?=\d*\.?)(\d{3})/g,'$1.');
        num = num.split('').reverse().join('').replace(/^[\.]/,'');
        input.value = num;
    }
    else{ alert('Solo se permiten numeros');
        input.value = input.value.replace(/[^\d\.]*/g,'');
    }
}

function formatearNumeros_convalor(input)
{
    var num = input.replace(/\./g,'');
    if(!isNaN(num)){
        num = num.toString().split('').reverse().join('').replace(/(?=\d*\.?)(\d{3})/g,'$1.');
        num = num.split('').reverse().join('').replace(/^[\.]/,'');
        input = num;
    }
    else{ alert('Solo se permiten numeros');
        input = input.replace(/[^\d\.]*/g,'');
    }
    return input;
}

function currentDate(){
    var today = new Date();
    var dd = today.getDate();
    var mm = today.getMonth() + 1; //January is 0!

    var yyyy = today.getFullYear();
    if (dd < 10) {
      dd = '0' + dd;
    }
    if (mm < 10) {
      mm = '0' + mm;
    }
    //today = dd + '/' + mm + '/' + yyyy;
    today = yyyy + '-' + mm + '-' + dd;
    document.getElementById('fecha').value = today;
    //input.value = today;
}