# Student Name: Ali Başaran
# Student Number: 2020400357
# Compile Status: Compiling
# Program Status: Working
# Notes:the name of the program is called main.py in the report but its name is AliBasaran.py
from mpi4py import MPI
import argparse


mpi = MPI.COMM_WORLD
rank = mpi.Get_rank()
size = mpi.Get_size()

parser = argparse.ArgumentParser()
parser.add_argument("--input_file", dest="inputfile",
                    help="Name of the input file",
                    required=True)

parser.add_argument("--test_file", dest="testfile",
                    help="Name of the test file",
                    required=True)

parser.add_argument("--merge_method", dest="mergemethod",
                    help="Merge method",
                    required=True)
args = parser.parse_args()
inputfile = args.inputfile
testfile = args.testfile
mergemethod = args.mergemethod

unigrams = dict()
bigrams = dict()

# Read the input file and distribute the data evenly to the worker processes
if rank == 0:

    # Create 2-d list to distribute the data
    datalist = []
    for i in range(size):
        datalist.append([])
    file = open(inputfile)
    i = 0
    # Distribute the data to lists
    for line in file:
        datalist[i % (size-1)].append(line)
        i += 1
    # Distribute the data to worker process
    for i in range(size-1):
        mpi.send(datalist[i], i+1)

    if (mergemethod == "MASTER"):
        # Receive the data from the worker processes and merge them
        for i in range(1, size):
            recUnigrams = mpi.recv(None, i)
            recBigrams = mpi.recv(None, i)
            for key, value in recUnigrams.items():
                unigrams[key] = unigrams.get(key, 0)+value
            for key, value in recBigrams.items():
                bigrams[key] = bigrams.get(key, 0)+value
    # Receive the data from the last worker process.
    elif (mergemethod == "WORKERS"):
        unigrams = mpi.recv(None, size-1)
        bigrams = mpi.recv(None, size-1)
    else:
        print("Unknown merge method")
    # Calculate the conditional probabilities for the given bigrams
    file = open(testfile)
    for line in file:
        line = line.rstrip()
        words = line.split()
        prob = bigrams.get(line, 0)/unigrams.get(words[0], 0)
        print("Bigram: {}, Conditional Probability: {}".format(line, prob))

else:
    # Get the data from the master process
    sentencelist = mpi.recv(None, 0)
    # Print the rank of the process and length of the data
    print("Rank: {}, Number of Sentences: {}".format(rank, len(sentencelist)))
    if (rank == size - 1):
        print("------")
    # Iterate over the given sentences
    for sentence in sentencelist:
        wordlist = sentence.split()
        # Count unigrams and bigrams
        for i in range(len(wordlist)):
            word = wordlist[i]
            unigrams[word] = unigrams.get(word, 0)+1
            if (i != len(wordlist)-1):
                bigram = word+" "+wordlist[i+1]
                bigrams[bigram] = bigrams.get(bigram, 0)+1
    # Send the data to the master process
    if (mergemethod == "MASTER"):
        mpi.send(unigrams, 0)
        mpi.send(bigrams, 0)
    elif (mergemethod == "WORKERS"):
        # Send the data to the next worker process
        if (rank == 1):
            if (size > 2):
                mpi.send(unigrams, rank+1)
                mpi.send(bigrams, rank+1)
            else:
                mpi.send(unigrams, 0)
                mpi.send(bigrams, 0)
        # Take the data from the previous worker process and merge that data with process' own data. Send the merged data to the next worker
        else:
            recUnigrams = mpi.recv(None, rank-1)
            recBigrams = mpi.recv(None, rank-1)
            for key, value in recUnigrams.items():
                unigrams[key] = unigrams.get(key, 0)+value
            for key, value in recBigrams.items():
                bigrams[key] = bigrams.get(key, 0)+value
            if (rank != size-1):
                mpi.send(unigrams, rank+1)
                mpi.send(bigrams, rank+1)
            # Send the merged data to the master process
            else:
                mpi.send(unigrams, 0)
                mpi.send(bigrams, 0)
    else:
        print("Unknown merge method")
