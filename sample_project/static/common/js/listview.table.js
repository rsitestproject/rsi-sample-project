$(function () {
  /**
   * Grid.jsを適用する
   * tableの外側のboxに付いているdata-fix-colsをGridのパラメータとして引き渡す
   * 高さ指定は別の場所で行う
   */
  $(".grid-table").each(function() {
    var obj = $(this);
    var param = {
      srcType: "dom",
      srcData: this.querySelector('table'),
      allowSelections: true,
    };
    if (obj.data('fix-cols')) {
      param.fixedCols = obj.data('fix-cols');
    }
    new Grid(this, param);
    $('.g_Cl>div:nth-child(even)').addClass('stripe-even')
  });

  /**
   * ページジャンプ
   */
  $('.page-jump').on('submit', function (){
    var url = $(this).data('url');
    var page = $('.page-jump-input').val();
    if (!page) { return }
    url += '&page=' + page;
    window.location = url;
    return false;
  });

  /**
   * 複数選択リストの操作メニュー
   */
  function checked_ids() {
    var ids = [];
    $("input.selected-object[type=checkbox]:checked").each(function (){
      ids.push($(this).data('pk'));
    });
    return ids
  }

  function action_redirect(){
    var url = $(this).data('url');
    var ids = checked_ids();
    if (ids.length > 1){
      alert('この操作は複数の行に対しては実行できません。');
      return;
    } else if (ids.length == 0) {
      alert('行を選択して下さい。');
      return
    }
    window.location = url + '?pk=' + ids[0];
  }
  $(".action-menu .action-update").on('click', action_redirect);
  $(".action-menu .action-detail").on('click', action_redirect);

  function action_duplicate(){
    var url = $(this).data('url');
    var ids = checked_ids();
    if (ids.length > 1){
      alert('この操作は複数の行に対しては実行できません。');
      return;
    } else if (ids.length == 0) {
      alert('行を選択して下さい。');
      return
    }
    window.location = url + '?_original_pk=' + ids[0];
  }
  $(".action-menu .action-duplicate").on('click', action_duplicate);

  function action_delete_multi(){
    var url = $(this).data('url');
    var ids = checked_ids();
    if (ids.length == 0) {
      alert('行を選択して下さい。');
      return
    }
    url += '?';
    ids.forEach(function(pk) { url += '&pk=' + pk;})
    window.location = url;
  }
  $(".action-menu .action-delete-multi").on('click', action_delete_multi);


});


