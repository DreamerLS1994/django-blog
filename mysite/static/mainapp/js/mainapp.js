let height=$(window).height();
 $(window).scroll(function(){
      if ($(window).scrollTop()>height){
         $(".top").fadeIn(50);
      }else{
         $(".top").fadeOut(50);
      }
 });
function returnTop(){
    $('body,html').animate({scrollTop:0},500);
}

$(function(){
    $('#my-article-body img').click(function(){
      let _this = $(this);//当前的img传入
      $('#myModal img')[0].src = _this[0].src;
      //展示模组框
      $('#myModal').modal('show');

    });

    $('[data-toggle="tooltip"]').tooltip()

});


$(function(){
    $("#btn_like_article").click(function(){
        //从html获取相关字段
        let csrf = $(this).data('csrf');                 // html 里面写的data-*, 这里就写 *
        let ajax_url = $(this).data('ajax_url');
        let articleid = $(this).data('article-id');

        //设置post Json字段
        let post_data={
            "this_articleid":articleid,
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
                //alert(data);
            },
            //{#请求失败回调函数#}
            error:function (data) {
                alert(data.msg);
            }
        });
    });

});
function show_date_time() {
    window.setTimeout("show_date_time()", 1000);
    let BirthDay = new Date("2018/12/21 08:08:08"); //建站日期
    let today = new Date();
    let timeold = (today.getTime() - BirthDay.getTime());
    let sectimeold = timeold / 1000;
    let  secondsold = Math.floor(sectimeold);
    let  msPerDay = 24 * 60 * 60 * 1000;
    let  e_daysold = timeold / msPerDay;
    let daysold = Math.floor(e_daysold);
    let e_hrsold = (daysold - e_daysold) * -24;
    let  hrsold = Math.floor(e_hrsold);
    let  e_minsold = (hrsold - e_hrsold) * -60;
    let  minsold = Math.floor((hrsold - e_hrsold) * -60);
    let  seconds = Math.floor((minsold - e_minsold) * -60);
    webtime.innerHTML = "本网站已运行  " + daysold + "天" + hrsold + "小时" + minsold + "分" + seconds + "秒";
}
