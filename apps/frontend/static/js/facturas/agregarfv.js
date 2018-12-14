$(document).ready(function() {
    var select_prov_client = $('#id_prov_client_select');
    inicializarSelectGenerales();
    var precio_uni = 0;
    var cantidad = 0;
    var iva10 = 0;
    var iva5 = 0;
    var exentas = 0;
    var subtotal_exentas = 0;
    var subtotal_iva5 = 0;
    var subtotal_iva10 = 0;
    var total_iva10 = 0;
    var total_iva5= 0;
    var total_iva = 0;
    currentDate();
    $(".precio_uni").focusout(function(data) {
        var id = this.dataset.id;
        precio_uni = $('#id_precio_' + id).val().split('.').join('');
        cantidad = $('#id_cantidad_' + id).val().split('.').join('');
        if ($('#id_impuesto_' + id).val() == "IVA10") {
            iva10 = precio_uni * cantidad;
            $('#id_iva10_' + id).val(formatearNumeros_convalor("" + iva10));
            calcularSubTotalesIva10();
            $('#id_iva5_' + id).val(0);
            $('#id_exentas_' + id).val(0);
        } else if($('#id_impuesto_' + id).val() == "IVA5") {
            iva5 = precio_uni * cantidad;
            $('#id_iva5_' + id).val(formatearNumeros_convalor("" + iva5));
            calcularSubTotalesIva5();
            $('#id_iva10_' + id).val(0);
            $('#id_exentas_' + id).val(0);
        }else{
            exentas = precio_uni * cantidad;
            $('#id_exentas_' + id).val(formatearNumeros_convalor("" + exentas));
            calcularSubTotalesExentas();
            $('#id_iva5_' + id).val(0);
            $('#id_iva10_' + id).val(0);
        }
        total_iva5 = parseInt(subtotal_iva5 / 21);
        total_iva10 = parseInt(subtotal_iva10/ 11);
        $('.total_iva5').val(formatearNumeros_convalor("" + total_iva5));
        $('.total_iva10').val(formatearNumeros_convalor("" + total_iva10));
        total_iva = total_iva5 + total_iva10
        $('.total_iva').val(formatearNumeros_convalor("" + total_iva));

    });
    $('#condicion_compra').on('change', function () {
        if ($('#condicion_compra').val() == "Credito") {
            $(".cantidad_cuotas").removeClass("ocultar");
        }else{
            $(".cantidad_cuotas").addClass("ocultar");
        }

    });

    $(".precio_uni").each(function(data) {
        var id = this.dataset.id;
        precio_uni = $('#id_precio_' + id).val().split('.').join('');
        cantidad = $('#id_cantidad_' + id).val().split('.').join('');
        if ($('#id_impuesto_' + id).val() == "IVA10") {
            iva10 = precio_uni * cantidad;
            $('#id_iva10_' + id).val(formatearNumeros_convalor("" + iva10));
            calcularSubTotalesIva10();
            $('#id_iva5_' + id).val(0);
            $('#id_exentas_' + id).val(0);
        } else if($('#id_impuesto_' + id).val() == "IVA5") {
            iva5 = precio_uni * cantidad;
            $('#id_iva5_' + id).val(formatearNumeros_convalor("" + iva5));
            calcularSubTotalesIva5();
            $('#id_iva10_' + id).val(0);
            $('#id_exentas_' + id).val(0);
        }else{
            exentas = precio_uni * cantidad;
            $('#id_exentas_' + id).val(formatearNumeros_convalor("" + exentas));
            calcularSubTotalesExentas();
            $('#id_iva5_' + id).val(0);
            $('#id_iva10_' + id).val(0);
        }
        total_iva5 = parseInt(subtotal_iva5 / 21);
        total_iva10 = parseInt(subtotal_iva10/ 11);
        $('.total_iva5').val(formatearNumeros_convalor("" + total_iva5));
        $('.total_iva10').val(formatearNumeros_convalor("" + total_iva10));
        total_iva = total_iva5 + total_iva10
        $('.total_iva').val(formatearNumeros_convalor("" + total_iva));
        precio_uni = formatearNumeros_convalor("" + $('#id_precio_' + id).val());
        cantidad = formatearNumeros_convalor("" + $('#id_cantidad_' + id).val());
        $('#id_precio_' + id).val(precio_uni);
        $('#id_cantidad_' + id).val(cantidad);
    });

    if ($('#numero_pre').val() != ""){
        $('#tipo_movimiento').val("VENTA");
        $('#tipo_movimiento').attr("disabled", "disabled");
        $('#id_prov_client_select').attr("disabled", "disabled");
    }
    function inicializarSelectGenerales() {
        select_prov_client.select2({
            tags: true,
            multiple: false,
            tokenSeparators: [','],
            allowClear: true,
            placeholder: "Seleccione el nombre del proveedor/cliente",
            ajax: {
                url: '/sismec/ajax/getProveedorAutocomplete/',
                dataType: "json",
                type: "GET",
                data: function (params) {
                    var queryParameters = {
                        nombres: params.term
                    };
                    return queryParameters;
                },
                processResults: function (data) {
                    return {
                        results: $.map(data, function (item) {
                            return {
                                text: item.nombres,
                                id: item.id
                            };
                        })
                    };
                }
            }
        })
            .on('select2:unselect ', function () {
                select_prov_client.find('option').remove().end();
                select_prov_client.val('').trigger('change');
            });
    }
    function calcularSubTotalesIva10(){
        subtotal_iva10 = 0;
        $('.detalles_factura tr.data').each(function(a, b){
            //console.log("a y b")
            //console.log(a,b);
            $('.iva_10', this).each(function(){
               var val = parseInt($(this).val().split('.').join('')) ? parseInt($(this).val().split('.').join('')) : 0;
               subtotal_iva10 += val;
               console.log(a,val);
            });
        });
        $('.sub_iva10').val(formatearNumeros_convalor("" + subtotal_iva10));
    }
    function calcularSubTotalesIva5(){
        subtotal_iva5 = 0;
        $('.detalles_factura tr.data').each(function(a, b){
            //console.log("a y b")
            //console.log(a,b);
            $('.iva_5', this).each(function(){

               var val = parseInt($(this).val().split('.').join('')) ? parseInt($(this).val().split('.').join('')) : 0;
               subtotal_iva5 += val;
               console.log(a,val);
            });
        });
        $('.sub_iva5').val(formatearNumeros_convalor("" + subtotal_iva5));
    }
    function calcularSubTotalesExentas(){
        subtotal_exentas = 0;
        $('.detalles_factura tr.data').each(function(a, b){
            $('.sub_exentas', this).each(function(){
               var val = parseInt($(this).val().split('.').join('')) ? parseInt($(this).val().split('.').join('')) : 0;
               subtotal_exentas += val;
               console.log(a,val);
            });
        });
        $('.sub_exentas').val(formatearNumeros_convalor("" + subtotal_exentas));
    }

    $('.guardar').on("click", function(e){
        objeto = {};
        $(".detalles_factura tr.data").each(function(index, element ){
			// Agregamos el elemento mas externo
			i = index + 1;
			//Se obtienen los datos.
            cantidad_item = $(this).find(".cantidad-item").val();
            precio_uni = $(this).find(".precio_uni").val().split('.').join('');
            exentas = $(this).find(".exentas").val().split('.').join('');
			iva_5 = $(this).find(".iva_5").val().split('.').join('');
			iva_10 = $(this).find(".iva_10").val().split('.').join('');
			id_producto = $(this).find(".id_producto").val();

			key = 'item' + i;
			value = {cantidad_item : cantidad_item, precio_uni : precio_uni, exentas: exentas, iva_5 : iva_5, iva_10 : iva_10, id_producto : id_producto};
			objeto[key] = value;
			JSON.stringify(objeto);

		});
        var detalle_factura = JSON.stringify(objeto);
        var id= $('#numero_pre').val();
        var request = $.ajax({
            type : "POST",
            url : "/sismec/facturas/generar_factura/" + id + "/",
            data : {
                tipo_movimiento:  $('#tipo_movimiento').val(),
                id_prov_client_select: $('#id_prov_client_select').val(),
                condicion_compra: $('#condicion_compra').val(),
                timbrado: $('#timbrado').val(),
                fecha_ini_timbrado: $('#fecha_ini_timbrado').val(),
                fecha_fin_timbrado: $('#fecha_fin_timbrado').val(),
                fecha: $('#fecha').val(),
                numero_factura: $('#numero_factura').val(),
                nro_cuota: parseInt($('#cantidad_cuotas').val()) || 0,
                fecha_vencimiento: $('#fecha_vencimiento').val(),
                sub_exentas: parseInt($('.sub_exentas').val().split('.').join('')) || 0,
                sub_iva5: parseInt($('.sub_iva5').val().split('.').join('')) || 0,
                sub_iva10: parseInt($('.sub_iva10').val().split('.').join('')) || 0,
                total_iva5: parseInt($('.total_iva5').val().split('.').join('')) || 0,
                total_iva10: parseInt($('.total_iva10').val().split('.').join('')) || 0,
                detalle_factura : detalle_factura
            },
            dataType : "json"
        });
        request.done(function(msg) {
            //window.location.replace("/sismec/principal_ventas?mensajes=" + msg.mensajes +"&status=" + msg.status);
            window.location.replace("/sismec/facturas/imprimir_factura?nro_movimiento="+msg.id);
        });
        request.error(function (msg) {
            window.location.replace("/sismec/principal_ventas?mensajes=" + msg.mensajes +"&status=" + msg.status);
        })
    });
});