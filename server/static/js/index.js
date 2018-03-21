$(document).ready(function () {
    $("#speed").myfunc({divFact:10});

    var socket = io.connect('http://' + document.domain + ':' + location.port + '/api');

    socket.on('pong', function(ms) {
        $("#latency").text(ms + ' ms');  // socket io periodically send ping to server, who responds with pong
    });

    socket.on('newdata', function (msg) {
        if(msg.hasOwnProperty('VehSpdAvgDrvn')){
            var gauge = $("#speed");
            gauge.val(msg.VehSpdAvgDrvn);
            gauge.trigger("change");
        }

        
		//console.log('AccPos ' + msg.AccPos);
		//console.log('BrkPdlPos ' + msg.BrkPdlPos);
		//console.log('TrnSwAct ' + msg.TrnSwAct);
		//console.log('TrnsShftLvrPos ' + msg.TrnsShftLvrPos);
		
        if(msg.hasOwnProperty('AccPos'))        { $("#acc").text(msg.AccPos); }
        if(msg.hasOwnProperty('BrkPdlPos'))     { $("#brake").text(msg.BrkPdlPos); }
        if(msg.hasOwnProperty('EngOilRmnLf'))   { $("#soc").text(msg.EngOilRmnLf); }
        if(msg.hasOwnProperty('PsngSysLat'))    { $("#lat").text(msg.PsngSysLat); }
        if(msg.hasOwnProperty('PsngSysLong'))   { $("#lon").text(msg.PsngSysLong); }


	    if(msg.hasOwnProperty('StrWhAng')) {
            msg.StrWhAng = msg.StrWhAng.startsWith('-') ? msg.StrWhAng.substring(1) : '-' +  msg.StrWhAng;
            $("#wheel").text(msg.StrWhAng);
        	$("#wheel_img").css('transform', 'rotate(' + msg.StrWhAng + 'deg)');
        }


        var leftlight = $("#leftlight button");
        var rightlight = $("#rightlight button");
        if (msg.hasOwnProperty('TrnSwAct') && msg.TrnSwAct == 1) {
            leftlight.css("background-color","red");
            rightlight.css("background-color","white");
        } else if (msg.hasOwnProperty('TrnSwAct') && msg.TrnSwAct == 2) {
            leftlight.css("background-color","white");
            rightlight.css("background-color","red");
        } else if (msg.hasOwnProperty('TrnSwAct')) {
            leftlight.css("background-color","white");
            rightlight.css("background-color","white");
        }


        if (msg.hasOwnProperty('TrnsShftLvrPos')) {
            for (var i = 1; i < 5; i++) {
                var gear = $("#gear button:nth-child(" + i + ")")
                gear.css("background-color", "white");
                if (i == msg.TrnsShftLvrPos) {
                    gear.css("background-color", "red");
                }
            }
        }

    });
    
//    var output = document.getElementById("steering-value");
//    var slider = document.getElementById("myRange");
//    output.innerHTML = slider.value;
//    slider.oninput = _.throttle(function () {
//        output.innerHTML = this.value;
//        socket.emit('slider', {'value': this.value});
//        console.log('slider send ' + this.value);
//    }, UPDATE_INTERVAL);

    //var accumulator = 0;
    //var id;
    //document.getElementById('car-break').onmousedown=function () {
     //   this.src = "static/break_pressed.png";
     //   id = setInterval(function () {
     //       socket.emit('break', {'value': accumulator++});
     //       console.log('break send' + accumulator);
     //       }, UPDATE_INTERVAL);
//
//    }

 //   document.getElementById('car-break').onmouseup=function() {
 //       this.src = "static/break.png";
 //       clearInterval(id);
 //       accumulator = 0;
 //   }
});
