# -*- coding: utf-8 -*-
possible_tags = [
    "part-time-job",
    "full-time-job",
    "hourly-wage",
    "salary",
    "associate-needed",
    "bs-degree-needed",
    "ms-or-phd-needed",
    "licence-needed",
    "1-year-experience-needed",
    "2-4-years-experience-needed",
    "5-plus-years-experience-needed",
    "supervising-job"
]

f = open('train.tsv')
header = f.readline()
tag_lists = []
descriptions = []

print "Opening the train dataset"
for line in f:
    fields = line.split('\t')
    tag_lists.append(fields[0].split(' '))
    descriptions.append(fields[1])

print "Loading sklearn libraries"
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import GridSearchCV
import numpy as np
import time

tag_models = {}
for tag in possible_tags:
    print "Building {} model".format(tag)
    time1 = time.time()

    targets = [tag in tag_list for tag_list in tag_lists]
    model = Pipeline([('vect', CountVectorizer()),
        ('tfidf', TfidfTransformer()),
        ('clf', MLPClassifier(verbose=True)),
    ])

    parameters = {
        'vect__ngram_range': [(1, 1), (1, 2)],
        'tfidf__use_idf': (True, False),
        'clf__hidden_layer_sizes': [(10)]
    }
    gs_model = GridSearchCV(model, parameters, n_jobs=-1, verbose=True)

    gs_model = gs_model.fit(descriptions, targets)
    tag_models[tag] = gs_model

    time2 = time.time()
    print "Took {} seconds".format(time2-time1)

print "Opening the test dataset"
f = open('test.tsv')
test_header = f.readline()
test_descriptions = []
for line in f:
    test_descriptions.append(line)

results_by_tag = {}
for tag, tag_model in tag_models.items():
    print "Getting predictions for {}".format(tag)
    results_by_tag[tag] = tag_model.predict(test_descriptions)

o = open('neural_net_output.tsv', 'w')
o.write('tags\n')
for index, _ in enumerate(test_descriptions):
    test_description_tags = []
    for tag, results in results_by_tag.items():
        if (results[index]):
            test_description_tags.append(tag)
            print tag
    o.write(' '.join(test_description_tags) + '\n')

o.close()
