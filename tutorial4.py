#!/usr/bin/env python

'''
Author: John D. Anderson
Email: jander43@vols.utk.edu
Description:
    Simple trading strategy from 'PyAlgoTrade' tutorial (see Attribution)
Attribution:
    Gabriel Becedillas 2011-2015
    http://gbeced.github.io/pyalgotrade/docs/v0.18/html/tutorial.html
Usage:
    tutorial4 basic
    tutorial4 iterate <start> <stop>
'''

# libraries
from pyalgotrade import strategy
from pyalgotrade.barfeed import yahoofeed
from pyalgotrade.technical import ma


# functions
def run_strategy(smaPeriod):
    # Load the yahoo feed from the CSV file
    feed = yahoofeed.Feed()
    feed.addBarsFromCSV("orcl", "orcl-2000.csv")

    # Evaluate the strategy with the feed.
    myStrategy = MyStrategy(feed, "orcl", smaPeriod)
    myStrategy.run()
    print "Final portfolio value: $%.2f" % myStrategy.getBroker().getEquity()
    print "SMA Period: %s\n" % smaPeriod


# classes
class MyStrategy(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument, smaPeriod):
        super(MyStrategy, self).__init__(feed, 1000)
        self.__position = None
        self.__instrument = instrument
        # We'll use adjusted close values instead of regular close values.
        self.setUseAdjustedValues(True)
        self.__sma = ma.SMA(feed[instrument].getPriceDataSeries(), smaPeriod)

    def onEnterOk(self, position):
        execInfo = position.getEntryOrder().getExecutionInfo()
        self.info('BUY at $%.2f' % (execInfo.getPrice()))

    def onEnterCanceled(self, position):
        self.__position = None

    def onExitOk(self, position):
        execInfo = position.getExitOrder().getExecutionInfo()
        self.info("SELL at $%.2f" % (execInfo.getPrice()))
        self.__position = None

    def onExitCanceled(self, position):
        # If the exit was canceled, re-submit it.
        self.__position.exitMarket()

    def onBars(self, bars):
        # Wait for enough bars to be available to calculate a SMA.
        if self.__sma[-1] is None:
            return

        # else get bars
        bar = bars[self.__instrument]

        # If position was not opened, check if we should enter a long position.
        if self.__position is None:
            if bar.getPrice() > self.__sma[-1]:
                # Enter buy for 10 shares. The order is good till canceled.
                self.__position = self.enterLong(self.__instrument, 10, True)

        # Check if we have to exit the position.
        elif bar.getPrice() < self.__sma[-1] \
                and not self.__position.exitActive():
            self.__position.exitMarket()


# executable
if __name__ == '__main__':

    # exec import only
    from docopt import docopt

    # check args
    args = docopt(__doc__)

    # control flow
    if args['basic']:
        # execute
        run_strategy(15)

    elif args['iterate']:
        # get start/stop
        start = int(args['<start>'])
        stop = int(args['<stop>'])

        # iterate
        for i in range(start, stop):
            run_strategy(i)
