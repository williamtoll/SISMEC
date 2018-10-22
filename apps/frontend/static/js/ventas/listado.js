$(document).ready(function() {
    var select_recepcion = $('#id_codigo_select');
    inicializarSelectGenerales();
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
            });
    }
});