/**
 * @author Ing. Rainer Segura Peña
 */

function ShowLinkMB(cellvalue, opts, inventory) {

    var arreglo = document.location.href.split('/');
    arreglo.pop();
    arreglo.pop();
    arreglo.pop();
    var url = "";
    if (inventory == null)
                inventory = true;

    if(inventory)
        url += arreglo.join("/") + "/resume/?id=" + cellvalue;
    else
        url += arreglo.join("/") + "/inventory/resume/?id=" + cellvalue;

    return '<a href="javascript:void(0);" target="_self" onclick="createResume(\''+url+'\')">'+cellvalue+'</a>'
}

function ExportExcel(url_export, exportAgent)  {
    var ButtonView = Backbone.View.extend({
	    tagName: 'button',
	    className: 'ui-button ui-widget ui-state-default ui-corner-all',

	    initialize: function (options) {
	        this.title = options.title || '';
	        this.icon = options.icon || '';
            this.target = '_blank';
            this.urlInicial  = url_export;
            this.exportAgent = exportAgent;
	        this.setUrl(url_export);

	    },

	    render: function () {
	        if (this.title)
	            this.$el.attr('title', this.title);
            if (this.target)
                this.$el.attr('target', this.target);

	        if (this.icon) {
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
                //window.open(url);

                $.get(url,function(data,status){
                    var flag = false;
                    //console.log(data)
                    if (status != 'success') {
                        flag = true;
                    }
                    else if(data == true) {
                         flag = true;
                    } else {
                       window.open(url);
                       //window.location.href = url;
                    }

                    if (flag) {
                        $("#messagesCrud").removeClass('msg-error msg');
                        $('#messagesCrud').addClass('msg-error msg')
                                        .html('<div class="msg-content msg-content-error">'+gettext('No items to export.')+'</div>');
                        $('#messagesCrud').show().fadeOut(10000);
                    }
                });

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

function FilterSelect(collection, optionsValues, placeholderOptions, patternOptions, typeDataOptions) {

    var select = $("select").val();
    if (select != "0") {
        var divHtml= '<div id = "'+select+'" style="width : 30%; float:left;"></div>'
        var placeholder = "";
        var pattern = null;
        var flag = false;

        for (var element in optionsValues) {
                if (element == select) {
                    flag = true;
                    placeholder = optionsValues[element];
                    if (patternOptions && patternOptions[element])
                        pattern = patternOptions[element]
                    break;
                }
        }

        if(!$('#'+select).length){
            var typeER = null;
            if(typeDataOptions && typeDataOptions[select]) {
                if (typeDataOptions[select] == 'date') {
                    pattern = "^(19|20)[0-9]{2}[-](0[1-9]|1[012])[-](0[1-9]|[12][0-9]|3[01])$";
                } else if (typeDataOptions[select] == 'mail') {
                       typeER = 1;
                } else if (typeDataOptions[select] == 'ip') {
                        typeER = 2;
                }

            }
            $("#filters").prepend(divHtml)
            var filter = new Backgrid.Extension.ServerSideFilter({
                    collection: collection,
                    name: select,
                    placeholder: placeholder,
                    pattern: pattern,
                    typeER: typeER
            });
            $('#'+select).append(filter.render().$el)

            if(typeDataOptions && typeDataOptions[select]) {

                    var data = typeDataOptions[select];
                    var typeData = typeof data;
                    if( data == 'date') {
                        $('#'+select+'_input').datepicker({
                                dateFormat: "yy-mm-dd",
                                onSelect: function(dateText) {
                                        $(this).submit();
                                }
                        });
                    }  else if (typeData == "object") {

                       if (data['type'] && data['type'] == 'select') {
                           var elementSelect = "<select id='"+select+"_input' type='search'> <option value=''>"+placeholder+"</option>";
                           if (data['options']) {
                              for (var value in data['options']) {
                                  elementSelect += "<option value='"+value+"'>"+data['options'][value]+"</option>"
                              }
                           }
                           elementSelect += "</select>";
                           $('#'+select+'_input').replaceWith(elementSelect);
                           $('#'+select+'_input').combobox();
                           $('#'+select+'_input').change(function(){
                               $(this).submit();
                           });
                           $('#'+select+' .custom-combobox').css({"margin-left": "12%", "margin-top": "3%", "min-width": "160px", "max-width":"160px"});
                       }
                    }
                }

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

            if(inventory)
                url += arreglo.join("/") + "/resume/?id=" + this.$('a').attr('title');
            else
                url += arreglo.join("/") + "/inventory/resume/?id=" + this.$('a').attr('title');

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
              order: 'asc'
          },
          queryParams: {
              totalPages: null,
              totalRecords: null,
              sortKey: "sort",
              pageSize: "page_size",
              order: -1
        },
        // get the state from Github's search API result
        parseState: function (resp, queryParams, state, options) {

            return {totalPages: resp.count, totalRecords: resp.records, order: 'asc'};
        },
        // get the actual records
        parseRecords: function (resp, options) {
            return resp.rows;
        }
    });

    return new collectionsView();
}

function Reload_Grid(tableid, collection) {
    var grid = jQuery("#"+tableid);
    jQuery("#"+tableid).jqGrid('clearGridData');

    collection.each(function(data, i) {
                            var dat = data.toJSON();
                            var object = {}
                            for (j in dat) {
                               var d = dat[j]
                               switch(d) {
                                   case true:
                                        d = '<center><span class="ui-icon ui-icon-check" style="" title="'+gettext(d)+'"></span></center>';
                                        break;
                                   case false:
                                        d = '<center><span class="ui-icon ui-icon-close" style="" title="'+gettext(d)+'"></span></center>';
                                        break;
                                   case 'shutdown':
                                        d = '<center><span class="ui-icon ui-icon-power" style="" title="'+gettext("Shutdown")+'"></span></center>';
                                        break;
                                    case 'restart':
                                        d = '<center><span class="ui-icon ui-icon-arrowrefresh-1-e" style="" title="'+gettext("Reset")+'"></span></center>';
                                        break;
                                   case 'hibernate':
                                        d = '<center><span class="ui-icon ui-icon-gear" style="" title="'+gettext("Hibernate")+'"></span></center>';
                                        break;
                                    case 'suspend':
                                        d = '<center><span class="ui-icon ui-icon-cancel" style="" title="'+gettext("Suspend")+'"></span></center>';
                                        break;
                                   case 'inventory':
                                        d = '<center><span class="ui-icon ui-icon-calculator" style="" title="'+gettext("Inventory")+'"></span></center>';
                                        break;
                                   default :
                                       d = gettext(d)

                               }

                               object[j] = d
                            }
                            grid.jqGrid('addRowData', (i + 1), object);
                        })

    var state = collection.state;
    grid.jqGrid('setGridParam', {lastpage: state.lastPage,page: state.currentPage,records: state.totalRecords});
    	grid.each(function() {
            if (this.grid) this.updatepager();
    });
}

