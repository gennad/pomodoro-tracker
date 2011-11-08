$(document).ajaxSend(function(event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});

function start_pomadoro() {
    $.ajax({
        type:"POST",
        url:'/pomadoro/start/',
        data:{},
        success: function(data){
            $('#active_pomadoro').html(data.html);
            $('#inactive_pomadoro').css('display', 'none');
            $('#active_pomadoro').css('display', 'block');
        },
        error: function(a, b, c) {
            alert(a);
        }
    });
}

function squash_pomadoro() {
    $.ajax({
        type:"POST",
        url:'/pomadoro/squash/',
        data:{},
        success: function(data){
            if (data.success = true) {
                $('#active_pomadoro').css('display', 'none');
                $('#inactive_pomadoro').css('display', 'block');
                return;
            }
            else {
                alert('FAIL');
            }
        }
    });
}

function count() {
    var seconds = $('#seconds').text();
    var minutes = $('#minutes').text();
    seconds = parseInt(seconds, 10);
    minutes = parseInt(minutes, 10);

    seconds--;
    if (seconds < 0) {
        seconds = '59';
        minutes--;
        if (minutes < 0) {
            $('#active_pomadoro').css('display', 'none');
            $('#inactive_pomadoro').css('display', 'block');
            return;
        }
    }

    seconds = seconds.toString();
    minutes = minutes.toString();

    if (seconds.length < 2) seconds = '0' + seconds;
    if (minutes.length < 2) minutes = '0' + minutes;

    $('#seconds').text(seconds);
    $('#minutes').text(minutes);
}
