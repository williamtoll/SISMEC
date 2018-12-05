require.config({
    paths:{
        table: STATIC_URL + 'js/backbone/table-grid',
        form: STATIC_URL + 'js/backbone/form'
    }
});

require(['table'], function (Table) {
    var User = Backbone.Model.extend({
         schema: {
            username: {title: gettext("User")},
            first_name: {title: gettext("Name")},
            last_name: {title: gettext("Last name")},
            email:{title:gettext("Email Address")},
            is_active:{title:gettext("Active")},
            is_superuser:{title:gettext("It is superuser")},
            groups: {title: gettext("Groups")},
            domain_set: {title: gettext("Domains")},
            permission_menu_set: {title: gettext("Menu | Permission")}
        }
    });

    var Users = Backbone.Collection.extend({
        url: '../api/users/',
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

    var Domain = Backbone.Model.extend({
            toString: function () {
                return this.get('description');
            }
    });

    var Domains = Backbone.Collection.extend({
        url: '../api/domain/',
        model: Domain
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


    var userSchema = {
        username: {title: gettext("User"), validators: ['required']},
        password: {
            title: gettext("Password"),
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
                    message: gettext("Confirmation does not have the same value as the password.")},
                'required'
            ]
        },
        first_name: {title: gettext("Name"),validators:['required','letters']},
        last_name: {title: gettext("Last name"),validators:['required','letters']},
        email:{title:gettext("Email Address"),validators:['required','email']},
        is_active:{title:gettext("Active"),type:'Checkbox'},
//        is_staff:{title:gettext("It is staff"),type:'Checkbox'},
        is_superuser:{title:gettext("It is superuser"),type:'Checkbox' },
        user_token:{title:gettext("Token"), type:'Checkbox'},
        groups: {
            title: gettext("Groups"),
            type: 'SelectMultiple',
            options: new Groups()/*,
            validators: ['required']*/
        },
        domain_set: {
            title: gettext("Domains"),
            type: 'SelectMultiple',
            options: new Domains()/*,
            validators: ['required']*/
        },
        permission_menu_set: {
            title: gettext("Menu | Permission"),
            type: 'SelectDragDrop',
            options: [new Permission_Menu_All(), []]
        }
    };

    var editUserSchema = {username: {title: gettext("User"), validators: ['required']},
        first_name: {title: gettext("Name"),validators:['required','letters']},
        last_name: {title: gettext("Last name"),validators:['required','letters']},
        email:{title:gettext("Email Address"),validators:['required','email']},
        is_active:{title:gettext("Active"),type:'Checkbox'},
        is_superuser:{title:gettext("It is superuser"),type:'Checkbox' },
//        user_token:{title:gettext("Token"), type:'Checkbox'},
        groups: {
            title: gettext("Groups"),
            type: 'SelectMultiple',
            options: new Groups()
        },
        domain_set: {
            title: gettext("Domains"),
            type: 'SelectMultiple',
            options: new Domains()
        },
        permission_menu_set: {
            title: gettext("Menu | Permission"),
            type: 'SelectDragDrop',
            options: [new Permission_Menu_All(), []]
        }
    };

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
                'required',
                {
                    type: 'match',
                    field: 'password',
                    message: gettext("Confirmation does not have the same value as the password.")}
            ]
        },
        change:{
            type: 'Hidden',
            value: 'change'
        }
    };

   editUserSchema.username.readonly = true;


   var colModel = [
                    {name:'id', index:'id', label: "ID", hidden: true, hideable: false},
                    {name:'username', index:'username', label: gettext("User"), resizable:false},
                    {name:'first_name', index:'first_name',label: gettext("Name"), resizable:false},
                    {name:'last_name', index:'last_name',label: gettext("Last name"), resizable:false},
                    {name:'last_login', index:'last_login',label: gettext("Last signed"), resizable:false}
   ]
   var mtype = 'GET';

   var optionsFilter = {
       username: gettext("User"),
       first_name: gettext("Name"),
       last_name: gettext("Last name")
   }

   var patternOptionsFilter = {
      username: RE_LETTER_SPECIAL,
      first_name: RE_LETTER,
      last_name: RE_LETTER
    }

   var cv = new Table.CRUDContainerView({
        el: $('#content'),
        model: User, //model de la collection
        url: '../api/users/', //Url de la coleccion
        mtype: mtype,
        colModel: colModel, // columnas del grid
        collectionCrud: new Users(), // collection del Crud
        optionsFilter: optionsFilter,
        patternOptionsFilter: patternOptionsFilter
    });

    var permissions = PERMISSION_MENU;


    for (var i in permissions) {
        if (permissions[i] == "add_user") {
            cv.get('crud').addForm('add', gettext("Add"), userSchema);
        } else if (permissions[i] == "change_user") {
            cv.get('crud').addForm('edit', gettext("Change"), editUserSchema);
        } else if (permissions[i] == "delete_user") {
            cv.get('crud').addForm('remove', gettext("Are you sure you want to delete?"));
        } else if (permissions[i] == "password_change") {
            cv.get('crud').addForm('change', gettext("Change Password"), PasswordChangeSchema);
        }


    }


    cv.render();


});







