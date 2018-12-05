 var initialize = Backbone.Form.editors.Base.prototype.initialize;




    var setError = Backbone.Form.Field.prototype.setError,
        render = Backbone.Form.Field.prototype.render;



    Backbone.Form.validators.errMessages.required = 'Por favor inserte un valor para este campo.';

    Backbone.Form.validators.errMessages.match = 'El valor del campo debe coincidir con el contenido del campo {{field}}';

    Backbone.Form.validators.errMessages.email = '{{value}} es una dirección de correos inválida.';

    var renderOptions = Backbone.Form.editors.Select.prototype.renderOptions;

    Backbone.Form.editors.Select = Backbone.Form.editors.Select.extend({

        renderOptions: function(options) {
            renderOptions.call(this, options);
            if (!(this instanceof Backbone.Form.editors.SelectMultiple)) {
                this.$el.prepend($('<option>'));
            }
            return this;
        }
    });

    Backbone.Form.editors.SelectMultiple = Backbone.Form.editors.Select.extend({
        initialize: function(options) {
            Backbone.Form.editors.Select.prototype.initialize.call(this, options);
            this.$el.attr('multiple', true);
        },

        setValue: function(value) {
            if (_.isArray(value))
                value = _.map(value, function(val) {
                    return _.isObject(val) ? val.id : val;
                });
            this.$el.val(value);
        },

        getValue: function() {
            return _.map(this.$el.val(), function(val) { return parseInt(val);});
        }
    });
