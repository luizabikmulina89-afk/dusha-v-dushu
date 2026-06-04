from app.calculations.tests_scoring import (
    score_psychotype, score_attachment, score_love_language,
    score_enneagram, attachment_compatibility, psychotype_compatibility
)

def test_psychotype_scoring():
    answers = ['E', 'T', 'S', 'J', 'T', 'E', 'S', 'J']
    result = score_psychotype(answers)
    assert result == "ESTJ"

def test_psychotype_length():
    answers = ['I', 'F', 'N', 'P', 'F', 'I', 'N', 'P']
    result = score_psychotype(answers)
    assert len(result) == 4

def test_attachment_secure():
    answers = ['secure', 'secure', 'anxious', 'secure', 'secure', 'anxious', 'secure', 'secure']
    assert score_attachment(answers) == 'secure'

def test_love_language_time():
    answers = ['time', 'words', 'time', 'time', 'acts', 'time', 'words', 'time']
    assert score_love_language(answers) == 'time'

def test_enneagram_type():
    answers = [4, 4, 9, 4, 4, 4, 9, 4, 4]
    assert score_enneagram(answers) == 4

def test_attachment_compat_secure_secure():
    assert attachment_compatibility('secure', 'secure') == 95

def test_attachment_compat_anxious_avoidant():
    assert attachment_compatibility('anxious', 'avoidant') == 30

def test_psychotype_compat_opposites():
    score = psychotype_compatibility('INTJ', 'ENFP')
    assert score >= 85
