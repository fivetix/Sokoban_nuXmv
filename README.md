# Sokoban_nuXmv
Sokoban using nuXmv solver

for creating new sokoban board thats two ways:
1.wright it on your on and inserd it in the py file.
2.use the python file "board_to_XSB_gui" - which open a board for you where you can place the werehouse keeper/boxes/goals..


for running the codes 
1.put the python files part2/3/4 inside nuXmv folder...\bin
2.inside the py file find the main function and inside "board_str10 =" put your wanted board.
2.open command line
3.right "python part2.py"

part2: creating a smv file and run it on nuXmv.
for part 2 the output will be 2 new files in the running folder:
    1.result_model.smv - smv file that contains the sokoban code for the input board which will run in nuXmv.
    2. result_model.out - will pring the nuXmv output into this file + result in LURD format (in the last line).

part3: creating a smv file and run it on nuXmv + show run time on BDD and SAT.
for part 3 the output will be 3 new files:
    1.result_model.smv
    2.result_model.out
    3.result_for_model.out - will print the running time for BDD run and SAT run. 

part4: creating a smv file, run it with solving one box at a time + show run time on BDD and SAT.
for part 4 the output will be 3 new files:
    1.result_model.smv
    2.result_model.out
    3.cumulative_results_for_model.out - will print the running time for BDD and SAT for all the runs + the sum of them. 


important notes:
1.our grid indicated '1' as wall and '0' as empty tile.
2.places of warehouse and boxes are shows as (i,j)
3.warehouse = person
4.boxes are numbered from 1 to n.
5.the board size is indicated as N and M. 
