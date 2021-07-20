# 📅 PLABLE
Timetable planner for FIT CTU.

## What is it?
This app uses [Evolution algorithm](https://en.wikipedia.org/wiki/Evolutionary_algorithm) to create a class schedule satisfying some strategy.

## How to use it?
- Simply write a list of courses you want to attend and select specific semester

for example:
```
BI-DBS, BI-SAP, BI-LIN, BI-PA2
```
- Select a criteria based on which the timetable will be planned
> currently the only strategy is `Minimal collision`, however, I plan to add some more in the future (f. e. `Least time in school`, `Minimal span between classes`,`...`)
- Hit generate button
- If the algorithm will be able to produce some solutions, you can prewiew them (max. 10)


## Possible extensions
- teacher (wish/black)list
- lunch breaks
- more strategies

## Evolution Algorihm


### Genotype
Based on provided list of courses, the application gets the information about `lectures`, `tutorials` and `labs` of each course (if present).

These informations are then encoded as a vector of numbers corresponding to an index of `lecture`/`tutorial`/`lab` of specific course.

<table style="border-collapse: collapse; border: medium none; border-spacing: 0px;">
	<tr>
		<td style="border-color: rgb(0, 0, 0); border-style: solid; border-width: 1px; padding-right: 3pt; padding-left: 3pt;">
			<center>Course name</
			<br>
		</td>
		<td style="padding-right: 3pt; padding-left: 3pt;" colspan="3">
			<center>course a</center>
		</td>
		<td style="padding-right: 3pt; padding-left: 3pt;">
			<center>course b<wbr></center>
		</td>
		<td style="padding-right: 3pt; padding-left: 3pt;" colspan="3">
			<center>course c<wbr></center>
		</td>
	</tr>
	<tr>
		<td style="border-color: rgb(0, 0, 0); border-style: solid; border-width: 1px; padding-right: 3pt; padding-left: 3pt;">
			Parallel type<wbr>
		</td>
		<td style="padding-right: 3pt; padding-left: 3pt;" colspan="2">
			Lecture
		</td>
		<td style="padding-right: 3pt; padding-left: 3pt;">
			Tutorial
		</td>
		<td style="padding-right: 3pt; padding-left: 3pt;">
			Tutorial<wbr>
		</td>
		<td style="padding-right: 3pt; padding-left: 3pt;" colspan="3">
			Lecture
		</td>
	</tr>
	<tr>
		<td style="border-color: rgb(0, 0, 0); border-style: solid; border-width: 1px; padding-right: 3pt; padding-left: 3pt;">
			Parallel no<wbr>
		</td>
		<td style="padding-right: 3pt; padding-left: 3pt;">
			<s>1</s>
		</td>
		<td style="padding-right: 3pt; padding-left: 3pt;">
			2
		</td>
		<td style="padding-right: 3pt; padding-left: 3pt;">
			1
		</td>
		<td style="padding-right: 3pt; padding-left: 3pt;">
			123
		</td>
		<td style="padding-right: 3pt; padding-left: 3pt;">
			<s>1</s>
		</td>
		<td style="padding-right: 3pt; padding-left: 3pt;">
			<s>2</s>
		</td>
		<td style="padding-right: 3pt; padding-left: 3pt;">
			3
		</td>
	</tr>
    	<tr>
		<td style="border-color: rgb(0, 0, 0); border-style: solid; border-width: 1px; padding-right: 3pt; padding-left: 3pt;">
			Index<wbr>
		</td>
		<td style="padding-right: 3pt; padding-left: 3pt;">
			0
		</td>
		<td style="padding-right: 3pt; padding-left: 3pt;">
			1
		</td>
		<td style="padding-right: 3pt; padding-left: 3pt;">
			0<wbr>
		</td>
		<td style="padding-right: 3pt; padding-left: 3pt;">
			0<wbr>
		</td>
		<td style="padding-right: 3pt; padding-left: 3pt;">
			0
		</td>
		<td style="padding-right: 3pt; padding-left: 3pt;">
			1
		</td>
		<td style="padding-right: 3pt; padding-left: 3pt;">
			2
		</td>
	</tr>
</table>

Could produce vector: 
[1, 0, 0, 2]

### Mutation
For each item in vector with a probability `p` the mutation is done as following:
```
get random number from range [0, max_index]
add the two numbers 
do new_number mod max_index+1
```

### Crossover 
I used [Uniform crossover](https://en.wikipedia.org/wiki/Crossover_(genetic_algorithm)#Uniform_crossover).

### Selection
I used [Tournament selection](https://en.wikipedia.org/wiki/Selection_(genetic_algorithm)#Tournament_Selection).

### Population
Initial population is `100` individuals, I run `20` generations.