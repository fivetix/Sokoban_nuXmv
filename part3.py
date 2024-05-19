import subprocess
import os
import re

class sokoban_smv_generator():
    def __init__(self, input_board):
        self.input_board = input_board.strip().splitlines()
        self.board = []  # 0s and 1s for floor and walls
        self.player = []  # [x, y] position of the player
        self.boxes = []  # List of [x, y] positions for boxes
        self.goals = []  # List of [x, y] positions for goals
        self.gen_board()
        self.N = len(self.board)
        self.M = len(self.board[0]) if self.board else 0  # Ensure correct width after gen_board
        self.res = "MODULE main\n"

    def gen_board(self):
        for y, row in enumerate(self.input_board):
            board_row = []
            for x, char in enumerate(row):
                if char == '#':
                    board_row.append(1)
                elif char == '-':
                    board_row.append(0)  # Explicit floor handling
                elif char == '.' or char == '*' or char == '+':
                    board_row.append(0)  # Goal, but treated as floor for this purpose
                    self.goals.append([x, y])
                else:
                    board_row.append(0)  # Treat all other characters as floor by default

                if char == '@'  or char == '+':
                    self.player = [x, y]
                elif char == '$' or char == '*':
                    self.boxes.append([x, y])
                
            self.board.append(board_row)

    def DEFINE_gen(self):
      self.res += "DEFINE\n"
      self.res += "  -- 1 represents wall, 0 represents an empty tile\n"
      self.res += "  grid := " + str(self.board).replace('[', '[').replace(']', ']') + ";\n"
      self.res += "  N := " + str(self.N) + ";\n"
      self.res += "  M := " + str(self.M) + ";\n"

      for index, goal in enumerate(self.goals):
          self.res += f"  i_box_goal{index+1} := {goal[1]};\n"  # j index is now i in SMV (column to row)
          self.res += f"  j_box_goal{index+1} := {goal[0]};\n"  # i index is now j in SMV (row to column)

    def VAR_gen(self):
        self.res += "VAR\n"
        self.res += f"  i_person : 0..{self.N-1};\n"
        self.res += f"  j_person : 0..{self.M-1};\n"

        # Generate variable definitions for each box
        for i in range(len(self.boxes)):
            self.res += f"  i_box{i+1} : 0..{self.N-1};\n"
            self.res += f"  j_box{i+1} : 0..{self.M-1};\n"

        self.res += "  action_person : {no-action, up, down, left, right};\n"
        self.res += "  boxes_overlap : boolean;\n"
        self.res += "  box_on_wall : boolean;\n"
        self.res += "  man_on_box : boolean;\n"
        self.res += "  man_on_wall : boolean;\n"

    def ASSIGN_gen(self):
        self.res += "ASSIGN\n"
        # Initialize player and box positions
        self.res += f"  init(i_person) := {self.player[1]};\n"
        self.res += f"  init(j_person) := {self.player[0]};\n"

        for i, box in enumerate(self.boxes):
            self.res += f"  init(i_box{i+1}) := {box[1]};\n"
            self.res += f"  init(j_box{i+1}) := {box[0]};\n"

        self.res += "  init(action_person) := {no-action};\n"
        self.res += "  init(boxes_overlap) := FALSE;\n"
        self.res += "  init(box_on_wall) := FALSE;\n"
        self.res += "  init(man_on_box) := FALSE;\n"
        self.res += "  init(man_on_wall) := FALSE;\n"

        # Define next states for man_on_wall
        self.res += "  next(man_on_wall) := case\n"
        self.res += f"    grid[i_person][j_person] = 1 : TRUE;\n"
        self.res += "    TRUE : FALSE;\n"
        self.res += "  esac;\n"

        # Define next states for man_on_box
        self.res += "  next(man_on_box) := case\n"
        for i in range(len(self.boxes)):
            self.res += f"    (i_person = i_box{i+1}) & (j_person = j_box{i+1}) : TRUE;\n"
        self.res += "    TRUE : FALSE;\n"
        self.res += "  esac;\n"

        # Define next states for box_on_wall
        self.res += "  next(box_on_wall) := case\n"
        for i in range(len(self.boxes)):
            self.res += f"    grid[i_box{i+1}][j_box{i+1}] = 1 : TRUE;\n"
        self.res += "    TRUE : FALSE;\n"
        self.res += "  esac;\n"

        # Define next states for boxes_overlap
        self.res += "  next(boxes_overlap) := case\n"
        for i in range(len(self.boxes)):
            for j in range(i + 1, len(self.boxes)):
                self.res += f"    (i_box{i+1} = i_box{j+1}) & (j_box{i+1} = j_box{j+1}) : TRUE;\n"
        self.res += "    TRUE : FALSE;\n"
        self.res += "  esac;\n"

        # Define next states for action_person considering walls
        self.res += "  next(action_person) := case\n"
        self.res += "    boxes_overlap : {no-action};\n"
        self.res += "    box_on_wall : {no-action};\n"
        self.res += "    man_on_box : {no-action};\n"
        self.res += "    man_on_wall : {no-action};\n"

        # Generate dynamic actions based on the player's position and nearby walls
        for i in range(self.N):
            for j in range(self.M):
                actions = []
                if self.board[i][j] == 0:  # Only consider actions if the current cell is not a wall
                    if i > 0 and self.board[i-1][j] == 0:  # Up
                        actions.append("up")
                    if i < self.N - 1 and self.board[i+1][j] == 0:  # Down
                        actions.append("down")
                    if j > 0 and self.board[i][j-1] == 0:  # Left
                        actions.append("left")
                    if j < self.M - 1 and self.board[i][j+1] == 0:  # Right
                        actions.append("right")

                # Add actions for this specific position
                if actions:
                    self.res += f"    (i_person = {i}) & (j_person = {j}) : {{{', '.join(actions)}}};\n"

        self.res += "    TRUE : {no-action};\n"  # Default case if no other conditions match
        self.res += "  esac;\n"
        for i in range(len(self.boxes)):
            # Next state for box i along the x-axis
            self.res += f"  next(i_box{i+1}) := case\n"
            self.res += f"    (next(action_person) = down) & (i_box{i+1} = i_person + 1) & (j_box{i+1} = j_person) & (i_box{i+1} + 1 < N) : i_box{i+1} + 1;\n"
            self.res += f"    (next(action_person) = up) & (i_box{i+1} = i_person - 1) & (j_box{i+1} = j_person) & (i_box{i+1} - 1 >= 0) : i_box{i+1} - 1;\n"
            self.res += f"    TRUE : i_box{i+1};\n"
            self.res += f"  esac;\n"

            # Next state for box i along the y-axis
            self.res += f"  next(j_box{i+1}) := case\n"
            self.res += f"     (next(action_person) = right) & (i_box{i+1} = i_person) & (j_box{i+1} = j_person + 1) & (j_box{i+1} + 1 < M) : j_box{i+1} + 1;\n"
            self.res += f"    (next(action_person) = left) & (i_box{i+1} = i_person) & (j_box{i+1} = j_person - 1) & (j_box{i+1} - 1 >= 0) : j_box{i+1} - 1;\n"
            self.res += f"    TRUE : j_box{i+1};\n"
            self.res += f"  esac;\n"

        # Define next states for moving the player
        self.res += "  next(i_person) := case\n"
        self.res += "    (next(action_person) = down) & (i_person + 1 < N) : i_person + 1;\n"
        self.res += "    (next(action_person) = up) & (i_person - 1 >= 0) : i_person - 1;\n"
        self.res += "    TRUE : i_person;\n"
        self.res += "  esac;\n"

        self.res += "  next(j_person) := case\n"
        self.res += "    (next(action_person) = right) & (j_person + 1 < M) : j_person + 1;\n"
        self.res += "    (next(action_person) = left) & (j_person - 1 >= 0) : j_person - 1;\n"
        self.res += "    TRUE : j_person;\n"
        self.res += "  esac;\n"


    def SPEC_gen(self):
        import itertools
        self.res += "LTLSPEC "

        # Generate all permutations of box indices matching with goal indices
        num_boxes = len(self.boxes)
        goal_permutations = list(itertools.permutations(self.goals, num_boxes))

        condition_groups = []
        for perm in goal_permutations:
            conditions = []
            for i, goal in enumerate(perm):
                # Notice goal[1] is the row index and goal[0] is the column index for the SMV specification
                conditions.append(f"(i_box{i+1} = {goal[1]}) & (j_box{i+1} = {goal[0]})")
            condition_groups.append("(" + " & ".join(conditions) + ")")

        # Join all permutations with an OR between them
        spec_condition = " | ".join(condition_groups)
        self.res += f"G!((!next(man_on_box) & !next(man_on_wall) & !next(box_on_wall) & !next(boxes_overlap)) & {spec_condition});\n"


    def generate_and_get_board(self):
        # Run code generation methods
        self.DEFINE_gen()
        self.VAR_gen()
        self.ASSIGN_gen()
        self.SPEC_gen()
        return self.res
        
def run_nuxmv(model_filename):
    # Run the command
    nuxmv_process = subprocess.Popen(["nuXmv", model_filename], stdin=subprocess.PIPE, stdout=subprocess.PIPE, universal_newlines=True)
    output_filename = model_filename.split(".")[0] + ".out"

    stdout, _ = nuxmv_process.communicate()

    # Save output to file
    with open(output_filename, "w") as f:
        f.write(stdout)

    print(f"Output saved to {output_filename}")

    LURD = result_to_LURD(output_filename)
    with open(output_filename, "a") as f:
        f.write(f"results in lurd format : {LURD} \n")

    return output_filename


def generate_model_file(model_string):
    model_filename = f"result_model.smv"
    with open(model_filename, "w") as f:
        f.write(model_string)
    return model_filename

def results_runtime_SAT(model_filename): # sets SAT-solver engine
    # Define the sequence of commands to run in nuXmv
    commands = f""" 
read_model -i {model_filename}
go_bmc
check_ltlspec_bmc -k 30
time
"""

    # Start nuXmv in interactive mode and send commands
    process = subprocess.Popen(['nuXmv', '-int'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output, errors = process.communicate(input=commands)

    # Optionally print outputs for debugging
    print("Output:\n", output)
    print("Errors:\n", errors)

    # Regex to find the final elapsed time and total time after check_ltlspec_bmc
    time_pattern = r"elapse: (\d+\.\d+) seconds, total: (\d+\.\d+) seconds"
    time_match = re.search(time_pattern, output)
    
    # Regex to find the last checked bound
    bound_pattern = r"-- no counterexample found with bound (\d+)"
    bound_matches = re.findall(bound_pattern, output)
    final_bound = bound_matches[-1] if bound_matches else 'unknown'

    # Extract the elapsed and total time if available
    if time_match:
        elapsed_time = time_match.group(1)
        total_time = time_match.group(2)
    else:
        elapsed_time = 'unknown'
        total_time = 'unknown'

    # Compile results into a result string
    result_string = f"Runtime after check_ltlspec_bmc -k 30: {elapsed_time} seconds (Total time: {total_time} seconds)\nLast checked bound: {final_bound}"
    return result_string

def results_runtime_BDD(model_filename): # sets BDD engine
    # Define the sequence of commands to run in nuXmv
    commands = f""" 
read_model -i {model_filename}
go
check_ltlspec
time
"""

    # Start nuXmv in interactive mode and send commands
    process = subprocess.Popen(['nuXmv', '-int'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output, errors = process.communicate(input=commands)

    # Optionally print outputs for debugging
    print("Output:\n", output)
    print("Errors:\n", errors)

    # Regex to find the final elapsed time and total time after check_ltlspec_bmc
    time_pattern = r"elapse: (\d+\.\d+) seconds, total: (\d+\.\d+) seconds"
    time_match = re.search(time_pattern, output)

    # Extract the elapsed and total time if available
    if time_match:
        elapsed_time = time_match.group(1)
        total_time = time_match.group(2)
    else:
        elapsed_time = 'unknown'
        total_time = 'unknown'

    # Compile results into a result string
    result_string = f"Runtime after check_ltlspec: {elapsed_time} seconds (Total time: {total_time} seconds)\n"
    return result_string

#def results_runtime_BDD_STEPS(model_filename):
#    return "template string BDD STEPS"
#def results_runtime_SAT(model_filename):
#    return "template string SAT"    

def generate_result_file(model_filename,output_filename):
    LURD = result_to_LURD(output_filename)
    runtime_BDD = results_runtime_BDD(model_filename)
    runtime_SAT = results_runtime_SAT(model_filename)
    
    #runtime_BDD_STEPS = results_runtime_BDD_STEPS(model_filename)
    #runtime_SAT = results_runtime_SAT(model_filename)
    results_filename = "results_for_model.out"
    with open(results_filename,"w") as f:
        
        f.write(f"results in lurd format : {LURD} \n")
        f.write(f"""runtime results SAT:\n
        {runtime_SAT}\n
        runtime results BDD:\n
        {runtime_BDD}\n
        """)
    
        
def result_to_LURD(output_filename):
    # Open the file containing the nuXmv output
    with open(output_filename, 'r') as file:
        lines = file.readlines()
    
    # Variable to store the final sequence of actions
    lurd_sequence = []
    
    # Variables to keep track of the last action and its continuation
    last_action = None
    action_count = 0

    # Loop through each line in the file
    for line in lines:
        if "action_person" in line:
            action = line.split('=')[-1].strip()
            
            # Map the action string to the corresponding direction character
            if action == "left":
                action = 'L'
            elif action == "right":
                action = 'R'
            elif action == "up":
                action = 'U'
            elif action == "down":
                action = 'D'
            else:
                action = None  # For 'no-action' or unrecognized actions
            
            if last_action and action != last_action:
                # Append the accumulated action sequence
                lurd_sequence.append(last_action * action_count)
                # Reset the count for the new action
                action_count = 0
            
            # Update the last action seen
            last_action = action
        
        if "-> State:" in line:
            if last_action:
                # Count continuity of the same action until a change occurs
                action_count += 1

    # Handle the last sequence after the loop ends
    if last_action and action_count:
        lurd_sequence.append(last_action * action_count)
    
    # Join all actions into a single string
    return ''.join(lurd_sequence)


def main():
    
    
    board_str10 = """
#########
##---####
##---#--#
###----.#
###-###.#
#-$-###.#
#-$$#####
#@--#####
#########
"""
    board_str10 = """
######
#-.###
#--###
#*@--#
#--$-#
#--###
######
"""
    board_str10 = """
########
###---##
#-$-#-##
#-#--.-#
#----#-#
##-#---#
##@--###
########
"""

    #build generator class
    generator = sokoban_smv_generator(board_str10)
    #generate smv model as a string
    smv_string = generator.generate_and_get_board()
    #convert model string to model smv 
    model_filename = generate_model_file(smv_string)
    #run nuxmv and save to output file
    output_filename = run_nuxmv(model_filename)
    #generate a result file containing runtime calculations and lurd steps
    generate_result_file(model_filename,output_filename)
    
if __name__ == "__main__":
    main()


# Example usage:
board_str1 = """
#####
#@$.#
#####
"""
# Example usage:
board_str3 = """
#######
#@----#
#--.$-#
#---###
#--$--#
#---#.#
#######
"""
# Example usage:
board_str4 = """
#######
###.###
###$###
#.$@$.#
###$###
###.###
#######
"""
# Example usage:
board_str2 = """
#####
#$@.#
#####
"""
# Example usage:
board_str5 = """
#######
#@----#
#---..#
#--#$$#
#--#--#
#--#--#
#######
"""
# Example usage:
board_str6 = """
########
#@-----#
#----###
#-$-#--#
#---#-$#
#-.-#-.#
########
"""
# Example usage:
board_str7 = """
##############
#            #
#            #
#            #
#            #
#            #
#            #
#            #
#            #
##############
"""
board_str7 = """
########
#     ##
#     ##
#     ##
#     ##
#     ##
#     ##
#     ##
#     ##
#      #
#      #
#      #
########
"""

board_str8 = """
----#####----------
----#---#----------
----#$--#----------
--###--$##---------
--#--$-$-#---------
###-#-##-#---######
#---#-##-#####--..#
#---------------..#
#####-###-#@##----#
----#-----#########
----#######--------
"""



