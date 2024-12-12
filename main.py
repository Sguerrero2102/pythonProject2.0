from gui import QuizApp
from logic import load_questions
from PyQt5.QtWidgets import QApplication
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QuizApp()

    # Load questions and pass to the app
    questions = load_questions('questions.json')
    window.load_questions(questions)

    window.show()
    sys.exit(app.exec_())

