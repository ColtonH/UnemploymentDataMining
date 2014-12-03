import math
from data.models import UnemploymentByStateMonthly, UsState, NatalityByStateYearly, MortalityByStateYearly

class StatisticalAssociationRule:
	def __init__(self,label,mu,std,interest):
		self.label = str(label)
		self.mu = str(mu)
		self.std = str(std)
		self.interest = interest
	def __str__(self):
		if self.interest:
			return "{Unemployment "+self.label+" &#8594; &mu;="+self.mu+", &sigma;="+self.std+"}"
		else:
		#	return "Unemployment "+self.label+" did not have an interesting association rule."
			return ''
def isInteresting(mu,stdd,n,others,delta):
	oMu = mean(others)
	oStd = std(others,oMu)
	oN = len(others)
	return z_score(mu,oMu,delta,stdd,oStd,n,oN)
	

def z_score(mu1, mu2, delta, std1, std2, n1, n2):
	if n1 == 0 or n2 == 0:
		return False
	denom = math.sqrt( ((std1**2)/n1 ) + ((std2**2)/n2) )
	if denom == 0:
		return True
	z = abs(mu2-mu1-delta)/denom
	print("z="+str(z))
	if z > 1.64:
		return True
	return False

def mean(values):
	if len(values)==0:
		return 0
	sum = 0
	for value in values:
		sum += value
	return sum/len(values)
	
def std(values, mean):
	if len(values)==0:
		return 0
	sum = 0
	for value in values:
		sum += (value - mean)**2
	sum /= len(values)
	return math.sqrt(sum)
	
def setDiff(wholeList,removeList):
	return [x for x in wholeList if x not in removeList]
	
# stateData = list[ (state_id,year,month,unemployment_value,comparison_value) ]
def stat_association(stateData,delta):
		lte2 = []
		btw24 = []
		btw46 = []
		btw68 = []
		btw810 =[]
		gt10 = []
		allValues = []
		
		for item in stateData:
			ueValue = item[3]
			allValues.append(item[4])
			
			if ueValue <= 2:
				lte2.append(item[4])
			elif ueValue > 2 and ueValue <= 4:
				btw24.append(item[4])
			elif ueValue > 4 and ueValue <= 6:
				btw46.append(item[4])
			elif ueValue > 6 and ueValue <= 8:
				btw68.append(item[4])
			elif ueValue > 8 and ueValue <= 10:
				btw810.append(item[4])
			else:
				gt10.append(item[4])
		
		rules = []
		
		lte2mu = mean(lte2)
		lte2std = std(lte2,lte2mu)
		lte2interest = isInteresting(lte2mu,lte2std,len(lte2),setDiff(allValues,lte2),delta)
		rules.append(str(StatisticalAssociationRule("&le; 2",lte2mu,lte2std,lte2interest)))
		
		btw24mu = mean(btw24)
		btw24std = std(btw24,btw24mu)
		btw24interest = isInteresting(btw24mu,btw24std,len(btw24),setDiff(allValues,btw24),delta)
		rules.append(str(StatisticalAssociationRule("&gt; 2 and &le; 4",btw24mu,btw24std,btw24interest)))
		
		btw46mu = mean(btw46)
		btw46std = std(btw46,btw46mu)
		btw46interest = isInteresting(btw46mu,btw46std,len(btw46),setDiff(allValues,btw46),delta)
		rules.append(str(StatisticalAssociationRule("&gt; 4 and &le; 6",btw46mu,btw46std,btw46interest)))
		
		btw68mu = mean(btw68)
		btw68std = std(btw68,btw68mu)
		btw68interest = isInteresting(btw68mu,btw68std,len(btw68),setDiff(allValues,btw68),delta)
		rules.append(str(StatisticalAssociationRule("&gt; 6 and &le; 8",btw68mu,btw68std,btw68interest)))
		
		btw810mu = mean(btw810)
		btw810std = std(btw810,btw810mu)
		btw810interest = isInteresting(btw810mu,btw810std,len(btw810),setDiff(allValues,btw810),delta)
		rules.append(str(StatisticalAssociationRule("&gt; 8 and &le; 10",btw810mu,btw810std,btw810interest)))
		
		gt10mu = mean(gt10)
		gt10std = std(gt10,gt10mu)
		gt10interest = isInteresting(gt10mu,gt10std,len(gt10),setDiff(allValues,gt10),delta)
		rules.append(str(StatisticalAssociationRule("&gt; 10",gt10mu,gt10std,gt10interest)))
		
		# values = list[ (state_id,year,month,unemployment_value,comparison_mu+2*std,comparison_mu-2*std) ]
		values = []
		for item in stateData:
			ueValue = item[3]
			if ueValue <= 2:
				values.append((item[0],item[1],item[2],item[3],lte2mu+(2*lte2std),lte2mu-(2*lte2std),item[4]))
			elif ueValue > 2 and ueValue <= 4:
				values.append((item[0],item[1],item[2],item[3],btw24mu+(2*btw24std),btw24mu-(2*btw24std),item[4]))
			elif ueValue > 4 and ueValue <= 6:
				values.append((item[0],item[1],item[2],item[3],btw46mu+(2*btw46std),btw46mu-(2*btw46std),item[4]))
			elif ueValue > 6 and ueValue <= 8:
				values.append((item[0],item[1],item[2],item[3],btw68mu+(2*btw68std),btw68mu-(2*btw68std),item[4]))
			elif ueValue > 8 and ueValue <= 10:
				values.append((item[0],item[1],item[2],item[3],btw810mu+(2*btw810std),btw810mu-(2*btw810std),item[4]))
			else:
				values.append((item[0],item[1],item[2],item[3],gt10mu+(2*gt10std),gt10mu-(2*gt10std),item[4]))
		
		return {'values':values,'rules':rules}
		
		
		
		
			
		
	
	
		