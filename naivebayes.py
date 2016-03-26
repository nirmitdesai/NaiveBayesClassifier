import math
from collections import defaultdict

dataset = []
traininglabels=[]
testlabels=[]
probDict = {}
probDigit = []
testDict = {}

def getMatrix():
	return [[1]*29 for i in xrange(29)]

def parseData():

	global probDigit,probDict,traininglabels,testlabels,testDict
	#read the testlabels in testlabel list
	with open("traininglabels.txt") as f:
		for line in f:
			traininglabels.append(int(line))
	
	#initialize all prob of digits to 0
	probDigit = [0 for i in xrange(10)]
	
	for i in xrange(10):
		probDict[i] = getMatrix()
		probDigit[i] = traininglabels.count(i)*1.0 / 5000

	#set counter to 1 since each digit is 28x28 pixel
	counter = 1
	index = 0
	
	with open("trainingimages.txt") as f:
		for line in f:
			row = line.rstrip('\n')			
			for i,j in enumerate(row):
				if j == '+' or j == '#':
					probDict[traininglabels[index]][counter][i+1] += 1
			
			counter = counter + 1
			if counter == 29:
				counter = 1
				index = index+1
	
def updateProb():

	#global probDigit,probDict,traininglabels,testlabels,testDict
	for i in xrange(10):
		for j in xrange(29):
			for k in xrange(29):
				probDict[i][j][k] = probDict[i][j][k]*1.0 / (traininglabels.count(i) +2)	
			
def runOnTest():

	#global probDigit,probDict,traininglabels,testlabels,testDict
	with open("testlabels.txt") as f:
		for line in f:
			testlabels.append(int(line))
	
	counter = 1
	index = 0
	testDict[index] = getMatrix()	
	with open("testimages.txt") as f:
		for line in f:
			row = line.rstrip('\n')
					
			for i,j in enumerate(row):
				if j == '+' or j == '#':
					testDict[index][counter][i+1] += 1

			counter = counter + 1
			if counter == 29:
				counter = 1
				index = index+1
				testDict[index] = getMatrix()
	
	del testDict[index]
	
def classify():

	#global probDigit,probDict,traininglabels,testlabels,testDict
	correctCount = 0
	prec = defaultdict(lambda: 0)

	for i in testDict:
		finalProb = [0]*10
		for t in xrange(10):
			finalProb[t] = math.log(probDigit[t])
		
		
		for j in range(1,29):
			for k in range(1,29):
				
				if testDict[i][j][k] == 1:
					for t in xrange(10):
						finalProb[t] += math.log(1 - probDict[t][j][k])
									
				else:
					for t in xrange(10):
						finalProb[t] += math.log(probDict[t][j][k])
					
		maxProb = finalProb.index(max(finalProb))
		
		#print "Test label = ",testlabels[i]," and assigned label = ",maxProb
		
		if maxProb == testlabels[i]:
			prec[maxProb] += 1
			correctCount += 1
	print
	print "Overall accuracy = ",correctCount*100* 1.0/1000,"%"
	print
	print "Digit	FrequencyInTestData	LabelledCorrectly	Accuracy"
	print "----------------------------------------------------------------"
	for i in range(10):
		print '{0:5d} {1:21d} {2:19d} {3:16f}'.format(i,testlabels.count(i),prec[i], prec[i]*100.0 / testlabels.count(i))
							
if __name__ == '__main__':
	
	parseData()
	updateProb()
	runOnTest()
	classify()
