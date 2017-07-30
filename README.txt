Files of interest: statistics.py, conversant.py

Setup:
Relevant libraries: scipy, numpy, matplotlib, pandas, sklearn
Installation: I installed anaconda for the scipy stack. Will need to run code.
How to run: Command prompt (I used anaconda prompt) and simply run 'python conversant.py data.Montoya.txt' or any data file as cmd line argument.
Execution: Code should only display data I deem relevant to my findings and conclusions. A few graphs should be generated in working directory and console should display results of statistical tools.  
Note: Code not optimized for large data

Findings:
1. Since data file has time, value and some data center type, draw standard line plot to understand nature of data.
2. Negative values might be insignificant. Simple google search suggests rtb-requests are real time bids and values are money values and therefore should not be negative. Negative values also mostly come from single data center. Reasons these exist could be sign overflow, corrupted network, or potential exploit? 
3. After reading and using augmented dickey fuller test, results suggest that Data center A does not have unit root and is a stationary time series of significance level around 5.5% (meaning around 5.5% chance that it is statistical fluke).Notable results show for data center I but at significance level of 8.6% while data center S is clearly not stationary with p-value at 0.788
4. Applied adfuller test again on the difference of data centers S and I. Theoretically, if one is simply offset by the other, the difference of the two should yield a stationary time series. Results showed that it may not be necessarily true with p-value of 0.205, even though there is a pattern to human eye. Linear regression test on set of difference values yielded no conclusion either.
Graphs:
simpleGraph.png - Since data file has time, value, and some data center type, first idea is to draw a standard line plot to better understand the nature of the data.
noNegatives.png - First graph is unreadable with the heavy negative skew values. A quick google search suggeests rtb = real time bids so values might be money. Remove negative values and plotted another graph.
simplify.png - Added vertical lines to represent instances where negatives values were recorded. In addition, both these data centers have 2 massive drops in value at approximately the same time while the 3rd data center has periodic trend except for one instance of time.


Challenges:
1. How to write code to analyze graphs without human eyes? Use math modules? Statistics? Machine learning? 
2. How to detect periodic trends for one of the data centers? 
3. How to show relationship between two line plots? Even with the common timestamps, ADFuller test on the differences might only work for a constant offset. What if one plot is multiplied or shifted?

