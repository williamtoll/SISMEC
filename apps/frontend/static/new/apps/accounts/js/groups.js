require.config({
    paths:{
        table: STATIC_URL + 'js/backbone/table-grid',
        form: STATIC_URL + 'js/backbone/form'
    }
});

require(['table'], function (Table) {

    var Group = Backbone.Model.extend({
        schema: {
            name: {title: 'Roles'},
            permission_menu_set: {title: 'Permission Menu'}
        }
    });

    var Groups = Backbone.Collection.extend({
        url: '../api/groups/',
        model: Group,
        initialize: function(model, options) {
            this.model.prototype.urlRoot = this.url;
        }
    });



    var Permission_Menu = Backbone.Model.extend({
            toString: function () {
                return gettext(this.get('menu_name'))+' | '+ gettext(this.get('permission_name'));
            }
    });
    var Permission_Menu_All = Backbone.Collection.extend({
        url: '../api/permissions_menus/',
        model: Permission_Menu
    });


    groupSchema = {
        name: {title: gettext("Name"), validators: ['required','letters']},
        permission_menu_set: {
            title: gettext("Menu | Permission"),
            type: 'SelectDragDrop',
            options: [new Permission_Menu_All(), []]
        }
    };

   var colModel = [
                    {name:'id', index:'id', label: 'ID', hidden: true, hideable: false},
                    {name:'name', index:'name', label:gettext("Name"), resizable:false}
   ]
   var mtype = 'GET';

   var optionsFilter = {
       name: gettext("Name")
   };

   var patternOptionsFilter = {
       name: RE_LETTER
   };

   var cv = new Table.CRUDContainerView({
        el: $('#content'),
        model: Group,
        url: '../api/groups/',
        collectionCrud: new Groups(),
        mtype: mtype,
        colModel: colModel, // columnas del grid
        optionsFilter: optionsFilter,
        patternOptionsFilter: patternOptionsFilter
    });
    var permissions = PERMISSION_MENU;
    for (var i in permissions) {
        if (permissions[i] == "add_group") {
            cv.get('crud').addForm('add', gettext("Add"), groupSchema);
        } else if (permissions[i] == "change_group") {
            cv.get('crud').addForm('edit', gettext("Change"), groupSchema);
        } else if (permissions[i] == "delete_group") {
            cv.get('crud').addForm('remove', gettext("Are you sure you want to delete?"));
        }
    }

    cv.render();
});


