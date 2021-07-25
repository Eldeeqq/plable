# 📅 PLABLE
Timetable planner for FIT CTU.

## What is it?
This app is written in Python 3(.8) and streamlit. It uses [Evolutionary algorithm](https://en.wikipedia.org/wiki/Evolutionary_algorithm) to create a timetable that satisfies some strategy.

Possible bugs submit via [github issues](https://github.com/Eldeeqq/plable/issues).
## How to use it?
- Simply write a list of courses you want to attend and select semester and strategy

for example:
```
BI-DBS, BI-SAP, BI-LIN, BI-PA2
```
- Select a criteria based on which the timetable will be planned
> currently the only strategy is `Least collisions`, however, I plan to add some more in the future (f. e. `Least time in school`, `Time between classes`,`...`)
- Hit *generate* button
- If the algorithm will be able to produce some solutions, you can prewiew them (currently max. 10)


## Possible extensions
- teacher (wish/black)list
- lunch breaks
- more strategies
- timetable.fit.cvut.cz like timetable

## Evolutionary Algorihm


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


Would produce a vector: 
[1, 0, 0, 2]

### Mutation
Basically with probability `p` for each number in genotype a value from range [0, len-1] is added and then `result % len` is the final mutated gene. This is due to fact that each lab/lecture/tutoroial has finite number of parallels and this w

### Crossover 
I used [Uniform crossover](https://en.wikipedia.org/wiki/Crossover_(genetic_algorithm)#Uniform_crossover).

### Selection
I used [Tournament selection](https://en.wikipedia.org/wiki/Selection_(genetic_algorithm)#Tournament_Selection).

### Population
Initial population is `100` individuals, I run `20` generations.