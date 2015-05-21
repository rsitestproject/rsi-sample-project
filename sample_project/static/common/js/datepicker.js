/*Date picker*/
$(function () {
  $.datepicker.setDefaults($.extend($.datepicker.regional['ja']));
  $(".datepicker").datepicker({
    dateFormat: 'yy/mm/dd',
    yearRange: '1981:2999',
    changeYear: false,
    changeYear: false,
    showMonthAfterYear: true
  });
});
