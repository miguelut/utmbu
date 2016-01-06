var SweetAssDragNDrop = {
    init: function() {
        $(".class-dragable").draggable({
            appendTo: 'body',
            revert: 'invalid',
            containment: '.schedule',
            helper: 'clone'
        });

        $(".class-dropable").droppable({
            drop: function(event, ui){
                this.appendChild(ui.draggable[0]);
            }
        });
    }
};

SweetAssDragNDrop.init();