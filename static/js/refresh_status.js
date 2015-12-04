/**
 * Created by charleszhuochen on 12/04/2015.
 */
$(document).ready(initRefreshPage);

var url_refresh_status_site = "/ChasingSomeone/refresh_status_site/";
var url_refresh_status_flr = "/ChasingSomeone/refresh_status_flr/";

function ajax_json(url, data, callback, csrftkn){
    $.ajaxSetup({
    beforeSend: function(xhr) {
            xhr.setRequestHeader("X-CSRFToken", csrftkn);
        }
    });
    $.ajax({
    url        : url,
    dataType   : 'json',
    contentType: 'application/json; charset=UTF-8',
    data       : JSON.stringify(data),
    type       : 'POST',
    complete   : callback
});
}

function initRefreshPage(){
    initCsrftoken();
    //$("div.socialnetwork").children("div.title").click(toggleSocialWork);
    //$("div.socialnetwork input.confirm-button").click(verify_account);
    //$("#btn_goto_add_follower").click(show_add_follower);
    //$("#btn_cancel_add_follower").click(hide_add_follower);
    //$("#btn_add_follower").click(add_follower);
    //$("#btn_save_accounts").click(save_accounts);
    //$("#follower_profile").find("div.add-hint").text(add_flr_hint);
    $("#btn_refresh_tw").click(toggle_status_site);
    $("#btn_refresh_qr").click(toggle_status_site);

}

function toggle_status_site(){
    toogle_disabled_btn($(this));
    var $div_status_list = $("#div_status_list");
    $div_status_list.slideUp("slow");
    $div_status_list.empty();
    refresh_status_site($(this));
    $div_status_list.slideDown("slow");
}

function toogle_disabled_btn($btn_this){
    var btn_value = $btn_this.text();
    if(btn_value == "Twitter"){
        $("#btn_refresh_tw").attr("disabled", "disabled");
        $("#btn_refresh_qr").removeAttr("disabled");
    }else if(btn_value == "Quora"){
        $("#btn_refresh_qr").attr("disabled", "disabled");
        $("#btn_refresh_tw").removeAttr("disabled");
    }
}

function refresh_status_site($btn_this){
    var site_type = $btn_this.attr("data-site_type");
    var data = {"site_type": site_type};
    ajax_json(url_refresh_status_site,data, response_refresh_status_site, csrftoken);
}

function response_refresh_status_site(data, status){
    var status_list = JSON.parse(data.responseText)['status_list'];

}

function new_status_item_tw(id, screen_name, url_profile_img, time_stamp, status_text){
    var div_push_post = document.createElement("div");
    var div_post_title = document.createElement("div");
    var div_post_info = document.createElement("div");

    //for post title div
    div_post_title.setAttribute("class", "post-title");
    var img = document.createElement("img");
    var div_screen_name = document.createElement("div");
    var div_time = document.createElement("div");
    img.setAttribute("src", url_profile_img);
    div_screen_name.setAttribute("class", "name");
    var screen_name_text = document.createTextNode(screen_name);
    div_screen_name.appendChild(screen_name_text);
    div_time.setAttribute("class", "time");
    var time_stamp_text = document.createTextNode(time_stamp);
    div_time.appendChild(time_stamp_text);

    //for post info div
    div_post_info.setAttribute("class", "post-info");
    var status_text_node = document.createTextNode(status_text);
    div_post_info.appendChild(status_text_node);

    //for push post div
    div_push_post.setAttribute("id", id);
    div_push_post.setAttribute("class", "push-post");
    div_push_post.appendChild(div_post_title);
    div_push_post.appendChild(div_post_info);

    //var wrap = document.createElement('div');
    //wrap.appendChild(div_push_post.cloneNode(true));
    //alert(wrap.innerHTML);
    return div_push_post;
}
