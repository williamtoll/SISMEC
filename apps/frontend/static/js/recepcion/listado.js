$(document).ready(function() {
    var select_cliente = $('#id_cliente_select');
    inicializarSelectGenerales();

    function inicializarSelectGenerales() {
        select_cliente.select2({
            tags: true,
            multiple: false,
            tokenSeparators: [','],
            allowClear: true,
            placeholder: "Seleccione el nombre del cliente",
            ajax: {
                url: '/sismec/ajax/getClienteAutocomplete/',
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
            select_cliente.find('option').remove().end();
            select_cliente.val('').trigger('change');
        });
    }
});