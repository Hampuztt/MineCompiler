
  
  

# Defined instructions:


```text

Constants will be represented by the letter 'c'.
Registers will be identified as Grx, where 'x' is the register number.
Memory addresses will be referred to as 'mem'. (For now only constants can be used to my knowledge)
Input/Output is referred to as IOx

ldi Grx c 			--Load Grx with c
add Grx mem 		--Add Grx with value in mem
add Grx, Gry 		--Add Grx with Gry
sub Grx, mem 		--Sub Grx with value in mem
and Grx, mem      	--And Operation store result in Grx
cmp Grx c, 	   		-- if equal, set Z = 1, else 0 (MAX 13 bits on c)
cmp Grx Gry      	-- if equal, set Z = 1, else 0

load Grx, mem 		--Load Grx with value in mem
load Grx, Gry		--Load memory in Grx with value in Gry
store mem, Grx    	--Store value in Grx to Mem
store Grx, Gry		--Store value in Gry into mem in Grx
out IOx, Grx 		--Load the IOx with the value in Grx

bra mem				--Jmp to mem
bne mem				--Jmp to mem if Z = 0
beq mem				--Jmp to mem if Z = 1
```

# Compiler syntax

* The compiler is case-insensitive and can process multiple spaces between arguments.
* To include comments, use ';'. 			
* To include labels, use 'label:'.
* To assign names to constants, utilize the #define directive with the format 'name' 'value'.
* It is crucial to avoid using the same name for a label and a constant, as it will result in overwriting.

# Naming convention

* Constants should have UPPER_CASE
* Defined memoryadresses m_name
  

# To be implemented once microcode is tested

* `"in Grx, IO": ?` r
	* in random Grx 	   -- Get random value and store it in Grx


* `"brareg": ` 
	* bra Grx 		  --Branch to memory in register

* `"mulmem": ` 
	* mul grx PM(m) 		  --Multiply with value in memory

* `"bge": 00111` 
	* bge mem 		  --Branch if greater or equal
  
# Guide to add instructions to the compiler:

1. Open the "input_check.py" file located in the "validation" folder.

2. Add the name of your new instruction and the number of arguments it requires to the "ins_args" section.
*For example: `"MY_INSTRUCTION": 3`*

3. Create a new function called "check_args_MY_INSTRUCTION(args)" to validate the arguments for your new instruction.

4. Use the "assert" statement to check that the arguments are valid.

5. In the "check_valid_args" function, add an "elif" statement to the instruction is "MY_INSTRUCTION," and call the "check_args_MY_INSTRUCTION()" function.

  

6. Now all input validation is finshed, open the "compiler.py" file located in the "compiling" folder.

7. Add "MY_INSTRUCTION" to operations with it corrosponding operation code

8. Create a new function called "compile_MY_INSTRUCTION()" and define how it should be compiled.

9. In the "compile_line" function, add an "elsif" statement to "MY_INSTRUCTION," and call the "compile_MY_INSTRUCTION()" function.

10. **Important!** Make a unittest in tester.py



# Instructions for Usage

If you wish to retain your current pMem in the sweeper_CPU directory, follow these steps:
Run the main.py file located in the MineCompiler directory.
Find the resulting file under the code_files directory named pMem.vhd.

# Windows Script
To compile and replace the pMem.vhd file directly in the sweeper_CPU directory, perform the following steps:

# 1 Run the compile_windows file.

# Linux Script
To create the necessary file for compilation in Linux, execute the command 'chmod +x compile_linux.sh' once. Afterward, you can simply run './compile_linux.sh' to compile and replace the pMem in the sweeper_CPU directory with the resulting file.
