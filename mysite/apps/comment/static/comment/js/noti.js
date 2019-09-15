$(function(){
    $(".noti_delete").click(function(){
        //从html获取相关字段
        let csrf = $(this).data('csrf');                 // html 里面写的data-*, 这里就写 *
        let ajax_url = $(this).data('ajax_url');
        let noti_id = $(this).data('noti_id');

        //设置post Json字段
        let post_data={
            "noti_id":noti_id,
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
                window.location.reload(); //刷新当前页面.
            },
            //{#请求失败回调函数#}
            error:function (data) {
                alert(data.msg);
            }
        });
    });

    $(".mark_read").click(function(){
        //从html获取相关字段
        let csrf = $(this).data('csrf');                 // html 里面写的data-*, 这里就写 *
        let ajax_url = $(this).data('ajax_url');
        let noti_id = $(this).data('noti_id');


        //设置post Json字段
        let post_data={
            "noti_id":noti_id,
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
                window.location.reload(); //刷新当前页面.
            },
            //{#请求失败回调函数#}
            error:function (data) {
                alert(data.msg);
            }
        });

    });

});


