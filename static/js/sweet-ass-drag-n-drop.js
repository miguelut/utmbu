var SweetAssDragNDrop = {
    init: function() {
        $(".draggable-course").draggable({
            revert: "invalid"
        });

        $("#course-catalog-dropzone").droppable({
            drop: function(event, ui) {
                var droppedCourse = ui.draggable;
                var appendingList = $("#catalog-course-list");
                handleDrop(droppedCourse, appendingList);
            }
        });

        $("#added-course-dropzone").droppable({
            drop: function(event, ui) {
                var droppedCourse = ui.draggable;
                var appendingList = $("#added-course-list");
                handleDrop(droppedCourse, appendingList);
            }
        });

        function handleDrop(droppedCourse, list) {
            droppedCourse.detach()
                .css({right: 'auto', left: 'auto', top: 'auto'})
                .appendTo(list);
        }
    }
};

SweetAssDragNDrop.init();