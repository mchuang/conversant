

Graphs:
1. Since data file has time, value, and some data center type, first idea is to draw a standard line plot to better understand the nature of the data.
2. I started by plotting line graphs for each of the data centers. First graph is unreadable with the heavy negative skew values. A quick google search suggeests rtb = real time bids so values might be money. Remove negative values and plot another graph. 
3. Second graph is readable and clearly displays similar pattern between two of the data center lines. In addition, both these data centers have 2 massive drops in value at approximately the same time while the 3rd data center has periodic trend except for one instance of time. 
4. How to analyze graphs programmatically. Find intersections, periodic trends, common slopes, common accelerations.

Findings:
1. Negative values might be significant. Reasons could be sign overflow, corrupted network, or server downtime?
2. Two data centers have a similar pattern in bids. Best to prove via common slopes and acceleration.
3. The third data center had its own periodic trend.
4. 

Challenges:
1. How to prove negative records have impact on graph? Current solution is to have a special Queue based on time for recent events as possible reason for big events in data stream.
2. How to detect periodic trends for one of the data centers? Temporary solution is to keep a running average value and see if it changes at equidistant points in time.
3. 
