

require.config({
    baseUrl: STATIC_URL + 'gadmin/js'
});


define(['text!./templates/form_field.html',
        'text!./templates/form_footer.html',
        'text!./templates/errors_popover.html',
        'text!./templates/form_title.html'],
        function(formField, formFooter, popoverTemplate, formTitle) {

    var _sync = Backbone.sync;

    Backbone.sync = function(method, model, options) {
        if (method == 'update') {
            delete model.attributes.id;
        }
        _sync.call(this, method, model, options);
    };


    Backbone.Form.setTemplates({

        form:  '<div><form class="form-horizontal">{{ fieldsets }}</form></div>',
        
        fieldset: '<fieldset>{{ fields }}</fieldset>',
        
        field: formField
    }, {
        error: 'error'
    });


    var initialize = Backbone.Form.editors.Base.prototype.initialize;

    Backbone.Form.editors.Base = Backbone.Form.editors.Base.extend({

        initialize: function(options) {
            initialize.call(this, options);

            if (this.schema.exclude) {
                delete this.model.attributes[this.key];
                this.commit = function () {};
            }
        }
    });


    var setError = Backbone.Form.Field.prototype.setError,
        render = Backbone.Form.Field.prototype.render;

    Backbone.Form.Field = Backbone.Form.Field.extend({

        setError: function(msg) {
            this.errors = this.errors || [];

            if (this.editor.hasNestedForm) return;

            if (!this.$el.hasClass(Backbone.Form.classNames.error))
                this.$el.addClass(Backbone.Form.classNames.error);

            if (!_.contains(this.errors, msg))
                this.errors.push(msg);

            this.$el.find('div.controls').popover({
                title: 'Errores',
                placement: 'left',
                html: true,
                trigger: 'hover',
                content: $(_.template(popoverTemplate)({messages: this.errors}))
            });
        },

        render: function() {
            render.call(this);
            if (this.schema.readonly)
                this.editor.$el.attr('disabled', 'disabled');
            return this;
        }
    });

    Backbone.Form.validators.errMessages.required = 'Por favor inserte un valor para este campo.';

    Backbone.Form.validators.errMessages.match = 'El valor del campo debe coincidir con el contenido del campo {{field}}';

    Backbone.Form.validators.errMessages.email = '{{value}} es una direcciÃ³n de correos invÃ¡lida.';

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

    var Form = Backbone.Form.extend({

        events: {
            'click .accept': 'commit',
            'click .cancel': function () {
                this.trigger('cancel');
            }
        },

        titleTemplate: _.template(formTitle),

        footerTemplate: _.template(formFooter),

        initialize: function(options) {
            Backbone.Form.prototype.initialize.call(this, options);
            this.title = options.title || '';
            this.oldAttributes = {};
            this.model.on('error', this.parseErrors, this);
            this.model.on('sync', this.success, this);

            for (var attr in this.model.schema)
                this.oldAttributes[attr] = this.model.get(attr);
        },

        commit: function(options) {
            if (!this.validate()) {
                this.model.save(this.getValue());
            }
        },

        parseErrors: function(model, response, options) {
            if (response.responseText) {
                try {
                    var responseText = $.parseJSON(response.responseText);
                    this.renderErrorMessages(responseText);
                } catch (error) {
                    // FIXME
                    console.log(error);
                }
            }
        },

        renderErrorMessages: function (messages) {
            for (var field in messages)
                for (var message in messages[field])
                    this.fields[field].setError(messages[field][message]);
        },

        success: function(model) {
            this.trigger('commit', this);
        },

        render: function() {
            Backbone.Form.prototype.render.call(this);
            _.each(this.fields, function(field) {
                if (field.schema.empty)
                    field.setValue();
            });
            this.$el.prepend(this.titleTemplate({title: this.title}));
            this.$el.find('form').append(this.footerTemplate());
            return this;
        }
    });

    var CreateForm = Form.extend({});

    var DeleteForm = Form.extend({

        commit: function(options) {
            this.model.destroy();
        },

        render: function() {
            Backbone.Form.prototype.render.call(this);
            this.$el.prepend(this.titleTemplate({title: this.title}));
            this.$el.find('form').append(this.footer());
            return this;
        },

        render: function() {
            this.$el.html(this.titleTemplate({title: this.title}));
            this.$el.append($('<form class="form-horizontal">').append(this.footerTemplate()));
            this.$el.find('.accept')
                .removeClass('btn-primary')
                .addClass('btn-danger');
            return this;  
        }

    });

    return {Create: CreateForm, Delete: DeleteForm};

});
