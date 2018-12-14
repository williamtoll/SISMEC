item_inicial_detalle_pedido =  '<div class="item-detalle">'
			+ '<input type="text" class="producto_desc col-xs-4" id="id_producto_select" name="id_producto_select">'
            + '<input type="number" class= "cantidad-item item col-xs-2" placeholder="Cantidad" value="1" min="1" style="left: 5px;" disabled>'
            + '<input type="text" class= "monto-item item col-xs-2" placeholder="Monto" value="" onkeyup="formatearNumeros(this)" onchange="formatearNumeros(this)" style="left: 5px;">'
			+ '<a href="#" class="btn btn-sm btn-danger rm-btn" style="height: 35px;margin-left: 10px;"><span class="glyphicon glyphicon-minus"></span></a>'
		    + ' <br><br></div>';


item_detalle_pedido = '<div class="item-detalle">'
			+ '<input type="text" class="producto_desc col-xs-4" id="id_producto_select" name="id_producto_select">'
            + '<input type="number" class= "cantidad-item item col-xs-2" placeholder="Cantidad" value="1" min="1" style="left: 5px;" disabled>'
            + '<input type="text" class= "monto-item item col-xs-2" placeholder="Monto" onkeyup="formatearNumeros(this)" onchange="formatearNumeros(this)" value="" style="left: 5px;">'
			+ '<a href="#" class="btn btn-sm btn-danger rm-btn" style="height: 35px;margin-left: 10px;"><span class="glyphicon glyphicon-minus"></span></a>'
		    + ' <br><br></div>';

var detalle_valido = true;
var es_repetido = false;
var stock_disponible = true;
$(document).ready(function() {
    var select_recepcion = $('#id_recepcion_select');
    var select_producto = $('#id_producto_agregar');
    inicializarSelectGenerales();
    var idsum= 1;
    var index = 0;
    var descripcion;
    var ok=false;
    var cantidad_item= 0;
    var fecha_recepcion = new Date();
    var fecha_presupuesto = new Date();
    var precio = 0;
    function inicializarSelectGenerales() {
        select_recepcion.select2({
                tags: true,
                multiple: false,
                tokenSeparators: [','],
                allowClear: true,
                placeholder: "Seleccione el codigo de recepcion",
                ajax: {
                    url: '/sismec/ajax/getRecepcionAutocomplete/',
                    dataType: "json",
                    type: "GET",
                    data: function (params) {
                        var queryParameters = {
                            codigo: params.term
                        };
                        return queryParameters;
                    },
                    processResults: function (data) {
                        return {
                            results: $.map(data, function (item) {
                                return {
                                    text: item.codigo_recepcion,
                                    id: item.id
                                };
                            })
                        };
                    }
                }
            })
            .on('select2:unselect ', function () {
                select_recepcion.find('option').remove().end();
                select_recepcion.val('').trigger('change');
            })
        select_producto.select2({
            tags: true,
            multiple: false,
            tokenSeparators: [','],
            allowClear: true,
            placeholder: "Seleccione el nombre del producto/servicio",
            ajax: {
                url: '/sismec/ajax/getProductoAutocomplete/',
                dataType: "json",
                type: "GET",
                data: function (params) {
                    var queryParameters = {
                        nombre: params.term
                    };
                    return queryParameters;
                },
                processResults: function (data) {
                    return {
                        results: $.map(data, function (item) {
                            return {
                                text: item.descripcion,
                                id: item.id

                            };
                        })
                    };
                }

            }
        })
    }
    $('#id_recepcion_select').on('change', function () {
        obtenerFechaRecepcion()
        $(".fecha_recepcion").removeClass("ocultar");
        $(".detalle_problema").removeClass("ocultar");

    });

    $('#id_producto_agregar').on('change', function () {
       obtenerPrecioVenta();
    });
    $('#cantidad').on('change', function () {
       verificarStock();
    });
    //para agregar un item
    $(".agregar").click(function () {
        es_repetido = itemRepetidos();
        if (es_repetido == false){
             if ($('#id_producto_agregar').val() == null){
                alert("Favor seleccionar un producto");
            }else{
               $('.detalle_pedido').append(item_detalle_pedido);
                index = $('.item-detalle').length;
                var inputs= $('.item-detalle')[index -1].children
                descripcion = $('#id_producto_agregar :selected').text();
                cantidad_item = $('#cantidad').val();
                precio = $("#precio_venta").val();
                inputs[0].value=descripcion;
                inputs[1].value=cantidad_item;
                inputs[2].value = precio;
                select_producto.find('option').remove().end();
                select_producto.val('').trigger('change');
                $('#cantidad').val('1');
                idsum +=1;
            }
        }else{
            select_producto.find('option').remove().end();
            select_producto.val('').trigger('change');
        }
    });
    // Para eliminar un item.
    $('.detalle_pedido').on("click",".rm-btn", function(e){
        e.preventDefault();
        $(this).parent('div').remove();
    });

    //Control del SUBMIT del FORM
    $("#form_add_oc").submit(function(){
        //1. TODO: Hacer chequeo de que todos los valores esten correctos.
        if (validarCabecera() && validarDetalle()){
            //2. Obtener el JSON del detalle
            detalle = generarDetalleJSON();
            $("#detalle").val(detalle);
            return true;
        }
        else{
            return false;
        }
    });
});

function itemRepetidos(){
    var repetidos = false;
    $(".item-detalle").each(function(index, element ){
		concepto = $(this).find(".producto_desc").val();
		// Verificar que ya no exista ese item agregado
		if (concepto == $('#id_producto_agregar :selected').text()){
		    alert("El item seleccionado ya se encuentra agregado")
            repetidos = true;
		}
	});
    return repetidos;
}

function generarDetalleJSON(){
		detalle_json = '';
		objeto = {};
		$(".item-detalle").each(function(index, element ){
			// Agregamos el elemento mas externo
			i = index + 1;
			//Se obtienen los datos.
            descripcion = $(this).find(".producto_desc").val();
			cantidad = $(this).find(".cantidad-item").val();
            monto = $(this).find(".monto-item").val();
            monto = monto.replace(".","");
		    monto = parseInt(monto) || 0;
			key = 'item' + i;
			value = {descripcion : descripcion, cantidad : cantidad, monto: monto};
			objeto[key] = value;
			JSON.stringify(objeto);

		});

		detalle_json = JSON.stringify(objeto);
		return detalle_json;
	}

function validarDetalle(){

	console.log('validando');
	detalle_valido = true;
	var len = $('.item-detalle').length;
	if (len == 0){
	    alert("Debe seleccionar al menos un item");
        detalle_valido =false;
    }
	$(".item-detalle").each(function(index, element ){
		cantidad = $(this).find(".cantidad-item").val();
		cantidad = parseInt(cantidad) || 0;
		concepto = $(this).find(".producto_desc").val();
        monto = $(this).find(".monto-item").val();
        monto=monto.split('.').join('');
		//monto = monto.replace("/.\s?/g",'');
		//monto = parseInt(monto) || 0;
		$(this).find(".monto-item").val(monto);
		//indicador_validez = '#840A0A'; // Por defecto invalido (Rojo)
		// Requerimieno minimo para un detalle valido
		if (cantidad != 0){
				// VALIDO
				console.log('Detalle VALIDO');
				//indicador_validez = '#1C842D';
		}
		else{
		    alert("Debe seleccionar al menos un item");
			detalle_valido =false;
		}
		//$(this).css('background',indicador_validez);
	});
	return detalle_valido;
}

function validarCabecera(){
    console.log('validando cabecera');
    if ($("#fecha").val() == ""){
        alert("Debe seleccionar una fecha valida");
        return false;
    }
    if ($("#id_recepcion_select").val() == null){
        alert("Debe seleccionar una Recepcion valida");
        return false;
    }
    fecha_recepcion = new Date($("#fecha_recepcion").val());
    fecha_presupuesto =  new Date($("#fecha").val());
    if(fecha_recepcion > fecha_presupuesto){
        alert("Debe seleccionar una fecha superior a la fecha de recepcion");
        return false;
    }
    return true;
}
function obtenerFechaRecepcion(){
    var request = $.ajax({
        type : "GET",
        url : "/sismec/ajax/getRecepcionById/",
        dataType: "json",
        data : {
            codigo: $("#id_recepcion_select option:selected").val()
        },
        dataType : "json"
    });
    // Obtenemos la fecha de la recepcion
    request.done(function(msg) {
        $("#fecha_recepcion").val(msg[0].fields.fecha_recepcion);
        $("#detalle_problema").val(msg[0].fields.detalle_problema);
    });
}

function obtenerPrecioVenta() {
    var producto_id = $('#id_producto_agregar').val();
    var precio_venta = 0;
    var request = $.ajax({
        type : "GET",
        url : "/sismec/ajax/getProductoById/",
        dataType: "json",
        data : {
            id_producto: producto_id
        },
        dataType : "json"
    });
    // Obtenemos la fecha de la recepcion
    request.done(function(msg) {
        if (msg != null){
            precio_venta = msg[0].fields.precio_venta;
            $("#precio_venta").val(precio_venta);
        }
    });
}
function verificarStock(){
     var producto_id = $('#id_producto_agregar').val();
     var cantidad = $('#cantidad').val();
      var request = $.ajax({
        type : "GET",
        url : "/sismec/ajax/verificarStock/",
        dataType: "json",
        data : {
            id_producto: producto_id
        },
        dataType : "json"
    });
    // Obtenemos la fecha de la recepcion
    request.done(function(msg) {
        if (msg != null){
           cantidad_stock = msg[0].fields.cantidad;
           if (cantidad_stock < cantidad){
               alert("No se tiene disponible esa cantidad de producto");
               $(".agregar").prop("disabled",true);
           }else{
               $(".agregar").prop("disabled",false);
           }
        }
    });
}