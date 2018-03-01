var UPDATE_INTERVAL = 500;
$(document).ready(function () {
    $("#speed").myfunc({divFact:10});

    var socket = io.connect('http://' + document.domain + ':' + location.port + '/api');
    socket.on('newdata', function (msg) {
        var gauge = $("#speed");
        gauge.val(msg.speed);
        gauge.trigger("change");
    });
    var output = document.getElementById("steering-value");
    var slider = document.getElementById("myRange");
    output.innerHTML = slider.value;
    slider.oninput = _.throttle(function () {
        output.innerHTML = this.value;
        socket.emit('slider', {'value': this.value});
        console.log('slider send ' + this.value);
    }, UPDATE_INTERVAL);

    var accumulator = 0;
    var id;
    document.getElementById('car-break').onmousedown=function () {
        this.src = "static/break_pressed.png";
        id = setInterval(function () {
            socket.emit('break', {'value': accumulator++});
            console.log('break send' + accumulator);
            }, UPDATE_INTERVAL);

    }

    document.getElementById('car-break').onmouseup=function() {
        this.src = "static/break.png";
        clearInterval(id);
        accumulator = 0;
    }
});

