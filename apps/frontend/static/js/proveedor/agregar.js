$(document).ready(function() {
    var select_proveedor = $('#id_proveedor_select');
    inicializarSelectGenerales();

    function inicializarSelectGenerales() {
        select_proveedor.select2({
            tags: true,
            multiple: false,
            tokenSeparators: [','],
            allowClear: true,
            placeholder: "Seleccione el nombre del Proveedor",
            ajax: {
                url: '/sismec/ajax/proveedor_autocomplete/',
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