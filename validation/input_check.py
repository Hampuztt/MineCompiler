from typing import *



#Responsible for all input validation 

max_constant = 8191 #2^13 -1

labels = []
registers = ["gr0", "gr1", "gr2", "gr3", "gr4", "gr5","gr6","gr7",
             "r0", "r1" , "r2" ,"r3"  ,"r4"  ,"r5"  ,"r6" ,"r7"]

io_registers = {"vga_x": 0, "vga_y": 1, "vga_tile": 2, "random": 3, "joystick": 8}
ins_args = {
    "bra": 1,
    "inc": 1,
    "add": 2,
    "mov": 2,
    "ldi": 2,
    "load": 2,
    "store": 2,
    "out": 2,
    "sub": 2,
    "and": 2,
    "cmp": 2,
    "breq": 1,
    "bne": 1,
    "bra": 1,
    "beq": 1,
    "mul": 2,
    "in":  2,
    "halt": 0,
    "draw": 0,
    "drawcursor": 0

    }



preprocess_ins = {
    "#define": 2,
}

PM_SIZE = 2048




def correct_argc(instr: str, args: List[str]) -> bool:
    if is_label(instr) or isNoArgs(instr) :
        #Since label names depend on the programmer unlike other instructions
        return len(args) == 0
    if is_preprocess_ins(instr):
        return len(args) == preprocess_ins.get(instr)
    else:
        return len(args) == ins_args.get(instr)


def is_label(instr: str) -> bool:
    #Label instructions are always str+:
    res = instr[-1] == ":" and len(instr) > 1
    return res

def isNoArgs(instr: str) -> bool:
    return instr in ins_args and ins_args[instr] == 0

def is_preprocess_ins(instr: str) -> bool:
    return instr in preprocess_ins

def isInstruction(instr: str) -> bool:
    return instr in ins_args or is_preprocess_ins(instr) or is_label(instr)

def isValidRegister(arg: str) -> bool:
    return arg in registers

def isIoRegister(arg: str) -> bool:
    return arg in io_registers

def isValidNumber(arg: str) -> bool:
    return arg.isdigit()

def isValidMemoryAdress(arg: str) -> bool:
    #To be implemented
    return isValidNumber(arg) and ( 0 <= int(arg) < PM_SIZE) 

def isValidJmpAdress(adress: str) -> bool:
    return (isValidNumber(adress) and 0 <= int(adress) < PM_SIZE) 


def is_undefined(arg: str) -> bool:
    return not (is_preprocess_ins(arg) or isInstruction(arg) or isValidRegister(arg) or isIoRegister(arg) or isValidNumber(arg) or isValidMemoryAdress(arg) or isValidJmpAdress(arg))


def check_args_jmp(adress: List[str]) -> None:
    adress = adress[0]
    assert isValidJmpAdress(adress), str(adress) + " Is not a viable jump-adress"

def check_args_inc(reg: List[str]) -> None:
    assert isValidRegister(reg[0]), str(reg) + " Is not a viable register to increment" 

def check_args_add(args: List[str]) -> None:
    #First args is always a register
    assert isValidRegister(args[0]), str(args[0]) + " can't be used as a register"
    assert isValidRegister(args[1]) or isValidMemoryAdress(args[1]), args[1] + " is either an incorrect register or an incorrect memory adress used foradd"

def check_args_define(args: List[str]) -> None:
    #args[1] is always the number
    assert isValidNumber(args[1]), str(args[1]) + " is not a viable integer to be used for redefines. Only redefines to integers are implemented"

def check_args_label(args: List[str]) -> None:
    assert (not args), "Label have the following arguments: " + str(args)

def check_args_mov(args: str) -> None:
    pass

def check_args_ldi(args: str) -> None:
    assert isValidRegister(args[0]) and isValidNumber(args[1]), "Ldi has the following arguments: " + str(args)

def check_args_load(args: str) -> None:
    assert (isValidRegister(args[0]) and isValidMemoryAdress(args[1]) or
            isValidRegister(args[0]) and isValidRegister(args[1])), "Load has the following arguments: " + str(args)

def check_args_store(args: str) -> None:
    assert  (isValidMemoryAdress(args[0]) and isValidRegister(args[1]) or 
            (isValidRegister(args[0]) and isValidRegister(args[1]) )), "Store have invalid arguments: " + str(args)

def check_args_out(args: str) -> None:
    assert isIoRegister(args[0]) and isValidRegister(args[1]), "Outs args are invalid: " + str(args)

def check_args_sub(args: str) -> None:
    assert isValidRegister(args[0]) and isValidMemoryAdress(args[1]), "sub args are invalid: " + str(args)

def check_args_and(args: str) -> None:
    assert isValidRegister(args[0]) and isValidMemoryAdress(args[1]), "and args are invalid: " + str(args)

def check_args_cmp(args: str) -> None:
    alt_1 = isValidRegister(args[0]) or isValidNumber(args[1])
    alt_2 = isValidRegister(args[0]) or isValidRegister(args[1]) 
    assert alt_1 or alt_2, f"Invalid arguments for cmp: {str(args)}"
    if isValidNumber(args[0]):
        assert int(args[0]) <= max_constant, f"CMP can only use 13 bits as constant: {str(args)}"

def check_args_breq(args: str) -> None:
    assert isValidJmpAdress(args[0]), "Invalid jump adress for breq: " + str(args)

def check_args_bne(args: str) -> None:
    assert isValidJmpAdress(args[0]), "Invalid jump adress for bne: " + str(args)

def check_args_bra(args: str) -> None:
    assert isValidJmpAdress(args[0]), "Invalid jump adress for bra: " + str(args)

def check_args_beq(args: str) -> None:
    assert isValidJmpAdress(args[0]), "Invalid jump adress for beq: " + str(args)

def check_args_mul(args: str) -> None:
    assert (isValidRegister(args[0]) and (isValidRegister(args[1]))) or (isValidRegister(args[0]) and isValidMemoryAdress(args[1])), "Invalid arguments for mul" + str(args)

def check_args_halt(args: str) -> None:
    assert (not args), "Halt have the following arguments: " + str(args)

def check_args_draw(args: str) -> None:
    assert (not args), "Draw have the following arguments: " + str(args)

def check_args_drawCursor(args: str) -> None:
    assert (not args), "DrawCursor have the following arguments: " + str(args)

def check_args_in(args: str) -> None:
    assert isValidRegister(args[0]) and isIoRegister(args[1])  

def checkValidArgs(instr: str, args: List[str]):
    if instr == "jmp":
        check_args_jmp(args)
    elif instr == "inc":        
        check_args_inc(args)
    elif instr == "add":
        check_args_add(args)
    elif instr == "mov":
        check_args_mov(args)
    elif instr == "#define":
        check_args_define(args)
    elif instr == "ldi":
        check_args_ldi(args)
    elif instr == "load":
        check_args_load(args)
    elif instr == "store":
        check_args_store(args)
    elif instr == "out":
        check_args_out(args)
    elif instr == "sub":
        check_args_sub(args)
    elif instr == "and":
        check_args_and(args)
    elif instr == "cmp":
        check_args_cmp(args)
    elif instr == "breq":
        check_args_breq(args)
    elif instr == "bne":
        check_args_bne(args)
    elif instr == "bra":
        check_args_bra(args)
    elif instr == "beq":
        check_args_beq(args)
    elif instr == "mul":
        check_args_mul(args)
    elif instr == "halt":
        check_args_halt(args)
    elif instr == "draw":
        check_args_draw(args)
    elif instr == "drawcursor":
        check_args_drawCursor(args)
    elif instr == "in":
        check_args_in(args)
    elif is_label(instr):
        check_args_label(args)
    
    else:
        assert False, str(instr) + " Undefined instruction!!!!!!! (check valid args)"
    return


def checkInput(instr: str, args: List[str], lineCount: int):
    try:
        assert (isInstruction(instr)), "'" + instr + "'" + " isn't a defined instruction "
        assert (correct_argc(instr, args)), "Too many arguments! \n'" + instr + "' have " + str(ins_args.get(instr)) + " argument/s, not '" + str(len(args)) +"'"
        #Will throw AssertionError (Proper custom made raises to be implemented in the future)
        checkValidArgs(instr, args)

    except AssertionError as msg:
        print("Error, The following line failed") 
        print("LINE = " + str(lineCount) + ": ", end="")
        print(instr+" ", end="")
        for arg in args:
            print(arg+" ", end="")
            pass
        print("", end ="")
        print("\nREASON: ", end="")
        print(msg)
        print("")
        exit()
    
