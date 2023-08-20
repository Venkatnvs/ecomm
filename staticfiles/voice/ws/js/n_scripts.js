const UserToken = JSON.parse(document.getElementById('user_token').textContent);
var SpeechRecognition = window.webkitSpeechRecognition;
var msg = new SpeechSynthesisUtterance();
var recognition = new SpeechRecognition();
var Textbox = $('#textbox');
var instructions = $('#instructions');
var Content = '';
recognition.continuous = true;

const VoiceSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/voice/v/'
    + UserToken
    + '/'
);

VoiceSocket.onmessage = function(e) {
    const d_mes = JSON.parse(e.data);
    console.log('connected');
    console.log(d_mes.message);
    const data = d_mes.message;
    if(data.type == 'url'){
        Content = data.content;
        console.log('data',data);
        Speekher(data.content);
        Textbox.val(Content);
        window.open(data.URL, '_blank');
    }else{
        Content = data.content;
        console.log('data',data);
        Textbox.val(Content);
        Speekher(data.content);
    }
};
    
VoiceSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};
// recognition.interimResults = true;
recognition.onresult = function(event) {
    var current = event.resultIndex;
    var transcript = event.results[current][0].transcript;
    console.log(transcript);
    VoiceSocket.send(JSON.stringify({
        'message': transcript
    }));
};

recognition.onstart = function() { 
    instructions.text('Voice recognition is ON.');
}

recognition.onspeechend = function() {
    instructions.text('No activity.');
    recognition.restart();
}

recognition.onerror = function(event) {
    if(event.error == 'no-speech') {
    instructions.text('Try again.');  
    }
}

$('#start-btn').on('click', function(e) {
    if (Content.length) {
        Content += ' ';
    }
    const d = new Date();
    let t_hour = d.getHours()
    fetch(`/voice/v/wish?val=${t_hour}`).then(res=>res.json()).then(data=>{
        console.log(data.content+' '+data.content_next);
    //    Speekher(data.content+' '+data.content_next);
    });
    recognition.start();
});

Textbox.on('input', function() {
    Content = $(this).val();
});

function Speekher(val){
    msg.text = val;
    window.speechSynthesis.speak(msg);
}