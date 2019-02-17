
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from goose import Goose
import re, sys, os
import urllib2, nltk
from sklearn import cluster
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

reload(sys)
sys.setdefaultencoding('utf8')
path_mitie_lib = 'MITIE/mitielib/';
sys.path.append (path_mitie_lib);

from mitie import *
path_to_ner_model = 'MITIE/MITIE-models/english/ner_model.dat';
ner = named_entity_extractor(path_to_ner_model);

class Clustering:
    """Number of articles in the data set."""
    N = 1000;

    """The data corpus with all articles content."""
    corpus = [];

    """The titles list."""
    titles = [];

    """Set of entities in the corpus."""
    entities = [];

    @classmethod
    def loadData(self):
        for i in range(0, self.N):
            self.titles.append(self.readFile('title', i));
            article = self.readFile('article', i);
            self.corpus.append(article);
            """Reload the file using the MITIE function."""
            tokens = tokenize(load_entire_file(('data/article-' + str(i) + '.txt')));
            entities = ner.extract_entities(tokens);
            for entity in entities:
                range_array = entity[0];
                tag = entity[1];
                score = entity[2];
                score_text = "{:0.3f}".format(score);
                entity_text = " ".join(tokens[j] for j in range_array);
                self.entities.append(entity_text.lower());
        """Array cleanup."""
        self.entities = np.unique(self.entities);



    @classmethod
    def readFile(self, type, index):
        file = open('data/' + type + '-' + str(index) + '.txt', "r+");
        content = file.read().replace('\n', ' ');
        file.close();
        return content.lower();

    """Do the clustering and print it."""
    @classmethod
    def createClusters(self):
        """Creates the matrix for tf-idf with the extracted entities for the corpus."""
        vector = TfidfVectorizer(sublinear_tf=True, max_df=0.5, analyzer='word',
                               stop_words='english', vocabulary=self.entities);
        corpus_tfidf = vector.fit_transform(self.corpus);

        """Do the clustering."""
        spectral = cluster.SpectralClustering(n_clusters= 7,
                                              eigen_solver='arpack',
                                              affinity="nearest_neighbors",
                                              n_neighbors = 10);
        spectral.fit(corpus_tfidf);

        """Prints it."""
        if hasattr(spectral, 'labels_'):
            cluster_assignments = spectral.labels_;
        for i in range(0, len(cluster_assignments)):
            print (i, cluster_assignments[i], self.titles[i])

    def main(self):
        self.loadData();
        self.createClusters();

if __name__ == '__main__':
    clustering = Clustering();
    clustering.main();
