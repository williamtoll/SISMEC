require.config({
    baseUrl:STATIC_URL + 'apps/accounts/js',
    paths:{
        table: STATIC_URL + 'js/backbone/table',
        form: STATIC_URL + 'js/backbone/form'
    }
});

require(['table'], function (Table) {
    var Resource = Backbone.Model.extend({
        schema:{
            menu_name:{title:'Menu'},
            permission_name:{title:'Permission'}
        }

    });

    var Resources = Backbone.Collection.extend({
        url:'../api/resources/',
        model:Resource,
        initialize: function(model, options) {
            this.model.prototype.urlRoot = this.url;
        }
    });



    var Menu = Backbone.Model.extend({
        toString:function () {
            return this.get('name');
        }
    });

    var Menus = Backbone.Collection.extend({
        url:'../api/menus/',
        model:Menu
    });

    var Permission = Backbone.Model.extend({
        toString:function () {
            return this.get('name');
        }
    });

    var Permissions = Backbone.Collection.extend({
        url:'../api/permissions/',
        model:Permission
    });

    var Group = Backbone.Model.extend({
        toString:function () {
            return this.get('name');
        }
    });

    var Groups = Backbone.Collection.extend({
        url:'../api/groups/',
        model:Group
    });

    resourceSchema = {
        menu:{
            title:'Menus',
            type:'Select',
            options:new Menus(),
            validators:['required']
        },
        permission:{
            title:'Permisos',
            type:'Select',
            options:new Permissions(),
            validators:['required']
        },
        group:{
            title:'Grupos',
            type:'SelectMultiple',
            options:new Groups(),
            validators:['required']
        }
    };

    var columns = [
        {
           name: "id",
           cell: "select-row",
           headerCell: "select-all"
        },
        {
            name: "menu_name",
            label: "Menu",
            cell: "string",
            editable: false
        },
        {
            name: "permission_name",
            label: "Permission",
            cell: "string",
            editable: false
        }

    ];

    var optionsFilter = ['menu_name', 'permission_name'];
    var placeholderOptionsFilter = ['Menu', 'Permission']; // HTML5 placeholder for the search box

    var cv = new Table.CRUDContainerView({
        el:$('#content'),
        model: Resource,
        url: '../api/resources/',
        columns: columns,
        collectionCrud: new Resources(),
        optionsFilter: optionsFilter,
        placeholderOptionsFilter: placeholderOptionsFilter
    });

    cv.get('crud').addForm('add', gettext("Add"), resourceSchema);
    cv.get('crud').addForm('edit', gettext("Change"), resourceSchema);
    cv.get('crud').addForm('remove', gettext("Are you sure you want to delete?"));
    cv.render();
});
