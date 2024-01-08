# gradient
The goal of the gradient.py script is to interpolate numerical values along a linear color gradient.
The python file integrates with Grasshopper script (gradient.gh, pictured in example.png), and offers a performance improvement of ~22% over the Grasshopper-only solution (tested with 8760 yearly data).
Note that "colors," "numbers," and "_range" variables are defined in the Grasshopper script--not in the python file.


INPUTS:
Three inputs are required:
    1 - colors: A list of RGB values
    2 - numbers: A list of floating point values (e.g. temperature measurements for every hour of the year)
    3 - _range: A list of floating point values matching the length of the "colors" list, and corresponding to the domain of "numbers"



PROCESS:
Each number falls into a bucket corresponding with steps in the range (e.g. 42.98 will fall into the bucket of 40 to 60).  That number is then normalized to a number between 0 and 1, corresponding to the low and high value of the bucket (e.g. 42.98 normalizes to .149).  The normalized number is called the "position."  To determine what color should represent the original number, the position is input to the following formula:

    deltaC = color2 - color1
    interpcolor = position(deltaC) + color1

For example:
position = .149
color1 = (206,233,237)
color2 = (245,245,245)
deltaC = (39, 12, 8)
interpcolor = .149 * (39,12,8) + (206,233,237) = (211,234,238)



OUTPUT
The output is a list of RGB values that represents the list of input numbers.
