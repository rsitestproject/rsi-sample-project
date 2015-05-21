(function (window) {

  $(function(){
    $("form.unique-post").on("submit", function (){
      if (this.submitted) {
        return false;
      }
      this.submitted = true;
    });
  });

})(window)
