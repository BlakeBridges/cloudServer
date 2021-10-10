
$("#Toggle").click( function()
{
    $("#HappyText").toggle();
    });


var gif = false;
function toggleGif() {
    var x = document.getElementById("spookyLantern");
    if (gif) {
        x.src = '';
        gif = false;
    }
    else {
        x.src = 'https://media.musclegrid.io/aliceasmartialarts.com/uploads/2019/10/23171012/jack-o-lantern-happy-halloween-animated-gif-image.gif';
        gif = true;
    }
    }
    


var played = false;
function playAudio() {
    if (!played) {
        var src = new Audio('src/clipping.mp3');
        src.play();
        played = true;
    }
}

