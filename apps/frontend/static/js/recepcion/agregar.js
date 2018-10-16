$(document).ready(function() {
    var select_marca_vehiculo = $('#id_marca_vehiculo_select');
    var select_modelo_vehiculo = $('#id_modelo_vehiculo_select');
    inicializarSelectGenerales();

    function inicializarSelectGenerales() {
        select_marca_vehiculo.select2({
            tags: true,
            multiple: false,
            tokenSeparators: [','],
            allowClear: true,
            placeholder: "Seleccione la marca del vehiculo",
            ajax: {
                url: '/sismec/ajax/marca_vehiculo_autocomplete/',
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
                select_marca_vehiculo.find('option').remove().end();
                select_marca_vehiculo.val('').trigger('change');
            });

        select_modelo_vehiculo.select2({
            tags: true,
            multiple: false,
            tokenSeparators: [','],
            allowClear: true,
            placeholder: "Seleccione el modelo del vehiculo",
            ajax: {
                url: '/sismec/ajax/modelo_vehiculo_autocomplete/',
                dataType: "json",
                type: "GET",
                data: function (params) {
                    var queryParameters = {
                        descripcion  : params.term,
                        marca: $('#id_marca_vehiculo_select').val()
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
                select_modelo_vehiculo.find('option').remove().end();
                select_modelo_vehiculo.val('').trigger('change');
            });
    }
    var anho = $('#año').val();
    anho.oninput = function () {
    if (this.value.length > 4) {
        this.value = this.value.slice(0,4);
    }
}
});