if (navigator.userAgent.toLowerCase().indexOf('msie 8') >= 0) {
  $(function (){

    // emulate maxlength
    function limitValueLength(e) {
      var self = $(this);
      var maxlength = Number(self.attr('maxlength'));

      return (self.val().length < maxlength);
    }
    $('textarea[maxlength]').on('keypress', limitValueLength);
    $('textarea[maxlength]').on('keyup', limitValueLength);

    function rollbackPaste(e) {
      var self = $(this);
      var maxlength = Number(self.attr('maxlength'));
      var data = self.val();
      setTimeout(function() {
        if (self.val().length > maxlength) {
          self.val(data);
        }
      }, 10);
    }
    $('textarea[maxlength]').on('paste', rollbackPaste);

  });
}
