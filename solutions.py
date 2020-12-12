import re
from copy import deepcopy


# day1
def two_sums_to_2020(file_name):
    with open(file_name,"r") as file:
        lines = file.readlines() 
    numbers = [int(num) for num in lines]

    lenght = len(numbers)
    result = -1
    for i in range(lenght):
        for j in range(i+1,lenght):
            if numbers[i] + numbers[j] == 2020: 
                result = numbers[i] * numbers[j]
                return result, numbers[i],numbers[j]


def three_sums_to_2020(file_name):
    with open(file_name,"r") as file:
        lines = file.readlines() 
    numbers = [int(num) for num in lines]


    lenght = len(numbers)
    result = -1
    for i in range(lenght):
        for j in range(i+1,lenght):
            for k in range(j+1,lenght):
                if numbers[i] + numbers[j] + numbers[k] == 2020:
                    result = numbers[i] * numbers[j] * numbers[k]
                    return result, numbers[i],numbers[j], numbers[k]


# day2
def validate_passwords(file_name,part):
    with open(file_name,"r") as file:
        lines = file.readlines() 
    
    valid_passwords = 0

    for line in lines:
        line = line.split(" ")
        min_occur = int(line[0].split("-")[0])
        max_occur = int(line[0].split("-")[1])
        letter = line[1][0]
        password = line[2][:-1]
        counter = 0

        for char in password:
            if char == letter and part == 1:
                counter+=1
        
        valid_passwords = valid_passwords+1 if min_occur<=counter<=max_occur and part == 1 else valid_passwords

            
        if (password[min_occur-1] == letter) ^ (password[max_occur-1] == letter) and part == 2:
            valid_passwords+=1
           

    return valid_passwords

# day3
def count_encountered_trees(file_name,move_right,move_down):
    with open(file_name,"r") as file:
        lines = list(map(lambda line: line.rstrip('\n'), file.readlines()))
    
    width = len(lines[0])
    height = len(lines)
    trees = 0

    start = (0,0)
    curr_row,curr_col = start
    for i in range(height):

        if lines[curr_row][curr_col] == "#":
            trees += 1

        curr_col += move_right
        curr_row += move_down

        if curr_col > width-1:
            curr_col = curr_col%width
        
        if curr_row > height-1:
            break

    return trees


# day4
def validate_passports(file_name,part = 1):
    with open(file_name,"r") as file:
        passports = file.read().split("\n")

    valid_passports = 0
    passport_str = ""

    fields = { 
        "byr":0,
        "iyr":0,
        "eyr":0,
        "hgt":0, 
        "hcl":0,
        "ecl":0,
        "pid":0} # without cid - it is no required
    
    # regex passport validation
    regex = { 
        "byr":"^19[2-9][0-9]|^200[0-2]$",
        "iyr":"^201[0-9]$|^2020$",
        "eyr":"^202[0-9]$|^2030$",
        "hgt":"^1[5-8][0-9]cm$|^19[0-3]cm$|^59in$|^6[0-9]in$|^7[0-6]in$", 
        "hcl":"^#[a-f0-9]{6}$",
        "ecl":"^amb$|^blu$|^brn$|^gry$|^grn$|^hzl$|^oth$",
        "pid":"^[0-9]{9}$"}

    # build a string of teh next lines in file
    for val in passports:
        passport_str += " "+val

        # if blank line then new passport begins so process current
        if val == "":
            
            passport = { e.split(":")[0]:e.split(":")[1]  for e in passport_str.strip().split(" ") }

            for key in fields:
                if key in passport.keys():

                    if part == 1:
                        fields[key] = 1
                    else:
                        if re.search(regex[key],passport[key]):
                            fields[key] = 1
                        else:
                            fields[key] = 0

            if all(fields.values()):
                valid_passports += 1

            fields = {x: 0 for x in fields}
            passport_str = ""

    return valid_passports

# day5
def find_highest_seat_id(file_name):
    with open(file_name,"r") as file:
        seats = file.read().split("\n")[:-1]

    max_id = 0
    seats_id = []

    for seat in seats:
        rows = [0,127]
        cols = [0,7]
        
        for i in range(7):
            new_rows_length = (rows[1]-rows[0])//2 + 1
            if seat[i] == "F":
                rows[1] -= new_rows_length
            else:
                rows[0] += new_rows_length
            
        for i in range(3):
            new_cols_length = (cols[1]-cols[0])//2 + 1

            if seat[7+i] == "L":
                cols[1] -= new_cols_length
            else:
                cols[0] += new_cols_length

    
        unique_id = rows[0] * 8 + cols[0]
        seats_id.append(unique_id)
        max_id = unique_id if unique_id > max_id else max_id


    seats_id.sort()

    for i in range(1,len(seats_id)-1):
        if not (seats_id[i-1]+1 == seats_id[i] == seats_id[i+1]-1):
            return max_id, seats_id[i]+1


# day6
def count_anyone_answered_yes(file_name):
    with open(file_name,"r") as file:
        answers = file.read().split("\n")

    _sum = 0
    letters = { chr(97+i):0 for i in range(26)}
    group_answer = ''

    for answer in answers:
        group_answer+=answer

        if answer == "":
            for l in group_answer:
                if l in letters.keys():
                    letters[l] = 1

            _sum += sum(letters.values())
            group_answer = ""
            letters = { chr(97+i):0 for i in range(26)}

    return _sum


def count_everyone_answered_yes(file_name):
    with open(file_name,"r") as file:
        answers = file.read().split("\n")
    
    _sum = 0
    tmp = []
    letters = { chr(97+i):0 for i in range(26)}

    for answer in answers:
        if answer != "":
            tmp.append(answer)
        else:
            for letter in tmp[0]:
                result = all( letter in person for person in tmp)
                letters[letter] = 1 if result else 0

            _sum += sum(letters.values())
            letters = { chr(97+i):0 for i in range(26) }
            tmp = []

    return _sum  


# day7
def contains_shiny_gold(file_name):
    with open(file_name) as file:
        bags = file.read().split('\n')[:-1]

    my_bag = "shiny gold"
    tmp = [my_bag]
  
    for t in tmp:
        for bag in bags:
            if t in bag:
                bag_name = bag.split(" ")[0]+" "+bag.split(" ")[1]
                bags.remove(bag)
                tmp.append(bag_name)
    
    tmp = list(filter(lambda bag: bag != my_bag ,tmp))

    return len(tmp)


# class for handling 2nd problem, I used it to prepare a tree
class Bag:
    def __init__(self,name,amount):
        self.name = name
        self.amount = amount
        self.children = []
        self.sum_of_children = 0
    
    def __str__(self):
        return self.name + " - " + str(self.amount)

    def add_child(self, child):
        self.children.append(child)
    
    def print_children(self):
        if self.children:
            for child in self.children:
                print(child)
                child.print_children()
    
    def count_bags(self):
        _sum = self.sum_of_children
        if self.children:
            for child in self.children:
                _sum += (child.amount + child.amount * child.count_bags())
        else:
            return 0
        return _sum


def individual_bags_in_shiny_gold(file_name):
    with open(file_name) as file:
        bags = file.read().split('\n')[:-1]

    my_bag = Bag("shiny gold",1)

    tmp = [my_bag]
    
    for t in tmp:
        for bag in bags:
            bag_name = bag.split(" ")[0] + " " + bag.split(" ")[1]
            if bag_name == t.name:
                inner_bags = bag.split("contain ")[1].split(", ")
                for b in inner_bags:
                    if inner_bags[0] != "no other bags.":
                        x = b.split(" ")
                        n_bag = Bag(x[1]+" "+x[2],int(x[0]))
                        t.add_child(n_bag)
                        tmp.append(n_bag)
    
    result = my_bag.count_bags()
    return result


# day8
def find_infinite_loop(file_name, instructions = None):
    if not instructions:
        with open(file_name) as file:
            instructions = list(map(lambda inst: [inst.split(" ")[0],int(inst.split(" ")[1]),0] ,file.read().split("\n")[:-1]))

    curr_idx = 0
    acc = 0
    run = True
    tmp = {}
    while run:
        
        curr_inst = instructions[curr_idx]
        curr_inst[2] += 1
        
        # adding suspected instr to tmp dict idx : instr
        if curr_inst[2] == 2:
            tmp[curr_idx] = curr_inst


        # actual executing given instr
        if curr_inst[0] == "jmp":
            curr_idx += curr_inst[1]

        elif curr_inst[0] == "acc":
            acc = acc + curr_inst[1] if curr_inst[2] < 2 else acc
            curr_idx += 1
        else:
            curr_idx += 1

        # after incrementing we know the next idx
        next_idx = curr_idx
        
        # if True - its OK we executed all instr in file without any loop, else still go to next instr
        if next_idx == len(instructions):
            run = False 
        else:
            next_inst = instructions[next_idx]


        run = False if next_inst[2] == 2 or next_idx == len(instructions) else True
        
        # return acc, tmp - suspected instr if loop exists, next idx in queue
    return acc,tmp,next_idx


def fix_infinite_loop(file_name):
    with open(file_name) as file:
        instructions = list(map(lambda inst: [inst.split(" ")[0],int(inst.split(" ")[1]),0] ,file.read().split("\n")[:-1]))

    # copy of original instr
    instr_copy = deepcopy(instructions)
    # get results of the given instr
    results = find_infinite_loop("null",instructions)
    # fetch from result suspected points of the loop
    inst_that_loop = results[1]
    

    # we know that only one nop/jmp instr causes loop so only that interest us
    instr_to_check = {}
    for suspect in inst_that_loop:

        if inst_that_loop[suspect][0] == "jmp":
            instr_to_check[suspect] = inst_that_loop[suspect]
        
        if inst_that_loop[suspect][0] == "nop":
            instr_to_check[suspect] = inst_that_loop[suspect]



    # now we change every suspected jmp/nop into opposite and finnaly fix and get final acc
    for idx in instr_to_check:

        if instr_to_check[idx][0] == "jmp":
            instr_copy[idx][0] = "nop"
            r = find_infinite_loop("null",instr_copy)
            
            if r[2] == len(instr_copy):
                return r[0]

            for val in instr_copy:
                val[2] = 0
            instr_copy[idx][0] = "jmp"
            
        
        if instr_to_check[idx][0] == "nop":
            instr_copy[idx][0] = "jmp"
            r = find_infinite_loop("null",instr_copy)

            if r[2] == len(instr_copy):
                return r[0]

            for val in instr_copy:
                val[2] = 0
            instr_copy[idx][0] = "nop"
           

 

if __name__ == "__main__":
    pass
    # day1
    # print(two_sums_to_2020('input1.txt'))
    # print(three_sums_to_2020('input1.txt'))

    # day2
    # print(validate_passwords("input2.txt",1))
    # print(validate_passwords("input2.txt",2))

    # day3
    # a = count_encountered_trees('input3.txt',1,1)
    # b = count_encountered_trees('input3.txt',3,1)
    # c = count_encountered_trees('input3.txt',5,1)
    # d = count_encountered_trees('input3.txt',7,1)
    # e = count_encountered_trees('input3.txt',1,2)
    # print(b)
    # print(a*b*c*d*e)

    # day4
    # print(validate_passports("input4.txt"))
    # print(validate_passports("input4.txt",2))

    # day5 
    #print(find_highest_seat_id("input5.txt"))

    # day6
    # print(count_anyone_answered_yes("input6.txt"))
    # print(count_everyone_answered_yes("input6.txt"))

    # day7
    # print(contains_shiny_gold("input7.txt"))
    # print(individual_bags_in_shiny_gold("input7.txt"))

    # day8
    # print(find_infinite_loop("input8.txt")[0])
    # print(fix_infinite_loop("input8.txt"))

    # day9

