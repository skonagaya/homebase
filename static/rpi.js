var isFocused = true;
var pollID;
var pollRate = 5000;
var checkLocked = false;

function onBlur() {
    if (isFocused) {
        //alert("blurred");
        clearInterval(pollID);
        isFocused = false;
        //$('#menu').hide( "blind" );
    }
    //document.body.className = 'blurred';
};
function onFocus(){
    if (!isFocused) {
        //alert("focused")
        isFocused = true;
        pollID = setInterval(function() {
            now = new Date().getTime();
            checkStates();
            lastFired = now;
        }, pollRate);
    }
    //document.body.className = 'focused';
};

if (/*@cc_on!@*/false) { // check for Internet Explorer
    document.onfocusin = onFocus;
    document.onfocusout = onBlur;
} else {
    window.onfocus = onFocus;
    window.onblur = onBlur;
}
pollID = setInterval(function() {
    now = new Date().getTime();
    checkStates();
    lastFired = now;
}, pollRate);

function sendSignal(toChannel){
    jQuery.ajax({
            type: "POST",
            data: {
                channel : toChannel, 
                state: "",
                mode: "signal"
            },
            success: function(data) {
                alert('done');

            },
    });
}

function initData(){


    jQuery.ajax({
            type: "POST",
            data: {
                channel : "", 
                state: "",
                mode: "check"
            },
            success: function(data) {

                if (data["ch1"] == "0") {
                    document.getElementById('ch1').checked = false;
                } else {document.getElementById('ch1').checked = true;}
                if (data["ch2"] == "0") {
                    document.getElementById('ch2').checked = false;
                } else {document.getElementById('ch2').checked = true;}
                if (data["ch3"] == "0") {
                    document.getElementById('ch3').checked = false;
                } else {document.getElementById('ch3').checked = true;}
                if (data["pir"] == "0") {
                    document.getElementById('pir').checked = false;
                } else {document.getElementById('pir').checked = true;}

                if (data["ch1on"] == "0") {
                    document.getElementById('ch1on').checked = false;
                    $("label[for='ch1on']").hide()
                } else {
                    document.getElementById('ch1on').checked = true;
                    setTime = data["ch1on"].trim().split(":")
                    hour = pad(setTime[0],2);
                    minute = pad(setTime[1],2);
                    $("#pickerch1on").combodate('setValue',hour+":"+minute);
                    $("#containerch1on").css("right","80px");
                    $("#containerch1on select").attr('disabled','disabled');
                }
                if (data["ch2on"] == "0") {
                    document.getElementById('ch2on').checked = false;
                    $("label[for='ch2on']").hide()
                } else {
                    document.getElementById('ch2on').checked = true;
                    setTime = data["ch2on"].trim().split(":")
                    hour = pad(setTime[0],2);
                    minute = pad(setTime[1],2);
                    $("#pickerch2on").combodate('setValue',hour+":"+minute);
                    $("#containerch2on").css("right","80px");
                    $("#containerch2on select").attr('disabled','disabled');
                }
                if (data["ch3on"] == "0") {
                    document.getElementById('ch3on').checked = false;
                    $("label[for='ch3on']").hide()
                } else {
                    document.getElementById('ch3on').checked = true;
                    setTime = data["ch3on"].trim().split(":")
                    hour = pad(setTime[0],2);
                    minute = pad(setTime[1],2);
                    $("#pickerch3on").combodate('setValue',hour+":"+minute);
                    $("#containerch3on").css("right","80px");
                    $("#containerch3on select").attr('disabled','disabled');
                }
                if (data["piron"] == "0") {
                    document.getElementById('piron').checked = false;
                    $("label[for='piron']").hide()
                } else {
                    document.getElementById('piron').checked = true;
                    setTime = data["piron"].trim().split(":")
                    hour = pad(setTime[0],2);
                    minute = pad(setTime[1],2);
                    $("#pickerpiron").combodate('setValue',hour+":"+minute);
                    $("#containerpiron").css("right","80px");
                    $("#containerpiron select").attr('disabled','disabled');
                }

                if (data["ch1off"] == "0") {
                    document.getElementById('ch1off').checked = false;
                    $("label[for='ch1off']").hide()
                } else {
                    document.getElementById('ch1off').checked = true;
                    setTime = data["ch1off"].trim().split(":")
                    hour = pad(setTime[0],2);
                    minute = pad(setTime[1],2);
                    $("#pickerch1off").combodate('setValue',hour+":"+minute);
                    $("#containerch1off").css("right","80px");
                    $("#containerch1off select").attr('disabled','disabled');
                }
                if (data["ch2off"] == "0") {
                    document.getElementById('ch2off').checked = false;
                    $("label[for='ch2off']").hide()
                } else {
                    document.getElementById('ch2off').checked = true;
                    setTime = data["ch2off"].trim().split(":")
                    hour = pad(setTime[0],2);
                    minute = pad(setTime[1],2);
                    $("#pickerch2off").combodate('setValue',hour+":"+minute);
                    $("#containerch2off").css("right","80px");
                    $("#containerch2off select").attr('disabled','disabled');
                }
                if (data["ch3off"] == "0") {
                    document.getElementById('ch3off').checked = false;
                    $("label[for='ch3off']").hide()
                } else {
                    document.getElementById('ch3off').checked = true;
                    setTime = data["ch3off"].trim().split(":")
                    hour = pad(setTime[0],2);
                    minute = pad(setTime[1],2);
                    $("#pickerch3off").combodate('setValue',hour+":"+minute);
                    $("#containerch3off").css("right","80px");
                    $("#containerch3off select").attr('disabled','disabled');
                }
                if (data["piroff"] == "0") {
                    document.getElementById('piroff').checked = false;
                    $("label[for='piroff']").hide()
                } else {
                    document.getElementById('piroff').checked = true;
                    setTime = data["piroff"].trim().split(":")
                    hour = pad(setTime[0],2);
                    minute = pad(setTime[1],2);
                    $("#pickerpiroff").combodate('setValue',hour+":"+minute);
                    $("#containerpiroff").css("right","80px");
                    $("#containerpiroff select").attr('disabled','disabled');
                }


                //$('#menu').show( "blind" );
            },
    });
}

function checkStates(){

    if (checkLocked) {
        return;
    }

    jQuery.ajax({
            type: "POST",
            data: {
                channel : "", 
                state: "",
                mode: "check"
            },
            success: function(data) {
                if (checkLocked) {
                    return;
                }

                if (data["ch1"] == "0") {
                    document.getElementById('ch1').checked = false;
                } else {document.getElementById('ch1').checked = true;}
                if (data["ch2"] == "0") {
                    document.getElementById('ch2').checked = false;
                } else {document.getElementById('ch2').checked = true;}
                if (data["ch3"] == "0") {
                    document.getElementById('ch3').checked = false;
                } else {document.getElementById('ch3').checked = true;}

                if (data["ch1on"] == "0") {
                    document.getElementById('ch1on').checked = false;
                } else {
                    document.getElementById('ch1on').checked = true;
                    setTime = data["ch1on"].trim().split(":")
                    hour = pad(setTime[0],2);
                    minute = pad(setTime[1],2);
                    $("#pickerch1on").combodate('setValue',hour+":"+minute);
                }
                if (data["ch2on"] == "0") {
                    document.getElementById('ch2on').checked = false;
                } else {
                    document.getElementById('ch2on').checked = true;
                    setTime = data["ch2on"].trim().split(":")
                    hour = pad(setTime[0],2);
                    minute = pad(setTime[1],2);
                    $("#pickerch2on").combodate('setValue',hour+":"+minute);
                }
                if (data["ch3on"] == "0") {
                    document.getElementById('ch3on').checked = false;
                } else {
                    document.getElementById('ch3on').checked = true;
                    setTime = data["ch3on"].trim().split(":")
                    hour = pad(setTime[0],2);
                    minute = pad(setTime[1],2);
                    $("#pickerch3on").combodate('setValue',hour+":"+minute);
                }
                if (data["piron"] == "0") {
                    document.getElementById('piron').checked = false;
                } else {
                    document.getElementById('piron').checked = true;
                    setTime = data["piron"].trim().split(":")
                    hour = pad(setTime[0],2);
                    minute = pad(setTime[1],2);
                    $("#pickerpiron").combodate('setValue',hour+":"+minute);
                }

                if (data["ch1off"] == "0") {
                    document.getElementById('ch1off').checked = false;
                } else {
                    document.getElementById('ch1off').checked = true;
                    setTime = data["ch1off"].trim().split(":")
                    hour = pad(setTime[0],2);
                    minute = pad(setTime[1],2);
                    $("#pickerch1off").combodate('setValue',hour+":"+minute);
                }
                if (data["ch2off"] == "0") {
                    document.getElementById('ch2off').checked = false;
                } else {
                    document.getElementById('ch2off').checked = true;
                    setTime = data["ch2off"].trim().split(":")
                    hour = pad(setTime[0],2);
                    minute = pad(setTime[1],2);
                    $("#pickerch2off").combodate('setValue',hour+":"+minute);
                }
                if (data["ch3off"] == "0") {
                    document.getElementById('ch3off').checked = false;
                } else {
                    document.getElementById('ch3off').checked = true;
                    setTime = data["ch3off"].trim().split(":")
                    hour = pad(setTime[0],2);
                    minute = pad(setTime[1],2);
                    $("#pickerch3off").combodate('setValue',hour+":"+minute);
                }
                if (data["piroff"] == "0") {
                    document.getElementById('piroff').checked = false;
                } else {
                    document.getElementById('piroff').checked = true;
                    setTime = data["piroff"].trim().split(":")
                    hour = pad(setTime[0],2);
                    minute = pad(setTime[1],2);
                    $("#pickerpiroff").combodate('setValue',hour+":"+minute);
                }

                if (data["pir"] == "0") {
                    document.getElementById('pir').checked = false;
                } else {document.getElementById('pir').checked = true;}


                //$('#menu').show( "blind" );
            },
    });
}

function readyTimerButton(mode,containerID,setTime){
    if (!setTime) {return;}
    if (mode == "show"){
            $("#container"+containerID).animate({
                right: '80px'
            }, 500,
            function() {
                $("label[for='"+containerID+"']").show()
            });
            setTime = setTime.trim().split(":")
            hour = pad(setTime[0],2);
            minute = pad(setTime[1],2);
            $("#picker"+containerID).combodate('setValue',hour+":"+minute);
            if (document.getElementById(containerID).checked) {
                $("#container"+containerID+" select").attr('disabled','disabled');
            }
        } else if (mode = "hide") {
            $("label[for='"+containerID+"']").hide()
            $("#container"+containerID).animate({
                right: '20px'
            }, 500);
        }
}

function pad(num, size) {
    var s = num+"";
    while (s.length < size) s = "0" + s;
    return s;
}

$(function() {
    $("#escapingBallGch1").hide()
    $("#escapingBallGch2").hide()
    $("#escapingBallGch3").hide()
    $("#escapingBallGpir").hide()

    $("#escapingBallGch1on").hide()
    $("#escapingBallGch2on").hide()
    $("#escapingBallGch3on").hide()
    $("#escapingBallGpiron").hide()

    $("#escapingBallGch1off").hide()
    $("#escapingBallGch2off").hide()
    $("#escapingBallGch3off").hide()
    $("#escapingBallGpiroff").hide()

    $('#pickerch1on').combodate({
        firstItem: 'name', //show 'hour' and 'minute' string at first item of dropdown
        minuteStep: 1
    });  
    $('#pickerch2on').combodate({
        firstItem: 'name', //show 'hour' and 'minute' string at first item of dropdown
        minuteStep: 1
    });  
    $('#pickerch3on').combodate({
        firstItem: 'name', //show 'hour' and 'minute' string at first item of dropdown
        minuteStep: 1
    });  
    $('#pickerpiron').combodate({
        firstItem: 'name', //show 'hour' and 'minute' string at first item of dropdown
        minuteStep: 1
    });  

    $('#pickerch1off').combodate({
        firstItem: 'name', //show 'hour' and 'minute' string at first item of dropdown
        minuteStep: 1
    }); 
    $('#pickerch2off').combodate({
        firstItem: 'name', //show 'hour' and 'minute' string at first item of dropdown
        minuteStep: 1
    }); 
    $('#pickerch3off').combodate({
        firstItem: 'name', //show 'hour' and 'minute' string at first item of dropdown
        minuteStep: 1
    }); 
    $('#pickerpiroff').combodate({
        firstItem: 'name', //show 'hour' and 'minute' string at first item of dropdown
        minuteStep: 1
    }); 

    /*
    function start() {
        alert('asdf');
        setTimeout(start, 3000);
    }

    // boot up the first call
    start();
    */


    $('.hour, .minute').change(function(){
        var containerID = this.parentNode.parentNode.id.replace("container","");
        var optionVal = this.options[ this.selectedIndex ].value;
        setTime = $('#picker'+containerID).combodate('getValue', 'H:m');
        if (setTime != "") {
            readyTimerButton("show", containerID, setTime);
        } else {
            readyTimerButton("hide", containerID, setTime);
        }
    })


    $('.Toggle').click(function(){

        var checkedState = '';
        checkLocked = true;

        if(this.checked) {checkedState = 'on';}
        else {checkedState = 'off';}

        if(this.name == "switch") {

            $("label[for='"+this.id+"']").hide();
            $("#escapingBallG"+this.id).show()

            jQuery.ajax({
                    type: "POST",
                    data: {
                        channel : this.id, 
                        state: checkedState,
                        mode: "toggle"
                    },
                    success: function(data) {
                        $("label[for='"+data["id"]+"']").show();
                        $("#escapingBallG"+data["id"]).hide()
                        checkLocked = false;
                    },
            });
        } else if (this.name == "picker") {
            setTime = $('#picker'+this.id).combodate('getValue', 'H:m');

            if (setTime == "") {
                alert("A valid time must be set. Ya dingus.");
                this.checked = false;
            }
            else{
                $("label[for='"+this.id+"']").hide();
                $("#escapingBallG"+this.id).show()

                if (checkedState == "on") {
                    readyTimerButton("show",this.id,setTime);
                }
                jQuery.ajax({
                        type: "POST",
                        data: {
                            channel : this.id, 
                            state: checkedState,
                            mode: "timer",
                            time: setTime
                        },
                        success: function(data) {
                            if (data["result"] == "off"){
                                $("#container"+data["id"]+" select").removeAttr('disabled');
                            }
                            $("label[for='"+data["id"]+"']").show();
                            $("#escapingBallG"+data["id"]).hide()
                            checkLocked = false;
                        },
                });
            }
        }
    }) 

    $('#menu')
        .mmenu({
            offCanvas   : false,
            isMenu      : true,
            classes     : 'mm-white',
            header      : true
    });
    initData()


});