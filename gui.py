from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QButtonGroup, QRadioButton, QLineEdit, QLabel
from PyQt5.QtCore import QTimer

class QuizApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('design.ui', self)

        # Initialize quiz state variables
        self.current_question_index = 0
        self.questions = []
        self.selected_answers = []
        self.timer = QTimer(self)
        self.time_elapsed = 0
        self.correct_answers = 0
        self.total_questions = 0

        # Set up radio buttons for multiple-choice options
        self.option_group = QButtonGroup(self)
        self.option_group.addButton(self.option1, 0)
        self.option_group.addButton(self.option2, 1)
        self.option_group.addButton(self.option3, 2)
        self.option_group.addButton(self.option4, 3)

        # Connect buttons to their corresponding methods
        self.nextButton.clicked.connect(self.next_question)
        self.restartButton.clicked.connect(self.restart_quiz)  # Connect the Restart button
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)

    def load_questions(self, questions):
        self.questions = questions
        self.selected_answers = [None] * len(questions)
        print(self.questions)  # Check if questions are loaded properly
        self.display_question()

    def display_question(self):
        question_data = self.questions[self.current_question_index]
        self.questionLabel.setText(question_data['question'])

        # Handling multiple choice questions
        if question_data['type'] == 'multiple_choice':
            options = question_data.get('options', [])
            for i, option in enumerate(options):
                self.option_group.button(i).setText(option)
                self.option_group.button(i).setVisible(True)
            for i in range(len(options), 4):
                self.option_group.button(i).setVisible(False)
            self.answerInput.setVisible(False)

        # Handling open-ended questions
        elif question_data['type'] == 'open_ended':
            for button in self.option_group.buttons():
                button.setVisible(False)

            self.answerInput.setVisible(True)
            self.answerInput.setText('')

    def next_question(self):
        # Store the selected answer for the current question
        selected_button = self.option_group.checkedButton()
        if selected_button:
            selected_answer_index = self.option_group.id(selected_button)
            self.selected_answers[self.current_question_index] = selected_answer_index

            # Check if the selected answer is correct
            question_data = self.questions[self.current_question_index]
            correct_answer = question_data['answer']

            # For multiple choice questions, get the actual selected answer
            if question_data['type'] == 'multiple_choice':
                selected_answer = question_data['options'][selected_answer_index]
            else:
                selected_answer = self.answerInput.text()

            if selected_answer == correct_answer:
                self.correct_answers += 1

            # Update the score label
            self.scoreLabel.setText(f"Score: {self.correct_answers} / {self.current_question_index + 1}")

        # Move to the next question
        self.current_question_index += 1
        if self.current_question_index < len(self.questions):
            self.option_group.setExclusive(False)
            for button in self.option_group.buttons():
                button.setChecked(False)
            self.option_group.setExclusive(True)

            self.display_question()
        else:
            self.finish_quiz()

    def clear_answers(self):
        for button in self.option_group.buttons():
            button.setChecked(False)
        self.answerInput.clear()

    def update_timer(self):
        self.time_elapsed += 1
        minutes, seconds = divmod(self.time_elapsed, 60)
        self.timerLabel.setText(f"Time: {minutes:02}:{seconds:02}")

    def finish_quiz(self):
        # Display final score message
        self.total_questions = len(self.questions)
        self.show_score()

    def show_score(self):
        score_message = f"Quiz Complete! You got {self.correct_answers} out of {self.total_questions} correct."
        self.questionLabel.setText(score_message)
        self.timer.stop()
        self.nextButton.setEnabled(False)
        for button in self.option_group.buttons():
            button.setVisible(False)
        self.answerInput.setVisible(False)

    def restart_quiz(self):
        # Reset quiz state
        self.current_question_index = 0
        self.correct_answers = 0
        self.time_elapsed = 0
        self.selected_answers = [None] * len(self.questions)

        # Restart the timer and UI elements
        self.timer.start(1000)
        self.nextButton.setEnabled(True)
        for button in self.option_group.buttons():
            button.setVisible(True)
            button.setChecked(False)
        self.answerInput.setVisible(False)
        self.answerInput.clear()
        self.timerLabel.setText("Time: 00:00")

        # Reset the score label
        self.scoreLabel.setText("Score: 0 / 0")

        # Display the first question
        self.display_question()
