/**
 * Created by ian on 2/12/17.
 */

var Notification = {
    Toast:{
        baseNode:null,
        stack:[],
        message:function(text, timeout){
            if( ! timeout ) timeout = 3000;
            var toast = Notification.Toast.__getToastDivNode();
            toast.innerHTML = text;
            document.body.appendChild(toast);
            Notification.Toast.stack.push(toast);
            Notification.Toast.__removeToast(toast, timeout);
            return toast;
        },
        __getToastDivNode:function () {
            var toast = document.createElement("div");
            toast.classList.add("card");
            toast.classList.add("toast");
            return toast;
        },
        __removeToast:function (toast, timeout) {
            if(timeout == -1) return;
            setTimeout(function () {
                document.body.removeChild(toast);
            }, timeout);
        },
        remove:function(toast){
            if(document.body == toast.parentNode) document.body.removeChild(toast);
        }
    }

};