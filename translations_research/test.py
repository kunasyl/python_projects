from nltk.translate.bleu_score import sentence_bleu

reference = [
    'this is a dog'.split(),
    'it is dog'.split(),
    'dog it is'.split(),
    'a dog, it is'.split() 
]
print(reference)
candidate = 'it is dog'.split()
print(sentence_bleu(reference, candidate, weights=(1.0, 0, 0, 0)))


reference2 = [
        ['Впервые', 'в', 'жизни', 'Габби', 'оставалась', 'дома', 'одна'],
        ['Впервые', 'в', 'жизни', 'Габби', 'осталась', 'дома', 'одна'],
    ]
candidate2 = 'Впервые в жизни Гэбби осталась дома одна'.split()
print('BLEU score -> {}'.format(sentence_bleu(reference2, candidate2, weights=(1.0, 0, 0, 0))))