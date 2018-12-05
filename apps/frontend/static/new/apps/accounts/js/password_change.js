require.config({
    baseUrl:STATIC_URL + 'apps/accounts/js',
    paths:{
        table: STATIC_URL + 'js/backbone/table',
        form: STATIC_URL + 'js/backbone/form'
    }
});

require(['table'], function (Table) {
    var User = Backbone.Model.extend({
         schema: {
            username: {title: 'Usuario'},
            first_name: {title: 'Nombre'},
            last_name: {title: 'Apellidos'},
            last_login: {title: 'Última conexión'}
        }
    });

    var Users = Backbone.Collection.extend({
        url: '../api/reset_password/',
        model: User,
        initialize: function(model, options) {
            this.model.prototype.urlRoot = this.url;
        }
    });

    var Group = Backbone.Model.extend({
            toString: function () {
                return this.get('name');
            }
    });

    var Groups = Backbone.Collection.extend({
        url: '../api/groups/',
        model: Group
    });


     var columns = [
     {

          cell: "select-row"

     },
       {
        name: "username",
        label: gettext("User"),
        cell: "string",
        editable: false
      },
      {
        name: "first_name",
        label: gettext("Name"),
        cell: "string",
        editable: false
      },
      {
          name: "last_name",
          label: gettext("Last name"),
          cell: "string",
          editable: false
      },
      {
          name: "last_login",
          label: gettext("Last signed"),
          cell: 'string',
          editable: false
      }
    ];
    var PasswordChangeSchema = {
        password: {
            title: gettext('Password'),
            type: 'Password',
            validators: ['required'],
            empty: true
        },
        confirm: {
            title: gettext("Password Confirm"),
            type: 'Password',
            exclude: true,
            validators: [
                {
                    type: 'match',
                    field: 'password',
                    message: gettext("Confirmation does not have the same value as the password.")}
            ]
        }};

   var optionsFilter = ['username'];
   var placeholderOptionsFilter = [gettext("User")]; // HTML5 placeholder for the search box
   var cv = new Table.CRUDContainerView({
        el: $('#content'),
        model: User, //model de la collection
        url: '../api/reset_password/', //Url de la coleccion
        columns: columns, // columnas del grid
        collectionCrud: new Users(), // collection del Crud
        optionsFilter: optionsFilter,
        placeholderOptionsFilter: placeholderOptionsFilter
    });


    cv.get('crud').addForm('edit', gettext("Change"), PasswordChangeSchema);


    cv.render();

});






