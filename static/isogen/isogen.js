/**
 * Created by ian on 12/29/16.
 */

window.addEventListener("load", highlightText);
window.addEventListener("load", initLoadImages);

function notification(text, closeable, classname){
    var notification = document.createElement("div");
    notification.className = "notification " + classname;
    if(closeable){
        var button = document.createElement("button");
        button.className = "delete";
        notification.appendChild(button);
    }
    notification.innerHTML += text;
    return notification;
}


function submitForm(event, form, on_success, on_fail){
    event.preventDefault();
    var url = form.getAttribute("action");
    var datastring = $(form).serialize();
    console.log(datastring, url);
    $.ajax({
        type: "POST",
        url: url,
        data: datastring,
        success: function(data) {
            console.log(data);
            var action = JSON.parse(data);
            if (action.success){
                on_success(action);
            }else{
                on_fail(action);
            }
        }
    });
}

function toggleLogin(){
    var logModal = document.getElementById('login');
    if (logModal.className.search(/is-active/) == -1){
        logModal.className += " is-active";
    }else{
        logModal.className = logModal.className.replace(/is-active/, "");
    }
}

function login(event, form){
    submitForm(event, form, function () {
        location.reload();
    }, function (data) {
        toggleLogin();
    })
}

function searchFor(){
    var query = document.getElementById("s").value;
    var baseurl = window.location.pathname.split("find")[0];
    window.location = baseurl + "find/" + query;
}

function highlightText(){
    if (typeof Search !== 'undefined'){
        if(Search){
            var text = document.getElementById('main-content').querySelectorAll(".searchable");
            var len = text.length;
            for(var i = 0; i<len; i++){
                text[i].innerHTML = text[i].innerHTML.replace(new RegExp("(" + Search + ")", "i") , "<a>$1</a>");
            }
        }

    }else{
        var sField = document.getElementById("s");
        sField.className += " is-disabled";
        sField.parentNode.querySelector("a").className += " is-disabled";
    }

}

function getCookie(name){
     var cookieValue = null;
     if (document.cookie && document.cookie != '') {
         var cookies = document.cookie.split(';');
         for (var i = 0; i < cookies.length; i++) {
             var cookie = cookies[i].trim();
             console.log(cookie.substring(0, name.length + 1));
             if (cookie.substring(0, name.length + 1) == (name + '=')) {
                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                 break;
             }
         }
     }
     return cookieValue;
}

function close_modal(modal_name){
    var modal = document.getElementById(modal_name);
    modal.classList.remove("is-active");
}

function open_modal(modal_name){
    var modal = document.getElementById(modal_name);
    modal.classList.add("is-active");
}

function setCookie(cname, cvalue, exdays) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays*24*60*60*1000));
    var expires = "expires="+ d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

function initLoadImages() {
    var imageLoaders = [...document.getElementsByClassName("display-on-load")];

    for(i = 0; i<imageLoaders.length; i++){
        console.log(imageLoaders[i]);
        imageLoaders[i].addEventListener("load", fadeInImage);

    }

}

function fadeInImage(element){
    // console.log(this);
    element.parentNode.style.backgroundImage = "url('" + element.src + "')";
    element.parentNode.style.opacity = 1;
    element.parentNode.removeChild(element);
}