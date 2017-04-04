/**
 * Created by ian on 12/29/16.
 */

window.addEventListener("load", highlightText);

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
    if (typeof Search !== "undefined"){
        if(Search.length > 0){
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
             // console.log(cookie.substring(0, name.length + 1));
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

function fadeInImage(element){
    // console.log(this);
    element.parentNode.style.backgroundImage = "url('" + element.src + "')";
    element.parentNode.style.opacity = 1;
    element.parentNode.removeChild(element);
}

function scrollToLocation(location, scrollDuration) {
    var cosParameter = (location - window.scrollY) / 2,
        scrollCount = 0,
        oldTimestamp = performance.now();
    function step (newTimestamp) {
        scrollCount += Math.PI / (scrollDuration / (newTimestamp - oldTimestamp));
        if (scrollCount >= Math.PI) window.scrollTo(0, location);
        if (window.scrollY === location) return;
        window.scrollTo(0, Math.round(cosParameter + cosParameter * Math.cos(scrollCount)));
        oldTimestamp = newTimestamp;
        window.requestAnimationFrame(step);
    }
    window.requestAnimationFrame(step);
}


function doScrolling(elementY, duration) {
  var startingY = window.pageYOffset
  var diff = elementY - startingY
  var start

  // Bootstrap our animation - it will get called right before next frame shall be rendered.
  window.requestAnimationFrame(function step(timestamp) {
    if (!start) start = timestamp
    // Elapsed miliseconds since start of scrolling.
    var time = timestamp - start
    // Get percent of completion in range [0, 1].
    var percent = Math.min(time / duration, 1)

    window.scrollTo(0, startingY + diff * percent)

    // Proceed with animation as long as we wanted it to.
    if (time < duration) {
      window.requestAnimationFrame(step)
    }
  })
}