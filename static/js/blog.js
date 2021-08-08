$(function () {

  /* Functions */

  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-contactform .modal-content").html("");
        $("#modal-contactform").modal("show");
      },
      success: function (data) {
        $("#modal-contactform .modal-content").html(data.html_form);
      }
    });
  };

  var saveForm = function () {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          $("#modal-contactform .modal-content").html(data.html_successmessage);
        }
        else {
          $("#modal-contactform .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };


  /* Binding */

  // Send form
  $(".js-contact").click(loadForm);
  $("#modal-contactform").on("submit", ".js-contactform", saveForm);

});
