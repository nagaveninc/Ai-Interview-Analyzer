class InterviewScorer:

    def calculate_score(self, answer, filler_count, sentiment):

        score = 100

        # Answer Length Score
        words = len(answer.split())

        if words < 20:
            score -= 25

        elif words < 40:
            score -= 10

        # Filler Words Penalty
        score -= filler_count * 2

        # Sentiment Score
        if sentiment == "Positive":
            score += 5

        elif sentiment == "Negative":
            score -= 10

        # Keep score between 0 and 100
        score = max(0, min(score, 100))

        return score


    def get_grade(self, score):

        if score >= 90:
            return "Excellent"

        elif score >= 75:
            return "Very Good"

        elif score >= 60:
            return "Good"

        elif score >= 40:
            return "Average"

        return "Needs Improvement"