import numpy as np
from scipy import stats

OUTLIER_COLOR = "red"
#simple z-score calculation used to obtain outliers based on z-score
class Outliers:
	def CalculateOutliers(self,threshold):
		self.outliers = np.array([])
		self.dataZScores = stats.zscore(self.data)		
		for scoreLoc in range(len(self.dataZScores)):
			if(self.dataZScores[scoreLoc] <= (-threshold) or self.dataZScores[scoreLoc] >= threshold):
				self.outliers = np.append(self.outliers, self.data[scoreLoc])
				self.colors.append(OUTLIER_COLOR)
			else:
				self.colors.append(None)

	def __init__(self, dataSource):
		self.data = dataSource
		self.outliers = np.array([])
		self.dataZScores = np.array([])
		self.colors = []
