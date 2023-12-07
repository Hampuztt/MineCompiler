; Fully working minesweeper 
;Joystick constants
#define null 0
#define LEFT 1
#define RIGHT 2
#define UP 3
#define DOWN 4
#define BTN1 5
#define BTN2 6
#define BTN3 7


; Constants
#define vga_bomb 3
#define vga_flag 2
#define vga_dirt 1
#define vga_hidden 0

#define REMOVE_FLAG 32767   ;1110111111111111
#define FLAG_BIT 4096    ;0001000000000000
#define MAXONES 65535    ; -1 

; Arrays 
#define board_x_size 20
#define board_y_size 15
#define BOARD_START 724  ; Start of game board tiles memory range
#define BOARD_END   1024  ; size = 300

; 1031-1040 temp stores
#define m_numLoops 723
#define m_TEMP2 722
#define m_TEMP3 721
#define m_TEMP4 720
#define m_TEMP5 719
#define m_TEMP6 718
#define m_TEMP7 717
#define m_stack1 716
#define m_stack2 715
#define m_stack3 714

;Player constants


;Initialize memory constants
ldi R1 BOARD_START
store BOARD_START r1
ldi R1 FLAG_BIT 
store m_flagBit R1; 0001000000000000 used to mask in flag
ldi R1 REMOVE_FLAG
store m_remFlag R1; 1110111111111111
ldi R1 1
store m_increment r1
ldi R1 board_y_size
store m_Ymultiplier R1
ldi R1 vga_bomb
store m_Bomb r1


reset_game:
    ldi R1 0
    ldi R2 0
    ldi R3 0
    ldi R4 0
    ldi R5 0
    ldi R6 0
    ldi R7 0
    reset_loop:
        ldi R0 BOARD_START
        store R0 R1
        add R0 m_increment
        cmp R0 BOARD_END
        bne reset_loop
reset_done:


#define NUM_BOMBS 15
bombs_init:
    ldi R1, BOARD_START    ; Initialize game board pointer
    ldi R2,  0             ; Bombs planted
    ldi R3, vga_bomb       ; Store bomb value in R3
    ;Store players absolute position in R5
    load R4 m_playerY
    mul R4 m_Ymultiplier
    add R4 m_playerX
    add R4 BOARD_START        ;Set to absolute value

bomb_loop:
    cmp R2, NUM_BOMBS          ; If the desired number of bombs has been placed, exit
    breq bomb_exit
    in R5 random        ;Get random value in R5
    ldi R1, BOARD_START ;Reach start of array
    add R1, R5          ;Get the absolute index of tile we are looking at
    cmp R1, R4          ;Compare player_pos and current_pos
    beq bomb_loop       ; If on player_tile, skip to next iteration
    load R3, R1         ; Load the value in memory R1 contains to R3
    cmp R3, vga_hidden  ; Check if the tile is hidden
    bne bomb_loop       ; If not hidden, skip to next iteration
    store R1, R3        ; If the tile is hidden, plant the bomb
    add R2, m_increment   ; Increment the bomb counter
    bra bomb_loop       ; Go back to the start of the loop
bomb_exit:

;R1 = y, R2 = x, R3 = current_tile, R4 = current_tile_val, m_TEMP9 = return adress
draw_board:     ;Nested loop to draw the entire board
    ldi R1, board_y_start ; R1 = y 
reset_x:
    ldi R2, board_x_start ; R2 = x

draw_loop:
    ldi r3 0
    add R3, R1         ;Get row number
    mul R3, m_Ymultiplier   ;Multiply with col_size to get absolute value 
    add R3, R2         ;Add X to the value
    add R3, BOARD_START ;Get the absolute index
    load R4 R3         ;Get tile value
    out vga_y R2       ;set vga positions
    out vga_x R1
draw_tile:
    store m_TEMP1 R4
    and R4 m_flagBit
    cmp R4 FLAG_BIT ;Have flag?
    bne not_flag    ;branch if less / if no flag
    is_flag:
        ldi R4 vga_flag
        out vga_tile R4 ;Draw flag
        bra tile_drawn
    not_flag:
        load R4 m_TEMP1
        out vga_tile R4 ;Draw the non flag tile
tile_drawn: ;Increment LC
    draw
    add R2 m_increment      
    cmp r2, board_x_size
    bne draw_loop
    add R1 m_increment
    cmp R1 board_y_size
    bne reset_x
draw_loop_end:
    load R1, m_TEMP9 ;TEMP_9 should always contain the return adress
    bra game_over
init_done:

game_loop:
    bra game_loop    

  ; read player input ...
  ; update game board ...


;--------------------------------------------------
;Logic for placing flag
;the 12'th bit decides if a flag is planted or not

place_flag:
    load R1, m_PlayerPos ;Get what tile is on the memory 
    and R1, m_flagBit    ;Mask in flag
    cmp R1, FLAG_BIT     ;Is flag? 
    ;Load value of player_tile into R1
    load R2, m_PlayerPos ;Get player position in memory
    load R1 R2           ;Get value that player is standing on to R2
    beq throw_flag         
    set_flag:
        add R1  m_flagBit    ;Add flagBit to player_tile
        bra flag_exit
    throw_flag:
        sub  R1, m_flagBit  ;remove flagBit to player_tile
flag_exit:
    load R2 m_PlayerPos ;Get where in array player is 
    store R2, R1        ;Update value to the game
    bra draw_board
    
;-----------------------------------------------------------------

;-----------------------------------------------------------------
;Logic for pressing revealing tile
reveal_tile:
    load R2 m_PlayerPos
    load R1 R2 ;Value of tile player pressed
    cmp R1, vga_bomb
    beq game_over  ;If on a bomb, player lost
    cmp  R1 vga_hidden ;Is hidden?
    bne reveal_exit    ;If not hidden, do nothing
;Now we know we pressed on a hidden tile

reveal_loop_init:
    load R1, m_playerX  ;R1 = X
    add R1, m_increment ;R1 = x + 1
    add R1, m_increment ;R1 = x + 2 (max val for cmp)

    store m_TEMP1, R1   ;STORE r1 max val
    load R1, m_playerX
    sub r1, m_increment ; R1 = x - 1 (min val)

    load R2, m_playerY   ;R2 = Y
    add R2, m_increment ;R2 = y + 1 
    add R2, m_increment ;R2 = y + 2 (max val for cmp)

    store m_TEMP2, R2   ;Store Ymax 
    load R2, m_playerY
    sub R2, m_increment ;R2 = y - 1 (min val)

    ldi R6, 0           ; R6 = NUM OF BOMBS AROUND
    ldi R7 BOARD_START; Used to store start of array

    ldi r0 0
    add r0 R1
reveal_reset_x:
    ldi R1 0
    add R1 R0


reveal_inbounds:
    ;Check if in bounds
    cmp R1 MAXONES ;minus 1
    beq reveal_increment
    cmp R1 board_x_size
    beq reveal_increment
    cmp R2 MAXONES
    beq reveal_increment
    cmp R2 board_y_size
    beq reveal_increment
reveal_loop:
;Will only enter if we are inbounds of the array
;R0 = m_playerX - 1, R1 = x, R2 = y, R3 = current_tile, R4 = value in current_tile, 
;R5 = used for compares, R6 = bomb_counter, R7=BOARD_START
    ldi R3 0
    add R3 R2   ;R3 = R2
    mul R3 m_Ymultiplier
    add R3 R1               ;R3 += X to become absolute index of array
    add R3 R7               ;R3 += BOARD_START to become absolute index in memory
    load R4, R3
    cmp R4, vga_bomb
    bne reveal_increment    ;If not bomb, go to next iteration. If bomb, increase count
    add R6, m_increment   
reveal_increment:
    load R5, m_TEMP1 ;Get R1 max val 
    add R1 m_increment
    cmp R1 R5 ; Are we at max val? 
    bne reveal_inbounds ;If not go to next iteration
    load R5, m_TEMP2
    add r2 m_increment ;Increase Y_val
    cmp R2, R5  ;max y_val?
    bne reveal_reset_x
; Finished with loop
reveal_exit:
    ;Jump somewhere
;-----------------------------------------------------------------


game_over:
    load R1 m_playerX
    out vga_x R1
    load R1 m_playerY
    out vga_y R1
    ldi R1 vga_bomb
    out vga_tile R1
    draw
halt    