hello = "twocattwocatcattwocatfour"

def mostRepeatedMany(n):
	for dna in seqs:
		dna = seqs[dna]
		mostRepeated(dna, n)

def mostRepeated(str, n):
	# Where the options are stored
	sequences = []
	sequencesCount = []
	greatestIndex = []

	# Go through each test sequence in dna
	for i in range (0, len(str)):
		test = str[i:i+n]
		searchIndex = 0
		repeatCount = 0

		# Iterate to find number of repeats if test has length n
		if (len(test) == n and test not in sequences):
			while (str.find(test,searchIndex) != -1):
				repeatCount += 1
				searchIndex = str.find(test, searchIndex) + 1

			# Add findings to sequence and sequencesCount
			sequences.append(test)
			
			
			# If it is the largest, then store this in greatestIndex
			if (repeatCount > max(sequencesCount)):
				print ("hi")
				greatestIndex=[]
				greatestIndex.append(i)
			elif (repeatCount == max(sequencesCount)):
				greatestIndex.append(i)

			sequencesCount.append(repeatCount)

	for ind in greatestIndex:
		print (sequences[ind]) 
		print (sequencesCount[ind])




print(mostRepeated(hello, 3))