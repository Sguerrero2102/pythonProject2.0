import json
import json

class QuizLogic:
    def __init__(self, question_file):
        with open(question_file, 'r') as f:
            self.questions = json.load(f)
        self.current_index = 0
        self.score = 0
        self.results = []

    def get_current_question(self):
        if self.current_index < len(self.questions):
            return self.questions[self.current_index]
        return None

    def check_answer(self, user_answer):
        correct_answer = self.questions[self.current_index]['answer']
        is_correct = user_answer.strip().lower() == correct_answer.strip().lower()
        self.results.append((self.current_index, is_correct))
        if is_correct:
            self.score += 1
        self.current_index += 1

    def is_quiz_finished(self):
        return self.current_index >= len(self.questions)

    def get_score(self):
        return self.score

    def get_incorrect_answers(self):
        return [(self.questions[i], correct) for i, correct in self.results if not correct]

import json

def load_questions(filename):
    """Load questions from a JSON file."""
    with open(filename, 'r') as file:
        return json.load(file)

