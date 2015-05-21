dashboard.controller('InformationGadgetController',
function($scope) {
  $scope.dialog = function(url, title) {
    $scope.modal = {
      'edit_mode': title,
      'post_url': url
    };
    $('#information-gadget-modal').modal();
  };
});
