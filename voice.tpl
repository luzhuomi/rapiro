<html>
<head>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
</head>
<body>
     <form action="/create">
       <input type="search" id="q" name="q" size=60>
     </form>
     <button id="button" onclick="toggleStartStop()"></button>

     <script type="text/javascript">
     var recognizing;
     var recognition = new webkitSpeechRecognition();
     recognition.lang = "en";
     recognition.continuous = true;
     reset();
     recognition.onend = reset();
     recognition.onresult = function (event) {
       for (var i = event.resultIndex; i < event.results.length; ++i) {
         if (event.results[i].isFinal) {
           console.log(event.results[i][0].transcript);
           q.value = event.results[i][0].transcript;
	   $.get("/"+q.value, function(data)
		{
		    console.log(q.value);
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
     $(document).ready(function() 
 	{ 
		toggleStartStop();
		console.log("hello");
	});
     </script>
</body>
</html>
