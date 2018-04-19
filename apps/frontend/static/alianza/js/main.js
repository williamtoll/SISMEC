$(document).ready(function () {


    $('#search-preview').hide();
    // $('.ui.search')
    //     .search({
    //         apiSettings: {
    //             url: '/backend/ajax/item_autocomplete_search/?search={query}'
    //         },
    //         fields: {
    //             results: 'results',
    //             title: 'title',
    //             url: 'url',
    //             image: 'imagen'
    //         },
    //         minCharacters: 3
    //     })
    // ;

    $('#search-input').keypress(function () {
        var search_preview_items = $('#search-preview-items');
        var search_input = $('#search-input');
        $('#search-preview').hide();
        search_preview_items.empty();
        if (search_input.val().length > 1) {
            $.ajax({
                url: '/backend/ajax/item_autocomplete_search/',
                type: 'GET',
                dataType: "html",
                data: {
                    search: search_input.val()
                },
                success: function (response) {
                    search_preview_items.empty();
                    $('#search-preview').show();
                    var data_response = JSON.parse(response);
                    var length_for = 5;
                    if (data_response.results.length < 5) {
                        length_for = data_response.results.length;
                    }

                    for (var i = 0; i < length_for; i++) {

                        var item = data_response.results[i];

                        var div_preview_item = $('<div class="search-preview-item clearfix">' + '<a href="' + item.url + '">' +
                            '                                        <div class="search-preview-item-image">' +
                            '                                            <img src="' + item.imagen + '" alt="">' +
                            '                                        </div>' +
                            '                                        <div class="search-preview-item-desc"><span style="float: left;color: #000000">' + item.title + '</span><br>' +
                            '                                            <span class="search-preview-item-category">' + item.categoria + '</span>' +
                            '                                            <span class="search-preview-item-sub" style="float: left">' + item.editorial + '</span>' +
                            '                                        </div>' + '</a>' +
                            '                                    </div>');

                        search_preview_items.append(div_preview_item);
                    }

                    var action = data_response.action;

                    var div_preview_item_a = $('<div class="search-preview-item clearfix">' +
                        '<div id="search-preview-items-ver-todos"><div id="ver-todos">' +
                        '<a href="' + action.url + '">' +
                        action.text + '</a></div></div></div>');

                    search_preview_items.append(div_preview_item_a);

                },
                error: function (xhr, errmsg, err) {
                    console.log(err);
                }
            });
        }
    });


    $("input").addClass("form-control");
    initMap();

    function initMap() {
        var myLatLng = {lat: -25.284403793483676, lng: -57.61788368225098};

        var map = new google.maps.Map(document.getElementById('google-map5'), {
            zoom: 17,
            center: myLatLng,
            scrollwheel: false,
            draggable: false,
            disableDefaultUI: false,
            zoomControl: true,
            mapTypeControl: false

        });

        var marker = new google.maps.Marker({
            position: myLatLng,
            map: map,
            title: 'Editorial En Alianza'
        });
    }

    $('#row_per_page').on('change', function () {
        window.location.href = $(this.selectedOptions[0]).attr('href')
    });


    "use strict";

    var window_width = $(window).width(),
        window_height = window.innerHeight,
        header_height = $(".default-header").height(),
        header_height_static = $(".site-header.static").outerHeight(),
        fitscreen = window_height - header_height;


    // $(window).on('load', function() {
    //        // Animate loader off screen
    //        $(".preloader").fadeOut("slow");;
    //    });

    $(".fullscreen").css("height", window_height);
    $(".fitscreen").css("height", fitscreen);

    //-------- Active Sticky Js ----------//
    $(".sticky-header").sticky({topSpacing: 0});

    // -------   Active Mobile Menu-----//

    $(".mobile-btn").on('click', function (e) {
        e.preventDefault();
        $(".main-menu").slideToggle();
        $("span", this).toggleClass("lnr-menu lnr-cross");
        $(".main-menu").addClass('mobile-menu');
    });
    $(".main-menu li a").on('click', function (e) {
        e.preventDefault();
        $(".mobile-menu").slideUp();
        $(".mobile-btn span").toggleClass("lnr-menu lnr-cross");
    });


    // $(function(){
    //     $('#Container').mixItUp();
    // });
    if ($('#filter-content').length > 0) {
        var mixer = mixitup('#filter-content');
    }

    $(".controls .filter").on('click', function (event) {
        $(".controls .filter").removeClass('active');
        $(this).addClass('active');
    });
    // Add smooth scrolling to Menu links
    $(".main-menu li a, .smooth").on('click', function (event) {
        if (this.hash !== "") {
            event.preventDefault();
            var hash = this.hash;
            $('html, body').animate({
                scrollTop: $(hash).offset().top - (-10)
            }, 600, function () {

                window.location.hash = hash;
            });
        }
    });

    $('.active-testimonial-carousel').owlCarousel({
        loop: true,
        dot: true,
        items: 3,
        margin: 30,
        autoplay: true,
        autoplayTimeout: 3000,
        autoplayHoverPause: true,
        animateOut: 'fadeOutLeft',
        animateIn: 'fadeInRight',
        responsive: {
            0: {
                items: 1,
            },
            600: {
                items: 3,
            }
        }
    });
    // -------   Mail Send ajax

    $(document).ready(function () {
        var form = $('#myForm'); // contact form
        var submit = $('.submit-btn'); // submit button
        var alert = $('.alert'); // alert div for show alert message

        // form submit event
        form.on('submit', function (e) {
            e.preventDefault(); // prevent default form submit

            $.ajax({
                url: 'mail.php', // form action url
                type: 'POST', // form submit method get/post
                dataType: 'html', // request type html/json/xml
                data: form.serialize(), // serialize form data
                beforeSend: function () {
                    alert.fadeOut();
                    submit.html('Sending....'); // change submit button text
                },
                success: function (data) {
                    alert.html(data).fadeIn(); // fade in response data
                    form.trigger('reset'); // reset form
                    submit.html(''); // reset submit button text
                },
                error: function (e) {
                    console.log(e)
                }
            });
        });
    });

    $(document).ready(function () {
        $('#mc_embed_signup').find('form').ajaxChimp();
    });
});
(function ($) {

    $.fn.bekeyProgressbar = function (options) {

        options = $.extend({
            animate: true,
            animateText: true
        }, options);

        var $this = $(this);

        var $progressBar = $this;
        var $progressCount = $progressBar.find('.progressBar-percentage-count');
        var $circle = $progressBar.find('.progressBar-circle');
        var percentageProgress = $progressBar.attr('data-progress');
        var percentageRemaining = (100 - percentageProgress);
        var percentageText = $progressCount.parent().attr('data-progress');

        //Calcule la circonférence du cercle
        var radius = $circle.attr('r');
        var diameter = radius * 2;
        var circumference = Math.round(Math.PI * diameter);

        //Calcule le pourcentage d'avancement
        var percentage = circumference * percentageRemaining / 100;

        $circle.css({
            'stroke-dasharray': circumference,
            'stroke-dashoffset': percentage
        })

        //Animation de la barre de progression
        if (options.animate === true) {
            $circle.css({
                'stroke-dashoffset': circumference
            }).animate({
                'stroke-dashoffset': percentage
            }, 3000)
        }

        //Animation du texte (pourcentage)
        if (options.animateText == true) {

            $({Counter: 0}).animate(
                {Counter: percentageText},
                {
                    duration: 3000,
                    step: function () {
                        $progressCount.text(Math.ceil(this.Counter) + '%');
                    }
                });

        } else {
            $progressCount.text(percentageText + '%');
        }

    };

})(jQuery);

$(document).ready(function () {

    $('.progressBar--animateNone').bekeyProgressbar({
        animate: false,
        animateText: false
    });

    $('.progressBar--animateCircle').bekeyProgressbar({
        animate: true,
        animateText: false
    });

    $('.progressBar--animateText').bekeyProgressbar({
        animate: false,
        animateText: true
    });

    $('.progressBar--animateAll').bekeyProgressbar();

})