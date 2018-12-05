require.config({
    baseUrl:STATIC_URL + 'apps/accounts/js',
    paths:{
        table: STATIC_URL + 'js/backbone/table',
        form: STATIC_URL + 'js/backbone/form'
    }
});

require(['table'], function (Table) {

    var Menu = Backbone.Model.extend({
        schema: {
            name: {title: gettext('Menus')},
            description: {title: gettext('Description')}
        }
    });

    var Menus = Backbone.Collection.extend({
        url: '../api/menus/',
        model: Menu,
        initialize: function(model, options) {
            this.model.prototype.urlRoot = this.url;
        }
    });



    var Permission = Backbone.Model.extend({
        toString: function () {
            return this.get('name');
        }
    });

    var Permissions = Backbone.Collection.extend({
        url: '../api/permissions_menu/',
        model: Permission
    });

    groupSchema = {
        name: {title: gettext("Name"), validators: ['required','letras']},
        permissions: {
            title: gettext("Permissions"),
            type: 'SelectMultiple',
            options: new Permissions(),
            validators: ['required']
        }
    };

    var columns = [
        {
          cell: "select-row"
          //headerCell: "select-all"
        },
        {
            name: "name",
            label: gettext("Name"),
            cell: "string",
            editable: false
        },

        {
            name: "description",
            label: gettext("Description"),
            cell: "string",
            editable: false
        }

    ];

   var optionsFilter = ['name'];
   var placeholderOptionsFilter = ["Name"]; // HTML5 placeholder for the search box
   var cv = new Table.CRUDContainerView({
        el: $('#content'),
        model: Menu,
        url: '../api/menus/',
        columns: columns,
        collectionCrud: new Menus()
        /*optionsFilter: optionsFilter,
        placeholderOptionsFilter: placeholderOptionsFilter*/
    });

    cv.get('crud').addForm('edit', gettext("Change"), groupSchema);

    cv.render();
});

