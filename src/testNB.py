import NaiveBayesClassificator as nb

c = nb.Classifier(["a", "b", "c","d"])
#c = nb.Classifier(["a","b"])
c.add_training_example("a",["ORA-000001","ORA-000002","ORA-000003"])
c.add_training_example("b",["ORA-000002","ORA-000004"])
c.add_training_example("c",["ORA-000001","ORA-000004","ORA-000005"])
c.add_training_example("d",["ORA-000004","ORA-000005"])
print c.most_likely_outcome(["ORA-000004","ORA-000005","ORA-000001"])
