from models.filler_words import FillerWordAnalyzer
from models.sentiment import SentimentAnalyzer
from models.scoring import InterviewScorer


class ReportGenerator:

    def __init__(self):
        self.filler_analyzer = FillerWordAnalyzer()
        self.sentiment_analyzer = SentimentAnalyzer()
        self.scorer = InterviewScorer()

    def generate_report(self, answers):

        results = []
        total_score = 0

        for item in answers:

            question = item["question"]
            answer = item["answer"]

            # Filler word analysis
            filler_result = self.filler_analyzer.analyze(answer)

            # Sentiment analysis
            sentiment_result = self.sentiment_analyzer.analyze(answer)

            # Score
            score = self.scorer.calculate_score(
                answer,
                filler_result["total_fillers"],
                sentiment_result["sentiment"]
            )

            grade = self.scorer.get_grade(score)

            results.append({
                "question": question,
                "answer": answer,
                "filler_count": filler_result["total_fillers"],
                "filler_details": filler_result["details"],
                "sentiment": sentiment_result["sentiment"],
                "polarity": sentiment_result["polarity"],
                "score": score,
                "grade": grade
            })

            total_score += score

        if results:
            overall_score = round(total_score / len(results))
        else:
            overall_score = 0

        overall_grade = self.scorer.get_grade(overall_score)

        return {
            "results": results,
            "overall_score": overall_score,
            "overall_grade": overall_grade
        }