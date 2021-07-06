import pandas as pd

def get_data_from_webpage(url):
    # This returns a list of dataframes
    # if there are multiple tables in html, we would need multiple dataframes
    # If there is one table in html, we only need one
    t_table = pd.read_html(url, header=0)
    # Element 0 is the DataFrame we want
    return t_table[0]

def get_float_array_from_dataframe(df, col_name):
    # First we will get the column in col_name
    col = df[col_name]
    # Next we have to strip off the first row of text
    col = col.drop(col.index[0])
    # We can then return it as an array -
    # col.values is an array of strings, the following code
    # converts all of the values to float
    return [float(x) for x in col.values]

def findClosestVal(data, val):
    mini = -1
    print("here goes...")
    avgDiff = 0
    avgDiffs = []
    sortedData = data
    sortedData = sorted(sortedData)
    minDiffs = []
    for d in data:
        print(d)
    print("-----------------")
    for d in sortedData:
        print(d)
    print("-----------------")
    for i in range(0,len(sortedData)-1):
        avgDiffs.append(sortedData[i+1]-sortedData[i])
    for i in range(0,len(avgDiffs)):
        avgDiff = avgDiff + avgDiffs[i]
    avgDiff = avgDiff/len(avgDiffs)
    print(avgDiff)
    # avgDiff is the average increment that the sorted list of values goes up by
    # We are checking to see if the input value is lower than the minimum value in the array by the average increment
    # and checking to see if it's higher than the maximum value by the average increment
    if val < min(data)-avgDiff:
        print("Looks like you've got a value that's too low")
    elif val > max(data)+avgDiff:
        print("Looks like you've got a value that's too high")
    else:
        for i in range(0,len(sortedData)):
            minDiffs.append(abs(val-sortedData[i]))
        minDiff = min(minDiffs)
        for i in range(0,len(minDiffs)):
            if minDiff == minDiffs[i]:
                mini = i
        val = sortedData[mini]
        for i in range(0,len(data)):
            if val == data[i]:
                mini = i
    return mini, val
    

url = r'http://ouopentextbooks.org/thermodynamics/saturation-properties-temperature-table/'
df = get_data_from_webpage(url)
#This is only so that we can see the whole data frame instead of just a snippet
with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    print(df)


print("=======================================================================")

#dfHeader is now an array of the column names to avoid typos
dfHeader = df.columns
#dfHeader has the 0th element as "Temp" for temperature
data = get_float_array_from_dataframe(df, dfHeader[0])
#this finds the index value and the closest value out of the data array given an input value
mini, val = findClosestVal(data, 75.5)


print(str(mini) + ":   " + str(data[mini]))

print("-----------------------------------------------------")
print(df.loc[mini+1,:])



