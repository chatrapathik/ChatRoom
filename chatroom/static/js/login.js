;(function(global){
  "use strict";
  window.chatroom = global;
  var $container = $("#form-data"),
      pathValues = window.location.pathname.split("/").filter(Boolean),
      page = (pathValues.length === 2) ? pathValues[1] : "login",
      ajaxCall = null;

  function init(){
    bindEvents();
  }

  function postCall(url, data){
    return $.ajax({
            url: url,
            type: "POST",
            data: JSON.stringify(data),
            dataType: "json"
        });
  }

  function logIn(e){
    e.preventDefault();
    var email = $container.find(".email").val(),
        password = $container.find(".password").val();

    if (!email || !password) {
      handleError("Fill all the required fields");
      return;
    }

    var  params = {
        email: email,
        password: password
    };

    var url = "/app/login_user";
    ajaxCall = postCall(url, params);
    ajaxCall.done(function(resp){
      if(!resp.success){
        handleError(resp.message);
        return;
      }
      location.href = "/app/home?user=" + resp.user;
    }).fail(function(resp){
      handleError("Something went bad!!");
      return;
    });
  }

  function handleError(message) {
    var $errorTag = $container.find(".error-message");
    $errorTag.text(message);
    $errorTag.removeClass("no-display");
    setTimeout(function(){
      $errorTag.addClass("no-display");
    }, 3000);
  }

  function registration(e){
    e.preventDefault();
    var username = $container.find(".username").val(),
        lastname = $container.find(".username").val(),
        email = $container.find(".email").val(),
        password = $container.find(".password").val(),
        cPassword = $container.find(".confirm-pwd").val();

    if (!email || !password || !username || !lastname || !cPassword) {
      handleError("Fill all the required fields");
      return;
    }

    if (password !== cPassword){
      handleError("Password doesn't match");
      return;
    }

    var  params = {
        username: username,
        lastname: lastname,
        email: email,
        password: password
    };

    var url = "/app/register";
    ajaxCall = postCall(url, params);
    ajaxCall.done(function(resp){
      if(!resp.success){
        handleError(resp.message);
        return;
      }

      location.href = "/app/home";
    }).fail(function(resp){
      handleError("Something went bad!!");
      return;
    });
  }

  function bindEvents(){
    $container.on("click", ".login-button", logIn)
              .on("click", ".registration-button", registration)
  }

  $(document).ready(function(){
    init();
  });
})(window.chatroom || {});
