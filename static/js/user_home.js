///**
// * Created by charleszhuochen on 11/01/2015.
// */
//$(document).ready(initPage);
//
//var csrftoken;
//
//function initPage(){
//    csrftoken = getCookie('csrftoken');
//    get_status_tw();
//}
//
//function show_add_follower(){
//    $("#post_div").hide();
//    $("#add_follower_div").show();
//}
//
//function add_follower_tw(){
//    var website_name, screen_name, follower_id;
//    //website_name = $("#website_name").val();
//    screen_name = $("#screen_name").val();
//    follower_id = $("#follower_id").val();
//    $.ajaxSetup({
//    beforeSend: function(xhr) {
//            xhr.setRequestHeader("X-CSRFToken", csrftoken);
//        }
//    });
//    $.post("/ChasingSomeone/add_follower_tw/",
//        {
//          //'website_name' : website_name,
//          'screen_name' : screen_name,
//          'follower_id' : follower_id,
//        }, function(data, status){
//        if (data == "True")
//        {
//            alert("success add Follower!")
//        }else
//        {
//            alert("sorry, we cannot find this user at Twitter:(")
//        }
//    });
//  }
//
//  function get_status_tw(){
//      $("#fresh_post_btn").attr("disabled","disabled");
//      var latest_post_id = $("div.post-info").first().attr("id");
//      var context_dict = {};
//      //alert(latest_post_id);
//      if (typeof latest_post_id != 'undefined')
//      {
//          context_dict = {id_latest_status: latest_post_id};
//      }
//
//
//      $.ajaxSetup({
//    beforeSend: function(xhr) {
//            xhr.setRequestHeader("X-CSRFToken", csrftoken);
//        }
//    });
//       $.post("/ChasingSomeone/get_status_tw/",
//           context_dict
//        , function(data, status){
//               $("#fresh_post_btn").removeAttr("disabled");
//        if(data == "False")
//         {
//             return;
//         }
//
//        //alert("Data: " + data + "\nStatus: " + status);
//        var tw_post_list = $.parseJSON(data);
//        //alert('<p class = "nickname">'+tw_post_list[0]['user']['screen_name']);
//               var list_len = tw_post_list.length;
//        for (var i = 0; i < list_len; i++) {
//            var back_index = list_len-1-i
//            var text = tw_post_list[back_index]['text'];
//            var screen_name = tw_post_list[back_index]['user']['screen_name'];
//            var profile_image_url_https = tw_post_list[back_index]['user']['profile_image_url_https'];
//            var created_at = tw_post_list[back_index]['created_at'];
//            var id = tw_post_list[back_index]['id'];
//
//            var post_div = '<div class="post-info" id="'+id+'">\
//                              <div class = "user-profile">\
//                        <img src="'+profile_image_url_https+'">\
//                        </div>\
//                        <div>\
//                    <p class = "nickname">'+screen_name+'</p>\
//                                    </div>\
//                                    <br>\
//                                    <div class = "post-date">'+created_at+'</div>\
//                                    <div class = "status">\
//                    <p class="status_text">'+text+'</p>\
//                </div>\
//                </div>';
//
//            $('#post_div').prepend(post_div);
//        }
//    });
//      $("#add_follower_div").hide();
//      $("#post_div").show();
//  }