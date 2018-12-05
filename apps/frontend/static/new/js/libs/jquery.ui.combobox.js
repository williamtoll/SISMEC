(function($) {
    $.widget("custom.combobox", {
        _create: function() {
            this.wrapper = $("<span>")
            .addClass("custom-combobox")
            .insertAfter(this.element);

            this.element.hide();
     
            
            /*
             *Me toca a mi
             **/
            
            var outerDiv = $("<div>"), maxWidth = 0;
            outerDiv.css({
                visibility: "hidden", 
                position: "absolute", 
                opacity: 0
            });
            $("body").append(outerDiv);
                        
            $(this.element[0]).children().each(function(){
                
                outerDiv.text($(this).text());
                if(maxWidth < outerDiv.width()){
                    maxWidth = outerDiv.width();
                }               
            });
            outerDiv.remove();
            
            /*Done*/
    
          
            
            this._createAutocomplete(maxWidth);
            this._createShowAllButton();
        /*Modificar el Metodo resizeMenu del autocomplete, solo asi se podra
             * pasar un Width por parametro para la creacion de un combobox 
             * ajustado al tamanno del texto en el contenido*/
         
           
            
        },
        
        
        _createAutocomplete: function(maxWidth) {
           
            var selected = this.element.children(":selected"),
            value = selected.text();
            //value = selected.val() ? selected.text() : "";
            var theSelect = this.element;
            
            
          

            this.input = $("<input>")
            .appendTo(this.wrapper)
            .val(value)
            .width((maxWidth + 40) + "px")
            .css({
                "padding-right":"20px"
            })
            .attr("title", "")
            .attr("type", "combobox")
            .attr("readonly", "")
            .addClass("custom-combobox-input ui-widget")
            .autocomplete({
                select:function(){
                    theSelect.trigger("change");
                },
                /* fromCombo:true,*/
                delay: 0,
                minLength: 0,
                source: $.proxy(this, "_source")
            }).focus(function() {
                $(this).parent().addClass("ui-color-active");
               
                
                
            }).blur(function() {
                $(this).parent().removeClass("ui-color-active");
                
            })

            this._on(this.input, {
                autocompleteselect: function(event, ui) {
                    ui.item.option.selected = true;
                    this._trigger("select", event, {
                        item: ui.item.option
                    });
                },
                autocompletechange: "_removeIfInvalid"
            });
        },
        _createShowAllButton: function() {
            var input = this.input,
            wasOpen = false;

            $("<a>")
            .attr("tabIndex", -1)
            .attr("title", "")
        
            .appendTo(this.wrapper)
            .button({
                icons: {
                    primary: "ui-icon-triangle-1-s"
                },
                text: false
            })
            .removeClass("ui-corner-all")
            .removeClass("ui-button-icon-only")
            .addClass("custom-combobox-toggle")
            .mousedown(function() {
                wasOpen = input.autocomplete("widget").is(":visible");
            })
            .click(function() {
                input.focus();

                // Close if already visible
                if (wasOpen) {
                    return;
                }

                // Pass empty string as value to search for, displaying all results
                input.autocomplete("search", "");
               
            });
        },
        _source: function(request, response) {
            var matcher = new RegExp($.ui.autocomplete.escapeRegex(request.term), "i");
            response(this.element.children("option").map(function() {
                var text = $(this).text();
                //if (this.value && (!request.term || matcher.test(text)))
                    return {
                        label: text,
                        value: text,
                        option: this
                    };
            }));
        },
        _removeIfInvalid: function(event, ui) {

            // Selected an item, nothing to do
            if (ui.item) {
                return;
            }

            // Search for a match (case-insensitive)
            var value = this.input.val(),
            valueLowerCase = value.toLowerCase(),
            valid = false;
            this.element.children("option").each(function() {
                if ($(this).text().toLowerCase() === valueLowerCase) {
                    this.selected = valid = true;
                    return false;
                }
            });

            // Found a match, nothing to do
            if (valid) {
                return;
            }

            // Remove invalid value
            this.input
            .val("")
            .attr("title", value + " didn't match any item")
            .tooltip("open");
            this.element.val("");
            this._delay(function() {
                this.input.tooltip("close").attr("title", "");
            }, 2500);
            this.input.data("ui-autocomplete").term = "";
        },
        _destroy: function() {
            this.wrapper.remove();
            this.element.show();
        }
    });
})(jQuery);