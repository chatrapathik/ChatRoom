;(function(global){
  "use strict";
  window.chatroom = global;
  var $container = $(".side-bar"),
      ajaxCall = null;

  function init(){
    bindEvents();
    listUsers();
  }

  function postCall(url, data){
    return $.ajax({
            url: url,
            type: "POST",
            data: JSON.stringify(data),
            dataType: "json"
        });
  }


  function listUsers(q){
    if (ajaxCall){
      ajaxCall.abort();
    }
    var $spinnerTag = $container.find(".search-spinner");
    var $resultsTag = $container.find("#results");
    var $errortag = $container.find(".no-res");
    $errortag.addClass("no-display");
    $resultsTag.empty();
    var data = {};
    if (q){
      data.q = q;
    }
    $spinnerTag.removeClass("no-diaplsy");
    ajaxCall = postCall("/app/list_users", data);
    ajaxCall.done(function(resp){
      $spinnerTag.addClass("no-diaplsy");
      if (!resp.success){
        $errortag.removeClass("no-display");
        return;
      }
      $container.find("#results").append(resp.html);
    })
  }

  function searchResults(){
    var value = $(this).val();
    if (!value){
      listUsers()
      return;
    }
    listUsers(value)
  }

  function bindEvents(){
    $container.on("keyup", ".search", searchResults)
  }

  $(document).ready(function(){
    init();
  });
})(window.chatroom || {});
