var DragonDrop = {
    init: function() {
        $(".draggable-course").draggable({
            revert: "invalid"
        });
        $(".course-dropzones").droppable({
            drop: function(event, ui) {
                console.log("HELL YEAH DROPPED ON");
            }
        });
    }
};

DragonDrop.init();