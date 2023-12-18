# scoring.py
class Scoring:
    def __init__(self, high_score_file):
        self.high_score_file = high_score_file
        self.high_scores = []
        self.load_high_scores()

    def load_high_scores(self):
        try:
            with open(self.high_score_file, "r") as file:
                self.high_scores = [line.strip().split(',') for line in file]
                self.high_scores.sort(key=lambda x: int(x[1]), reverse=True)
        except FileNotFoundError:
            pass

    def save_high_scores(self):
        with open(self.high_score_file, "w") as file:
            for name, score in self.high_scores:
                file.write(f"{name},{score}\n")

    def update_high_scores(self, name, score):
        self.high_scores.append((name, score))
        self.high_scores.sort(key=lambda x: int(x[1]), reverse=True)
        self.high_scores = self.high_scores[:10]  # Keep only top 10 scores
        self.save_high_scores()

    def is_high_score(self, score):
        return len(self.high_scores) < 10 or score > int(self.high_scores[-1][1])

    def get_top_high_scores(self, number_of_scores=10):
        return self.high_scores[:number_of_scores]
