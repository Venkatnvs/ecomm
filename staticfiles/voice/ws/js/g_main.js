var speech = true;
window.SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
const recognition = new SpeechRecognition();
recognition.interimResults = true;
const words = document.querySelector(".words");
words.appendChild(p);

recognition.addEventListener("result", (e) => {
    const transcript = Array.from(e.results)
        .map((result) => result[0])
        .map((result) => result.transcript)
        .join("");

    document.getElementById("p").innerHTML = transcript;
    console.log(transcript);
});
if (speech == true) {
    recognition.start();
    recognition.addEventListener("end", recognition.start);
}