import os, re
from nltk.translate.bleu_score import sentence_bleu
# from rouge_score import rouge_scorer
# from rouge_metric import PerlRouge
# from pyrouge import Rouge155


def get_candidates(lang):
    '''lang = [ru|en]
    Getting candidates from txt files'''
    candidates_dict = {}
    result_files = f"{os.getcwd()}/translation_results/{lang}"
    for filename in os.listdir(result_files):
        translator = filename.split('_')[0]
        with open(os.path.join(result_files, filename), 'r', encoding='UTF-8') as f:
            sentences = [x.split() for x in f.read().split('.')]
            filtered_sentences = [[re.sub(r'[\'\"\\\-]', '', word) for word in sentence] for sentence in sentences]
            candidates_dict[translator] = filtered_sentences

    return candidates_dict


def get_refences(lang):
    '''lang = [ru|en]
    Getting references from txt files'''
    references_dict = {}
    reference_files = f"{os.getcwd()}/references/{lang}"
    i = 0
    for filename in os.listdir(reference_files):
        with open(os.path.join(reference_files, filename), 'r', encoding='UTF-8') as f:
            sentences = [x.split() for x in f.read().split('.')]
            filtered_sentences = [[re.sub(r'[\'\"\\\-]', '', word) for word in sentence] for sentence in sentences]
            references_dict[i] = filtered_sentences
        i += 1

    sentences = {}
    for s, (r1, r2) in enumerate(zip(references_dict[0], references_dict[1])):
        sentences[s] = [r1, r2]

    return sentences


def get_traslator_sentences(candidates, translator):
    sentences = {}
    for i, sentence in enumerate(candidates[translator]):
        sentences[i] = sentence

    return sentences


def avg_bleu_score(references, candidates):
    scores = []
    for candidate, reference in zip(candidates.values(), references.values()):
        # print(candidate, reference)
        scores.append(sentence_bleu(reference, candidate, weights=(1.0, 0, 0, 0)))

    return sum(scores) / len(scores)


def init():
    '''BLEU ru'''
    # print(references[0])  [['Впервые', 'в', 'жизни', 'Габби', 'оставалась', 'дома', 'одна'], ['Впервые', 'в', 'жизни', 'Габби', 'осталась', 'дома', 'одна']]
    # print(candidates[0])  ['Увы,', 'Габби', 'был', 'единственным', 'в', 'округе']

    languages = ('ru', 'en')
    language = languages[0]
    translators = ('bing', 'google', 'chatgpt', 'yandex', 'deepl')
    for translator in translators:
        candidates_dict = get_candidates(language)
        references = get_refences(language)
        candidates = get_traslator_sentences(candidates=candidates_dict, translator=translator)
        print(f"avg BLEU score for {translator} translator: {avg_bleu_score(references, candidates)}")




if __name__ == '__main__':
    init()