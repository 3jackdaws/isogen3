/**
 * Created by ian on 12/29/16.
 */
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
    console.log(query);
    window.location = "/directory/" + query;
}