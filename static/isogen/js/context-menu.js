var ContextMenu = {
    current:null,
    base:null,
    init:function(){
        ContextMenu.base = document.createElement("div");
        ContextMenu.base.className = "context-menu";
        ContextMenu.base.onclick = function (event) {
            event.stopPropagation();
        };

        document.addEventListener("click", function(){
            if(ContextMenu.current){
                document.body.removeChild(ContextMenu.current);
                ContextMenu.current = null;
            }
        });
    },
    /**
     *
     * @param mouseEvent
     * @param nodeList
     * @returns {boolean}
     *
     * Decription:  Creates a context menu and appends it to the body of the HTML doc.
     *              Requires the right-click mouse event and a list of HTML Elements
     *              that are to be included inb the context menu
     */
    create:function(mouseEvent, nodeList){
        mouseEvent.preventDefault();
        mouseEvent.stopPropagation();
        ContextMenu.close();

        if(!ContextMenu.base) ContextMenu.init();

        ContextMenu.current = ContextMenu.base.cloneNode(false);
        ContextMenu.appendNodes(nodeList);
        ContextMenu.current.style.left = event.pageX;
        ContextMenu.current.style.top = event.pageY;
        ContextMenu.current.zIndex = 99999999999999999;
        document.body.appendChild(ContextMenu.current);
        return false;
    },
    /**
     * Closes the current open context menu
     */
    close:function(){
        if(ContextMenu.current){
            document.body.removeChild(ContextMenu.current);
        }
    },
    /**
     * Do not call publicly, only internally used
     * @param nodeList
     */
    appendNodes:function(nodeList){
        var menuitemslen = nodeList.length;
        for(var i = 0; i<menuitemslen; i++){
            ContextMenu.current.appendChild(nodeList[i]);
        }
    },
    /**
     *
     * @param label
     * @param classname
     * @param onclick
     * @returns {Element}
     * Description: Creates a menu link (<a> element).  Requires the name of the link, any
     *              classnames the link should have, can be none, and the callback to execute
     *              when the link is clicked.
     */
    createMenuLink:function(label, classname, onclick){
        var link = document.createElement("a");
        link.innerHTML = label;
        link.className = classname;
        link.onclick = onclick;
        return link;
    },
    createLabel:function(text){
        var label = document.createElement('p');
        label.innerHTML = text;
        return label;
    }
};