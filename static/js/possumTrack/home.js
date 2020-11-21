var pendingRelayAck=null;
var pendingRelayState=false;
var telemetryCache;
window.onscroll = function () { window.scrollTo(0, 0); };
$(document).ready(function(){
    M.AutoInit();
    navigator.geolocation.getCurrentPosition(function(location) {
  console.log(location.coords.latitude);
  console.log(location.coords.longitude);
  console.log(location.coords.accuracy);
});
  });


$(".inverterSW ").change(function() {
  if(this.checked) {
      toggleRelay("inverter",true)
  }
  else{
    toggleRelay("inverter",false)
  }
});

$(".fridgeSW ").change(function() {
  if(this.checked) {
      toggleRelay("fridge",true)
  }
  else{
    toggleRelay("fridge",false)
  }
});

$(".heaterSW ").change(function() {
  if(this.checked) {
      toggleRelay("heater",true)
  }
  else{
    toggleRelay("heater",false)
  }
});

$(".fuseSW ").change(function() {
    if(this.checked) {
        toggleRelay("fuse",true)
    }
    else{
      toggleRelay("fuse",false)
    }
});

function toggleRelay(target,state){

  pendingRelayAck=target
  pendingRelayState=state
  var instance = M.Modal.getInstance($("#toggleWaitModal"));
  instance.open()
  $.ajax({
          type: "POST",
          url: window.location.pathname+"toggle",//other option is search
          data:{target:target,state,state},
          success: function(response) {
              console.log(response);
          },
          error: function(response) {
              console.log(response);
          }
  });
  M.toast({html: 'Waiting for Possum Response'})
  window.setTimeout(function(){
    var instance = M.Modal.getInstance($("#toggleWaitModal"));
    if (instance.isOpen){
      instance.close()
      M.toast({html: 'Possum Response Timedout'})
      $(".fuseSW ").prop( "checked", !state );
      pendingRelayAck=null;
    }
  },30000);
}


window.setInterval(function(){
  var d = new Date();

  var dayDict=["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
  var weekDayStr=dayDict[d.getDay()-1]


  var dayStr=String(d.getDate())
  if (dayStr == "1" | dayStr == "21"){
    dayStr += "st"
  }
  else if (dayStr == "2" | dayStr == "22"){
    dayStr += "nd"
  }
  else if (dayStr == "3" | dayStr == "23"){
    dayStr += "rd"
  }
  else{
    dayStr += "th"
  }

  var moonDict=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

  var monStr=moonDict[d.getMonth()]

  $(".time").text(d.toLocaleTimeString())
  $(".date").text(weekDayStr + " "+monStr+" "+dayStr)
}, 1000);

window.setInterval(function(){
  updateSnapshot()
},5000);

function updateBattery(SoC){
  if (SoC > 30){
    $(".battery-level").removeClass("alert")
    $(".battery-level").removeClass("warn")
    $(".battery-level").height(SoC+"%")
  }
  else if (SoC >10 & SoC <= 30){
    $(".battery-level").removeClass("alert")
    $(".battery-level").addClass("warn")
    $(".battery-level").height(SoC+"%")
  }
  else{
    $(".battery-level").removeClass("warn")
    $(".battery-level").addClass("alert")
    $(".battery-level").height(SoC+"%")
  }

}
function updateTimestamp(generatedTimestamp){
  var now = new Date()
  var d = new Date(generatedTimestamp)

  var dayDict=["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
  var weekDayStr=dayDict[d.getDay()-1]


  var dayStr=String(d.getDate())
  if (dayStr == "1" | dayStr == "21"){
    dayStr += "st"
  }
  else if (dayStr == "2" | dayStr == "22"){
    dayStr += "nd"
  }
  else if (dayStr == "3" | dayStr == "23"){
    dayStr += "rd"
  }
  else{
    dayStr += "th"
  }

  var moonDict=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

  var monStr=moonDict[d.getMonth()]

  secs=(now-d)/1000

  if (secs <=120){
    agoStr= Math.round(secs)+" s ago"
  }
  else if (secs >120 & secs <= 3600){
    agoStr= Math.round(secs/60)+" min ago"
  }
  else if (secs >3600 & secs < 86400){
    agoStr= Math.round(secs/3600)+" hr ago"
  }
  else{
    agoStr= Math.round(secs/86400)+" day ago"
  }

  $(".timestamp span").text("("+agoStr+") Updated: "+d.toLocaleTimeString() +" "+weekDayStr + " "+monStr+" "+dayStr )
}
function updateSnapshot(){
    console.log("grabbing latest snapshot")
    $.ajax({
            type: "GET",
            url: window.location.pathname+"snapshot",//other option is search
            success: function(response) {
                console.log(response);
                telemetryCache=response;
                $(".battery-SOC span").text(response.SoC.toFixed(0)+"%")
                updateBattery(response.SoC.toFixed(0))

                $(".battery-Voltage span").text(response.batteryV.toFixed(1)+"V")
                $(".insideTemp").text(response.tempInternal.toFixed(0))
                $(".insideHum").text(response.humInternal.toFixed(0))
                $(".cabTemp").text(response.tempCab.toFixed(0))
                $(".cabHum").text(response.humCab.toFixed(0))
                $(".PVWatt span").text((response.PVI*response.PVV).toFixed(1)+"W")
                updateTimestamp(response.generatedTimestamp)

                if (response.batteryIN>response.batteryIP){
                  $(".battery-status span").text("Discharging")
                  $(".battery-current span").text(response.batteryIN.toFixed(2)+"A")
                }
                else{
                  $(".battery-status span").text("Charging")
                  $(".battery-current span").text(response.batteryIP.toFixed(2)+"A")
                }


                if (pendingRelayAck=="inverter"){
                  if (pendingRelayState == response.bInverter){
                    var instance = M.Modal.getInstance($("#toggleWaitModal"));
                    if (instance.isOpen){
                      instance.close()
                      M.toast({html: 'Inverter toggled'})
                      $(".inverterSW ").prop( "checked", response.bInverter );
                      pendingRelayAck=null;
                    }
                  }
                }
                $(".inverterSW ").prop( "checked", response.bInverter );

                if (pendingRelayAck=="fridge"){
                  if (pendingRelayState == response.bFridge){
                    var instance = M.Modal.getInstance($("#toggleWaitModal"));
                    if (instance.isOpen){
                      instance.close()
                      M.toast({html: 'Fridge toggled'})
                      $(".fridgeSW ").prop( "checked", response.bFridge );
                      pendingRelayAck=null;
                    }
                  }
                }
                $(".fridgeSW ").prop( "checked", response.bFridge );
                // $(".heaterSW ").prop( "checked", response.humCab );

                if (pendingRelayAck=="fuse"){
                  if (pendingRelayState == response.bUVLO){
                    var instance = M.Modal.getInstance($("#toggleWaitModal"));
                    if (instance.isOpen){
                      instance.close()
                      M.toast({html: 'Fuse toggled'})
                      $(".fuseSW ").prop( "checked", response.bUVLO );
                      pendingRelayAck=null;
                    }
                  }
                }
                $(".fuseSW ").prop( "checked", response.bUVLO );


            },
            error: function(response) {
                console.log(response);
            }
    });
};


function updateWeather(weatherText, weatherIcon, temp,hum,location){
  $(".weatherText span").text(weatherText);
  $(".weatherIcon").attr("src","https://developer.accuweather.com/sites/default/files/"+String(weatherIcon).padStart(2,"0")+"-s.png")
  $(".outsideTemp").text(temp.toFixed(0));
  $(".outsideHum").text(hum.toFixed(0));
  $(".weatherText .location").text(location);
}
