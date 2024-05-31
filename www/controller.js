$(document).ready(function () {
    
    // Display Speak Message
    eel.expose(DisplayMessage)
    function DisplayMessage(message) {

        $(".siri-message li:first").text(message);
        $('.siri-message').textillate('start');

    }

    // Display hood
    eel.expose(ShowHood)
    function ShowHood() {
        $("#Oval").attr("hidden", false);
        $("#SiriWave").attr("hidden", true);
    }

    eel.expose(PlayVideo)
    function PlayVideo(videoPath) {
        window.location.replace("playvideo.html");

    }
    
    eel.expose(ImageToWord)
    function ImageToWord() {
        window.location.replace("image2txt.html");

    }
    eel.expose(monitorSpeech)
    function monitorSpeech() {
        window.location.replace("monivoice.html");

    }

    eel.expose(PlayVideo)
    function PlayVideo(videoPath) {
        window.location.replace("playvideo.html");

    }
    
    eel.expose(ImageToWord)
    function ImageToWord() {
        window.location.replace("image2txt.html");

    }
    eel.expose(stepToURL)
    function stepToURL(urlAdd) {
        window.location.replace(urlAdd);

    }
    
});