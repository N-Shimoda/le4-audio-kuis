import pickle

with open("ex16/pickle_test/test_file.pickle", mode="rb") as f:
  list_from_pickle = pickle.load(f)

print(list_from_pickle)