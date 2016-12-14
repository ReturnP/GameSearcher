$(document).ready(function() {
    var submit_form = function() {
        console.log($('input[name="searchPath"]').val())
        $.getJSON($SCRIPT_ROOT + '/search', {
            title: $('input[name="searchPath"]').val()
        }, function(data) {
            $('#results').empty();
            for (i in data.result) {
                b = data.result[i]['id']
                image = '<li><img src="' + data.result[i]['cover']['url'] + '"/>'
                link = '<a href="/displayGame/' + b + '">' + data.result[i]['name'] + "</a></li>"
                $('#results').append(image + link)
            }

        });
        return false;
    };
    var timer
    $('#sp').keyup(function(){
        clearTimeout(timer);
        timer = setTimeout(function(){submit_form()}, 500);
    });
});
