/**
 * Created by charleszhuochen on 12/03/2015.
 */
/**
 * Created by charleszhuochen on 12/02/2015.
 */

$(document).ready(initFollowingPage);

var add_flr_hint = "set people name you want to follow:";
var b4_add_flr_hint = "success add follower, follower name is:";
var url_add_follower = "/ChasingSomeone/add_follower/";
var url_verify_account = "/ChasingSomeone/verify_account/";
var url_save_account = "/ChasingSomeone/save_account/";

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

function new_following_item(flr_name, flr_id, url_img){
        var div_fl_item = document.createElement("div");
        var div_profile_picture = document.createElement("div");
        var div_following_name = document.createElement("div");
        var a_href_to_more = document.createElement("a");
        //for profile picture
        div_profile_picture.setAttribute("class", "profile-picture");
        var img = document.createElement("img");
        img.setAttribute("src", url_img);
        div_profile_picture.appendChild(img);

        //for following name
        var flr_name_text = document.createTextNode(flr_name);
        div_following_name.appendChild(flr_name_text);
        div_following_name.setAttribute("class", "following-name");

        //for a href to more information
        var url_href = "/ChasingSomeone/follower_profile/"+flr_id+"/";
        a_href_to_more.setAttribute("href", url_href);
        var a_text = document.createTextNode("more information");
        a_href_to_more.appendChild(a_text);

        //for following item div
        div_fl_item.setAttribute("class", "following-item");
        div_fl_item.setAttribute("id", flr_id);
        div_fl_item.appendChild(div_profile_picture);
        div_fl_item.appendChild(div_following_name);
        div_fl_item.appendChild(a_href_to_more);

        //var wrap = document.createElement('div');
        //wrap.appendChild(div_fl_item.cloneNode(true));
        //alert(wrap.innerHTML);
        return div_fl_item;
}


function initFollowingPage(){
    initCsrftoken();
    $("div.socialnetwork").children("div.title").click(toggleSocialWork);
    $("div.socialnetwork input.confirm-button").click(verify_account);
    $("#btn_goto_add_follower").click(show_add_follower);
    $("#btn_cancel_add_follower").click(hide_add_follower);
    $("#btn_add_follower").click(add_follower);
    $("#btn_save_accounts").click(save_accounts);
    $("#follower_profile").find("div.add-hint").text(add_flr_hint);


}

function show_add_follower(){
    $("#follower_list").fadeOut();
    $("#add_section").slideDown();
}

function hide_add_follower(){
    var $input_flr_name = $("#follower_profile").find("input[name~='fname']");
    $input_flr_name.val("");
    $input_flr_name.removeAttr("disabled");
    $("#add_section").slideUp("slow");
    $("#follower_list").fadeIn();
}

function toggleSocialWork()
{
    $(this).next().slideToggle("slow");
}

function add_follower()
{
    var $flr_profile = $("#follower_profile");
    var flr_name = $flr_profile.find("input[name~='fname']").val();
    if (flr_name == ""){
        alert("please input follower name.");
        return;
    }
    $flr_profile.find("button[name~='add']").attr("disabled","disabled");
    var data = {"flr_name": flr_name};
    ajax_json(url_add_follower,data, response_add_follower, csrftoken);
}

function response_add_follower(data, status){
     var $flr_profile = $("#follower_profile");
    var $btn_add = $("#btn_add_follower");
    var $btn_cancel = $("#btn_cancel_add_follower");
    $btn_add.removeAttr("disabled");

    if (data.responseText == "False"){
        alert("Sorry, This follower already exist. Please change the name.");
        return;
    }
    var flr = JSON.parse(data.responseText);
    var new_flr_item = new_following_item(flr["flr_name"], flr["flr_id"], '../../static/img/profile_picture.png');
    document.getElementById("following_list").appendChild(new_flr_item);
    $btn_add.hide();
    $btn_cancel.hide();
    $flr_profile.find("input[name~='fname']").attr("disabled", "disabled");
    //alert(flr["flr_id"]);
    $flr_profile.find("div.add-hint").text(b4_add_flr_hint);
    $("#add_account_div").fadeIn();

}

function verify_account(){
    var act_type = $(this).attr("data-act_type");
    //alert(act_type);
    var data = {"act_type": act_type};
    switch(data.act_type){
        case "twitter":
            var screen_name = $(this).parent().find("#screen_name").val();
            if(screen_name == ""){
                alert("please input twitter user name");
                return;
            }
            data.screen_name = screen_name;
            break;
        case "quora":
            var user_name = $(this).parent().find("#user_name").val();
            if(user_name == ""){
                alert("please input quora user name");
                return;
            }
            data.user_name = user_name;
            break;
        default :
            return;
    }
    $(this).attr("disabled", "disabled");
    $(this).attr("value", "checking");
    $(this).css("background-color", "orangered");
    ajax_json(url_verify_account, data, response_verify_account($(this)), csrftoken);
}

function response_verify_account($btn_clicked){
    return function(data, status, jqXHR){
        $btn_clicked.removeAttr("disabled");
        if(data.responseText == "False"){
            alert("Sorry, this follower already have a "+$btn_clicked.attr("data-act_type")+" account in our system.");
            $btn_clicked.removeAttr("style");
            $btn_clicked.attr("value", "check");
            return;
        }
        if(data.responseText == "404"){
            alert("Sorry, this account doesn't exist.");
            $btn_clicked.removeAttr("style");
            $btn_clicked.attr("value", "check");
            return;
        }
        $btn_clicked.attr("value", "verified");
        $btn_clicked.css("background-color", "orange");
        $btn_clicked.attr("disabled", "disabled");
        var act_type = $btn_clicked.attr('data-act_type');
        if(act_type == "twitter"){
            $btn_clicked.parent().find("#screen_name").attr("disabled", "disabled");
        }
        else if(act_type == "quora"){
            $btn_clicked.parent().find("#user_name").attr("disabled", "disabled");
        }
        //$btn_clicked.removeAttr("style");
    };
}

function back_to_flr_list(){
    var $add_act_div = $("#add_account_div");
    $add_act_div.find("div.add-form").each(function(index, obj){

        var $btn_confirm =  $(this).find("input.confirm-button");
        $btn_confirm.removeAttr("style");
        $btn_confirm.removeAttr("disabled");
        $btn_confirm.attr("value", "check");
        var act_type = $btn_confirm.attr("data-act_type");
        switch(act_type){
            case "twitter":
                var $input_screen_name = $(this).find("#screen_name");
                $input_screen_name.val("");
                $input_screen_name.removeAttr("disabled");
                break;
            case "quora":
                var $user_name = $(this).find("#user_name");
                $user_name.val("");
                $user_name.removeAttr("disabled");
                break;
            default: return;
        }
        $(this).hide();
    });
    var $flr_profile = $("#follower_profile");
    $("#btn_add_follower").show();
    $("#btn_cancel_add_follower").show();
    $flr_profile.find("div.add-hint").text(add_flr_hint);
    $add_act_div.hide();

    hide_add_follower();
}

function save_accounts(){
    var $add_act_div = $("#add_account_div");
    $add_act_div.find("div.add-form:visible").each(function(index, obj){
        var $btn_confirm = $(this).find("input.confirm-button");
        var check_status = $btn_confirm.attr("value");
        if(check_status == "verified"){
            $btn_confirm.attr("value", "saving");
            $btn_confirm.css("background-color", "yellowgreen");
            var flr_name = $("#follower_profile").find("input[name~='fname']").val();
            var act_type = $btn_confirm.attr("data-act_type");
            var data = {"flr_name": flr_name,
                        "act_type": act_type};
            switch(data.act_type){
                case "twitter":
                    var screen_name = $(this).find("#screen_name").val();
                    data["screen_name"] = screen_name;
                    break;
                case "quora":
                    var user_name = $(this).find("#user_name").val();
                    data["user_name"] = user_name;
                    break;
                default :
                    return;
            }
            ajax_json(url_save_account, data, response_save_account($btn_confirm), csrftoken);
        }
    });
}

function response_save_account($btn_clicked){
    return function(data, status, jqXHR){
        if(data.responseText == "False"){
            alert("cannot save "+$btn_clicked.attr("data-act_type")+" account: follower doesn't exist or already have this kind account.");
            return;
        }
        if(data.responseText == "404"){
            alert("cannot save "+$btn_clicked.attr("data-act_type")+" account: this account does not exist.");
            return;
        }
        if(data.responseText == "True"){
            $btn_clicked.attr("value", "Saved");
            $btn_clicked.css("background-color", "green");
            trigger_b2_flr_list();
        }
    };
}

function trigger_b2_flr_list(){
    var loop_result = true;
        $("#add_account_div").find("div.add-form").each(function(){
        if($(this).find("input.confirm-button").attr("value") == "saving") {
            loop_result = false;
        }
    });
    if(loop_result == true){
        back_to_flr_list();
    }
}