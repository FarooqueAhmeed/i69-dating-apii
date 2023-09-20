window.addEventListener("load", function () {
    (function ($) {
      var paginator = $(".paginator");
      var list_per_page = $(
        '<select id=\'list_per_page_selector\'>\
          <option value="25">25</option>\
          <option value="50">50</option>\
          <option value="75">75</option>\
          <option value="100">100</option>\
          <option value="250">250</option>\
          </select>'
      );
      var url = new URL(window.location);
      var initial_list_per_page = url.searchParams.get("list_per_page");
      if (initial_list_per_page === null) {
        initial_list_per_page = 25;
      }
  
      console.log(initial_list_per_page);
      $(".paginator a").each(function () {
        var $this = $(this);
        var _href = $this.attr("href");
        if (_href !== "?all=") {
          $this.attr("href", _href + "&list_per_page=" + initial_list_per_page);
        }
      });
  
      paginator.append(list_per_page);
      if (initial_list_per_page === null) {
        $("#list_per_page_selector").val(25);
      } else {
        $("#list_per_page_selector").val(initial_list_per_page);
      }
      $("#list_per_page_selector").on("change", function (event) {
        url.searchParams.set("list_per_page", event.target.value);
        window.location.href = url.href;
      });
    })(django.jQuery);
  });
  