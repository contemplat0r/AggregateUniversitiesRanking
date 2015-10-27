(function ($) {

 /**
  * Get the total displacement of given region.
  *
  * @param region
  *   Region name. Either "top" or "bottom".
  *
  * @return
  *   The total displacement of given region in pixels.
  */
  if (Drupal.overlay) {
    Drupal.overlay.getDisplacement = function (region) {
      var displacement = 0;
      var lastDisplaced = $('.overlay-displace-' + region + ':last');
      if (lastDisplaced.length) {
        displacement = lastDisplaced.offset().top + lastDisplaced.outerHeight();

        // In modern browsers (including IE9), when box-shadow is defined, use the
        // normal height.
        var cssBoxShadowValue = lastDisplaced.css('box-shadow');
        var boxShadow = (typeof cssBoxShadowValue !== 'undefined' && cssBoxShadowValue !== 'none');
        // In IE8 and below, we use the shadow filter to apply box-shadow styles to
        // the toolbar. It adds some extra height that we need to remove.
        if (!boxShadow && /DXImageTransform\.Microsoft\.Shadow/.test(lastDisplaced.css('filter'))) {
          displacement -= lastDisplaced[0].filters.item('DXImageTransform.Microsoft.Shadow').strength;
          displacement = Math.max(0, displacement);
        }
      }
      return displacement;
    };
  };

})(jQuery);
;
Drupal.settings.spotlight_settings = Drupal.settings.spotlight_settings || {};

(function ($) {

  /**
   * Form behavior for Spotlight
   */
  Drupal.behaviors.panopolySpotlight = {
    attach: function (context, settings) {
      if ($('.field-name-field-basic-spotlight-items', context).length) {
        $('.field-name-field-basic-spotlight-items', context).each(function() {
          var rotation_time = $(this).find('.panopoly-spotlight-buttons-wrapper').data('rotation-time'),
              $widget = $(this),
              $slides = $widget.find('.panopoly-spotlight'),
              $controls = $widget.find('.panopoly-spotlight-buttons-wrapper li'),
              current = 0,
              timer = null;

          function start() {
            if (timer === null) {
              timer = setTimeout(rotate, rotation_time);
            }
          }

          function stop() {
            if (timer !== null) {
              clearTimeout(timer);
              timer = null;
            }
          }

          function rotate() {
            // Increment the current slide.
            current++;
            if (current >= $controls.length) {
              current = 0;
            }

            // Click the control for the next slide.
            $controls.eq(current).children('a').trigger('click.panopoly-widgets-spotlight');
          }

          // Navigation is hidden by default, display it if JavaScript is enabled.
          $widget.find('.panopoly-spotlight-buttons-wrapper').css('display', 'block');

          // Hide all the slides but the first one.
          $slides.hide();
          $slides.eq(0).show();
          $controls.eq(0).addClass('active');

          // Bind the event for the slide numbers.
          $controls.once('panopoly-spotlight').children('a').bind('click.panopoly-widgets-spotlight', function (event) {
            var selector = $(this).attr('href');
            if (selector.indexOf('#') === 0) {
              event.preventDefault();

              // Mark the slide number as active.
              $controls.removeClass('active');
              $(this).parent().addClass('active');

              // Hide all slides but the selected one.
              $slides.hide();
              $slides.filter(selector).show();

              // Start the timer over if it's running.
              if (timer !== null) {
                stop();
                start();
              }

              return false;
            }
          });

          // Bind events to all the extra buttonts.
          $widget.find('.panopoly-spotlight-pause-play').once('panopoly-spotlight').bind('click.panopoly-widgets-spotlight', function(event) {
            event.preventDefault();
            if ($(this).hasClass('paused')) {
              start();
              $(this).text(Drupal.t('Pause'));
              $(this).removeClass('paused');
            }
            else {
              stop();
              $(this).text(Drupal.t('Play'));
              $(this).addClass('paused');
            }
          });
          if ($widget.find('.panopoly-spotlight-previous').length && $widget.find('.panopoly-spotlight-next').length) {
            $widget.find('.panopoly-spotlight-previous').once('panopoly-spotlight').bind('click.panopoly-widgets-spotlight', function (event) {
              event.preventDefault();
              $widget.find('.panopoly-spotlight-pause-play:not(.paused)').trigger('click.panopoly-widgets-spotlight');
              var activeControl = $($controls.filter('.active'));

              if (activeControl.prev().length != 0) {
                activeControl.prev().children('a').trigger('click.panopoly-widgets-spotlight');
              }
              else {
                $controls.last().children('a').trigger('click.panopoly-widgets-spotlight');
              }
            });
            $widget.find('.panopoly-spotlight-next').once('panopoly-spotlight').bind('click.panopoly-widgets-spotlight', function (event) {
              event.preventDefault();
              $widget.find('.panopoly-spotlight-pause-play:not(.paused)').trigger('click.panopoly-widgets-spotlight');
              var activeControl = $($controls.filter('.active'));

              if (activeControl.next().length != 0) {
                activeControl.next().children('a').trigger('click.panopoly-widgets-spotlight');
              }
              else {
                $controls.first().children('a').trigger('click.panopoly-widgets-spotlight');
              }
            });
          }

          start();
        });
      }
    }
  };

})(jQuery);
;
/**
 * @file
 * Javscript file for loading MZ Analytics tracking file.
 */

(function ($) {
  $(document).ready(function () {
    window.TES = window.TES || {};
    var pageMetadata = {};
    var a = document.getElementsByTagName('meta');
    for (var i = 0; i < a.length; i++) {
      var p = a[i].getAttribute("property");
      if (p) {
        p.toString();
        if (p.indexOf('mz') > -1) {
          var content = a[i].getAttribute("content");
          var mz_property = p.replace('mz:', '');
          pageMetadata[mz_property] = content.toLowerCase();
        }
      }
    }

    window.TES.pageMetadata = pageMetadata;
    window.TES.userMetadata = Drupal.settings.mz_variables.user_variables;
    window.TES.domain = Drupal.settings.mz_variables.mz_domain;

    function getCookie(name) {
      var re = new RegExp(name + "=([^;]+)");
      var value = re.exec(document.cookie);
      return (value != null) ? unescape(value[1]) : null;
    }

    if (getCookie('TESCookieUser')) {
      window.TES.userMetadata.id = getCookie('TESCookieUser');
    }

    // MZ is very specific about ordering so we load the script inside JS
    // Removed in favour of local caching.
    /*$.getScript(Drupal.settings.mz_variables.mz_script, function ()
     {
     _mz.emit(_mze.PAGE_VIEW);
     });*/

    // Allow the MZ script to be cached by the browser:
    // http://api.jquery.com/jQuery.getScript/
    jQuery.cachedScript = function (url, options) {
      // Allow user to set any option except for dataType, cache, and url.
      options = $.extend(options || {}, {
        dataType: "script",
        cache: true,
        url: url
      });
      // Use $.ajax() since it is more flexible than $.getScript.
      // Return the jqXHR object so we can chain callbacks.
      return jQuery.ajax(options);
    };

    // The actual call to get the script.
    $.cachedScript(Drupal.settings.mz_variables.mz_script).done(function (script, textStatus) {
      _mz.emit(_mze.PAGE_VIEW);
    });

    // @TODO This is a horrid temp solution for page views whilst we work out phase 2. We should improve this.
    $('a[href="#tab-ranking-dataset"],a[href="#tab-ranking-analysis"],a[href="#tab-ranking-methodology"]')
      .click(function() {
        googletag.pubads().refresh();
        window.TES.pageMetadata.type = 'informer';
        _mz.emit(_mze.PAGE_VIEW);
      });

    /**
     * Fires MZ Submit event when Save your basket was clicked.
     */
    $("#wur-lists-list-basket-form .form-submit").once('mz').on('click', function() {
      if (!$(".view-wur-list-basket").length) {
        return;
      }
      var list = $(".view-wur-list-basket .views-field-title a");
      var basket = [];
      $.each(list, function(i, e) {
        basket.push($(e).text());
      });
      _mz.emit(_mze.SUBMIT, {
        // eventTitle: "Add To List / Remove from List / Login Modal / Save List",
        eventTitle: $(this).val(),
        basketItems: basket,
        viewType: $(this).val()
      });
    });

    /**
     * Fires MZ Submit event when you register.
     */
    $("#user-register-form .form-submit").once('mz').on('click', function() {
      _mz.emit(_mze.SUBMIT, {
        eventTitle: 'user register',
        viewType: 'modal',
      });
        goog_snippet_vars = function () {
            var w = window;
            w.google_conversion_id = 1007358525;
            w.google_conversion_label = "Cia_CNWilGAQvaSs4AM";
            w.google_remarketing_only = false;
        }
        // DO NOT CHANGE THE CODE BELOW.
        goog_report_conversion = function (url) {
            goog_snippet_vars();
            window.google_conversion_format = "3";
            window.google_is_call = true;
            var opt = new Object();
            opt.onload_callback = function () {
                if (typeof(url) != 'undefined') {
                    window.location = url;
                }
            }
            var conv_handler = window['google_trackConversion'];
            if (typeof(conv_handler) == 'function') {
                conv_handler(opt);
            }
        }
        
    });
    /**
     * Fires MZ Submit event when you login.
     */
    $("#user-login .form-submit").once('mz').on('click', function() {
      _mz.emit(_mze.SUBMIT, {
        eventTitle: 'user login',
        viewType: 'modal',
      });
    });



    // For some reason, profiles do not attach behaviours, with little time spare - we'll have to manually init.
    // @TODO Investigate why behaviours aren't attaching for profiles and basket page.
    $('*[data-target="#add-to-list-modal"]').ready(function() {
      Drupal.attachBehaviors($('*[data-target="#add-to-list-modal"]'), Drupal.settings);
    });

    /**
     * Implements behaviours for adding MZ attributes to dynamic elements.
     */
    Drupal.behaviors.mzAnalyticsBehaviour = {
      attach: function (context) {

        // Add to list: Anonymous users.
        $('#datatable-1 tbody .loginmodal', context).once('mz').click(function() {
          // Register click with MZ.
          _mz.emit(_mze.CLICK, {
            eventAction: "Add to list",
            eventTitle: "Login Modal",
            id: $(this).closest('tr').data('nid')
          });
        });

        // Add to list: Authenticated users.
        // Use standard selector and if empty, check actual context element.
        var list_selector = $('.list-button-add, .list-button-remove', context);
        if (!list_selector.length && typeof $(context).attr('class') != 'undefined') {
          var classes = $(context).attr('class');
          if (classes.match('list-button-add|list-button-remove')) {
            list_selector = $(context);
          }
        }
        // Whoever won, this should still attach.
        if (list_selector.length) {
          $(list_selector).once('mz').on('click', _mz_add_to_list_auth_users);
        }

        // Save List modal.
        $("#add-to-list-modal .modal-body a", context).once('mz').on('click', _mz_add_to_list_save_list_modal);

        // THE WUR Table.
        $(".view-the-wur-datatables #edit-title").once('mz').on('blur', _mz_wur_search);
        $(".view-the-wur-datatables #edit-field-country-tid").once('mz').on('change',_mz_wur_search);
        $(".view-the-wur-datatables #edit-jump").once('mz').once('mz').on('change', _mz_wur_search);
        $(".view-the-wur-datatables input[name='display']").once('mz').on('change', _mz_wur_search);
        $(".view-the-wur-datatables select[name='datatable-1_length']").once('mz').on('change', _mz_wur_search);
        $(".view-the-wur-datatables .paginate_button").once('mz').on('click', function() {
          _mz_wur_search();
          // Also refresh ads for pagination changes.
          googletag.pubads().refresh();
        });


      }

    };



    /**
     * Helper function that reads the datatable choices.
     */
    _mz_wur_search = function() {
      var datatable = datatable || $("#datatable-1").DataTable();
      var settings = Drupal.settings.datatables["#datatable-1"];

      var order = datatable.order();
      var sort_by = settings.columns[order[0][0]].data;
      var sort_order = order[0][1];

      var countries = [];
      $(".view-the-wur-datatables #edit-field-country-tid option:selected").each(function(i, e) {
        countries.push($(e).text());
      });

      _mz.emit(_mze.SUBMIT, {
        eventTitle: 'search filter',
        filterPagination: datatable.page(),
        filterName: $(".view-the-wur-datatables #edit-title").val(),
        filterCountry: countries,
        filterYear: $("#ctools-jump-menu #edit-jump option:selected").text().trim(),
        viewType: $(".view-the-wur-datatables input[name='display']:checked").val(),
        sortOrder: sort_order,
        sortBy: sort_by,
        itemsPerPage: datatable.page.len()
      });
    }

    /**
     * Fires MZ Click event when logged in users add to list.
     */
    _mz_add_to_list_auth_users = function() {
      // The best place to get the entity id is on this link.
      var classes = $(this).attr('class').split(/\s+/);
      if (classes.length) {
        $.each(classes, function(i, item) {
          if (typeof entity_id == 'undefined') {
            if (item.indexOf('institution-id-') >= 0) {
              entity_id = item.replace('institution-id-', '');
            }
          }
        });
      }
      // We'll only create a click event if there's an entity ID, else it's useless.
      if (typeof entity_id != 'undefined') {
        _mz.emit(_mze.CLICK, {
          // eventTitle: "Add To List / Remove from List / Login Modal / Save List",
          eventTitle: $(this).attr('title'),
          id:entity_id
        });
      }
    };

    /**
     * Fires MZ Submit when the modal save list was clicked.
     */
    _mz_add_to_list_save_list_modal = function() {
      var titles = [];
      $(".view-wur-list-basket-modal .views-field-title a").each(function(i, e) {
        titles.push($(e).text());
      });
      _mz.emit(_mze.SUBMIT, {
        // eventTitle: "Add To List / Remove from List / Login Modal / Save List",
        eventTitle: $(this).attr('title'),
        basketItems: titles,
        id:  $(this).closest('tr').data('nid')
      });
    };


  });
}(jQuery));
;
