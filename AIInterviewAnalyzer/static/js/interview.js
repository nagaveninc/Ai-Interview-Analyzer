const questions = [
    "Tell me about yourself.",
    "Why should we hire you?",
    "What are your strengths?",
    "What are your weaknesses?",
    "Describe one challenging project you worked on.",
    "Why do you want to join our company?",
    "Where do you see yourself in five years?",
    "How do you handle pressure?",
    "Tell me about a time you worked in a team.",
    "Do you have any questions for us?"
];

let currentQuestion = 0;

const question = document.getElementById("question");
const questionNumber = document.getElementById("questionNumber");
const answer = document.getElementById("answer");

// Check browser support
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

if (!SpeechRecognition) {
    alert("Speech Recognition is not supported in this browser. Please use Google Chrome.");
    throw new Error("Speech Recognition not supported.");
}

const recognition = new SpeechRecognition();

recognition.lang = "en-IN";
recognition.continuous = true;
recognition.interimResults = true;
recognition.maxAlternatives = 1;

// Start Recording
document.getElementById("startBtn").addEventListener("click", () => {
    answer.value = "";
    recognition.start();
});

// Stop Recording
document.getElementById("stopBtn").addEventListener("click", () => {
    recognition.stop();
});

// Convert Speech to Text
recognition.onresult = (event) => {

    let transcript = "";

    for (let i = event.resultIndex; i < event.results.length; i++) {
        transcript += event.results[i][0].transcript + " ";
    }

    answer.value = transcript;
};

// Error Handling
recognition.onerror = (event) => {
    console.error(event.error);

    if (event.error === "not-allowed") {
        alert("Please allow microphone permission.");
    } else if (event.error === "no-speech") {
        alert("No speech detected. Please speak louder.");
    } else if (event.error === "audio-capture") {
        alert("No microphone found.");
    } else {
        alert("Speech Recognition Error: " + event.error);
    }
};

// Next Question
document.getElementById("nextBtn").addEventListener("click", () => {

    fetch("/save_answer", {

        method: "POST",

        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },

        body:
            "question=" + encodeURIComponent(questions[currentQuestion]) +
            "&answer=" + encodeURIComponent(answer.value)

    })

    .then(response => response.json())

    .then(data => {

        currentQuestion++;

        answer.value = "";

        if (currentQuestion < questions.length) {

            questionNumber.innerHTML = "Question " + (currentQuestion + 1);
            question.innerHTML = questions[currentQuestion];

        } else {

            alert("Interview Completed Successfully!");
            window.location.href = "/dashboard";

        }

    })

    .catch(error => {

        console.error(error);
        alert("Error saving answer.");

    });

});