var SweetAssDragNDrop = {
    init: function() {
        $(".draggable-course").draggable({
            revert: 'invalid',
            appendTo: 'body',
            helper: 'clone'
        });

        $("#course-catalog-dropzone").droppable({
            drop: function(event, ui) {
                var droppedCourse = ui.draggable;
                var appendingList = $("#catalog-course-list");
                $.post(
                    "http://localhost:8000/scout/unenroll_course/",
                    {'course_instance_id': droppedCourse.attr('id')},
                    function(data) {
                        handleDrop(droppedCourse, appendingList);
                    }
                ).error(function() {
                    ui.draggable.draggable('option', 'revert', true);
                });
            }
        });

        $("#added-course-dropzone").droppable({
            drop: function(event, ui) {
                var droppedCourse = ui.draggable;
                var appendingList = $("#added-course-list");
                $.post(
                    "http://localhost:8000/scout/enroll_course/",
                    {'course_instance_id': droppedCourse.attr('id')},
                    function(data) {
                        handleDrop(droppedCourse, appendingList);
                    }
                ).error(function() {
                    ui.draggable.draggable('option', 'revert', true);
                });
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