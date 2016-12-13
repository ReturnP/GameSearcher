$(document).ready(function() {
    var submit_form = function() {
        $.getJSON($SCRIPT_ROOT + '/search', {
            title: $('input[name="searchPath"]').val()
        }, function(data) {
            $('#test').empty();
            for (i in data.result) {
                b = data.result[i]['id']
                $('#test').append('<li><a href="/displayGame/' + b + '">' + data.result[i]['name'] + "</a></li>")

            }


        });
        return false;
    };
    $('#sp').keyup(submit_form);
});
