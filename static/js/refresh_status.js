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
    $("#btn_refresh_site").click(refresh_status_site_wrapper);
    $(".btn_refresh_flr").click(toogle_status_flr);
    $("#btn_refresh_flr").click(refresh_status_flr_wrapper);

}

function toogle_status_flr(){
    $(".btn_refresh_flr").removeAttr("disabled");
    $(this).attr("disabled", "disabled");
    $("#btn_refresh_flr").attr("data-flr_name",$(this).attr("data-flr_name"));
    var $div_status_list = $("#flr_div_status_list");
    $div_status_list.slideUp("slow");
    $div_status_list.empty();
    refresh_status_flr($(this));
    $div_status_list.fadeIn("slow");
}


function toggle_status_site(){
    toogle_disabled_btn($(this));
    $("#btn_refresh_site").attr("data-site_type",$(this).attr("data-site_type"));
    var $div_status_list = $("#div_status_list");
    $div_status_list.slideUp("slow");
    $div_status_list.empty();
    refresh_status_site($(this));
    $div_status_list.fadeIn("slow");
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

//action_type & target for quora
function refresh_status_site($btn_this){
    var site_type = $btn_this.attr("data-site_type");
    var data = {"site_type": site_type};
    var $div_status_list = $("#div_status_list");
    if (site_type = "twitter"){
        var since_id = $div_status_list.children().first().attr("id");
        if(typeof since_id != "undefined"){
            data['since_id'] = since_id;
        }
    }
    else if(site_type = "quora"){
        //var target = $div_status_list.children().first()
    }
    ajax_json(url_refresh_status_site, data, response_refresh_status_site, csrftoken);
}

function refresh_status_flr($btn_this){
    var flr_name = $btn_this.attr("data-flr_name");
    var data = {'flr_name': flr_name};
    ajax_json(url_refresh_status_flr, data, response_refresh_status_flr, csrftoken);
}

function refresh_status_site_wrapper(){
    refresh_status_site($(this));
}

function refresh_status_flr_wrapper(){
    refresh_status_flr($(this));
}

function response_refresh_status_site(data, status){
    var post_list = JSON.parse(data.responseText)['status_list'];
    if (post_list.length == 0){
        return;
    }
    var $div_status_list = $("#div_status_list");
    for(var i = post_list.length - 1; i >= 0; i--){
        if(post_list[i]['act_type'] == 'twitter'){
            var text = post_list[i]['text'];
            var screen_name = post_list[i]['user']['screen_name'];
            var url_profile_img = post_list[i]['user']['profile_image_url_https'];
            var time_stamp = post_list[i]['time_stamp'];
            var id = post_list[i]['id'];
            var div_new_post = new_status_item_tw(id, screen_name, url_profile_img, time_stamp, text);
            var wrap = document.createElement('div');
            wrap.appendChild(div_new_post.cloneNode(true));
            $div_status_list.prepend(wrap.innerHTML);
        }
        else if (post_list[i]['act_type'] == 'quora'){
            var user_name = post_list[i]['user_name'];
            var url_profile_img = post_list[i]['user_profile_image'];
            var action_type = post_list[i]['action_type'];
            var target = post_list[i]['target'];
            var url_target = post_list[i]['url'];
            var time_stamp = post_list[i]['time_stamp'];
            var div_new_post = new_status_item_qr(user_name,url_profile_img,action_type,target, url_target, time_stamp);
            var wrap = document.createElement('div');
            wrap.appendChild(div_new_post.cloneNode(true));
            $div_status_list.prepend(wrap.innerHTML);
        }
    }
}

function response_refresh_status_flr(data, status){
    var post_list = JSON.parse(data.responseText)['status_list'];
    if (post_list.length == 0){
        return;
    }
    var $div_status_list = $("#flr_div_status_list");
    for(var i = post_list.length - 1; i >= 0; i--){
        if(post_list[i]['act_type'] == 'twitter'){
            var text = post_list[i]['text'];
            var screen_name = post_list[i]['user']['screen_name'];
            var url_profile_img = post_list[i]['user']['profile_image_url_https'];
            var time_stamp = post_list[i]['time_stamp'];
            var id = post_list[i]['id'];
            var div_new_post = new_status_item_tw(id, screen_name, url_profile_img, time_stamp, text);
            var wrap = document.createElement('div');
            wrap.appendChild(div_new_post.cloneNode(true));
            $div_status_list.prepend(wrap.innerHTML);
        }
        else if (post_list[i]['act_type'] == 'quora'){
            var user_name = post_list[i]['user_name'];
            var url_profile_img = post_list[i]['user_profile_image'];
            var action_type = post_list[i]['action_type'];
            var target = post_list[i]['target'];
            var url_target = post_list[i]['url'];
            var time_stamp = post_list[i]['time_stamp'];
            var div_new_post = new_status_item_qr(user_name,url_profile_img,action_type,target, url_target, time_stamp);
            var wrap = document.createElement('div');
            wrap.appendChild(div_new_post.cloneNode(true));
            $div_status_list.prepend(wrap.innerHTML);
        }
    }
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
    div_post_title.appendChild(img);
    div_post_title.appendChild(div_screen_name);
    div_post_title.appendChild(div_time);


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

function new_status_item_qr(user_name, url_profile_img, action_type, target, url_target, time_stamp){
    var div_push_post = document.createElement("div");
    var div_post_title = document.createElement("div");
    var div_post_info = document.createElement("div");

    //for post title div
    div_post_title.setAttribute("class", "post-title");
    var img = document.createElement("img");
    var div_user_name = document.createElement("div");
    var div_time = document.createElement("div");
    img.setAttribute("src", url_profile_img);
    div_user_name.setAttribute("class", "name");
    div_time.setAttribute("class", "time");
    var user_name_text = document.createTextNode(user_name);
    var time_stamp_text = document.createTextNode(time_stamp);
    div_user_name.appendChild(user_name_text);
    div_time.appendChild(time_stamp_text);
    div_post_title.appendChild(img);
    div_post_title.appendChild(div_user_name);
    div_post_title.appendChild(div_time);

    //for post info div
    div_post_info.setAttribute("class", "post-info");
        //action type
    var div_action_type = document.createElement("div");
    var div_target = document.createElement("div");
    var div_url_target = document.createElement("div");

    div_action_type.setAttribute("class", "action-type");
    var action_type_text = document.createTextNode(action_type);
    div_action_type.appendChild(action_type_text);

    var target_text = document.createTextNode(target);
    div_target.appendChild(target_text);


    var label_url = document.createElement("label");
    var label_url_text = document.createTextNode("url:");
    label_url.appendChild(label_url_text);
    var a_url = document.createElement("a");
    a_url.setAttribute("href", url_target);
    var url_text = document.createTextNode(url_target);
    a_url.appendChild(url_text);

    div_url_target.appendChild(label_url);
    div_url_target.appendChild(a_url);

    div_post_info.appendChild(div_action_type);
    div_post_info.appendChild(div_target);
    div_post_info.appendChild(div_url_target);

    //for push post div
    div_push_post.setAttribute("class", "push-post-quora");
    div_push_post.appendChild(div_post_title);
    div_push_post.appendChild(div_post_info);

    return div_push_post;
}