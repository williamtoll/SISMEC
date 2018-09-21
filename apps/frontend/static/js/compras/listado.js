$(document).ready(function() {
    var select_proveedor = $('#id_proveedor_select');
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
    }
});
