function add_troop() {
    console.log("create post is working!")
    var form_data = $('#troop_modal_form').serialize();

    $.ajax({
        url : "/register/troop/",
        type : "POST",
        data : form_data,

        success : function(data) {
            console.log("success");
            console.log(data);
        },

        error : function(xhr,errmsg,err) {
            console.log(err);
        }
    });
};

$('#submit_button').on('click', function() {
    event.preventDefault();
    console.log("form submitted!")
    add_troop();
});

$('#test').on('click', function() {
    var select_widget = $("#id_council");
    console.log(select_widget.size());
    select_widget.append('<option value=' + (select_widget.length + 1) +'>DERP</option>');
});
