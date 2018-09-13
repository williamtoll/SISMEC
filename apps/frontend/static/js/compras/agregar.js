item_inicial_detalle_pedido = '<div class="item-detalle">'
			+ '<input type="text" class="producto_desc col-xs-4" id="id_producto_select" name="id_producto_select" value="">'
            + '<input type="number" class= "cantidad-item item col-xs-2" placeholder="Cantidad" value="">'
		    + '<br> <br><br></div> ';


item_detalle_pedido = '<div class="item-detalle">'
			+ '<input type="text" class="producto_desc col-xs-4" id="id_producto_select" name="id_producto_select">'
            + '<input type="number" class= "cantidad-item item col-xs-2" placeholder="Cantidad" value="" style="left: 5px;">'
			+ '<a href="#" class="btn btn-sm btn-danger rm-btn" style="height: 35px;margin-left: 10px;"><span class="glyphicon glyphicon-minus"></span></a>'
		    + ' <br><br></div>';
var detalle_valido = true;
$(document).ready(function() {
    $('.detalle_pedido').append(item_inicial_detalle_pedido);
    var select_proveedor = $('#id_proveedor_select');
    var select_producto = $('#id_producto_agregar')
    inicializarSelectGenerales();
    var idsum= 1;
    var index = 0;
    var descripcion;
    var ok=false;
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

    //para agregar un item
    $(".agregar").click(function () {
        if(idsum == 1 && ok == false){
            index = $('.item-detalle').length;
            var inputs= $('.item-detalle')[index -1].children
            descripcion = $('#id_producto_agregar :selected').text();
            inputs[0].value=descripcion;
            ok=true;
        }else{
            $('.detalle_pedido').append(item_detalle_pedido);
            index = $('.item-detalle').length;
            var inputs= $('.item-detalle')[index -1].children
            descripcion = $('#id_producto_agregar :selected').text();
            inputs[0].value=descripcion;
            idsum +=1;
        }

    });
    // Para eliminar un item.
		$('.detalle_pedido').on("click",".rm-btn", function(e){
        	e.preventDefault();
        	$(this).parent('div').remove();
    	});

        // // Control del SUBMIT del FORM
    	$("#form_add_oc").submit(function(){

			//1. TODO: Hacer chequeo de que todos los valores esten correctos.
			if (formOk()){
			    validarDetalle();
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
function generarDetalleJSON(){
		detalle_json = '';
		objeto = {};
		$(".item-detalle").each(function(index, element ){
			// Agregamos el elemento mas externo
			i = index + 1;
			//Se obtienen los datos.
            descripcion = $(this).find(".producto_desc").val();
			cantidad = $(this).find(".cantidad-item").val();

			key = 'item' + i;
			value = {descripcion : descripcion, cantidad : cantidad};
			objeto[key] = value;
			JSON.stringify(objeto);

		});

		detalle_json = JSON.stringify(objeto);
		return detalle_json;
	}

function formOk(){
		// Realizar validaciones.
		if (detalle_valido){
			return true;
		}
		else {
			alert('Detalle de factura incorrecto, por favor corrija y vuelva a enviar');
		}
	}

function validarDetalle(){

	console.log('validando');
	detalle_valido = true;
	var len = $('.item-detalle').length;
	$(".item-detalle").each(function(index, element ){
		cantidad = $(this).find(".cantidad-item").val();
		cantidad = parseInt(cantidad) || 0;
		concepto = $(this).find(".producto_desc").val();
		indicador_validez = '#840A0A'; // Por defecto invalido (Rojo)
		// Requerimieno minimo para un detalle valido
		if (cantidad != 0){
				// VALIDO
				console.log('Detalle VALIDO');
				indicador_validez = '#1C842D';
		}
		else{
			detalle_valido = false;
		}
		$(this).css('background',indicador_validez);
	});
}