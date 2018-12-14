item_detalle_pedido = '<div class="item-detalle">'
            + '<input type="text" class="id_detalle col-xs-2" id="id_detalle" name="id_detalle_item" disabled value="0">'
			+ '<input type="text" class="producto_desc col-xs-4" id="id_producto_select" name="id_producto_select" disabled>'
            + '<input type="number" class= "cantidad-item item col-xs-2" placeholder="Cantidad" value="" style="left: 5px;">'
            + '<input type="text" class= "monto-item item col-xs-2" placeholder="Precio de Compra" value="" style="left: 5px;">'
			+ '<a href="#" class="btn btn-sm btn-danger rm-btn" style="height: 35px;margin-left: 10px;"><span class="glyphicon glyphicon-minus"></span></a>'
		    + ' <br><br></div>';
var detalle_valido = true;
var es_repetido = false;
$(document).ready(function() {
    var select_proveedor = $('#id_proveedor_select');
    var select_producto = $('#id_producto_agregar');
    var idsum= 1;
    var estado_compra = $('#estado_cabecera').val();
    $('#condicion_compra').val(estado_compra).change();
    $(".monto-item").each(function() {
        console.log($(this).val());
        $(this).val(formatearNumeros_convalor($(this).val()));
        console.log(formatearNumeros_convalor($(this).val()))
    });

    $('#condicion_compra').on('change', function () {
        if ($('#condicion_compra').val() == "ANULADO") {
            $(".motivo_anulacion").removeClass("ocultar");
        }else{
            $(".motivo_anulacion").addClass("ocultar");
        }

    });
    inicializarSelectGenerales();
    function inicializarSelectGenerales() {
        select_proveedor.select2({
            tags: true,
            multiple: false,
            tokenSeparators: [','],
            allowClear: true,
            placeholder: "Seleccione el nombre del proveedor",
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
                select_proveedor.find('option').remove().end();
                select_proveedor.val('').trigger('change');
            });
        select_producto.select2({
            tags: true,
            multiple: false,
            tokenSeparators: [','],
            allowClear: true,
            placeholder: "Seleccione el nombre del producto",
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
            .on('select2:unselect ', function () {
                select_producto.find('option').remove().end();
                select_producto.val('').trigger('change');
            });
    }
    $('#presupuesto').on('change', function () {
	var files = $('#presupuesto').prop('files');
	console.log('validando path');
	console.log(files)
	var path = ""
	if (files.length > 0) {
		console.log("prueba");
	    var reader = new FileReader();
	    reader.readAsDataURL(files[0]);
	    reader.onload = function () {
		   console.log(reader.result);
		   path = reader.result;
		   console.log(path)
		   $('#presupuesto_path').val(path)
		};
	}
    });
    //para agregar un item
    $(".agregar").click(function () {
        es_repetido = itemRepetidos();
        if (es_repetido == false){
           $('.detalle_pedido').append(item_detalle_pedido);
            index = $('.item-detalle').length;
            var inputs= $('.item-detalle')[index -1].children
            descripcion = $('#id_producto_agregar :selected').text();
            cantidad_item = $('#cantidad').val();
            inputs[0].value=0;
            inputs[1].value=descripcion;
            inputs[2].value=cantidad_item;
            select_producto.find('option').remove().end();
            select_producto.val('').trigger('change');
            $('#cantidad').val('1');
            idsum +=1;
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

    function validarCabecera(){
        console.log('validando cabecera');
        if ($("#fecha").val() == ""){
            alert("Debe seleccionar una fecha valida");
            return false;
        }
        if ($("#id_proveedor_select").val() == null){
            alert("Debe seleccionar un proveedor valido");
            return false;
        }
        return true;
    }
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


function validarDetalle(){

	console.log('validando');
	detalle_valido = true;
	var len = $('.item-detalle').length;
	$(".item-detalle").each(function(index, element ){
	    id_detalle = $(this).find(".id_detalle").val();
		cantidad = $(this).find(".cantidad-item").val();
		cantidad = parseInt(cantidad) || 0;
		concepto = $(this).find(".producto_desc").val();
		monto = $(this).find(".monto-item").val();
		monto = monto.split('.').join('');
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



function generarDetalleJSON(){
		detalle_json = '';
		objeto = {};
		$(".item-detalle").each(function(index, element ){
			// Agregamos el elemento mas externo
			i = index + 1;
			//Se obtienen los datos.
            id_detalle = $(this).find(".id_detalle").val();
            descripcion = $(this).find(".producto_desc").val();
			cantidad = $(this).find(".cantidad-item").val();
			monto = $(this).find(".monto-item").val();
			monto = monto.replace(".","");
		    monto = parseInt(monto) || 0;

			key = 'item' + i;
			value = {id_detalle : id_detalle, descripcion : descripcion, cantidad : cantidad , monto : monto};
			objeto[key] = value;
			JSON.stringify(objeto);

		});

		detalle_json = JSON.stringify(objeto);
		return detalle_json;
}

function getBase64(file) {

   reader.onload = function () {
     console.log(reader.result);


   };
   reader.onerror = function (error) {
     console.log('Error: ', error);
     return error;
   };

    return reader.result;
}