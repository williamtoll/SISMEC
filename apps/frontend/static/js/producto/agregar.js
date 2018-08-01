$(document).ready(function() {
    var select_tipo_producto = $('#id_tipo_producto_select');
    inicializarSelectGenerales();

    function inicializarSelectGenerales() {
        select_tipo_producto.select2({
            tags: true,
            multiple: false,
            tokenSeparators: [','],
            allowClear: true,
            placeholder: "Seleccione el nombre del tipo de producto",
            ajax: {
                url: '/sismec/ajax/tipo_producto_autocomplete/',
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
                                text: item.nombre,
                                id: item.id
                            };
                        })
                    };
                }
            }
        })
            .on('select2:unselect ', function () {
                select_tipo_producto.find('option').remove().end();
                select_tipo_producto.val('').trigger('change');
            });
    }
});