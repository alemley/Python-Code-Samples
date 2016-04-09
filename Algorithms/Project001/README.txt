I could not figure out how to read files from a sub directory in time,
but it works if the .txt files are in the working directory.

Pseudo-code:

if (x,y, maze out_of_bounds) 
	basic_operations++
	return false
if (x,y, maze occupied) 
	basic_operations++
	return false
if (x,y, maze finish) 
	basic_operations++
	return true
mark x,y, maze with 'o'
if (find_path(North of x,y, maze) is true) 
	basic_operations++
	return true
if (find_path(East of x,y, maze) is true)
	basic_operations++
	return true
if (find_path(South of x,y, maze) is true) 
	basic_operations++
	return true
if (find_path(West of x,y, maze) is true) 
	basic_operations++
	return true
mark x,y, maze as dead-end
return false