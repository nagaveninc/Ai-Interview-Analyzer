class FillerWordAnalyzer:

    def __init__(self):

        self.filler_words = [
            "um",
            "uh",
            "like",
            "actually",
            "basically",
            "literally",
            "you know",
            "i mean",
            "so",
            "well"
        ]

    def analyze(self, text):

        text = text.lower()

        count = 0

        found = []

        for word in self.filler_words:

            occurrences = text.count(word)

            if occurrences > 0:

                count += occurrences

                found.append({
                    "word": word,
                    "count": occurrences
                })

        return {
            "total_fillers": count,
            "details": found
        }