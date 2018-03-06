var UPDATE_INTERVAL = 500;
$(document).ready(function () {
    $("#speed").myfunc({divFact:10});

    var socket = io.connect('http://' + document.domain + ':' + location.port + '/api');
    socket.on('newdata', function (msg) {
        var gauge = $("#speed");
        gauge.val(msg.VehSpdAvgDrvn);
        gauge.trigger("change");
        
		//console.log('AccPos ' + msg.AccPos);
		//console.log('BrkPdlPos ' + msg.BrkPdlPos);
		//console.log('TrnSwAct ' + msg.TrnSwAct);
		//console.log('TrnsShftLvrPos ' + msg.TrnsShftLvrPos);
		
        $("#acc").text(msg.AccPos);
        $("#brake").text(msg.BrkPdlPos);
        $("#soc").text(msg.EngOilRmnLf);
        $("#lat").text(msg.PsngSysLat);
        $("#lon").text(msg.PsngSysLong);
        $("#wheel").text(msg.StrWhAng);
        
	if(msg.StrWhAng != undefined && msg.StrWhAng != null) {
                if (!msg.StrWhAng.startsWith('-')) {
                    msg.StrWhAng = '-' +  msg.StrWhAng;
                } else {
                    msg.StrWhAng = msg.StrWhAng.substring(1);
                }
        	$("#wheel_img").css('transform', 'rotate(' + msg.StrWhAng + 'deg)');
        }

        var leftlight = $("#leftlight button");
        var rightlight = $("#rightlight button");
        leftlight.css("background-color","white");
        rightlight.css("background-color","white");
        
        if (msg.TrnSwAct == 1) {
            leftlight.css("background-color","red");
        } else if (msg.TrnSwAct == 2) {
            rightlight.css("background-color","red");
        }

        for (var i = 1 ; i < 5; i++) {
            var gear = $("#gear button:nth-child(" + i + ")")
            gear.css("background-color","white");
            if (i == msg.TrnsShftLvrPos) {
                gear.css("background-color","red");
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

