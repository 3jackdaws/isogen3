    console.info("Loaded Stcikynote.js");
    var NoteContainer = null;
    var StickyNotes = {};
    var HeldNote = null;
    var ContextMenuNodeLists = {};
    var NoteSocket = null;


    var zRatio;
    var GlobalZIndex = 0;

    function ConnectWebsocket(){
        var url = "wss://isogen.net:8000/ws/stickynotes/";
        NoteSocket = new WebSocket(url);
        NoteSocket.onmessage = function (evt) {
            var message = JSON.parse(evt.data);
            console.info(message);
            switch(message.action){
                case "alter":
                {
                    if(message.id in StickyNotes){
                        if (StickyNotes[message.id] != HeldNote){
                            StickyNotes[message.id].translate(message.x, message.y);
                            if(message.content !== 0)
                                StickyNotes[message.id].setContent(message.content);
                        }


                    }else{
                        var note = new StickyNote(message.content, message.x, message.y, ++GlobalZIndex, message.id, message.style)
                        StickyNotes[note.id] = note;
                        NoteContainer.appendChild(note.node);
                    }
                }
                break;

                case "delete":
                {
                    console.log("del");
                    if(message.id in StickyNotes){
                        var note = StickyNotes[message.id];
                        note.remove();
                    }
                }
                break;

                case "notify":
                {
                    console.log("notify");
                    Notification.Toast.message(message.text);
                }
            }
        }

        NoteSocket.onopen = function(){
            Notification.Toast.message("Connected", 1000);
            NoteSocket.send(JSON.stringify(
                {
                    "action":"fetch"
                }
            ))};


        NoteSocket.onerror = function(err){
            console.error(err);
        };

        NoteSocket.onclose = function () {
            Notification.Toast.message("Reconnecting...", 5000);
            setTimeout(ConnectWebsocket, 5000);
        };
    }

    window.addEventListener("load", function(){

        zRatio = screen.width/1200;
        if(!(zRatio < 1)) zRatio=1;
        console.log(zRatio);

        NoteContainer = document.getElementById("note-container");


        NoteContainer.addEventListener("contextmenu", function(event){
            ContextMenu.create(event, ContextMenuNodeLists['note-container']);
        });

        ConnectWebsocket();
    });

    ContextMenuNodeLists['note-container'] = [
        ContextMenu.createLabel("Sticky Notes"),
        ContextMenu.createMenuLink("New Note", "", function(){
            var x = ContextMenu.current.style.left;
            var y = ContextMenu.current.style.top;
            var note = StickyNote.createNew(x, y, GlobalZIndex++);
        }),

    ];



    document.body.addEventListener("mouseup", function(){
        if(HeldNote)
            HeldNote.putDown();
    });

    document.body.addEventListener("mousemove", function(event){
        if(HeldNote){
            HeldNote.hasChanged = true;
            var x = (event.pageX/zRatio + HeldNote.offsetX);
            var y = (event.pageY/zRatio + HeldNote.offsetY);
            HeldNote.setPosition(x, y);
        }
    });

    setInterval(function () {
        if(HeldNote){
            HeldNote.save();
        }
    }, 50);

    var StickyNote = function(content, x, y, z, id, style){

        this.node = document.createElement("textarea");
        this.node.className = "stickynote";
        this.id = id;
        this.hasChanged = false;
        this.setContent(content);
        this.node.style = style;
        this.setPosition(x,y,z);
        this.node['object'] = this;
        this.node.readOnly = true;
        this.node.onclick = function (event) {
            event.preventDefault();
        };
        var _this = this;

        this.node.onmousedown = function(event){
            HeldNote = this.object;
            HeldNote.offsetX = -(event.offsetX/zRatio);
            HeldNote.offsetY = -(event.offsetY/zRatio);
            this.style.zIndex = ++GlobalZIndex;
        };

        this.node.onblur = function(){
            this.classList.remove("editable");
            this.object.save();
            this.readOnly = true;
        };

        this.node.ondblclick = function(event){
            event.preventDefault();
            this.classList.add("editable");
            this.readOnly = false;
            this.select();
            this.focus();
            this.object.hasChanged = true;
        };

        var obj = this;

        this.node.oncontextmenu = function (event) {
            ContextMenu.create(event, noteContextNodes(obj));
        };

        this.node.style.transitionDuration = "0.2s";
        this.node.style.transitionProperty = "transform";
    };

    StickyNote.prototype.remove = function () {
        NoteContainer.removeChild(this.node);
    };
    
    StickyNote.prototype.setPosition = function (x,y,z) {
        this.node.style.left = x;
        this.node.style.top = y;
        if(z)
            this.node.style.zIndex = z;
    };

    StickyNote.prototype.putDown = function(){
        this.save();
        HeldNote = null;
    };
    
    StickyNote.prototype.setContent = function (content) {
        this.node.innerHTML = content;
    };

    StickyNote.prototype.translate = function (x,y) {
        var currentX = parseInt(this.node.style.left.slice(0,-2));
        var currentY = parseInt(this.node.style.top.slice(0,-2));

        var dx = x-currentX;
        var dy = y-currentY;
        var tform = "translate(" + dx + "px," + dy + "px)";
        this.node.style.transform = tform;
        // console.log(tform, x, dx, y, dy);

    }

    StickyNote.createNew = function (x,y,z) {
        NoteSocket.send(JSON.stringify(
            {
                "action":"new",
                "content":"",
                "style":"",
                "x":x,
                "y":y,
                "z":z
            }
        ));
    };

    StickyNote.prototype.save = function () {
        if(this.hasChanged){
            this.hasChanged = false;
            var message = {
                "action":"alter",
                "id":this.id,
                "content":this.node.value,
                "style":this.node.className,
                "x":this.node.style.left.slice(0,-2),
                "y":this.node.style.top.slice(0,-2),
                "z":this.node.style.zIndex
            };
            NoteSocket.send(JSON.stringify(message));
        }
    };

    StickyNote.prototype.signalDelete = function () {
        var message = {
                "action":"delete",
                "id":this.id
            };
        NoteSocket.send(JSON.stringify(message));
    };


    function noteContextNodes(note){
        var label = ContextMenu.createLabel("Note");
        var deletenote = ContextMenu.createMenuLink("Delete Note", "warning", function(){
            note.signalDelete();
        });

        return [label, deletenote];
    }

