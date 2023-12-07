from typing import *
import sys
sys.path.append("..") # Adds higher directory to python modules path.
from validation import input_check

dont_care = "dont_care"

operations = {
    "ldi" : "00000",
    "load": "00000",
    "store": "00001",
    "add": "00010",
    "and": "00011",
    "sub": "00100",
    "lsr": "00101",
    "bra": "00110",
    "bne": "00111",
    "out": "01000",
    "addreg": "01001",
    "cmp": "10010", 
    "beq": "01011",
    "bge": "01100",
    "mul": "01110",
    "loadreg": "10000",
    "storereg": "10001",
    "cmpreg": "01101",
    "draw":   "01010",
    "drawcursor": "10111",
    "in":    "10011",
    "mulmem": "10100",
    "random": "10101"
}


io_registers = {"vga_x": 0, "vga_y": 1, "vga_tile": 2, "random": 24, "joystick": 8, "dont_care": 0}
registers = {"gr0": "000", "gr1": "001", "gr2": "010", "gr3": "011", "gr4": "100", "gr5": "101", "gr6": "110", "gr7": "111",
             "r0": "000", "r1": "001", "r2": "010", "r3": "011", "r4": "100", "r5": "101", "r6": "110", "r7": "111", "dont_care": "000"}
modes = {
    "direkt"    :   "000",
    "immediate" :   "001", #Använder adressen under som konstant
    "indirekt"  :   "010",
    "index"     :   "011",
    "holder_1"  :   "100",
    "holder_2"  :   "101",
    "holder_3"  :   "110",
    "holder_4"  :   "111",
    "dont_care" :   "000"
}
#immediate plockar PM under

OP_BITS = 5
GRx_BITS = 3
MODE_BITS = 3
ADRESS_BITS = 13
EMPTY = "000000000000000000000000"
_  =    "00000_000_000_1000000000000"

def chooseOP(line: str, op: str) -> str:
    return operations[op] + line[5:]

def chooseGrx(line: str, reg: str):
    return line[:OP_BITS] + registers[reg] + line[OP_BITS+GRx_BITS:]

def chooseMode(line: str, mode: str) -> str:
    return line[:OP_BITS+GRx_BITS] + modes[mode] + line[OP_BITS+GRx_BITS+MODE_BITS:]

def chooseAdress(line: str, constant: str) -> str:
    if constant == "dont_care":
        constant = 0
    if constant in io_registers:
        constant = io_registers[constant]
    return line[:OP_BITS+GRx_BITS+MODE_BITS] + format(int(constant), "013b")

def createConstantLine(constant: str) -> str:
    return "{0:024b}".format(int(constant)) 

def createLine(op: str, grx: str, mode: str, adress: str) -> str:
    line = chooseOP(EMPTY, op)
    line = chooseGrx(line, grx)
    line = chooseMode(line, mode)
    return chooseAdress(line, adress)

def getModeFromReg(reg: str) -> str:
    for mode, value in modes.items():
        if value == registers[reg]:
            return mode

def compile_ldi(args: List[str]):
    line_1 = createLine("ldi", args[0], "immediate", 0)
    line_2 = createConstantLine(args[1])
    return line_1 + "\n" + line_2

def compile_load(args: List[str]):    
    if input_check.isValidRegister(args[0]) and input_check.isValidRegister(args[1]):
        return createLine("loadreg", args[0], getModeFromReg(args[1]), 0)
    return createLine("load", args[0], "direkt", args[1])

def compile_store(args: List[str]):
    #store 500 gr2
    if input_check.isValidRegister(args[0]) and input_check.isValidRegister(args[1]):
        return createLine("storereg", args[0], getModeFromReg(args[1]), 0)
    res = createLine("store", args[1], "direkt", args[0])
    return res


def compile_add(args: List[str]):
    #add gr2, 256
    if input_check.isValidNumber(args[1]):
        return createLine("add", args[0], "direkt", args[1])
    
    #add gr3, gr4
    elif input_check.isValidRegister(args[1]):
        #puts the second register in mode bits
        for mode, value in modes.items():
            if value == registers[args[1]]:
                return createLine("addreg", args[0], mode, 0)
    print("UNDEFINED IN COMPILE_ADD!!!!!!!!")
    exit()

def compile_out(args: List[str]):
    #out vga_x gr3
    return createLine("out", args[1], "direkt",io_registers[args[0]] )

def compile_sub(args: List[str]):
    #sub gr5 400
    return createLine("sub", args[0], "direkt", args[1])

def compile_and(args: List[str]):
    #and gr5 400
    return createLine("and", args[0], "direkt", args[1])
def compile_halt(args: List[str]):
    return "011110000000000000000000"

def compile_mul(args: List[str]):
    if input_check.isValidMemoryAdress(args[1]):
        return createLine("mulmem", args[0], "direkt", args[1])
    for mode, value in modes.items():
            if value == registers[args[1]]:
                return createLine("mul", args[0], mode, 0) 
    return "?????????????????????? mul failed"

def compile_bra(args: str) -> str:
    return createLine("bra", "gr0", "direkt", args[0])

def compile_cmp(args: str) -> str:
    if input_check.isValidRegister(args[0]) and input_check.isValidRegister(args[1]):
        return createLine("cmpreg", args[0], getModeFromReg(args[1]), 0)
    return createLine("cmp", args[0], "direkt", args[1])

def compile_bne(args: str) -> str:
    return createLine("bne", dont_care, dont_care, args[0])

def compile_draw(args: str) -> str:
    return createLine("draw", dont_care, dont_care, dont_care)

def compile_drawCursor(args: str) -> str:
    return createLine("drawcursor", dont_care, dont_care, dont_care)

def compile_bra(args: str) -> str:
    return createLine("bra", dont_care, dont_care, args[0])

def compile_in(args: str) -> str:
    if args[1] == "random":
        return createLine("random", args[0], "direkt", args[1])
    elif args[1] == "joystick":
        return createLine("in", args[0], "direkt", args[1])
    return f"undefined IN ???????????????????????? {args}" 

def compile_beq(args: str) -> str:
    return createLine("beq", dont_care, dont_care, args[0])

def compiled_line(line: str) -> str:
    instr = line.split()[0]
    args = line.split()[1:]
    if instr == "ldi":
        return compile_ldi(args)
    elif instr == "add":
        return compile_add(args)
    elif instr == "load":
        return  compile_load(args)
    elif instr == "store":
        return compile_store(args)
    elif instr == "out":
        return compile_out(args)
    elif instr == "sub":
        return compile_sub(args)
    elif instr == "and":
        return compile_and(args)
    elif instr == "halt":
        return compile_halt(args)
    elif instr == "mul":
        return compile_mul(args)
    elif instr == "bra":
        return compile_bra(args)
    elif instr == "cmp":
        return compile_cmp(args)
    elif instr == "bne":
        return compile_bne(args)
    elif instr == "draw":
        return compile_draw(args)
    elif instr == "drawcursor":
        return compile_drawCursor(args)    
    elif instr == "in":
        return compile_in(args)
    elif instr == "beq":
        return compile_beq(args)
    
    return "UNDEFINED INSTRUCTION"


