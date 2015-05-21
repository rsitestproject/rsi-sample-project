dashboard.controller('ImageDisplayGadgetController', ['$scope', '$upload',
function($scope, $upload) {
  $scope.dialog = function(url, title) {
    $scope.modal = {
      'edit_mode': title,
      'post_url': url
    };
    $('#image_display-gadget-modal').modal();
  };
  $scope.onFileDrop = function(post_url, $files) {
    if ($files.length > 0) {
      var csrftoken = $('input[name=csrfmiddlewaretoken]').val();
      var file = $files[0];
      $scope.upload = $upload.upload({
        url: post_url,
        data: {csrfmiddlewaretoken: csrftoken},
        fileFormDataName: 'data',
        file: file
      }).success(function(data, status, headers, config) {
        // 成功したら画面をリロード
        window.parent.location.reload();
      });
    }
  };
}]);
