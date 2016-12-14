$(document).ready(function() {
    var submit_form = function() {
        console.log($('input[name="searchPath"]').val())
        $.getJSON($SCRIPT_ROOT + '/search', {
            title: $('input[name="searchPath"]').val()
        }, function(data) {
            $('#results').empty();
            for (i in data.result) {
                b = data.result[i]['id']
                $('#results').append('<li><a href="/displayGame/' + b + '">' + data.result[i]['name'] + "</a></li>")
            }
            /*for(i = 0; i < 3; i++){
                $('#test').append("123")
            }*/
        });
        return false;
    };
    var timer
    $('#sp').keyup(function(){
        clearTimeout(timer);
        timer = setTimeout(function(){submit_form()}, 500);
    });
});
