/**
 * Created by Ing. Ernesto Avilés Vázquez and Ing. Rainer Segura Peña on 14/04/14.
 */
//ui-widget ui-state-default ui-corner-all ui-button-icon-only
function ExportExcel(url_export, exportAgent)  {
    var ButtonView = Backbone.View.extend({
	    tagName: 'a',
	    className: 'ui-widget ui-state-default ui-corner-all',

	    initialize: function (options) {
	        this.title = options.title || '';
	        this.icon = options.icon || '';
            this.urlInicial  = url_export;
            this.exportAgent = exportAgent;
	        this.setUrl(url_export);

	    },

	    render: function () {
	        if (this.title)
	            this.$el.attr('title', this.title);
            this.$el.attr('target', '_blank');
	        if (this.icon) {
	            /*var icon = $('<i>');
	            icon.addClass(this.icon);*/
	            this.$el.html("<img src='"+STATIC_URL+"images/spreadsheet.gif' />");

	        }
            URL = this.$el.href;
	        return this;

	    },

	    enable: function () {
	        this.isEnabled = true;
	        this.$el.removeAttr('disabled');
	    },

	    disable: function () {
	        this.isEnabled = false;
	        this.$el.attr('disabled', true);
	    },

	    setUrl: function (url) {
	        this.$el.attr('href', url);
	    },

        events: {
            'click': function() {

                    var filter = $("#filters");
                    var input = filter.find("input");
                    var exportA = true;
                    if (this.exportAgent == null)
                        exportA = false;
                    var url = this.urlInicial;
                    var cadena = "";
                    var cont = 0;
                    for ( var i = 0; i < input.length; i++) {
                        if  (input[i].value != "") {
                            if (exportA) {
                                if (cont == 0)
                                    cadena += "?"+input[i].name+"="+input[i].value;
                                else
                                    cadena += "&"+input[i].name+"="+input[i].value;
                                cont++;
                            } else {
                                cadena += "&"+input[i].name+"="+input[i].value;
                            }
                        }


                    }
                    url+=cadena;
                    this.setUrl(url)
                }

            }


	});

	var button = new ButtonView({
	    title: gettext('Export to excel'),
	    icon: 'ui-button-icon-primary ui-icon ui-icon-calculator'

	});

    $("#toolbar").removeClass("ui-toolbar")
    $("#toolbar").addClass("ui-toolbar")
	$("#toolbar").append(button.render().$el);
}

function FilterSelect(collection, optionsValues, placeholderOptions) {

    var select = $("select").val();
    if (select != "0") {
        var divHtml= '<div id = "'+select+'" style="width : 47%; float:left;"></div>'
        var placeholder = "";
        for(var i = 0; i < optionsValues.length; i++) {
            if(optionsValues[i] == select) {
                placeholder = placeholderOptions[i];
                break;
            }
        }

        if(!$('#'+select).length){
            //var filter = ;
            $("#filters").prepend(divHtml)
            $('#'+select).append(new Backgrid.Extension.ServerSideFilter({
                    collection: collection,
                    name: select,
                    placeholder: placeholder
            }).render().$el)
        }
    }
}

function createResume(url) {
    $("#content").empty();
    $("#toolbar").remove();

    $("#content").load(url);

}

function Uricells(inventory) {
    var uriCell = Backgrid.UriCell.extend({
        render: function () {
            Backgrid.UriCell.prototype.render.call(this);
            var arreglo = document.location.href.split('/');
            arreglo.pop();
            arreglo.pop();
            arreglo.pop();
            var url = "";
            if (inventory == null)
                inventory = true;
            var id = this.$("a").attr("title");
            if(inventory)
                url += arreglo.join("/") + '/resume/?id='+id;
            else
                url += arreglo.join("/") + '/inventory/resume/?id='+id;

            this.$('a').attr('onclick', "createResume('"+url+"')");
            this.$('a').attr('href', 'javascript:void(0);');
            this.$('a').attr('target', '_self');
            return this
        }

    });

    return uriCell;
}

function Collections(model, url) {
    var collectionsView = Backbone.PageableCollection.extend({
          model: model,
          url: url,
          state: {
              pageSize: 10,
              order: 1
          },
          queryParams: {
              totalPages: null,
              totalRecords: null,
              sortKey: "sort",
              pageSize: "page_size"
        },
        // get the state from Github's search API result
        parseState: function (resp, queryParams, state, options) {
            return {totalPages: resp.count, totalRecords: resp.count * state.pageSize};
        },
        // get the actual records
        parseRecords: function (resp, options) {
            return resp.rows;
        }
    });

    return new collectionsView();
}

require.config({
    baseUrl: STATIC_URL + 'js/backbone'
});

define(['text!templates/table.html',
        'text!templates/table_item.html',
        'text!templates/pagination.html',
        'text!templates/crud_buttons.html',
        'form'],
        function(tableTemplate, itemTemplate, paginationTemplate, crudTemplate, Form) {

    var initialize = Backbone.Collection.prototype.initialize,
    parse = Backbone.Collection.prototype.parse,
    fetch = Backbone.Collection.prototype.fetch;


    var TableView = Backgrid.Grid.extend({
        tagName: 'table'

    });


    var SelectFilterView = Backbone.View.extend({
        tagName: 'select',
        initialize:function(options) {
              this.optionsValues = options.optionsFilter;
              this.placeholderOptionsFilter = options.placeholderOptionsFilter;
              this.collection = options.collection

        },
        events: {
            'change': function() {

                FilterSelect(this.collection, this.optionsValues,this.placeholderOptionsFilter)
            }
        },
        render:function() {
            this.$el.attr('id','skills')


            if(this.optionsValues)
            {
                var options = "<option value='0' selected>"+gettext('Select')+"</option>";

                for(var i=0; i < this.optionsValues.length; i++)
                {
                    options+= "<option value='"+this.optionsValues[i]+"' >"+this.placeholderOptionsFilter[i]+"</option>"
                    //title='"+this.placeholderOptionsFilter[i]+"'
                }

                this.$el.html(options)
            }
            return this
        }


    });

    var SelectComponent =   Backbone.View.extend({
       selectFilterView: SelectFilterView,
       className: "SelectComponent",
       setup:function(container) {
           this.select = new this.selectFilterView({
                optionsFilter: container.get('optionsFilter'),
                placeholderOptionsFilter: container.get('placeholderOptionsFilter'),
                collection: container.get('collection')

           })
           this.el = container.$el;

       },
       render:function(){
           if(this.select.optionsValues){

               this.el.append("<label for='skills' class='search_label'>"+gettext('Filter Search')+":</label>")
              return this.select.render().el;
           }
       }
    });

    var ButtonView = Backbone.View.extend({

        tagName: 'button',

        events: {
            'click': function() {
                if (this.isActive)
                    this.trigger('click');
            }
        },

        initialize: function(options) {
            this.title = options.title;
            this.icon = options.icon;
            this.className = options.className;
            this.isActive = options.isActive;
        },

        render: function() {
            this.$el.addClass(this.className);
            if (!this.isActive)
                this.$el.addClass('ui-button-disabled ui-state-disabled')

               // this.$el.addClass('disabled');

            if (this.title)
                this.$el.attr('title', this.title);

            if (this.icon) {
                var icon = $('<span>');
                icon.addClass(this.icon);
                this.$el.html(icon);
            }

            return this;
        }
    });

    var CRUDView = Backbone.View.extend({

        forms: {
            add: Form.Create,
            edit: Form.Create,
            remove: Form.Delete
        },

        createUpdateForm: Form.Create,
        deleteForm: Form.Delete,

        buttons: {
            add: {
                title: gettext('Add'),
                icon: 'ui-button-icon-primary ui-icon ui-icon-circle-plus',
                className: 'ui-button ui-widget ui-state-default ui-corner-all ui-button-icon-only add',
                id: 'add-button'
            },
            edit: {
                title: gettext('Change'),
                icon: 'ui-button-icon-primary ui-icon ui-icon-pencil',
                className: 'ui-button ui-widget ui-state-default ui-corner-all ui-button-icon-only edit',
                id: 'edit-button'
            },
            remove: {
                title: gettext('Delete'),
                icon: 'ui-button-icon-primary ui-icon ui-icon-trash',
                className: 'ui-button ui-widget ui-state-default ui-corner-all ui-button-icon-only remove',
                id: 'remove-button'
            }
        },

        className: 'ui-btn-group pull-right',
        //className: 'ui-btn-group',

        initialize: function(options) {
            this.collection = options.collection;
            this.model = null;
           // this.$el.attr('style', 'margin-bottom: 4px;');
            this.forms = {};
        },

        render: function() {
           // this.$el.html('');
            //$("#toolbar").html('');
             $("#add-button").remove()
            $("#edit-button").remove()
            $("#remove-button").remove()

            var flag = false;
            if (this.forms.add) {
               $("#toolbar").removeClass("ui-toolbar")
                var options = _.clone(CRUDView.prototype.buttons.add);
                _.extend(options, {isActive: true});
                var button = new ButtonView(options);
                button.on('click', this.add, this);

                //this.$el.append(button.render().el);
                $("#toolbar").append(button.render().el);
                flag = true;
            }

            _.each(["edit", "remove"], function(name) {
                if (this.forms[name]) {
                    $("#toolbar").removeClass("ui-toolbar")
                    var options = _.clone(this.buttons[name]);
                    _.extend(options, {isActive: this.model ? true : false});
                    var button = new ButtonView(options);
                    button.on('click', this[name], this);
                   // this.$el.append(button.render().el);
                    $("#toolbar").append(button.render().el);
                    flag = true;
                }

            }, this);
                if(flag)
                  $("#toolbar").addClass("ui-toolbar");
            this.delegateEvents();
            return this;
        },

        createForm: function(type, model) {
            if (!this.forms[type])
                throw _.template('There must be an {{ type }} form before to use it.')({type: type});

            var options = _.extend(
                this.forms[type],
                {model: model}
            );
            var form = new CRUDView.prototype.forms[type](options);
            this.trigger('build', form);
            form.on('commit', function() { this.trigger('commit');}, this);

            form.on('cancel', function() { this.trigger('cancel');}, this);
            return form;
        },

        add: function() {
            this.createForm('add', new this.collection.model()).on('commit', function() {
                this.trigger('created');
            }, this);
        },

        edit: function() {
            this.createForm('edit', this.model);
        },

        remove: function() {
            this.createForm('remove', this.model);
        },

        addForm: function(type, title, schema) {
            this.forms[type] = {
                title: title,
                schema: schema
            };
        }
    });


    var TableComponent = Backbone.View.extend({

        tableView: TableView,
        setup: function(container) {


            this.table = new this.tableView({
                collection: container.get('collection'),
                columns: container.get('columns')


            });
            this.el = container.$el;
            this.pagination = new Backgrid.Extension.Paginator({
               collection: container.get('collection')
            })
           /* this.table.on('selected', function(models) {
                this.trigger('selected', models);
            }, this);*/
            if (!container.get('collection').length) {
                var self = this;
                $(function() {
                    container.get('collection').fetch({success: function() {
                        self.el.append("<div id='filters'></div>")
                        self.el.append(self.table.render().$el);
                        self.el.append(self.pagination.render().$el);
                    }});
                });
            }

        },

        render: function() {

            return this.table.render().el;
        }

    });

    var CRUDComponent = Backbone.View.extend({

        crudView: CRUDView,
        tableView: TableView,
       // collections: Collections,
        setup: function(container) {
            this.crud = new this.crudView({
                collection: container.get('collectionCrud')
            });




            this.table = new this.tableView({
                collection: container.get('collection'),
                columns: container.get('columns')

            });
            this.crud.on('build', function(form) {
                    //container.$el.html(form.render().el);
                    var $_dialog = $("#dialog-form");
                    $_dialog.dialog({
                                                resizable: false,
                                                autoOpen: false,
                                                title: form.title,
                                                modal: true,
                                                closeOnEscape: false,
                                                width: 500,
                                                maxHeight: 550,
                                                close:function(){
                                                    $("#dialog-form").empty();
                                                    $("#dialog-form").dialog('destroy');
                                                }


                                            });
                    $_dialog.append(form.render().el);
                    $_dialog.dialog("open");
                }, this);
            this.crud.on('cancel', function() {

                var col =  container.get('collection');
                col.fetch();

                 $("#dialog-form").empty();
                 $("#dialog-form").dialog('destroy');
                 this.crud.model = null;
                 this.crud.render();

            }, this);
            this.crud.on('commit create', function() {
                    container.get('collectionCrud').fetch({success: function() {
                    //container.render();
                     $("#messagesCrud").removeClass('msg-success msg');
                     $('#messagesCrud').addClass('msg-success msg')
                                        .html('<div class="msg-content msg-content-success">'+gettext('The operation was performed successfully')+'.</div>');
                     $('#messagesCrud').show().fadeOut(10000);
                      var col =  container.get('collection');
                      col.fetch();

                   $("#dialog-form").empty();
                   $("#dialog-form").dialog('destroy');
                   this.crud.model = null;
                   this.crud.render();
               }});
            }, this);

            this.table.collection.on('backgrid:selected', function(model, selected) {
                       //$('#edit').button( "option", "disabled", false );
                    var table = container.get('table');
                    var models = table.table.collection.models;
                    var rowSeleted = new Array();
                    var i = 0;
                    $(".backgrid tbody tr").each(function(index){
                        var tr = arguments[1]
                        if(tr.className == "selected") {
                            rowSeleted[i] = index;
                            i++;
                        }
                    });

                    var arrSelectedModels = new Array();
                    for(var i = 0; i < rowSeleted.length; i++)
                        arrSelectedModels[i] = models[rowSeleted[i]]

                    if(arrSelectedModels.length == 1) {
                        this.crud.model = arrSelectedModels[0];
                    } else {
                        this.crud.model = null;
                    }
                    this.crud.render();

            },this);

        },

        render: function() {
            return this.crud.render().el;
        },

        addForm: function(type, title, schema) {
            this.crud.addForm(type, title, schema);
        }
    });

    var ContainerView = Backbone.View.extend({

        initialize: function(options) {
            Backbone.View.prototype.initialize.call(this, options);
            this.components = options.components || {};
            this.setup();
        },

        setup: function() {
            _.each(this.components, function(component) {
                if(component)
                    if (component.setup)
                        component.setup(this);
            }, this);


        },

        render: function() {
            this.$el.html('');

            _.each(this.components, function(component) {
                if(component) {
                    var className = component.className;
                    if (component.render)
                    {

                            this.$el.append(component.render());
                    }
                }
            }, this);
             $("#skills").combobox();
            return this;
        },

        get: function(name) {
            if (_.has(this.components, name))
                return this.components[name];
            throw _.template('Component {{ name }} is not registered in this ContainerView')({name: name});
        }
    });

    var CRUDContainerView = ContainerView.extend({

        initialize: function(options) {
            options = _.extend(options, {
                components: {
                    collection: Collections(options.model, options.url),
                    crud: new CRUDComponent,
                    select: new SelectComponent,
                    table: new TableComponent,
                    columns: options.columns,
                    collectionCrud: options.collectionCrud,
                    optionsFilter: options.optionsFilter,
                    placeholderOptionsFilter: options.placeholderOptionsFilter

                }
            });
            ContainerView.prototype.initialize.call(this, options);

        }
    });

    return {

            ContainerView: ContainerView,
            TableComponent: TableComponent,
            CRUDComponent: CRUDComponent,
            CRUDContainerView: CRUDContainerView,
            SelectComponent: SelectComponent,
            TableView: TableView

    };
});

