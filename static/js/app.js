function add_troop() {
    console.log("create post is working!")
    var form_data = $('#troop_modal_form').serialize();

    $.ajax({
        url : "/register/troop/",
        type : "POST",
        data : form_data,

        success : function(created_troop_json_string) {
            var parse = JSON.parse(created_troop_json_string);
            var created_troop_json = JSON.parse(parse);

            //Add created Council to troop select widget
            var register_select_widget = $("#id_scout-0-troop");
            register_select_widget.append('<option value=' + created_troop_json[0].pk +'>' + created_troop_json[0].fields.number + '</option>');
        },

        error : function(xhr,errmsg,err) {
            console.log(err);
        }
    });
};

$('#troop_submit_button').on('click', function() {
    event.preventDefault();
    console.log("form submitted!")
    add_troop();
});

function add_council() {
    console.log("create post is working!")
    var form_data = $('#council_modal_form').serialize();

    $.ajax({
        url : "/register/council/",
        type : "POST",
        data : form_data,

        success : function(created_council_json_string) {
            //Not sure why, but we need to parse this string twice to convert to JSON
            var parse = JSON.parse(created_council_json_string);
            var created_council_json = JSON.parse(parse);

            //Add created Council to troop select widget
            var troop_select_widget = $("#id_council");
            troop_select_widget.append('<option value=' + created_council_json[0].pk +'>' + created_council_json[0].fields.name + '</option>');
        },

        error : function(xhr,errmsg,err) {
            console.log("form submission error")
        }
    });
};

$('#council_submit_button').on('click', function() {
    event.preventDefault();
    console.log("form submitted!")
    add_council();
});

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        var csrftoken = $.cookie('csrftoken');
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});
