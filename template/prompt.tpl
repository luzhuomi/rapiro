<html>
<head>
<!--script src="/static/jquery-2.1.4.min.js"></script-->
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.0/jquery.min.js"></script>
</head>
<body>
     <form action="/create">
       <input type="search" id="q" name="q" size=60>
     </form>
     <div><span id="answer"></span></div>
     <button id="button" onclick="toggleStartStop()"></button>

     <script type="text/javascript">
var recognizing = true;
var recognition = new webkitSpeechRecognition();
recognition.lang = "en";
recognition.continuous = true;
reset();
recognition.onend = function () { console.log("onend"); recognition.start(); };
recognition.onresult = function (event) {
  for (var i = event.resultIndex; i < event.results.length; ++i) {
    if (event.results[i].isFinal) {
      q.value = event.results[i][0].transcript;
      if (q.value.toLowerCase() == "ryan") 
      {
        console.log(q.value);
        speak("Yes?");
      }
    }
  }
}
function reset() {
  recognizing = false;
  button.innerHTML = "Click to Speak";
}
function toggleStartStop() {
  if (recognizing) {
    recognition.stop();
    reset();
  } else {
    recognition.start();
    recognizing = true;
    button.innerHTML = "Click to Stop";
  }
}

var msg = new SpeechSynthesisUtterance();
var voices = window.speechSynthesis.getVoices();
msg.voice = voices[2]; // Note: some voices don't support altering params
msg.voiceURI = 'native';
msg.volume = 1; // 0 to 1
msg.rate = 0.7; // 0.1 to 10
msg.pitch = 1; //0 to 2
msg.lang = 'en-US';

function speak(mesg)
{ // TODO: fixed on raspberry pi vnc chromium, if using mac it works. Now we use espeak in python
  msg.text = mesg; 
  speechSynthesis.speak(msg);
  // $("#answer").text(mesg);
  msg.onend = function() { window.location.href = "/voice"; } ;
}
$(document).ready(function() 
{ 
  toggleStartStop();
  recognition.stop()
});
     </script>
</body>
</html>
