/**
 * Created by Ing. Rainer Segura Peña on 14/04/14.
 * @author Ing. Rainer Segura Peña and Ing. Ernesto Aviles
 */

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
              this.patternOptionsFilter = options.patternOptionsFilter,
              this.typeDataOptions = options.typeDataOptions,
              this.collection = options.collection

        },
        events: {
            'change': function() {

                FilterSelect(this.collection, this.optionsValues,this.placeholderOptionsFilter,this.patternOptionsFilter, this.typeDataOptions)
            }
        },
        render:function() {
            this.$el.attr('id','skills')


            if(this.optionsValues)
            {
                var options = "<option value='' selected>---"+gettext('Select')+"---</option>";
                   for (var element in this.optionsValues) {
                       options+= "<option value='"+element+"' >"+this.optionsValues[element]+"</option>"
                   }
//                for(var i=0; i < this.optionsValues.length; i++)
//                {
//                    options+= "<option value='"+this.optionsValues[i]+"' >"+this.placeholderOptionsFilter[i]+"</option>"
//                    //title='"+this.placeholderOptionsFilter[i]+"'
//                }

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
                patternOptionsFilter: container.get('patternOptionsFilter'),
                typeDataOptions: container.get('typeDataOptions'),
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
            change: Form.Create,
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
            },
            change: {
                title: gettext('Change Password'),
                icon: 'ui-button-icon-primary ui-icon ui-icon-circle-check',
                className: 'ui-button ui-widget ui-state-default ui-corner-all ui-button-icon-only change',
                id: 'change-button'
            }
        },

        className: 'ui-btn-group pull-right',
        //className: 'ui-btn-group',

        initialize: function(options) {
            this.collection = options.collection;
            this.collectionGrid = options.collectionGrid;
            this.model = null;
            this.desactivateButton = options.desactivateButton;
           // this.$el.attr('style', 'margin-bottom: 4px;');
            this.forms = {};
        },

        render: function() {

            $("#add-button").remove()
            $("#edit-button").remove()
            $("#change-button").remove()
            $("#remove-button").remove()

            var flag = false;
            if (this.forms.add) {
               $("#toolbar").removeClass("ui-toolbar")
                var options = _.clone(CRUDView.prototype.buttons.add);
                if(this.desactivateButton) {
                  _.extend(options, {isActive: this.collectionGrid.length ? false : true});
                } else {
                    _.extend(options, {isActive: true});
                }
                var button = new ButtonView(options);
                button.on('click', this.add, this);
                $("#toolbar").append(button.render().el);
                flag = true;
            }

            _.each(["edit", "remove", "change"], function(name) {
                if (this.forms[name]) {
                    $("#toolbar").removeClass("ui-toolbar")
                    var options = _.clone(this.buttons[name]);
                    _.extend(options, {isActive: this.model ? true : false});
                    var button = new ButtonView(options);
                    button.on('click', this[name], this);
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

        change: function() {
            this.createForm('change', this.model);
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

        setup: function(container) {

            this.el = container.$el;

            if (!container.get('collection').length) {
                var self = this;

                $(function() {


                    container.get('collection').fetch({data:{order:'asc', sort: 'id'},success: function() {


                        var tableid = 'grid';
                        if (container.get('tableid'))
                            tableid = container.get('tableid')


                        var paginationid = 'paginacion';
                        if (container.get('paginationid'))
                            paginationid = container.get('paginationid');

                        self.el.append("<div id='filters'></div>");
                        self.el.append('<table id="'+tableid+'"></table>');
                        self.el.append('<div id="'+paginationid+'"> </div>');

                        var width = 770;
                        if(screen.width <= 1366 && screen.width > 1024)
                            width = 1100
                        if(container.get('tablewidth'))
                            width = container.get('tablewidth')
                        var multiselect = false;
                        if(container.get('multiselect'))
                            multiselect = true;
                       var grid =  jQuery("#"+tableid);
                       grid.jqGrid({
                                    //url: container.get('url'),
                                    //data: models.toJson(),
                                    //datatype: 'json',
                                    //mtype: container.get('mtype'),
                                    datatype: 'local',
                                    width: width,
                                    height: 250,
                                    colNames: container.get('colNames'),
                                    colModel: container.get('colModel'),
                                    pager: '#'+paginationid,
                                    rowNum:10,
                                    rowList:[10,25,50],
                                    sortname: 'id',
                                    sortorder: 'asc',
                                    viewrecords: true,
                                    multiselect: multiselect,
                                    postData: {
                                        csrfmiddlewaretoken: $.cookie('csrftoken')
                                        },
                                    onSelectRow: function(id){
                                         var colletion = container.get('collection');
                                         var models = colletion.models;
                                         var childNodes = $("#"+id).get(0).childNodes;
                                         var idElement = null;
                                         var aria_describedby = null;
                                         for (var i = 0; i < childNodes.length; i++) {

                                             aria_describedby = $(childNodes[i]).attr('aria-describedby').split(tableid+"_");
                                             if (aria_describedby[1] == 'id') {
                                                idElement = $(childNodes[i]).attr('title');
                                                break;
                                             }

                                         }
                                         var model = null;
                                         if(container.get('multiselect')) {
                                             model = grid.jqGrid('getGridParam','selarrrow');
                                         } else {
                                             for (var i = 0; i < models.length; i++) {
                                                 if(models[i]['attributes']['id'] == idElement) {
                                                     model = models[i];
                                                     break;
                                                 }
                                             }
                                         }
                                        if (model == null) {
                                            CRUD.model = null;
                                        } else {
                                            CRUD.model = model;
                                        }
                                         CRUD.render()
                                    },
                                    loadComplete:function(){

                                        CRUD.model = null;
                                        CRUD.render();

                                    },
                                    loadError:function(error) {

                                    },
                                    onPaging: function(id) {

                                            var page = 1;
                                            var order = grid.jqGrid('getGridParam','sortorder');
                                            var sort = grid.jqGrid('getGridParam','sortname');
                                            var flag = true;
                                            if (id === 'user') {
                                               page = parseInt($('#input-pag').val());
                                               container.get('collection').getPage(page, {data:{order:order, sort: sort},
                                                                            success: function(){
                                                                       Reload_Grid(tableid, container.get('collection'))
                                                                       }});

                                            } else {
                                                if (id != "records") {

                                                    var classs = $('#' + id).attr('class').split(" ");
                                                    var disabled = $.inArray('ui-state-disabled', classs);
                                                    if (disabled != -1)
                                                        flag = false;
                                                    var splitter = id.split("_");
                                                    var button = splitter[0];
                                                    if (flag) {
                                                        if (button === 'first') {
                                                            container.get('collection').getFirstPage({
                                                                data: {order: order, sort: sort},
                                                                success: function () {
                                                                    Reload_Grid(tableid, container.get('collection'))
                                                                }
                                                            });
                                                        }
                                                        if (button === 'prev') {
                                                            container.get('collection').getPreviousPage({
                                                                data: {order: order, sort: sort},
                                                                success: function () {
                                                                    Reload_Grid(tableid, container.get('collection'))
                                                                }
                                                            });
                                                        }
                                                        if (button === 'next') {
                                                            container.get('collection').getNextPage({
                                                                data: {order: order, sort: sort},
                                                                success: function () {
                                                                    Reload_Grid(tableid, container.get('collection'))
                                                                }
                                                            });
                                                        }
                                                        if (button === 'last') {
                                                            container.get('collection').getLastPage({
                                                                data: {order: order, sort: sort},
                                                                success: function () {
                                                                    Reload_Grid(tableid, container.get('collection'))
                                                                }
                                                            });
                                                        }
                                                    }
                                                }
                                            }

                                    },
                                    onSortCol: function(sort){

                                       var order = grid.jqGrid('getGridParam','sortorder');
                                       var sort = grid.jqGrid('getGridParam','sortname');
                                        container.get('collection').fetch({data:{order:order, sort: sort}, success: function(){
                                            Reload_Grid(tableid, container.get('collection'))
                                        }
                                        })
                                    }



                                });

                        Reload_Grid(tableid, container.get('collection'));

                        $('.ui-pg-selbox').bind('change',function() {
                             var rowNum = grid.jqGrid("getGridParam", "rowNum");
                             var order = grid.jqGrid('getGridParam','sortorder');
                             var sort = grid.jqGrid('getGridParam','sortname');
                             container.get('collection').setPageSize(parseInt(rowNum), {data:{order:order, sort: sort}, success: function(){
                                 Reload_Grid(tableid, container.get('collection'));
                             }});
                        });

                        var models = grid.jqGrid('getGridParam', 'colModel');
                        $('.ui-jqgrid-htable').find("div.ui-jqgrid-sortable").each(function(){
                            var splitID = $(this).attr('id').split('_' + tableid + '_');
                            var idDiv = splitID[1];

                            for (var i = 0; i < models.length; i++) {
                                var model = models[i];
                                if (model.name == idDiv) {
                                    if (model.sortable == false) {
                                        $(this).removeClass("ui-jqgrid-sortable");
                                        $(this).css({cursor:"default"})
                                    }
                                    break;
                                }
                            }
                        });







                    }});
                });
            }

        },

        render: function() {
            //return this.table.render().el;
        }

    });

    var CRUDComponent = Backbone.View.extend({

        crudView: CRUDView,

        setup: function(container) {
            CRUD = new this.crudView({
                collection: container.get('collectionCrud'),
                collectionGrid: container.get('collection'),
                desactivateButton: container.get('desactivateButton')
            });

            CRUD.on('build', function(form) {

                    var $_dialog = $("#dialog-form");
                    $_dialog.dialog({
                                                resizable: false,
                                                autoOpen: false,
                                                title: form.title,
                                                modal: true,
                                                closeOnEscape: false,
                                                closeText: gettext('Close'),
                                                width: "auto",
                                                maxHeight: 550,
                                                open: function(){
                                                    $("#dialog-form").keypress(function(e) {
                                                          if (e.keyCode == $.ui.keyCode.ENTER) {
                                                            $(this).parent().find("a:eq(0)").trigger("click");
                                                            return false;
                                                          }
                                                        });
                                                },
                                                close:function(){
                                                     var col =  container.get('collection');
                                                     var tableid = 'grid';
                                                     if (container.get('tableid'))
                                                        tableid = container.get('tableid')
                                                     var grid = $("#grid");
                                                     var order = grid.jqGrid('getGridParam','sortorder');
                                                     var sort = grid.jqGrid('getGridParam','sortname');

                                                     col.fetch({data:{order:order, sort: sort}, success: function(){
                                                         Reload_Grid(tableid, col);
                                                     }});
                                                    $("#dialog-form").empty();
                                                    $("#dialog-form").dialog('destroy');
                                                    CRUD.model = null;
                                                    CRUD.render();
                                                }


                                            });
                    $_dialog.append(form.render().el);

                    $_dialog.dialog("open");


                }, this);
            CRUD.on('cancel', function() {

                 var col =  container.get('collection');
                 var tableid = 'grid';
                 if (container.get('tableid'))
                    tableid = container.get('tableid')
                 var grid = $("#grid");
                 var order = grid.jqGrid('getGridParam','sortorder');
                 var sort = grid.jqGrid('getGridParam','sortname');

                 col.fetch({data:{order:order, sort: sort}, success: function(){
                     Reload_Grid(tableid, col);
                 }});
                 $("#dialog-form").empty();
                 $("#dialog-form").dialog('destroy');
                 CRUD.model = null;
                 CRUD.render();

            }, this);
            CRUD.on('commit create', function() {

                    var tableid = 'grid';
                     if (container.get('tableid'))
                        tableid = container.get('tableid')
                     var grid = $("#grid");


                     $("#messagesCrud").removeClass('msg-success msg');
                     $('#messagesCrud').addClass('msg-success msg')
                                        .html('<div class="msg-content msg-content-success">'+gettext('The operation was performed successfully')+'.</div>');
                     $('#messagesCrud').show().fadeOut(10000);
                     var order = grid.jqGrid('getGridParam','sortorder');
                     var sort = grid.jqGrid('getGridParam','sortname');
                     var col =  container.get('collection');
                     col.fetch({data:{order:order, sort: sort}, success: function(){
                         var length = col.length;
                         if (length == 0) {
                             var total = col.state.totalPages;
                             var page = total-1;
                             col.getPreviousPage();
                             grid.jqGrid('setGridParam', {page:page})

                         }
                         Reload_Grid(tableid,col);
                         $("#dialog-form").empty();
                         $("#dialog-form").dialog('destroy');
                         CRUD.model = null;
                         CRUD.render();
                     }, error: function(error, data) {

                            col.getPreviousPage({
                                                            data: {order: order, sort: sort},
                                                            success: function () {
                                                                Reload_Grid(tableid, container.get('collection'))
                                                            }
                                                        });
                         $("#dialog-form").empty();
                         $("#dialog-form").dialog('destroy');
                     }});

               //}});
            }, this);


        },

        render: function() {
            return CRUD.render().el;
        },

        addForm: function(type, title, schema) {
            CRUD.addForm(type, title, schema);
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
                    url: options.url,
                    collection: Collections(options.model, options.url),
                    crud: new CRUDComponent,
                    select: new SelectComponent,
                    table: new TableComponent,
                    tableid: options.tableid,
                    tablewidth: options.tablewidth,
                    paginationid: options.paginationid,
                    colModel: options.colModel,
                    colNames: options.colNames,
                    mtype: options.mtype,
                    collectionCrud: options.collectionCrud,
                    optionsFilter: options.optionsFilter,
                    placeholderOptionsFilter: options.placeholderOptionsFilter,
                    patternOptionsFilter: options.patternOptionsFilter,
                    typeDataOptions: options.typeDataOptions,
                    multiselect: options.multiselect,
                    desactivateButton: options.desactivateButton

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