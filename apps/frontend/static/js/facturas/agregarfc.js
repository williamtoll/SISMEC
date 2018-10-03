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
    $(".precio_uni").focusout(function(data) {
        var id = this.dataset.id;
        precio_uni = $('#id_precio_' + id).val();
        cantidad = $('#id_cantidad_' + id).val();
        if ($('#id_impuesto_' + id).val() == "IVA10") {
            iva10 = precio_uni * cantidad;
            $('#id_iva10_' + id).val(iva10);
            calcularSubTotalesIva10();
            $('#id_iva5_' + id).val(0);
            $('#id_exentas_' + id).val(0);
        } else if($('#id_impuesto_' + id).val() == "IVA5") {
            iva5 = precio_uni * cantidad;
            $('#id_iva5_' + id).val(iva5);
            calcularSubTotalesIva5();
            $('#id_iva10_' + id).val(0);
            $('#id_exentas_' + id).val(0);
        }else{
            exentas = precio_uni * cantidad;
            $('#id_exentas_' + id).val(exentas);
            calcularSubTotalesExentas();
            $('#id_iva5_' + id).val(0);
            $('#id_iva10_' + id).val(0);
        }
        total_iva5 = parseInt(subtotal_iva5 / 21);
        total_iva10 = parseInt(subtotal_iva10/ 11);
        $('.total_iva5').val(total_iva5);
        $('.total_iva10').val(total_iva10);
        $('.total_iva').val(total_iva5 + total_iva10);

    });

    if ($('#numero_oc').val() != ""){
        $('#tipo_movimiento').val("Compra");
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
               var val = parseInt($(this).val()) ? parseInt($(this).val()) : 0;
               subtotal_iva10 += val;
               console.log(a,val);
            });
        });
        $('.sub_iva10').val(subtotal_iva10);
    }
    function calcularSubTotalesIva5(){
        subtotal_iva5 = 0;
        $('.detalles_factura tr.data').each(function(a, b){
            //console.log("a y b")
            //console.log(a,b);
            $('.iva_5', this).each(function(){
               var val = parseInt($(this).val()) ? parseInt($(this).val()) : 0;
               subtotal_iva5 += val;
               console.log(a,val);
            });
        });
        $('.sub_iva5').val(subtotal_iva5);
    }
    function calcularSubTotalesExentas(){
        subtotal_exentas = 0;
        $('.detalles_factura tr.data').each(function(a, b){
            $('.sub_exentas', this).each(function(){
               var val = parseInt($(this).val()) ? parseInt($(this).val()) : 0;
               subtotal_exentas += val;
               console.log(a,val);
            });
        });
        $('.sub_exentas').val(subtotal_exentas);
    }

    $('.guardar').on("click", function(e){
        objeto = {};
        $(".detalles_factura tr.data").each(function(index, element ){
			// Agregamos el elemento mas externo
			i = index + 1;
			//Se obtienen los datos.
            cantidad_item = $(this).find(".cantidad-item").val();
            precio_uni = $(this).find(".precio_uni").val();
            exentas = $(this).find(".exentas").val();
			iva_5 = $(this).find(".iva_5").val();
			iva_10 = $(this).find(".iva_10").val();
			id_producto = $(this).find(".id_producto").val();

			key = 'item' + i;
			value = {cantidad_item : cantidad_item, precio_uni : precio_uni, exentas: exentas, iva_5 : iva_5, iva_10 : iva_10, id_producto : id_producto};
			objeto[key] = value;
			JSON.stringify(objeto);

		});
        var detalle_factura = JSON.stringify(objeto);
        var id= $('#numero_oc').val();
        var request = $.ajax({
            type : "POST",
            url : "/sismec/facturas/agregar/" + id + "/",
            data : {
                tipo_movimiento:  $('#tipo_movimiento').val(),
                id_prov_client_select: $('#id_prov_client_select').val(),
                condicion_compra: $('#condicion_compra').val(),
                timbrado: $('#timbrado').val(),
                fecha_ini_timbrado: $('#fecha_ini_timbrado').val(),
                fecha_fin_timbrado: $('#fecha_fin_timbrado').val(),
                fecha: $('#fecha').val(),
                numero_factura: $('#numero_factura').val(),
                sub_exentas: parseInt($('.sub_exentas').val()) || 0,
                sub_iva5: parseInt($('.sub_iva5').val()) || 0,
                sub_iva10: parseInt($('.sub_iva10').val()) || 0,
                total_iva5: parseInt($('.total_iva5').val()) || 0,
                total_iva10: parseInt($('.total_iva10').val()) || 0,
                detalle_factura : detalle_factura
            },
            dataType : "json"
        });
        request.done(function(msg) {

            return true;
        });
    });
});