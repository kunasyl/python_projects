
import os
from nltk.translate.bleu_score import sentence_bleu


references_dict = {}
'''Getting references from txt files'''
result_files = f"{os.getcwd()}/translation_results"
for filename in os.listdir(result_files):
    with open(os.path.join(result_files, filename), 'r', encoding='UTF-8') as f:
        references_dict[filename] = [x.split() for x in f.read().split('.')]

print(references_dict)


'''BLEU'''
# reference = [
#     'this is a dog'.split(),
#     'it is dog'.split(),
#     'dog it is'.split(),
#     'a dog, it is'.split() 
# ]
# candidate = 'it is dog'.split()
# print('BLEU score -> {}'.format(sentence_bleu(reference, candidate)))


