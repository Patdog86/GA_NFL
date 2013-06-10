from datetime import datetime
import string

import numpy as np

from pandas.core.api import DataMatrix, DateRange
from pandas.stats.linmodel import LinearModel, XSLinearModel

N = 100

start = datetime(2009, 9, 2)
dateRange = DateRange(start, periods=N)

def makeDataMatrix():
    data = DataMatrix(np.random.randn(N, 7),
                      columns=list(string.ascii_uppercase[:7]),
                      index=dateRange)

    return data

#-------------------------------------------------------------------------------
# Standard rolling linear regression

data = makeDataMatrix()
model = LinearModel(data, window=100, minPeriods=80)
model.parseFormula('A ~ B + C + D + E + F + G + I')
model.fit()

# Extremely basic summary

model.summary(dateRange[-1])

print model.beta()
print model.rsquare()
print model.tstat()

#-------------------------------------------------------------------------------
# Panel regression

data = {
    'A' : makeDataMatrix(),
    'B' : makeDataMatrix(),
    'C' : makeDataMatrix()
}

panelModel = XSLinearModel(data, window=50, minPeriods=20)
panelModel.parseFormula('A ~ B + C + I')
panelModel.fit()

# Same diagnostic statistics as per above

rows = random.sample(nfldata1.index, int(round(split*samplesize)))
nfldata1_train = np.array(nfldata1.ix[rows])
nfldata1_test = np.array(nfldata1.drop(rows))
nfltarget1_train = np.array(nfltarget1.ix[rows])
nfltarget1_test = np.array(nfltarget1.drop(rows))
results = sm.OLS(nfltarget1_train, nfldata1_train).fit()
results.summary()