; Constants
#define HIDDEN 1
#define BOMB 2
#define REM_FLAG 32767   ;0111111111111111
#define FLAG_BIT 32768   ;1000000000000000
#define VGA_FLAG 10      ; ? needs to be defined
#define player_cursor_offset 16


; Memory defines (should be lower_case)
#define TEMP_1 1897
#define TEMP_2 1898
#define TEMP_3 1899
#define flag_bit_mem 1200 ; AND to mask in flag
#define rem_flag_mem 1199 ; AND to remove flag
#define increment 1198    ;used for easy add



#define PLAYER_MEM 1002 ;Position in memory
#define PLAYER_Y 1001
#define PLAYER_X 1000
#define GAME_OVER 1902
#define TILE_START 1903  ; Start of game board tiles memory range
#define TILE_END   2048
#define BOARD_SIZE 144   ; Number of game board tiles
#define NUM_BOMBS 12
start: 
;Initialize memory constants
ldi R1 1
store increment r1

#define board_y_start 0
#define board_x_start 0
#define max_x 20
#define max_y 15
draw_board:     ;Nested loop to draw the entire board
    ldi R1, board_y_start ; R1 = y 
    ldi R2, board_x_start ; R2 = x
    ldi R7, 14
    ldi r6 0
reset_x:
    ldi R2 0

draw_loop:
    ldi r3 0
    add R3, R1         ;Get row number
    mul R3, R7         ;Multiply with 14 to get absolute value 
    add R3, R2         ;Add X to the value
    out vga_y R1       ;set vga positions
    out vga_x R2
    add r6 increment
    cmp r6 4
    bne skip_1
    ldi r6, 0    
skip_1:
    out vga_tile r6
    draw

tile_drawn: ;Increment LC
    add R2 increment      
    cmp r2, max_x
    bne draw_loop
    add R1 increment
    cmp R1 max_y
    bne reset_x
halt    

  ; read player input ...
  ; update game board ...


