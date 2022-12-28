import pickle

my_variable = ["locanda", "suiki", "bar", "lounge"]

with open("ex16/pickle_test/test_file.pickle", mode="wb") as f:
  pickle.dump(my_variable, f)