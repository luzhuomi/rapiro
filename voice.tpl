<html>
<head>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
</head>
<body>
     <form action="/create">
       <input type="search" id="q" name="q" size=60>
     </form>
     <div><span id="answer"></span></div>
     <button id="button" onclick="toggleStartStop()"></button>

     <script type="text/javascript">
     var recognizing;
     var recognition = new webkitSpeechRecognition();
     recognition.lang = "en";
     recognition.continuous = true;
     reset();
     recognition.onend = function () { console.log("onend"); recognition.start(); };
     recognition.onresult = function (event) {
       for (var i = event.resultIndex; i < event.results.length; ++i) {
         if (event.results[i].isFinal) {
           // console.log(i + recognizing);
           // console.log(event.results.length);
           q.value = event.results[i][0].transcript;
	   $.get("/voice/"+q.value, function(data)
		{
		    console.log(q.value);
        speak(data);
		});
           // q.form.submit();           
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
     {
      msg.text = mesg;      
      speechSynthesis.speak(msg);
      $("#answer").text(mesg);
     }     
     $(document).ready(function() 
     	{ 
    		toggleStartStop();
    	});


     </script>
</body>
</html>
