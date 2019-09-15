let editor;
ClassicEditor
  .create( document.querySelector( '#_editor' ), {
   ckfinder: {
        uploadUrl: '/ckeditor/upload/'
    }
  } )
  .then( newEditor => {
     editor = newEditor;
  } )
  .catch( error => {
     console.error( error );
  } );

$(function(){
    let rep_to_id;
    let rep_to_username;
    let csrf;
    let article_id;
    let comment_id;
    let ajax_url;
    let new_url;

    $(".btn_comment").click(function(){
        let replyto = $(this).data('reply_to_username');
        comment_id = $(this).data('comment_id');
        editor.setData("[@"+ replyto + "] ：");

    });

    $(".btn_comment2").click(function(){
        comment_id = $(this).data('comment_id');
        reply_id = $(this).data('child_comment_id');
        rep_to_username = $(this).data('child_comment_owner');
        editor.setData("[@"+ rep_to_username + "] ：");

    });


    $("#comment_submit").click(function(){
        csrf = $(this).data('csrf');
        article_id = $(this).data('article_id');
        ajax_url = $(this).data('ajax_url');
        let content = editor.getData();
        if (content === '<p>&nbsp;</p>') {
            alert("内容太短了，多写点内容吧....");
            return;
        }

        $(this)[0].innerText = "提交中..";
        $(this)[0].disabled = true;

        //设置post Json字段
        let post_data={
        "article_id":article_id,
        "body":content,
        "parent_id":comment_id,
        "rep_to_id":rep_to_id,
        };

        $.ajaxSetup({
            data:{'csrfmiddlewaretoken': csrf }
        });

        $.ajax({
            url:ajax_url,
            type:'post',
            data:post_data,

            //{#请求成功回调函数#}
            success:function (data) {
                alert(data.msg);

                let new_url = window.location.href.split("#")[0];
                //window.location.reload(); //刷新当前页面.
                if (data.new_cmt_id) {
                    window.location.reload(); //刷新当前页面.
                    self.location.href = new_url + data.new_cmt_id;
                    return;
                }
                $('#comment_submit')[0].innerText = "提交";
                $('#comment_submit')[0].disabled = false;
            },
            //{#请求失败回调函数#}
            error:function (data) {
                alert(data.msg);
            }
        });

    });
})
