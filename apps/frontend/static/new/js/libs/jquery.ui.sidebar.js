/*!
 * jQuery UI Menu 1.10.3
 * http://jqueryui.com
 *
 * Copyright 2013 jQuery Foundation and other contributors
 * Released under the MIT license.
 * http://jquery.org/license
 *
 * http://api.jqueryui.com/menu/
 *
 * Depends:
 *	jquery.ui.core.js
 *	jquery.ui.widget.js
 *	jquery.ui.position.js
 */
(function ($, undefined) {

    $.widget("ui.sidebar", {
        version: "1.10.3",
        defaultElement: "<ul>",

        options: {
            collapsible: true,
            oneOnly: false,
            icons: {
                submenu: "ui-icon-carat-1-e"
            },
            menus: "ul"

        },

        _create: function () {

           
            var autoPadding = function (el) {
                increment+=18;
                
                el.find("a").each(function(){
                    $(this).css({
                        "padding-left": (increment) + "px"
                        
                    });
                    
                    $(this).find("span").css({
                        left:(increment-22)+"px"
                    })
                });
                
                el.children("li").children("ul").each(function(){
                    autoPadding($(this));
                });
               
           

            };


            this.element.addClass("ui-side-menu ui-menu ui-widget-content");
            this.element.find("li").addClass("ui-menu-item");

            /* this.element.find("ul").addClass("ui-vmenu ui-menu ui-widget ui-widget-content ui-corner-all ui-menu-icons")*/

            /*Verificar que es un Side Menu Simple, o sea no tiene SubItems*/


            /*Verificar que es un Side Menu con Iconos*/
            var hasIcons = false, where = this.element.find("span.ui-icon");
            if (where.length > 0) {
                where.parent().parent().parent().addClass("ui-menu-icons");
            /*     this.element.addClass("ui-menu-icons")*/

            }

            var increment = parseFloat($(this.element.children("li").children("a")[0]).css("padding-left"));
           
            /*Los <a> del <ul> contendor adquieren Padding Left por el CSS, entonces el proceso empiesa por sus hijos*/
            autoPadding(this.element.children("li").children("ul"));
            /*Construir en Refresh*/
            this.refresh();


        /*


             this.activeMenu = this.element;
             // flag used to prevent firing of the click handler
             // as the event bubbles up through nested menus
             this.mouseHandled = false;
             this.element
             .uniqueId()
             .addClass( "ui-menu ui-widget ui-widget-content ui-corner-all" )
             .toggleClass( "ui-menu-icons", !!this.element.find( ".ui-icon" ).length )
             .attr({
             role: this.options.role,
             tabIndex: 0
             })
             // need to catch all clicks on disabled menu
             // not possible through _on
             .bind( "click" + this.eventNamespace, $.proxy(function( event ) {
             if ( this.options.disabled ) {
             event.preventDefault();
             }
             }, this ));

             if ( this.options.disabled ) {
             this.element
             .addClass( "ui-state-disabled" )
             .attr( "aria-disabled", "true" );
             }




             this.refresh();

             // Clicks outside of a menu collapse any open menus
             /*this._on( this.document, {
             click: function( event ) {
             if ( !$( event.target ).closest( ".ui-menu" ).length ) {
             this.collapseAll( event );
             }

             // Reset the mouseHandled flag
             this.mouseHandled = false;
             }
             });*/
        },

        _destroy: function () {
            // Destroy (sub)menus
            this.element
            .removeAttr("aria-activedescendant")
            .find(".ui-menu").addBack()
            .removeClass("ui-menu ui-widget ui-widget-content ui-corner-all ui-menu-icons")
            .removeAttr("role")
            .removeAttr("tabIndex")
            .removeAttr("aria-labelledby")
            .removeAttr("aria-expanded")
            .removeAttr("aria-hidden")
            .removeAttr("aria-disabled")
            .removeUniqueId()
            .show();

            // Destroy menu items
            this.element.find(".ui-menu-item")
            .removeClass("ui-menu-item")
            .removeAttr("role")
            .removeAttr("aria-disabled")
            .children("a")
            .removeUniqueId()
            .removeClass("ui-corner-all ui-state-hover")
            .removeAttr("tabIndex")
            .removeAttr("role")
            .removeAttr("aria-haspopup")
            .children().each(function () {
                var elem = $(this);
                if (elem.data("ui-menu-submenu-carat")) {
                    elem.remove();
                }
            });

            // Destroy menu dividers
            this.element.find(".ui-menu-divider").removeClass("ui-menu-divider ui-widget-content");
        },


        refresh: function () {
            //TODO:
            /*
                 *Marcar al LI si hay un Span con Image dentro
                 *Es ditinto cuando es Single a cuando tiene Childrens
                 *Imagenes para desplegar, que se sepa que tiene algo dentro.
                 **/

            var items = this.element.find("li"),
            isCollapsible = this.options.collapsible,
            oneOnly = this.options.oneOnly,
            icon = this.options.icons.submenu,
            subitems = this.element.find(this.options.menus);

            /*Por defecto, los UL, que son los Hijos de los LI no son Visibles*/
            subitems.hide();

            /*Mostrar los UL siempre que los LI tengan estado activo*/

            items.filter(".ui-state-active")
            .children()
            .show()
            /*Ademas marcar a los Elementos <a> como activos, al menos diferenciarlos de algun modo*/
            .prev()
            .addClass("ui-state-highlight");

            /*Annadir funcionalidad!!*/

            items.find("a").click(function () {
                var element = ($(this).next());// el UL que se desplego, o sea el hijo del LI donde hice click

                var others = ($(this).parent().parent().find("ul"));

                //Si estas visible
                if (element.is(":visible")) {

                    //si se paso la opcion collapsible
                    if (isCollapsible) {
                        /*Esonder el UL*/
                        element.slideUp("normal", function () {
                            /* element.prev().removeClass("ui-state-highlight");*/
                            element.parent().removeClass("ui-state-active");
                        });

                    }
                    /*No hacer nada*/
                    return false;

                } else {
                    /*Si solo puede haber visible un LI con si respectivo Ul*/
                    if (oneOnly) {
                        /*Entonces recoger a todo el mundo*/
                        others.each(function () {
                            var el = $(this);
                            el.slideUp("normal", function () {
                                /* el.prev().removeClass("ui-state-highlight");*/

                                });
                        });
                    }

                    /*Nadie queda activo*/
                    items.removeClass("ui-state-active");


                    /*Desplegar solo al que se le hizo click*/
                    element.slideDown("normal", function () {
                        /* element.prev().addClass("ui-state-highlight");*/


                        });
                    /*Marcarlo como activo*/
                    $(this).parent().addClass("ui-state-active");

                }

            });


        /*

             var menus,
             icon = this.options.icons.submenu,
             submenus = this.element.find( this.options.menus );

             // Initialize nested menus
             submenus.filter( ":not(.ui-menu)" )
             .addClass( "ui-menu ui-widget ui-widget-content ui-corner-all" )
             .hide()
             .attr({
             role: this.options.role,
             "aria-hidden": "true",
             "aria-expanded": "false"
             })
             .each(function() {
             var menu = $( this ),
             item = menu.prev( "a" ),
             submenuCarat = $( "<span>" )
             .addClass( "ui-menu-icon ui-icon " + icon )
             .data( "ui-menu-submenu-carat", true );

             item
             .attr( "aria-haspopup", "true" )
             .prepend( submenuCarat );
             menu.attr( "aria-labelledby", item.attr( "id" ) );
             });

             menus = submenus.add( this.element );

             // Don't refresh list items that are already adapted
             menus.children( ":not(.ui-menu-item):has(a)" )
             .addClass( "ui-menu-item" )
             .attr( "role", "presentation" )
             .children( "a" )
             .uniqueId()
             .addClass( "ui-corner-all" )
             .attr({
             tabIndex: -1,
             role: this._itemRole()
             });

             // Initialize unlinked menu-items containing spaces and/or dashes only as dividers
             menus.children( ":not(.ui-menu-item)" ).each(function() {
             var item = $( this );
             // hyphen, em dash, en dash
             if ( !/[^\-\u2014\u2013\s]/.test( item.text() ) ) {
             item.addClass( "ui-widget-content ui-menu-divider" );
             }
             });

             // Add aria-disabled attribute to any disabled menu item
             menus.children( ".ui-state-disabled" ).attr( "aria-disabled", "true" );

             // If the active item has been removed, blur the menu
             if ( this.active && !$.contains( this.element[ 0 ], this.active[ 0 ] ) ) {
             this.blur();
             }*/
        }


    });

}(jQuery));
