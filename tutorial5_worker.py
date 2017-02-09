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
    tutorial5_worker
'''

# libraries
from pyalgotrade.optimizer import worker
import rsi2

# executable
if __name__ == '__main__':
    worker.run(rsi2.RSI2, "localhost", 5000, workerName="localworker")
