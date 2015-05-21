dashboard.controller('LinksGadgetController',
function($scope) {
  $scope.dialog = function(url, title) {
    $scope.modal = {
      'edit_mode': title,
      'post_url': url
    };
    $('#links-gadget-modal').modal();
  };
});
