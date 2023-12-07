import time
import sys
import os
from typing import *

import shutil
import validation.input_check as validate
import compiling.compiler as compile

hexadecimal = True  #Set to true if you want hexadecimal in pMem, false for binary
fast_compile = False
ASSEMBLER_FILE    = os.path.join("code_files", "mini_test.s")
PREPROCESSED_FILE = os.path.join("code_files", "preprocessedSweeper.txt")
COMPILED_FILE     = os.path.join("code_files", "compiledSweeper.txt")
VHDL_FILE         = os.path.join("code_files", "pMem.vhd")
 

#Stores all redefined 
redefinitions = {
}

undefined = []

def sendError(error_message: str) -> None:
    print("Warning!!! File couldn't compile")
    print(error_message)

def removeComments(line: str):
    index = line.find(";")
    if index == -1:
        return line
    else:
        return line[0:index]
    
def addDefines(line: str):
    result = ""
    for word in line.split():
        if word in redefinitions:
            result += str(redefinitions.get(word)) + " "
        else:
            result += word + " "
    return result
        

def cleanLine(line: str):
    #removes comments
    line = removeComments(line)
    #cleanups userinput
    line = line.replace(",", " ").lower()
    #Adds program defined renames
    line = addDefines(line)
    #Removes additional spaces between words
    words = line.split()
    line = " ".join(words)
    return line

def add_define(name: str, number: int):
    if name in redefinitions:
        print("Warning!! Redefinition have been made. ")
        print(f"From: {name} -> {redefinitions[name]}")
        print(f"To:   {name} -> {number}")
    redefinitions[name] = number

def add_label(name: str, pm_count: int):
    if name.endswith(":"):
        name = name[:-1]
    add_define(name, pm_count)

def execute_define(instruction: str, argv: List[str]):
    if instruction.startswith("#define"):
        add_define(argv[0], argv[1])
    else:
        assert False, "Couldn't find instruction: '" + str(instruction) + "'"

def countLines(filename: str) -> int:
    with open(filename, "r") as file:
        return len(file.readlines())

def initVhdl(vhdl_file):

    start = """library IEEE;
use IEEE.STD_LOGIC_1164.all;
use IEEE.NUMERIC_STD.all;
--  PM(24bit)
-- OP_GRx_M_ADDR  (5_3_3_13)
-- 00000_000_000_00000000000000
entity pMem is
  port(
    clk : in std_logic;
    pAddr : in unsigned(11 downto 0);
    add_pMem : in unsigned(23 downto 0);
    we_pMem : in std_logic;
    pData : out unsigned(23 downto 0));
end pMem;

architecture Behavioral of pMem is


""" 


    l0 = "--Following redefines exists: \n"
    for key, value in redefinitions.items():
        l0 += "--\t"+ str(key) + " = " + str(value) + "\n"
    l0 += "\n"
    l1 = "type p_mem_t is array (0 to 255) of unsigned(23 downto 0); \n"
    l2 = "constant p_mem_c : p_mem_t := \n "
    l3 = "\t ( \n"
    vhdl_file.write(start+l0+l1+l2+l3)

def vhdlClose(vhdl_file):
    vhdl_file.write("\n   others => (others=> '0'));") 
    end = """
  signal p_mem : p_mem_t := p_mem_c;


begin  -- pMem

  process(clk)
  begin 
    if rising_edge(clk) then
      if (we_pMem = '1') then
        p_mem(to_integer(pAddr)) <= add_pMem;
      end if;
    end if;
  end process;

  pData <= p_mem(to_integer(pAddr));

end Behavioral;

    """
    vhdl_file.write(end)
    vhdl_file.close()



def writeFiles(compiled, vhdl, line: str):
    compiled_line = compile.compiled_line(line)
    #compiled_line = compiled_line[:5] + "_" + compiled_line[5:8] + "_" + compiled_line[8:11] + "_" + compiled_line[11:]
    if hexadecimal:
        compiled_line = '\n'.join([hex(int(line, 2))[2:].zfill(6) for line in compiled_line.split('\n')])
    compiled.write(compiled_line + "\n")    
    for i, l in enumerate(compiled_line.splitlines()):
        comment = "\t --" + line if i == 0 else ""  # Conditional comment for the first line
        if hexadecimal:
            vhdl.write(f'\t x"{l}",{comment}\n')
        else:
            vhdl.write(f'\t"{l}",{comment}\n')



def preCompile():
    pm_count = 0 
    preprocess   = open(PREPROCESSED_FILE, "w+")

    with open(ASSEMBLER_FILE, "r") as assembler_code:
        for count, line in enumerate(assembler_code):
            assert all(ord(c) < 128 for c in line), "Line '" + count + "' is NOT ascii"
            line = cleanLine(line)
            if line.isspace() or len(line) == 0: 
                continue
            instruction = line.split()[0]
            args = line.split()[1:]

            args_copy = args.copy()
            for i, l in enumerate(args_copy):
                if validate.is_undefined(l):
                    undefined.append(l)
                    args_copy[i] = "0" 


            validate.checkInput(instruction, args_copy, count)

            if validate.is_preprocess_ins(instruction):
                execute_define(instruction, args)
                continue
            if validate.is_label(instruction):
                add_label(instruction, pm_count)
                continue
            modified_line = [instruction] + args_copy
            pm_count += compile.compiled_line(' '.join(modified_line)).count('\n') + 1
            preprocess.write(line + "\n")
    preprocess.close()

    for label in undefined:
        if label not in redefinitions:
            sendError(f"The label '{label}' have NOT been defined. Please change it")
            exit(0)
            


def compile_code():
    compiled_code       = open(COMPILED_FILE, "w+")
    vhdl_code           = open(VHDL_FILE, "w+")
    initVhdl(vhdl_code)
    with open(PREPROCESSED_FILE, "r") as assembler_code:
        for count, line in enumerate(assembler_code):
            line = cleanLine(line)
            instruction = line.split()[0]
            args = line.split()[1:]

            validate.checkInput(instruction, args, count)

            if validate.is_preprocess_ins(instruction):
                execute_define(instruction, args)
                continue
            if validate.is_label(instruction):
                compiled_code.close()
                pm_count = countLines(COMPILED_FILE)
                compiled_code = open(COMPILED_FILE, "a+")
                add_label(instruction, pm_count)
                continue

            writeFiles(compiled_code, vhdl_code, line)

    compiled_code.close()
    vhdlClose(vhdl_code)




def copy_file(filename):
    # Open the original file in read-binary mode
    with open(filename, 'rb') as original_file:
        # Create a new file name for the copy
        copy_filename = filename + '.copy'
        # Open the copy file in write-binary mode
        with open(copy_filename, 'wb') as copy_file:
            # Copy the contents of the original file to the copy file
            shutil.copyfileobj(original_file, copy_file)
    # Return the name of the copy file
    return copy_filename



def progressbar(it, prefix="", size=60, out=sys.stdout): # Python3.3+
    count = len(it)
    def show(j):
        x = int(size*j/count)
        print("{}[{}{}] {}/{}".format(prefix, "#"*x, "."*(size-x), j, count), 
                end='\r', file=out, flush=True)
    show(0)
    for i, item in enumerate(it):
        yield item
        show(i+1)
    print("\n", flush=True, file=out)


if __name__ == '__main__':
    if os.name == 'posix':
        os.system('clear')
    if os.name == 'nt':
        os.system('cls')
    print("Compile begins\n")
    preCompile()
    compile_code()
    if not fast_compile:
        for i in progressbar(range(15), "Computing: ", 40):
            time.sleep(0.1) # any code you need
        print("Compile finished without failures\n")
        time.sleep(2.5)
    else:
        print("Compile finished without failures\n")





