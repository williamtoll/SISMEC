$(document).ready(function() {
    $('#monto_pagado').on('change', function () {
        var saldo= parseInt($("#saldo_actual").val());
        var saldo_nuevo = saldo - parseInt($("#monto_pagado").val());
        $("#saldo").val(saldo_nuevo);
        $("#saldo").prop("readonly", true);
    });
    currentDate();
     $('#forma_pago').on('change', function () {
        if ($('#forma_pago').val() == "TARJETA") {
            $(".forma-pago-tarjeta").removeClass("ocultar");
            $(".forma-pago-cheque").addClass("ocultar");
        }else if($('#forma_pago').val() == "CHEQUE"){
            $(".forma-pago-cheque").removeClass("ocultar");
            $(".forma-pago-tarjeta").addClass("ocultar");
        }else{
            $(".forma-pago-tarjeta").addClass("ocultar");
            $(".forma-pago-cheque").addClass("ocultar");
        }

    });

     $('.guardar').on("click", function(e){
         if(validarDatos() == false){
             return false;
         };
         var dato_adicional = {}
          if ($('#forma_pago').val() == "TARJETA") {
            dato_adicional.nro_cupon = $('#nro_cupon').val();
        }else if($('#forma_pago').val() == "CHEQUE"){
            dato_adicional.nro_cheque = $('#nro_cheque').val();
            dato_adicional.banco = $('#banco').val();
            dato_adicional.fecha_vencimiento = $('#fecha_vencimiento').val();
            dato_adicional.nombre_titular = $('#nombre_titular').val();
        }
        var id = $('#id_factura').val();
        dato_adicional=JSON.stringify(dato_adicional);
        var request = $.ajax({
            type : "POST",
            url : "/sismec/facturas/cobrar_factura/" + id + "/",
            data : {
                fecha: $('#fecha').val(),
                numero_factura:  $('#numero_factura').val(),
                numero_recibo: $('#numero_recibo').val(),
                forma_pago: $('#forma_pago').val(),
                monto_total: $('#monto_total').val(),
                saldo_actual: $('#saldo_actual').val(),
                monto_pagado: $('#monto_pagado').val(),
                saldo: $('#saldo').val(),
                dato_adicional: dato_adicional
            },
            dataType : "json"
        });
        request.done(function(msg) {
            window.location.replace("/sismec/facturas/imprimir_recibo_cobro?id_cobro=" + msg.id_cobro );
        });
        request.error(function (msg) {
            window.location.replace("/sismec/principal_cobros?mensajes=" + msg.mensajes +"&status=" + msg.status);
        })
     });
});

function validarDatos(){
    console.log('validando cabecera');
    if ($("#fecha").val() == ""){
        alert("Debe seleccionar una fecha valida");
        return false;
    }
    if ($("#saldo").val() < 0 ){
        alert("El saldo es inferior a cero");
        return false;
    }
    return true;
}