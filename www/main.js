$(document).ready(function () {

  //siri configration
  var siriWave = new SiriWave({
    container: document.getElementById("siri-container"),
    width: 800,
    height: 200,
    amplitude: "0.5",
    speed: "0.30",
  });

  // Siri message animation
  $('.siri-message').textillate({
    loop: true,
    sync: true,
    in: {
      effect: "fadeInUp",
      sync: true,
    },
    out: {
      effect: "fadeOut",
      sync: true,
    },

  });

  //mic button click event
  $("#MicBtn").click(function () {
    $("#Oval").attr("hidden", true);
    $("#SiriWave").attr("hidden", false);
    eel.allCommands()()    //调用此函数
  });

});