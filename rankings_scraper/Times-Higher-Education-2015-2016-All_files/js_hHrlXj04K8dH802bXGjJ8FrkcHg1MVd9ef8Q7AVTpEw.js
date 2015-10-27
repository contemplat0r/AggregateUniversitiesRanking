(function($) {
  Drupal.behaviors.panopolyImagesModule = {
    attach: function (context, settings) {
      var captions = $('.caption', context).has('img');
      $(captions).once('panopoly-images').imagesLoaded(function () {
        panopolyImagesResizeCaptionBox(captions);
      });

      function panopolyImagesResizeCaptionBox(captions) {
        captions.each(function() {
          var imageSet = $('img', this),
              imgBoxWidth = getImgWidth(imageSet),
              wrapperBoxWidth =
                  getWrapperSpacing($('.caption-inner', this))
                + getWrapperSpacing($('.caption-width-container', this)),
              totalWidth = imgBoxWidth + wrapperBoxWidth;
          $(this).width(totalWidth);
        });
      }

      // Get width of image plus margins, borders and padding
      function getImgWidth(imageSet) {
        var imgWidth = 0,
            imgBoxExtra = 0,
            testWidth = 0;
        var attrWidth;

        // We shouldn't have more than one image in a caption, but it would be
        // possible, so we make sure we have the widest one
        for (var i = 0; i < imageSet.length; i++) {
          // If we have a hardcoded width attribute from manual resizing in
          // TinMCE, use that. If not, use the image naturalWidth. We can't
          // reliably use width() for responsive images.
          attrWidth = $(imageSet[i]).attr("width");
          if (typeof attrWidth !== 'undefined') {
            // attr() returns a string. Must convert to int for math to work.
            testWidth = parseInt(attrWidth, 10);
          }
          else {
            testWidth = imageSet[i].naturalWidth;
          }
          if (testWidth > imgWidth) {
            imgWidth = testWidth;
            imgBoxExtra = getWrapperSpacing(imageSet[i])
          }
        }
        return imgWidth + imgBoxExtra;
      }

      // We want the total of margin, border and padding on the element
      function getWrapperSpacing(el) {
        var spacing = ['margin-left', 'border-left', 'padding-left', 'padding-right', 'border-right', 'margin-right'],
            totalPx = 0,
            spacePx = 0,
            spaceRaw = '';
        for (var i = 0; i < spacing.length; i++) {
          spaceRaw = $(el).css(spacing[i]);

          // Themers might add padding, borders or margin defined in ems, but we can't
          // add that to pixel dimensions returned by naturalWidth, so we just throw
          // away anything but pixels. Themers have to deal with that.
          if(spaceRaw && spaceRaw.substr(spaceRaw.length - 2) == 'px') {
            spacePx = parseInt(spaceRaw, 10);
            totalPx += ($.isNumeric(spacePx)) ? spacePx : 0;
          }
        }
        return totalPx;
      }
    }
  }
})(jQuery);
;
/**
 * @file
 * Javascript for MZ Analytics tracking External links.
 *
 * Click handler to track external links not altered by mz_analytics_preprocess_link().
 */

(function ($) {
  "use strict";

  $(document).ready(function() {
    // Select all 'a' elements with an absolute href;
    $("a[href^=\'http\'],a[href^=\'www\']")
      // And not already tagged with data-mz;
      .not("[data-mz]")
      // And not this domain;
      .not("[href*=\'" + window.location.hostname + "\']")
      // And not already processed.
      .not(".processed")
      .each(function(i, e) {
        // External links are tracked by simply adding "data-mz" to the link element.
        $(e).addClass("processed").attr({
          "data-mz": ""
        });
      });
  });

})(jQuery);
;
(function ($) {

 /**
   * UI Improvements for the Content Editing Form
   */
 Drupal.behaviors.panopolyAdmin = {
   attach: function (context, settings) {
     // Make the permalink field full width.
     var width = $('#node-edit #edit-title').width() - $('#node-edit .form-item-path-alias label').width() - $('#node-edit .form-item-path-alias .field-prefix').width() - 10;
     $('#node-edit .form-item-path-alias input').css('width', width);

     // Hide the body label in Javascript if requested, which allows the summary
     // Javacript to continue working.
     $('#node-edit .panopoly-admin-hide-body-label .form-item-body-und-0-value label', context)
      .once('panopoly-admin-hide-body-label')
      .wrapInner('<span class="element-invisible"></span>')
      .css('text-align', 'right');

     if ($('#node-edit .form-item-field-featured-image-und-0-alt label')) {
       $('#node-edit .form-item-field-featured-image-und-0-alt label').html('Alt Text');
     }
   }
 }

 /**
   * Automatically Upload Files/Images Attached
   */
 Drupal.behaviors.panopolyAutoUpload = {
    attach: function (context, settings) {
      $('#node-edit input#edit-field-featured-image-und-0-upload').next('input[type="submit"]').hide();
      $('form', context).delegate('#node-edit input#edit-field-featured-image-und-0-upload', 'change', function() {  
        $(this).next('input[type="submit"]').mousedown();
      }); 
    }
  };

  /**
   * Automatically fill in a menu link title, if possible.
   *
   * NOTE: This behavior is a copy and paste from the Core Menu module's menu.js
   * script. It has been adapted to update proper targeting. This brings back
   * the core functionality.
   */
  Drupal.behaviors.panopolyLinkAutomaticTitle = {
    attach: function (context) {
      $('.pane-node-form-menu', context).each(function () {
        // Try to find menu settings widget elements as well as a 'title' field in
        // the form, but play nicely with user permissions and form alterations.
        var $checkbox = $('.form-item-menu-enabled input', this);
        var $link_title = $('.form-item-menu-link-title input', context);
        var $title = $(this).closest('form').find('.form-item-title input');
        // Bail out if we do not have all required fields.
        if (!($checkbox.length && $link_title.length && $title.length)) {
          return;
        }
        // If there is a link title already, mark it as overridden. The user expects
        // that toggling the checkbox twice will take over the node's title.
        if ($checkbox.is(':checked') && $link_title.val().length) {
          $link_title.data('menuLinkAutomaticTitleOveridden', true);
        }
        // Whenever the value is changed manually, disable this behavior.
        $link_title.keyup(function () {
          $link_title.data('menuLinkAutomaticTitleOveridden', true);
        });
        // Global trigger on checkbox (do not fill-in a value when disabled).
        $checkbox.change(function () {
          if ($checkbox.is(':checked')) {
            if (!$link_title.data('menuLinkAutomaticTitleOveridden')) {
              $link_title.val($title.val());
            }
          }
          else {
            $link_title.val('');
            $link_title.removeData('menuLinkAutomaticTitleOveridden');
          }
          $checkbox.closest('fieldset.vertical-tabs-pane').trigger('summaryUpdated');
          $checkbox.trigger('formUpdated');
        });
        // Take over any title change.
        $title.keyup(function () {
          if (!$link_title.data('menuLinkAutomaticTitleOveridden') && $checkbox.is(':checked')) {
            $link_title.val($title.val());
            $link_title.val($title.val()).trigger('formUpdated');
          }
        });
      });
    }
  };

})(jQuery);
;
(function ($) {
  Drupal.behaviors.panopolyMagic = {
    attach: function (context, settings) {
 
      /**
       * Title Hax for Panopoly
       *
       * Replaces the markup of a node title pane with
       * the h1.title page element
       */
      if ($.trim($('.pane-node-title .pane-content').html()) == $.trim($('h1.title').html())) {
        $('.pane-node-title .pane-content').html('');
        $('h1.title').hide().clone().prependTo('.pane-node-title .pane-content');
        $('.pane-node-title h1.title').show();
      }
 
      // Focus on the 'Add' button for a single widget preview, after it's loaded.
      if (settings.panopoly_magic && settings.panopoly_magic.pane_add_preview_mode === 'single' && settings.panopoly_magic.pane_add_preview_subtype) {
        // Need to defer until current set of behaviors is done, because Panels
        // will move the focus to the first widget by default.
        setTimeout(function () {
          var link_class = 'add-content-link-' + settings.panopoly_magic.pane_add_preview_subtype.replace(/_/g, '-') + '-icon-text-button';
          $('#modal-content .panopoly-magic-preview-link .content-type-button a.' + link_class, context).focus();
        }, 0);
      }
    }
  };
})(jQuery);

(function ($) {
  // Used to only update preview after changes stop for a second.
  var timer;

  // Used to make sure we don't wrap Drupal.wysiwygAttach() more than once.
  var wrappedWysiwygAttach = false;

  // Triggers the CTools autosubmit on the given form. If timeout is passed,
  // it'll set a timeout to do the actual submit rather than calling it directly
  // and return the timer handle.
  function triggerSubmit(form, timeout) {
    var $form = $(form),
        preview_widget = $('#panopoly-form-widget-preview'),
        submit;
    if (!preview_widget.hasClass('panopoly-magic-loading')) {
      preview_widget.addClass('panopoly-magic-loading');
      submit = function () {
        $form.find('.ctools-auto-submit-click').click();
      };
      if (typeof timeout === 'number') {
        return setTimeout(submit, timeout);
      }
      else {
        submit();
      }
    }
  }

  // Used to cancel a submit. It'll clear the timer and the class marking the
  // loading operation.
  function cancelSubmit(form, timer) {
    var $form = $(form),
        preview_widget = $('#panopoly-form-widget-preview');
    preview_widget.removeClass('panopoly-magic-loading');
    clearTimeout(timer);
  }

  function onWysiwygChangeFactory(editorId) {
    return function () {
      var textarea = $('#' + editorId),
          form = textarea.get(0).form;

      if (textarea.hasClass('panopoly-textarea-autosubmit')) {
        // Wait a second and then submit.
        cancelSubmit(form, timer); 
        timer = triggerSubmit(form, 1000);
      }
    };
  }

  // A function to run before Drupal.wysiwygAttach() with the same arguments.
  function beforeWysiwygAttach(context, params) {
    var editorId = params.field,
        editorType = params.editor,
        format = params.format;

    if (Drupal.settings.wysiwyg.configs[editorType] && Drupal.settings.wysiwyg.configs[editorType][format]) {
      wysiwygConfigAlter(params, Drupal.settings.wysiwyg.configs[editorType][format]);
    }
  }

  // Wouldn't it be great if WYSIWYG gave us an alter hook to change the
  // settings of the editor before it was attached? Well, we'll just have to
  // roll our own. :-)
  function wysiwygConfigAlter(params, config) {
    var editorId = params.field,
        editorType = params.editor,
        onWysiwygChange = onWysiwygChangeFactory(editorId);

    switch (editorType) {
      case 'markitup':
        $.each(['afterInsert', 'onEnter'], function (index, funcName) {
          config[funcName] = onWysiwygChange;
        });
        break;

      case 'tinymce':
        config['setup'] = function (editor) {
          editor.onChange.add(onWysiwygChange);
          editor.onKeyUp.add(onWysiwygChange);
        }
        break;
    }
  }

  // Used to wrap a function with a beforeFunc (we use it for wrapping
  // Drupal.wysiwygAttach()).
  function wrapFunctionBefore(parent, name, beforeFunc) {
    var originalFunc = parent[name];
    parent[name] = function () {
      beforeFunc.apply(this, arguments);
      return originalFunc.apply(this, arguments);
    };
  }

  /**
   * Improves the Auto Submit Experience for CTools Modals
   */
  Drupal.behaviors.panopolyMagicAutosubmit = {
    attach: function (context, settings) {
      // Replaces click with mousedown for submit so both normal and ajax work.
      $('.ctools-auto-submit-click', context)
      // Exclude the 'Style' type form because then you have to press the
      // "Next" button multiple times.
      // @todo: Should we include the places this works rather than excluding?
      .filter(function () { return $(this).closest('form').attr('id').indexOf('panels-edit-style-type-form') !== 0; })
      .click(function(event) {
        if ($(this).hasClass('ajax-processed')) {
          event.stopImmediatePropagation();
          $(this).trigger('mousedown');
          return false;
        }
      });

      // e.keyCode: key
      var discardKeyCode = [
        16, // shift
        17, // ctrl
        18, // alt
        20, // caps lock
        33, // page up
        34, // page down
        35, // end
        36, // home
        37, // left arrow
        38, // up arrow
        39, // right arrow
        40, // down arrow
         9, // tab
        13, // enter
        27  // esc
      ];

      // Special handling for link field widgets. This ensures content which is ahah'd in still properly autosubmits.
      $('.field-widget-link-field input:text', context).addClass('panopoly-textfield-autosubmit').addClass('ctools-auto-submit-exclude');

      // Handle text fields and textareas.
      $('.panopoly-textfield-autosubmit, .panopoly-textarea-autosubmit', context)
      .once('ctools-auto-submit')
      .bind('keyup blur', function (e) {
        var $element;
        $element = $('.panopoly-magic-preview .pane-title', context);

        cancelSubmit(e.target.form, timer);

        // Filter out discarded keys.
        if (e.type !== 'blur' && $.inArray(e.keyCode, discardKeyCode) > 0) {
          return;
        }

        // Set a timer to submit the form a second after the last activity.
        timer = triggerSubmit(e.target.form, 1000);
      });

      // Handle WYSIWYG fields.
      if (!wrappedWysiwygAttach && typeof Drupal.wysiwygAttach == 'function') {
        wrapFunctionBefore(Drupal, 'wysiwygAttach', beforeWysiwygAttach);
        wrappedWysiwygAttach = true;

        // Since the Drupal.behaviors run in a non-deterministic order, we can
        // never be sure that we wrapped Drupal.wysiwygAttach() before it was
        // used! So, we look for already attached editors so we can detach and
        // re-attach them.
        $('.panopoly-textarea-autosubmit', context)
        .once('panopoly-magic-wysiwyg')
        .each(function () {
          var editorId = this.id,
              instance = Drupal.wysiwyg.instances[editorId],
              format = instance ? instance.format : null,
              trigger = instance ? instance.trigger : null;

          if (instance && instance.editor != 'none') {
            params = Drupal.settings.wysiwyg.triggers[trigger];
            if (params) {
              Drupal.wysiwygDetach(context, params[format]);
              Drupal.wysiwygAttach(context, params[format]);
            }
          }
        });
      }
  
      // Handle autocomplete fields.
      $('.panopoly-autocomplete-autosubmit', context)
      .once('ctools-auto-submit')
      .bind('keyup blur', function (e) {
        // Detect when a value is selected via TAB or ENTER.
        if (e.type === 'blur' || e.keyCode === 13) {
          // We defer the submit call so that it happens after autocomplete has
          // had a chance to fill the input with the selected value.
          triggerSubmit(e.target.form, 0);
        }
      });

      // Prevent ctools auto-submit from firing when changing text formats.
      $(':input.filter-list').addClass('ctools-auto-submit-exclude');

    }
  }
})(jQuery);
;
(function ($) {

 Drupal.behaviors.PanelsAccordionStyle = {
   attach: function (context, settings) {
     for ( region_id in Drupal.settings.accordion ) {
    		var accordion = Drupal.settings.accordion[region_id] ;
		    jQuery('#'+region_id).accordion(accordion.options);
  	 }
   }
  }

})(jQuery);
;
(function ($, Drupal, window, document, undefined) {

  $(document).ready(function(){
    var $pane = $('.pane-most-viewed-commented');
    var $titles = $pane.find('h2');
    var titleHeight = $titles.first().outerHeight();

    //
    $titles.click(function(){
      var $this = $(this);
      var $parent = $this.parent();
      var $content = $parent.find('.content');
      var $siblings = $parent.siblings();
      var $siblingsContent = $siblings.find('.content');

      // remove class from other blocks
      $siblings.removeClass('selected');

      // hide other content
      $siblingsContent.hide();

      // add class to this block
      $parent.addClass('selected');

      // show the content
      $content.show();

      // fix the height
      var newHeight = titleHeight + $content.height();
      $pane.css("min-height", newHeight);
    });

    // trigger a click on the first block to make sure it all starts correctly
    $titles.first().trigger('click');

  });

})(jQuery, Drupal, this, this.document);
;
/**
 * @file
 * JS to poorly enforce a paywall.
 */

(function ($, Drupal, window, document, undefined) {

  Drupal.behaviors.paywall = {
    attach: function(context, settings) {
      var $body = $('body');

      // Check if the page is paywalled.
      // Exit if it's not
      var paywalled = $body.attr('data-paywall');
      if (typeof paywalled === typeof undefined && paywalled !== true) {
        return false;
      }

      // Check if the logged in user has role to by pass the paywall
      var roleException = $body.attr('data-paywall-role-exception');
      if (roleException === "true") {
        return false;
      }

      // Some vars
      var cookieName = Drupal.settings.the_user_restrictions.cookie_name;
      var cookieLifetimeDays = Drupal.settings.the_user_restrictions.cookie_lifetime_days;
      var viewingLimit = Drupal.settings.the_user_restrictions.limit;
      var nid = $body.attr('data-nid');
      var paywallAllowedPanes = Array(
        'pane-page-title',
        'pane-node-field-standfirst',
        'pane-bylines-social-media',
        'pane-breaking-news-images-panel-pane-1',
        'pane-bylines-panel-pane-1',
        'pane-social-links',
        'article-metadata-date',
        'pane-paywall-cta'
      );
      var cookieSettings = {
        expires: cookieLifetimeDays,
        path: '/'
      };

      // Check for cookie
      var viewedNids = $.cookie(cookieName);

      // Set the first nid if the cookie does not exist
      if(viewedNids === null) {
        viewedNids = nid;
        // Add the nid to the cookie
        $.cookie(cookieName, viewedNids, cookieSettings);
        return false;
      }


      // Create an array of nids
      var viewedNidsArray = viewedNids.split(',');

      // If the nid is in the array exit
      if ($.inArray(nid, viewedNidsArray) != -1) {
        return false;
      }

      // Check if they have reached the viewing limit
      var numViewedArticles = viewedNidsArray.length;
      if (numViewedArticles < viewingLimit) {
        // Add the new nid to the list in the cookie
        viewedNids = viewedNids + ',' + nid;
        $.cookie(cookieName, viewedNids, cookieSettings);
        return false;
      }

      // If we've made it this far then the paywall is in affect.

      // Get the panes
      var $panes = $('.panel-pane');
      var $paywallMessagePane = $('.pane-paywall-message');

      // Hide everything that is not in the allowed pane list
      var paywallAllowedPanesSelector = '.' + paywallAllowedPanes.join(',.');
      $panes
        .not(paywallAllowedPanesSelector)
        .hide();

      // Show the paywall message pane
      $paywallMessagePane
        .show()
        .removeClass('element-invisible');

      $(".paywall-cta").show();
    }
  };

})(jQuery, Drupal, this, this.document);
;
(function ($, Drupal, window, document, undefined) {

  $(document).ready(function() {

    /**
     * The pane has a set height this will adjust the height of the pane to
     * match the height of the content in the iframe.
     *
     * @TODO This needs some later testing once it's on a TES environment
     * because CORs requests aren't allowed.
     */
    Drupal.comments_iframe_loaded = function() {
      var $pane = $('.pane-rating-comments');
      var $iframe = $pane.find('iframe');
      var $iframeBody = $iframe.contents().find('body');

      // Match the pane height the the iframe body
      $pane.height($iframeBody.height());
    };

  });

})(jQuery, Drupal, this, this.document);
;
/**
 * @file
 * JS to switch between ranking datasets.
 */

(function ($, Drupal, window, document, undefined) {

  Drupal.behaviors.wur_institution_dataset_list = {
    attach: function(context, settings) {

      // Check if we're on the page before going further
      var $dropdown_rankings = $('#ranking-types-list');
      if($dropdown_rankings.length == 0) {
        return false;
      }

      // Get/set some vars.
      var $dropdown_years = $('#ranking-years-list');
      var datasets = Drupal.settings.wur_institution_dataset_list.all;
      var path = Drupal.settings.wur_institution_dataset_list.path_alias;
      var generateNewPath = function generateNewPathF(path, nid) {
        return '/' + path + "?ranking-dataset=" + nid;
      };

      // Update the dataset to the new year.
      $dropdown_years.change(function(event) {
        var $this = $(this);
        var rankingValue = $dropdown_rankings.find("option:selected").text();
        var yearValue = $this.find("option:selected").text();
        var datasetNid = Object.keys(datasets[rankingValue][yearValue])[0];
        var newPath = generateNewPath(path, datasetNid);
        window.location.href = newPath;
      });

      // Update the year dropdown when the ranking type changes.
      $dropdown_rankings.change(function(){
        var $this = $(this);
        var ranking = $this.find("option:selected").text();
        var selectedYear = $dropdown_years.find("option:selected").text();

        // Change ranking to the selected year.  If no ranking exists for
        // that year go to the next most recent.
        var dataset = datasets[ranking][selectedYear];
        if(dataset != undefined) {
          var datasetNid = Object.keys(datasets[ranking][selectedYear])[0];
          var newPath = generateNewPath(path, datasetNid);
          window.location.href = newPath;
        } else {
          var yearsArray = Object.keys(datasets[ranking]);
          // Sort the array to deal with x-browser nuances around indexes
          yearsArray.sort();
          var numYears = yearsArray.length;
          var latestYearIndex = numYears - 1;
          var latestYear = yearsArray[latestYearIndex];
          var datasetNid = Object.keys(datasets[ranking][latestYear])[0];
          var newPath = generateNewPath(path, datasetNid);
          window.location.href = newPath;
        }
      });
    }
  };





})(jQuery, Drupal, this, this.document);
;
/**
 * @file
 * JavaScript integrations between the Caption Filter module and particular
 * WYSIWYG editors. This file also implements Insert module hooks to respond
 * to the insertion of content into a WYSIWYG or textarea.
 */
(function ($) {

$(document).bind('insertIntoActiveEditor', function(event, options) {
  if (options['fields']['title'] && Drupal.settings.captionFilter.widgets[options['widgetType']]) {
    options['content'] = '[caption caption="' + options['fields']['title'].replace(/"/g, '\\"') + '"]' + options['content'] + '[/caption]';
  }
});

Drupal.captionFilter = Drupal.captionFilter || {};

Drupal.captionFilter.toHTML = function(co, editor) {
  return co.replace(/(?:<p>)?\[caption([^\]]*)\]([\s\S]+?)\[\/caption\](?:<\/p>)?[\s\u00a0]*/g, function(a,b,c){
    var id, cls, w, tempClass;

    b = b.replace(/\\'|\\&#39;|\\&#039;/g, '&#39;').replace(/\\"|\\&quot;/g, '&quot;');
    c = c.replace(/\\&#39;|\\&#039;/g, '&#39;').replace(/\\&quot;/g, '&quot;');
    id = b.match(/id=['"]([^'"]+)/i);
    cls = b.match(/align=['"]([^'"]+)/i);
    ct = b.match(/caption=['"]([^'"]+)/i);
    w = c.match(/width=['"]([0-9]+)/);

    id = ( id && id[1] ) ? id[1] : '';
    cls = ( cls && cls[1] ) ? 'caption-' + cls[1] : '';
    ct = ( ct && ct[1] ) ? ct[1].replace(/\\\\"/,'"') : '';
    w = ( w && w[1] ) ? parseInt(w[1])+'px' : 'auto';

    if (editor == 'tinymce')
      tempClass = (cls == 'caption-center') ? 'mceTemp mceIEcenter' : 'mceTemp';
    else if (editor == 'ckeditor')
      tempClass = (cls == 'caption-center') ? 'mceTemp mceIEcenter' : 'mceTemp';
    else
      tempClass = '';

    if (ct) {
      return '<div class="caption ' + cls + ' ' + tempClass + ' draggable"><div class="caption-width-container" style="width: ' + w + '"><div class="caption-inner">' + c + '<p class="caption-text">' + ct + '</p></div></div></div>';
    }
    else {
      return '<div class="caption ' + cls + ' ' + tempClass + ' draggable"><div class="caption-width-container" style="width: ' + w + '"><div class="caption-inner">' + c + '</div></div></div>';
    }
  });
};

Drupal.captionFilter.toTag = function(co) {
  return co.replace(/(<div class="caption [^"]*">)\s*<div[^>]+>\s*<div[^>]+>(.+?)<\/div>\s*<\/div>\s*<\/div>\s*/gi, function(match, captionWrapper, contents) {
    var align;
    align = captionWrapper.match(/class=.*?caption-(left|center|right)/i);
    align = (align && align[1]) ? align[1] : '';
    caption = contents.match(/\<p class=\"caption-text\"\>(.*)\<\/p\>/);
    caption_html = (caption && caption[0]) ? caption[0] : '';
    caption = (caption && caption[1]) ? caption[1].replace(/"/g, '\\"') : '';
    contents = contents.replace(caption_html, '');

    return '[caption' + (caption ? (' caption="' + caption + '"') : '') + (align ? (' align="' + align + '"') : '') + ']' + contents + '[/caption]';
  });
};

})(jQuery);
;
