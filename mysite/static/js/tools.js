$(function(){
    $("#btn_like_tool").click(function(){
        //从html获取相关字段
        let csrf = $(this).data('csrf');                 // html 里面写的data-*, 这里就写 *
        let ajax_url = $(this).data('ajax_url');
        let tool_id = $(this).data('tool_id');
        console.log(tool_id);
        //设置post Json字段
        let post_data={
            "this_toolid":tool_id,
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
                //window.location.reload(); //刷新当前页面.
                //alert(data);
            },
            //{#请求失败回调函数#}
            error:function (data) {
                //alert(data.msg);
            }
        });
    });

});

