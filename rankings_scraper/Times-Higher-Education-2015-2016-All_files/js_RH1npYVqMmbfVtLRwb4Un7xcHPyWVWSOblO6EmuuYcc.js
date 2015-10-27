(function(c,q){var m="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///ywAAAAAAQABAAACAUwAOw==";c.fn.imagesLoaded=function(f){function n(){var b=c(j),a=c(h);d&&(h.length?d.reject(e,b,a):d.resolve(e));c.isFunction(f)&&f.call(g,e,b,a)}function p(b){k(b.target,"error"===b.type)}function k(b,a){b.src===m||-1!==c.inArray(b,l)||(l.push(b),a?h.push(b):j.push(b),c.data(b,"imagesLoaded",{isBroken:a,src:b.src}),r&&d.notifyWith(c(b),[a,e,c(j),c(h)]),e.length===l.length&&(setTimeout(n),e.unbind(".imagesLoaded",
p)))}var g=this,d=c.isFunction(c.Deferred)?c.Deferred():0,r=c.isFunction(d.notify),e=g.find("img").add(g.filter("img")),l=[],j=[],h=[];c.isPlainObject(f)&&c.each(f,function(b,a){if("callback"===b)f=a;else if(d)d[b](a)});e.length?e.bind("load.imagesLoaded error.imagesLoaded",p).each(function(b,a){var d=a.src,e=c.data(a,"imagesLoaded");if(e&&e.src===d)k(a,e.isBroken);else if(a.complete&&a.naturalWidth!==q)k(a,0===a.naturalWidth||0===a.naturalHeight);else if(a.readyState||a.complete)a.src=m,a.src=d}):
n();return d?d.promise(g):g}})(jQuery);
;
/*

Licence:
==============================================================================

(c) 2011, Kaldor Holdings Ltd. All rights reserved.

Use in source and binary forms for commercially licensed Pugpig customers is governed by the Pugpig Software Licence Agreement at http://pugpig.com/download/licences/pugpig_licence_agreement.txt

For all other parties, use in source and binary forms is governed by the Pugpig Software Evaluation Agreement at http://pugpig.com/download/licences/pugpig_evaluation_agreement.txt

By downloading, reading and/or using this source, you agree to become a licensee of the Pugpig Software Suite and you are bound by the terms of the the licence agreement.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

 */
// Make all links with rel having external value open in new window
// For Drupal 7 to use jQuery $
(function($) {
  $(function() {
      $('a[rel*=external]').click( function() {
          window.open(this.href);
          return false;
      });
      $('#edit-field-pugpig-key-und-0-value').change(function() {
	  $this = $(this);
	  /*if ($this && $this.val() != '')
	      alert('Warning! Changing the key for a published edition could result in readers being unable to read this edition.');
      });*/
  });
    });


  function marketSummaryCSV($el, regex) {
    $el.val($el.val().replace(/(\n|\r)([-+–0-9])/mg, ' $2').replace(/(\t| )+/g, ' ').replace(regex, '$1,$2'));
  }

  function updateImageFieldLabels() {
    $('.image-widget-data label').each(function() {
      $el = $(this);
      switch ($el.text()) {
        case 'Alternate text ': $el.html('Caption'); break;
        case 'Title ': $el.html('Credit'); break;
      }
    });
  }

  $('body').ready(function() {
    theme_base = $('#theme_base').attr('data-url') + '/';
    $('#stay-link').bind('click', function() {
      $('#stay').val('here');
      $('#article-node-form').submit();
    });
    $('#edit-title').bind('change', function() {
      heading = $('#edit-field-heading-und-0-value');
      if (heading && heading.length > 0 && heading.val() == '')
        heading.val($(this).val());
    });
    $('#market-summary-node-form textarea').bind('paste', function() {
      var $el = $(this);
      if ($el.val() == '')
        setTimeout(function() {
          marketSummaryCSV($el, /([^-+–0-9])([-+–0-9]+\.[0-9]+)/g);
        }, 100);
    });
    $('#edit-field-market-sterling-und-0-value').bind('paste', function() {
      var $el = $(this);
      if ($el.val() == '')
        setTimeout(function() {
          $el.val($el.val().replace('g', '€'));
          marketSummaryCSV($el, /(.)([€$¥][0-9]+\.[0-9]+)/g);
        }, 100);
    });
    updateImageFieldLabels();

    if (document.addEventListener)
      document.addEventListener('DOMSubtreeModified', updateImageFieldLabels);
    else if (document.attachEvent)
      document.attachEvent('DOMSubtreeModified', updateImageFieldLabels);
  });

})(jQuery);

;
(function ($) {
    $(document).ready(function() {
        if (typeof Drupal.ajax != 'undefined') {
            Drupal.ajax.prototype.commands.show_modal = function (ajax, response, status) {
                $("#add-to-list-modal").modal("show");
            };
        }
    });



    //show-add-to-list
    Drupal.behaviors.showAddToList = {
        attach: function (context, settings) {
            if ($('.added-count-footer', context).length) {
                $('.added-count-footer').once('atl-footer', function() {
                    var added = $('.added-count-footer').text();
                    if (added == 0) {
                        $('.show-add-to-list').hide();
                    } else {
                        $('.show-add-to-list').show();
                    }
                });
            }
        }
    };
})(jQuery);
;
(function ($) {
    Drupal.behaviors.the_login_modal = {
        attach: function (context) {
            $("#loginModal", context).appendTo("body");
            $("#registerModal", context).appendTo("body");
        }
    };
})(jQuery);
;

(function($) {
  Drupal.behaviors.CToolsJumpMenu = {
    attach: function(context) {
      $('.ctools-jump-menu-hide')
        .once('ctools-jump-menu')
        .hide();

      $('.ctools-jump-menu-change')
        .once('ctools-jump-menu')
        .change(function() {
          var loc = $(this).val();
          var urlArray = loc.split('::');
          if (urlArray[1]) {
            location.href = urlArray[1];
          }
          else {
            location.href = loc;
          }
          return false;
        });

      $('.ctools-jump-menu-button')
        .once('ctools-jump-menu')
        .click(function() {
          // Instead of submitting the form, just perform the redirect.

          // Find our sibling value.
          var $select = $(this).parents('form').find('.ctools-jump-menu-select');
          var loc = $select.val();
          var urlArray = loc.split('::');
          if (urlArray[1]) {
            location.href = urlArray[1];
          }
          else {
            location.href = loc;
          }
          return false;
        });
    }
  }
})(jQuery);
;
/**
 * @file
 * Javascript for World University Rankings.
 */

/**
 * Standard Drupal wrapper for jQuery.
 *
 */
(function($, Drupal, window, document, undefined) {

  /**
   * Prepare and initialize the DataTables Plugin.
   *
   * Also performs all necessary event bindings and DOM alterations.
   */
  $(document).ready(function() {

    // Print the server side page if this is a google index.
    if (window.location.search.indexOf('_escaped_fragment_') >= 0) {
      return;
    }

    // Get the passed in Drupal settings for this instance.
    var selector = "#datatable-1";
    var drupal_settings = Drupal.settings.datatables[selector];

    // Provide custom render functions for Title and Add to List.
    drupal_settings.columns[3].render = customDtColumnTitleRender;
    // Add to list shoudl always be the last columm.
    var last_column = (drupal_settings.columns.length - 1);
    drupal_settings.columns[last_column].render = customDtColumnListRender;

    // Add in a draw callback for enabling behaviours.
    drupal_settings.drawCallback = function(settings) {
      Drupal.attachBehaviors($(".view-id-the_wur_datatables"), Drupal.settings);
    };

    // Add row callback for enhanced profiles.
    drupal_settings.rowCallback = function(row, data, index) {
      if (parseInt(data.field_institution_member_level) > 0) {
        $(row).addClass('enhanced');
      }
      // Add the institution id to each row, not sure why data() doesn't work?
      if (data.institution_entity) {
        $(row).attr('data-nid', data.institution_entity);
      }
    };

    // Set initial start and length from window hash.
    _the_wur_hash_navigation();

    // Tnitialize DataTables with our additional settings/handlers.
    datatable = $(selector).DataTable(drupal_settings);

    // Set default class on datatable.
    $('table#datatable-1').addClass('rank-only');

    // Update window hash on pagination.
    $(selector).on('page.dt', _update_window_hash);
    // Update window hash on length change.
    $(selector).on('length.dt', _update_window_hash);

    // Bind the column toggle as radio button or selects depending on device.
    var toggleCols = mobileColumnElements(drupal_settings);
    // As well as creating the mobile HTML, add a change handler to action toggle.
    $(toggleCols).insertBefore(selector).on('change', desktopColumnHandler);

    // Add a custom title search.
    $('#edit-title').on('keyup input',_the_wur_search_title);
    // Add in country search using jquery auto-complete.
    $('#edit-field-country-tid').on('change', _the_wur_search_country);

    // Prevent view filter from submitting.. hmmmm degradation?
    $("#views-exposed-form-the-wur-datatables-panel-pane-1").submit(function (event) {
      event.preventDefault();
    });
    // Remove views submit button.
    $(".views-exposed-widget.views-submit-button").remove();

    // Set chosen data placeholder to Countries.
    $('select#edit-field-country-tid').attr("data-placeholder", "Countries");

    // I dunno what this is meant to be but its not right.
    //$('select#edit-field-country-tid').data("chosen").default_text = "Countries";
    $('select#edit-field-country-tid').chosen();

    // Placeholder text for search form.
    $('#views-exposed-form-the-wur-datatables-panel-pane-1 #edit-title').data("placeholder", "Filter by name");
    $('#views-exposed-form-the-wur-datatables-panel-pane-1 #edit-title').attr("placeholder", "Filter by name");
    $('#views-exposed-form-the-wur-datatables-panel-pane-1 .chosen-choices input').data("placeholder", "Filter by country");
    $('#views-exposed-form-the-wur-datatables-panel-pane-1 .chosen-choices input').val("Filter by country");
    $('#views-exposed-form-the-wur-datatables-panel-pane-1 div.chosen-container li.search-field input').css({ width: '200px' });
    // Filter fields toggling on mobile.
    _mobile_filter_toggling();

    // Enable tooltips.
    $('[data-toggle="tooltip"]').tooltip();

    // Select current year.
    $("select#edit-jump option").filter(function() {
      return $.trim($(this).text()) == drupal_settings.year;
    }).prop('selected', true);

    // Hide WUR Dataset body, providing a toggle.
    _wur_body_text_toggle();
  });

  /**
   * Trigger Profile view when Row is clicked.
   */
  Drupal.behaviors.datatablesClickRow = {
    attach: function (context) {
      // Click handler for anonymous users adding to list, call the login modal - if it exists.
      $('#datatable-1 tbody .loginmodal', context).once('wur').click(function() {
        $('#registerModal').modal('show');
        return false;
      });
      // Click handler on the row for navigating to the profile.
      $('#datatable-1 tbody tr', context).once('wur').click(function() {
        window.location = $(this).find('td:nth-child(2) a').attr('href');
        return false;
      });
    }
  };

  /**
   * Generate elements for mobile column visibility.
   *
   * Helper function that interrogates the datatable settings and extracts the
   * Score and Stat columns for use as a filter.
   *
   * @param settings
   *
   * @constructor
   */
  mobileColumnElements = function(settings) {

    var toggleCols, wrapper;
    if (window.matchMedia("(max-width: 759px)").matches) {
      // Initialise a select element for Scores.
      var selectScores = $('<select id="mobile-toggle-scores" class="form-control form-select"></select>');
      $(selectScores).append($("<option></option>").text('Select..').val(""));

      // Initialise the select element for Stats.
      var selectStats = $('<select id="mobile-toggle-stats" class="form-control form-select"></select>');
      $(selectStats).append($("<option></option>").text('Select..').val(""));

      // Iterate the DataTable Columns to extract score and stat field.
      $.each(settings.columns, function(i, e) {
        // Scores.
        if (e.targets && e.targets.indexOf('score') > 0) {
          // Use the target (css class) as the index and name as value.
          $(selectScores).append(
            $("<option></option>").text(settings.aoColumnHeaders[i]).val(i)
          );
        }
        // Stats.
        if (e.targets && e.targets.indexOf('statistics') > 0) {
          // Use the target (css class) as the index and name as value.
          $(selectStats).append(
            $("<option></option>").text(settings.aoColumnHeaders[i]).val(i)
          );
        }
      });

      // Bind change event to show/hide columns for Scores.
      $(selectScores).on('change', mobileColumnHandler);
      // Bind change event to show/hide columns for Stats.
      $(selectStats).on('change', mobileColumnHandler);

      // Put the select elements inside a label tag.
      var scores = $('<label for="mobile-toggle-scores">Performance Breakdown</label>').append(selectScores);
      var stats = $('<label for="mobile-toggle-stats">Key Statistics *</label>').append(selectStats);

      // Wrap the selects in a div as per desktop version.
      wrapper = $('<div class="toggle-cols"></div>');
      $(wrapper).append(scores).append(stats);
    }
    else {
      // Desktop is much simpler, so just written inline.
      toggleCols = '<div class="toggle-cols"><i class="fa fa-times" id="hide-cols"></i>'
        + '<label for="rank_only"><input type="radio" name="display" id="rank_only" value="rank_only" checked="checked"><span>Rankings Only</span></label>'
        + '<label for="scores"><input type="radio" name="display" id="scores" value="scores"><span>Performance Breakdown</span></label>'
        + '<label for="stats"><input type="radio" name="display" id="stats" value="stats"><span>Key Statistics *</span></label>'
        + '</div>';
      // Wrap the selects in a div as per desktop version.
      wrapper = toggleCols;
    }

    return $(wrapper);
  };

  /**
   * Change handler for select elements that control the toggling of column visibility.
   */
  mobileColumnHandler = function() {
    // Get all checked values.
    var selected = $(this).find(':checked').val();
    var id = $(this).attr('id');

    // Hide all columns.
    datatable.columns('.stats').visible(false, false);
    datatable.columns('.scores').visible(false, false);

    // Reset the other select option to "please select".
    if (id == 'mobile-toggle-scores') {
      $('#mobile-toggle-stats').val("");
    }
    else if (id == 'mobile-toggle-stats') {
      $('#mobile-toggle-scores').val("");
    }
    // If option selected, show it.
    if (selected !== "") {
      $('table#datatable-1').addClass('details').removeClass('rank-only');
      datatable.columns(selected).visible(true, false);
      datatable.columns.adjust().draw(false);
    }
    else {
      $('table#datatable-1').addClass('rank-only').removeClass('details');
    }
  };

  /**
   * Handler that toggles the column visibility for desktop.
   */
  desktopColumnHandler = function() {
    var selected = $(this).find('[name="display"]:checked');
    var val = $(selected).val();
    // Apply and remove classes to parent labels for theming.
    $(this).find('label').removeClass('active');
    $(selected).closest('label').addClass('active');
    // Depending on the view selected, toggle the column visibility.
    // @see https://datatables.net/reference/type/column-selector.
    switch (val) {

      case "rank_only":
        datatable.columns('.scores').visible(false, false);
        datatable.columns('.stats').visible(false, false);
        datatable.columns.adjust().draw(false);
        $('table#datatable-1').addClass('rank-only').removeClass('details');
        break;

      case "scores":
        datatable.columns('.stats').visible(false, false);
        datatable.columns('.scores').visible(true, false);
        datatable.columns.adjust().draw(false);
        $('table#datatable-1').addClass('details').removeClass('rank-only');
        break;

      case "stats":
        datatable.columns('.scores').visible(false, false);
        datatable.columns('.stats').visible(true, false);
        datatable.columns.adjust().draw(false);
        $('table#datatable-1').addClass('details').removeClass('rank-only');
        break;
    }
  };

  /**
   * Provides a custom render for the Title Column in THE WUR.
   *
   */
  customDtColumnTitleRender = function(data, type, full, meta) {
    // Always return data when not of type display.
    if (type !== 'display') {
      return data;
    }
    var ret,
      country = full.field_country,
      dataset_nid = Drupal.settings.datatables["#datatable-1"].dataset_nid;
    ret = '<a href="' + full.path +'?ranking-dataset=' + dataset_nid + '">'
      + data + '</a><div class="country">' + country + '</div>';
    return ret;
  };

  /**
   * Provides a custom render for the Add to List column in the THE WUR.
   *
   */
  customDtColumnListRender = function(data, type, full, meta) {
    // Always return data when not of type display.
    if (type !== 'display') {
      return data;
    }

    // Set some vars and get the wur lists from the settings.
    var auth = {}, return_value = '',
      wur_lists = Drupal.settings.datatables["#datatable-1"].wur_lists;

    // If wur_list is undefined, then present a modal to anon user.
    if (typeof wur_lists === 'undefined') {
      return_value = $("<a />", {
        "href": "#",
        "text": "+",
        "data-toggle": "modal",
        "data-target": "#login-modal",
        "class": "loginmodal"
      }).prop('outerHTML');
    }
    else {
      // A list exists, create a base object with the common settings.
      var base_object = {
        "href": "/wur_list/" + full.institution_entity + "/add_to_list/nojs",
        "data-toggle": "modal",
        "data-target": "#add-to-list-modal"
      };
      // Extend the base object depending on whether this institution exists in the lists.
      if (wur_lists[full.institution_entity]) {
        auth = {
          text: "-",
          title: "Remove university from list",
          "class": "use-ajax list-button-remove institution-id-" + full.institution_entity
        };
      }
      else {
        auth = {
          text: "+",
          title: "Add university to list",
          "class": "use-ajax list-button-add institution-id-" + full.institution_entity
        };
      }
      // Merge the base and auth objects for our add/remove button.
      return_value = $("<a />", $.extend(base_object, auth)).prop('outerHTML');
    }
    return return_value;
  };

  /**
   * Get the hash values as an object.
   */
  get_hash = function() {
    var hash = location.href.substr(location.href.indexOf('#') + 1);
    var hashes_arr = hash.split('/');
    var hashes = {};
    $.map( hashes_arr, function(val, i) {
      if(val) {
        switch(val) {

          case 'page':
            hashes.page = parseInt(hashes_arr[i+1]);
            break;

          case 'length':
            hashes.length = parseInt(hashes_arr[i+1]);
            break;
        }
      }
    });
    return hashes;
  };

  /**
   * Synchronises the initial start and length from window hash.
   *
   */
  _the_wur_hash_navigation = function() {
    drupal_settings = Drupal.settings.datatables["#datatable-1"];
    var hashes = get_hash();
    if(hashes && hashes.page && hashes.length) {
      // Start is needed for initial pagination.
      var start = hashes.page * hashes.length;
      drupal_settings.displayStart = start;
      drupal_settings.pageLength = hashes.length;
    }
    else {
      // Set as first page and whatever pagelength is set to.
      window.location.hash = "!/page/0/length/" + drupal_settings.pageLength;
    }
  };

  /**
   * Helper function for updating window hash, as is shared.
   */
  _update_window_hash = function() {
    var info = datatable.page.info();
    window.location.hash = "!/page/" + info.page + "/length/" + info.length;
  };

  /**
   * Perform a datatable search on the views Title filter.
   *
   * Note: Views filters are disabled for THE WUR.
   */
  _the_wur_search_title = function() {
    /*
     * Bah.. table.search() works but table.columns([3,15]).search()
     * doesn't! i.e. when an array of cols is supplied:
     * datatable.columns(3).search($(this).val()).draw();
     * datatable.columns([3,15]).search($(this).val()).draw();
     */
    // This searches the whole darn file.. but it does work.
    datatable.search($(this).val(), false, false).draw();
  };

  /**
   * Perform a datatable search on the views Country filter.
   *
   * Note: Views filters are disabled for THE WUR.
   */
  _the_wur_search_country = function() {
    var items = [];
    $('#edit-field-country-tid option:selected').each(function () {
      // Push each value onto the array, spaces break the regex pattern by only matching
      // the word with the space (such as "Hong Kong"), use a period to denote any character.
      // Provide g (Global) modifier to replace all occurences.
      items.push($(this).text().replace(/ /g, '.'));
    });
    // Join by a pipe, as in regex for OR.
    var result = items.join('|');
    // The additional 1 parameter is to enable regex.
    datatable.column(4).search(result, 1).draw();
  };

  /**
   * Toggle filter fields on mobile view.
   */
  _mobile_filter_toggling = function() {
    if (window.matchMedia("(max-width: 759px)").matches) {

      // Toggle buttons.
      var toggleButtons = '<div class="view-toggle-buttons">'
        + '<button class="btn btn-default" id="rankings-toggle-view">Change View <i class="fa fa-angle-right"></i></button>'
        + '<button class="btn btn-default" id="rankings-toggle-filters">Filter <i class="fa fa-angle-right"></i></button></div>';
      $(toggleButtons).insertBefore('.view-the-wur-datatables .view-filters');
      $('.view-filters').prepend('<i class="fa fa-times" id="hide-filters"></i>').hide();

      // Handler for toggling "change view & filter" buttons.
      $('.view-toggle-buttons .btn').click(function() {
        $(this).find('.fa').toggleClass('fa-angle-right fa-angle-down');
      });
      // Handler for toggling Filter controls.
      $('#rankings-toggle-filters').click(function() {
        $('.view-filters').slideToggle('slow');
      });
      // Handler for toggling Column Visibility controls.
      $('#rankings-toggle-view').click(function() {
        $('.toggle-cols').slideToggle('slow');
      });
      // Handler for hiding Filter toggle.
      $('#hide-filters').click(function() {
        $(this).parent().hide();
        $('#rankings-toggle-filters .fa').toggleClass('fa-angle-right fa-angle-down');
      });
      // Handler for hiding Column toggle.
      $('#hide-cols').click(function() {
        $(this).parent().hide();
        $('#rankings-toggle-view .fa').toggleClass('fa-angle-right fa-angle-down');
      });

    }
  };

  /**
   * Hides WUR Dataset body and provides a toggle.
   */
  _wur_body_text_toggle = function() {
    if($(".rankings-dataset-body p")) {
      var paragraph, first_stop, teaser, bodytext;
      paragraph = $(".rankings-dataset-body p").prop('innerHTML');
      // Get all text up to the first full stop.
      first_stop = paragraph.indexOf(".");
      teaser = paragraph.substr(0, first_stop+1);
      // Apply this text before the original message.
      $(".pane-node-body").prepend(teaser);
      // Get the rest of the text, which will be applied back to the original body.
      bodytext = paragraph.substr(first_stop+1, paragraph.length);
      $(".rankings-dataset-body p").html(bodytext);
      // Signify the paragraph which is collapsible.
      $(".rankings-dataset-body p").attr('id', "collapse_text").addClass('collapse');
      // Add link for toggling.
      $(".rankings-dataset-body").append('<a href="#collapse_text" data-toggle="collapse"><i class="fa fa-caret-down"></i></a>');
      // When toggling, show different message.
      $(".rankings-dataset-body p").on("hide.bs.collapse", function(){
        $("[data-toggle='collapse'] i").toggleClass('fa-caret-down fa-caret-up');
      });
      $(".rankings-dataset-body p").on("show.bs.collapse", function(){
        $("[data-toggle='collapse'] i").toggleClass('fa-caret-down fa-caret-up');
      });
    }
  };

})(jQuery, Drupal, this, this.document);
;
(function($) {
  Drupal.behaviors.chosen = {
    attach: function(context, settings) {
      settings.chosen = settings.chosen || Drupal.settings.chosen;

      // Prepare selector and add unwantend selectors.
      var selector = settings.chosen.selector;

      // Function to prepare all the options together for the chosen() call.
      var getElementOptions = function (element) {
        var options = $.extend({}, settings.chosen.options);

        // The width default option is considered the minimum width, so this
        // must be evaluated for every option.
        if ($(element).width() < settings.chosen.minimum_width) {
          options.width = settings.chosen.minimum_width + 'px';
        }
        else {
          options.width = $(element).width() + 'px';
        }

        // Some field widgets have cardinality, so we must respect that.
        // @see chosen_pre_render_select()
        if ($(element).attr('multiple') && $(element).data('cardinality')) {
          options.max_selected_options = $(element).data('cardinality');
        }

        return options;
      };

      // Process elements that have opted-in for Chosen.
      // @todo Remove support for the deprecated chosen-widget class.
      $('select.chosen-enable, select.chosen-widget', context).once('chosen', function() {
        options = getElementOptions(this);
        $(this).chosen(options);
      });

      $(selector, context)
        // Disabled on:
        // - Field UI
        // - WYSIWYG elements
        // - Tabledrag weights
        // - Elements that have opted-out of Chosen
        // - Elements already processed by Chosen
        .not('#field-ui-field-overview-form select, #field-ui-display-overview-form select, .wysiwyg, .draggable select[name$="[weight]"], .draggable select[name$="[position]"], .chosen-disable, .chosen-processed')
        .filter(function() {
          // Filter out select widgets that do not meet the minimum number of
          // options.
          var minOptions = $(this).attr('multiple') ? settings.chosen.minimum_multiple : settings.chosen.minimum_single;
          if (!minOptions) {
            // Zero value means no minimum.
            return true;
          }
          else {
            return $(this).find('option').length >= minOptions;
          }
        })
        .once('chosen', function() {
          options = getElementOptions(this);
          $(this).chosen(options);
        });
    }
  };
})(jQuery);
;
