/**
 * @author Ing. Rainer Segura Peña and Ing. Ernesto Aviles
 */

require.config({
    baseUrl: STATIC_URL + 'js/backbone'
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

        form:  '<div><form id="form-dialog" enctype="multipart/form-data" class="form-horizontal">{{ fieldsets }}<div id="error-message-form"></div></form>',
        
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

            //this.errors = this.errors || [];
            this.errors = []
            if (this.editor.hasNestedForm) return;

            if (!this.$el.hasClass(Backbone.Form.classNames.error))
                this.$el.addClass(Backbone.Form.classNames.error);
                //this.$el.removeClass(Backbone.Form.classNames.error);


            if (!_.contains(this.errors, msg))
                this.errors.push(msg);
            //this.$el.find('div.controls').popover('destroy');
            this.$el.find('div.controls').popover({
                //title: 'Error',
                //placement: 'rig',
                html: true,
                //delay: 1,
                //container: true,
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

    Backbone.Form.validators.errMessages.required = gettext('Please insert a value for this field')+'.';

    Backbone.Form.validators.errMessages.match = gettext('The field value must match the contents of the previous field')+'.';

    Backbone.Form.validators.errMessages.email = '{{value}} '+gettext('is an invalid e-mails')+'.';
    
    Backbone.Form.validators.errMessages.letters = gettext('Only letters are accepted in this field')+'.';

    Backbone.Form.validators.errMessages.number = gettext('Enter a whole number')+'.';

    Backbone.Form.validators.errMessages.required_select = gettext('Please select a value for this field')+'.';

    var renderOptions = Backbone.Form.editors.Select.prototype.renderOptions;

    Backbone.Form.editors.Select = Backbone.Form.editors.Select.extend({
        initialize: function(options) {
            Form.editors.Base.prototype.initialize.call(this, options);

//            if (!(this instanceof Backbone.Form.editors.SelectMultiple)) {
//                if (options.model && !options.model.attributes.id)
//                    this.$el.prepend('<option value="" selected="selected">---'+gettext("Select")+'---</option>');
//            }
        },
        renderOptions: function(options) {
            renderOptions.call(this, options);
            if (!(this instanceof Backbone.Form.editors.SelectMultiple)) {
                var option = '<option value="" selected="selected">---'+gettext("Select")+'---</option>';
                if(this.model.id)
                    option = '<option value="">---'+gettext("Select")+'---</option>';
                this.$el.prepend(option);
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
            return _.map(this.$el.val(), function(val) { return val;});
        }
    });

    Backbone.Form.editors.Datepicker = Backbone.Form.editors.Text.extend({
        initialize: function(options) {
            Form.editors.Base.prototype.initialize.call(this, options);
            this.$el.datetimepicker({
                dateFormat: 'yy-mm-dd',
                timeFormat: 'HH:mm:ss'
            });

        }
    });

    Backbone.Form.editors.File = Backbone.Form.editors.Text.extend({

        initialize: function(options) {
            Form.editors.Base.prototype.initialize.call(this, options);
            this.$el.attr('type', 'file');
        }
    });

    Backbone.Form.editors.SelectDragDrop = Backbone.Form.editors.Base.extend({

    tagName: 'div',

    events: {
      'change': function(event) {
        this.trigger('change', this);
      },
      'focus':  function(event) {
        this.trigger('focus', this);
      },
      'blur':   function(event) {
        this.trigger('blur', this);
      }
    },

    initialize: function(options) {
      Backbone.Form.editors.Base.prototype.initialize.call(this, options);

      if (!this.schema || !this.schema.options) throw "Missing required 'schema.options'";
    },

    render: function() {
     //

      this.setOptions(this.schema.options);

      return this;
    },

    /**
     * Sets the options that populate the <select>
     *
     * @param {Mixed} options
     */
    setOptions: function(options) {
      var self = this;

      //If a collection was passed, check if it needs fetching



          if (options instanceof Backbone.Collection) {
            var collection = options;

            //Don't do the fetch if it's already populated
            if (collection.length > 0) {
              this.renderOptions(options);
            } else {
              collection.fetch({
                success: function(collection) {
                  self.renderOptions(options);
                }
              });
            }
          }

          //If a function was passed, run it to get the options
          else if (_.isFunction(options)) {
            options(function(result) {
              self.renderOptions(result);
            });
          }

          //Otherwise, ready to go straight to renderOptions
          else {

            this.renderOptions(options);
          }

    },

    /**
     * Adds the <option> html to the DOM
     * @param {Mixed}   Options as a simple array e.g. ['option1', 'option2']
     *                      or as an array of objects e.g. [{val: 543, label: 'Title for object 543'}]
     *                      or as a string of <option> HTML to insert into the <select>
     */
    renderOptions: function(options) {
      var $select = this.$el,
          html;

      var self = this
      //Accept string of HTML
      if (_.isString(options)) {
        html = options;
      }

      //Or array
      else if (_.isArray(options)) {
        var flag = true

        if (options[0] instanceof Backbone.Collection) {
            var collection = options[0];
           /* if (collection.length > 0) {
              html = this._collectionToHtml([collection,0]);

              html += this._arrayToHtml([options[1],1]);
              $select.html(html);
              this.setValue(this.value);

            } else {*/
              collection.fetch({
                success: function(collection) {
                  html = self._collectionToHtml([collection,0]);
                  if (options[1] instanceof Backbone.Collection) {
                        var collection = options[1];
                        if (collection.length > 0) {
                          html.push(self._collectionToHtml([collection,1]));
                        } else {
                          collection.fetch({
                            success: function(collection) {
                              html += self._collectionToHtml([collection,1]);
                              $select.html(html);

                              self.setValue(self.value);
                            }
                          });
                        }
                  } else {
                      html += self._arrayToHtml([options[1],1]);
                      $select.html(html);

                      self.setValue(self.value);
                  }
                  //$select.html(html);
                }
              });




          }

      }

      //Or Backbone collection
      else if (options instanceof Backbone.Collection) {
        html = this._collectionToHtml(options);
      }

      //Insert options
      $select.html(html);

      //Select correct option
      //this.setValue(this.value);
    },

    getValue: function() {
      var arrElements = [];
      var div = $('#destinationFields')[0];
      var node = div.childNodes;
      for (var i = 0; i < node.length; i++)
           arrElements[i] = node[i].id;

      return _.map(arrElements, function(val) { return val;});
    },

    setValue: function(value) {
      if (_.isArray(value)) {

          var divSourceFields = '';
          if ($('#sourceFields') > 0) {
              divSourceFields = $('#sourceFields').childNodes;
          } else {
              divSourceFields = this.$el[0].childNodes[0].childNodes[0].childNodes;
          }

          var element = [];
          for(var i = 0; i < value.length; i++) {
              var id = value[i].toString();
              for (var j = 0; j < divSourceFields.length; j++) {
                    var idSourceFields = divSourceFields[j].id
                    if (idSourceFields == id) {
                        element.push(divSourceFields[j]);
                        if ($('#sourceFields') > 0) {
                            $('#sourceFields').childNodes[j].remove();
                        } else {
                            this.$el[0].childNodes[0].childNodes[0].childNodes[j].remove();
                        }

                    }

              }
          }
          for (var i = 0; i < element.length; i++) {
             if ($('#destinationFields') > 0) {
                            $('#destinationFields').append(element[i]);
             } else {
                 this.$el[0].childNodes[0].childNodes[1].appendChild(element[i]);
             }

          }

      }

    },

    focus: function() {
      if (this.hasFocus) return;

      this.$el.focus();
    },

    blur: function() {
      if (!this.hasFocus) return;

      this.$el.blur();
    },


    _collectionToHtml: function(collect) {
      //Convert collection to array first
      var array = [];
      var collection =  collect[0]
      collection.each(function(model) {
        array.push({ val: model.id, label: model.toString() });
      });

      //Now convert to HTML
      var html = this._arrayToHtml([array, collect[1]]);

      return html;
    },


    _arrayToHtml: function(arra) {
      var html = [];

      //Generate HTML
      var array = arra[0];
      var pos = arra[1];
        if (pos == 0) {
            html.push('<div id="fieldChooser" tabIndex="1"><div id="sourceFields">')
        } else {
            html.push('<div id="destinationFields">')
        }

      _.each(array, function(option) {

        if (_.isObject(option)) {


          var val = (option.val || option.val === 0) ? option.val : '';
          html.push('<div id="'+val+'">'+option.label+'</div>');
        }
        else {
          html.push('<div>'+option+'</div>');
        }

      });
      html.push('</div>')
      if(pos == 1) {
          html.push('</div><script>$(document).ready(function () {   var $sourceFields = $("#sourceFields"); var $destinationFields = $("#destinationFields"); var $chooser = $("#fieldChooser").fieldChooser(sourceFields, destinationFields); }); </script>')
      }

      return html.join('');
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

            for (var attr in this.model.schema) {
                var oldsplit = attr.split("_");
                this.oldAttributes[attr] = this.model.get(attr);
                this.oldAttributes[oldsplit[0]] = this.model.get(oldsplit[0]);
            }

        },

        commit: function(options) {
            $('.controls').popover('destroy');
            if (!this.validate()) {
                var flag = true;
                var values = this.getValue();

                if (this.model.id) {
                    var oldAttributes = this.oldAttributes;
                    var cont = 0;
                    for (var val in values) {
                        var val1 = values[val];
                        var val2 = oldAttributes[val];

                        if (typeof val1 == "object" && typeof val2 == "object") {
                            var cont1 = 0;
                            for (var i in val1) {
                                var flag1 = true;
                                for (var j in val2) {
                                      if (typeof val2[j] == "object") {
                                          for (var v in val2[j]) {
                                              if (typeof val2[j][v] == "object") {
                                                  for (var z in val2[j][v]) {
                                                      if (String(val1[i]) === String(val2[j][v][z])) {
                                                          flag1 = false;
                                                          cont1++;
                                                          break;
                                                      }
                                                  }
                                                  if (!flag1)
                                                        break;
                                              } else {
                                                  if (String(val1[i]) === String(val2[j][v])) {
                                                       flag1 = false;
                                                       cont1++;
                                                       break;
                                                  }
                                              }
                                          }
                                      }
                                      else if (String(val1[i]) === String(val2[j])) {
                                        flag1 = false;
                                        cont1++;
                                        break;
                                    }
                                }
                                if (flag1)
                                    break;
                            }

                            if (cont1 != 0 && cont1 == val2.length)
                                cont++;
                        } else {
                            if (String(val1) == String(val2))
                                cont++;
                        }

                    }
                    var contAux = 0;

                    for (var v in values )
                       contAux++;
                    if (contAux == cont)
                        flag = false;

                }

                if (flag)
                    this.model.save(values);
                else {
                    $("#error-message-form").removeClass('msg-error msg');
                    $('#error-message-form').addClass('msg-error msg')
                                        .html("<div class='msg-content msg-content-error'>"+gettext('There have been no changes')+".</div>");
                }

            }
        },

        parseErrors: function(model, response, options) {

            if (response.responseText) {
                try {
                    var responseText = $.parseJSON(response.responseText);
                    this.renderErrorMessages(responseText);
                } catch (error) {
                    // FIXME

                    var responseText = $.parseJSON(response.responseText);
                    var messageError = 'Error';
                    if (typeof responseText.__all__ != "undefined") {
                        messageError = responseText.__all__[0]
                    }
                    else if (typeof responseText.non_field_errors != "undefined") {
                        messageError = responseText.non_field_errors[0]
                    }

                    $("#error-message-form").removeClass('msg-error msg');
                    $('#error-message-form').addClass('msg-error msg')
                                        .html("<div class='msg-content msg-content-error'>"+gettext(messageError)+".</div>");
                    //$('#error-message-form').show().fadeOut(10000);

                }
            }
        },

        renderErrorMessages: function (messages) {
            for (var field in messages)
                for (var message in messages[field])
                    this.fields[field].setError(gettext(messages[field][message])+'.');
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
        events: {
            'click .accept': function() {
                if (!$('#a-accept').hasClass('ui-state-disabled'))
                    this.model.destroy();
            },
            'click .cancel': function () {
                this.trigger('cancel');
            }
        },
        commit: function(options) {
            this.model.destroy();
        },
        parseErrors: function(model, response, options) {

            if (response.responseText) {
                try {
                    var responseText = $.parseJSON(response.responseText);
                    this.renderErrorMessages(responseText);
                } catch (error) {


                    var responseText = $.parseJSON(response.responseText);
                    var messageError = 'Error';
                    if (typeof responseText.__all__ != "undefined") {
                        messageError = responseText.__all__[0]
                    }
                    else if (typeof responseText.non_field_errors != "undefined") {
                        messageError = responseText.non_field_errors[0]
                    }

                    $("#error-message-form").removeClass('msg-error msg');
                    $('#error-message-form').addClass('msg-error msg')
                                        .html("<div class='msg-content msg-content-error'>"+gettext(messageError)+".</div>");
                    $('#a-accept').addClass('ui-state-disabled');

                }
            }
        },

        render: function() {
            Backbone.Form.prototype.render.call(this);
            this.$el.prepend(this.titleTemplate({title: this.title}));
            this.$el.append('<div id="error-message-form"></div>');
            this.$el.find('form').append(this.footer());
            return this;
        },

        render: function() {
            this.$el.html(this.titleTemplate({title: this.title}));
            console.log(this)
            this.$el.append($('<form id="form-dialog" enctype="multipart/form-data" class="form-horizontal">').append('<div id="error-message-form"></div>').append(this.footerTemplate()));
            this.$el.find('.accept')
                .removeClass('btn-primary')
                .addClass('btn-danger');
            return this;  
        }

    });

    return {Create: CreateForm, Delete: DeleteForm};

});
