(function () {

    var init = function() {
        $(".class-draggable").draggable({
            appendTo: 'body',
            revert: 'invalid',
            containment: '.schedule',
            helper: 'clone'
        });

        $(".class-schedule-droppable").droppable({
            drop: function(event, ui) {
                this.innerHTML = '';
                this.appendChild(ui.draggable[0]);
            }
        });

        $(".courses-droppable").droppable({
            drop: function(event, ui) {
                this.appendChild(ui.draggable[0]);
            }
        });
    };

    init();
}());