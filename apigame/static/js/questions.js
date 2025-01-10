// Wait for the DOM to be fully loaded before executing the code
document.addEventListener("DOMContentLoaded", function () {
    // Get all the questions from the DOM
    const questions = document.querySelectorAll(".question");
    let currentQuestionIndex = 0; // Keep track of the current question

    // Display the questions (only the first one should be visible initially)
    displayQuestions(questions, currentQuestionIndex);

    // Add event listeners to all the answer buttons
    addAnswerButtonListeners(questions, currentQuestionIndex);

    addHintButtonListeners(questions);
});

// Function to display the current question and hide the rest
function displayQuestions(questions, currentQuestionIndex) {
    questions.forEach((question, index) => {
        if (index === currentQuestionIndex) {
            // Show the current question
            showQuestion(question);
        } else {
            // Hide the other questions
            hideQuestion(question);
        }
    });
}

// Function to add event listeners to each answer button
function addAnswerButtonListeners(questions, currentQuestionIndex) {
    // Get all buttons in the quiz
    const buttons = document.querySelectorAll(".btn");

    // Loop through each button and add a click event listener
    buttons.forEach((button) => {
        if (button.classList.contains("hint-button")) {
            return; // Skip this iteration if it's the hint button
        }

        button.addEventListener("click", function () {
            // Get the selected answer text
            const selectedAnswer = button.textContent.trim();

            // Get the current question's data (can be adjusted depending on your structure)
            const question = questions[currentQuestionIndex];
            const questionId = question.dataset.id.trim().replace(/;$/, '');


            // Send the selected answer to the server
            sendAnswerToServer(questionId, selectedAnswer);

            // Hide the current question when an answer is selected
            hideQuestion(questions[currentQuestionIndex]);

            // Move to the next question
            currentQuestionIndex++;

            // If there are more questions, display the next one
            if (currentQuestionIndex < questions.length) {
                showQuestion(questions[currentQuestionIndex]);
            } else {
                // If no more questions, redirect the user to the /results page
                redirectToResultsPage();
            }
        });
    });
}

function addHintButtonListeners(questions) {
    questions.forEach((question) => {
        const hintButton = question.querySelector(".hint-button");
        const hintText = question.querySelector(".hint-text");

        if (hintButton && hintText) {
            hintButton.addEventListener("click", function () {
                // Toggle visibility of the hint text
                hintText.style.display = (hintText.style.display === "none" || hintText.style.display === "") ? "block" : "none";
            });
        }
    });
}

// Function to hide a given question
function hideQuestion(question) {
    question.style.display = "none";
}

// Function to show a given question
function showQuestion(question) {
    question.style.display = "block";
}

// Function to send the selected answer to the server
function sendAnswerToServer(questionId, selectedAnswer) {
    // Prepare the data to be sent
    const data = {
        questionId: questionId,
        selectedAnswer: selectedAnswer,
    };
    console.log(data)

    // Send the data to the server using fetch
    fetch('/game/solo', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
        .then(response => response.json()) // Assuming the server responds with JSON
        .then(data => {
            // Optionally, handle the server response (e.g., show feedback to the user)
            console.log('Answer submitted successfully:', data);
            // You can process feedback here if necessary (e.g., showing if the answer was correct)
        })
        .catch(error => {
            console.error('Error submitting answer:', error);
        });
}

// Function to show a completion message (optional, for better UX)
function showCompletionMessage() {
    const quizContainer = document.getElementById('quiz-container');
    quizContainer.innerHTML = `
        <div class="text-center">
            <h2>Partida finalizada!</h2>
            <p>Redirecionando para os resultados...</p>
        </div>
    `;
}

// Function to redirect the user to the results page
function redirectToResultsPage() {
    showCompletionMessage(); // Optional, to show a message before redirecting

    // Redirect after a short delay
    setTimeout(() => {
        window.location.href = '/game/results'; // Adjust the path if needed
    }, 1500); // 2-second delay for UX
}
