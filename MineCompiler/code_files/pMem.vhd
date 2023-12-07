library IEEE;
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


--Following redefines exists: 
--	null = 0
--	left = 1
--	right = 2
--	up = 3
--	down = 4
--	btn1 = 5
--	btn2 = 6
--	btn3 = 7
--	vga_bomb = 3
--	vga_flag = 2
--	vga_dirt = 1
--	vga_hidden = 0
--	remove_flag = 32767
--	flag_bit = 4096
--	maxones = 65535
--	board_x_size_plus_one = 20
--	board_y_size_plus_one = 15
--	board_x_size = 19
--	board_y_size = 14
--	board_start = 0
--	board_end = 0
--	m_numloops = 255
--	m_temp2 = 254
--	m_temp3 = 253
--	m_temp4 = 252
--	m_temp5 = 251
--	m_temp6 = 250
--	m_temp7 = 249
--	m_stack1 = 248
--	m_stack2 = 247
--	m_stack3 = 246
--	m_flagbit = 245
--	m_remflag = 244
--	m_increment = 243
--	m_boardheight = 242
--	m_boardwidth = 241
--	m_vga_bomb = 240
--	m_boardstart = 239
--	player_x_start = 8
--	player_y_start = 8
--	m_playerx = 200
--	m_playery = 201
--	m_playerpos = 202
--	game_loop = 42
--	update_tile = 54
--	move_player = 65
--	move_left = 77
--	normal_left = 81
--	move_right = 83
--	normal_right = 87
--	move_up = 89
--	normal_up = 93
--	move_down = 95
--	normal_down = 99
--	move_player_exit = 101
--	dont_move = 114
--	wait_loop = 118
--	loop = 126
--	wait_exit = 134

type p_mem_t is array (0 to 255) of unsigned(23 downto 0); 
constant p_mem_c : p_mem_t := 
 	 ( 
	 x"a80018",	 --in r0 random
	 x"aa0018",	 --in r2 random
	 x"002000",	 --ldi r0 4096
	 x"001000",
	 x"0800f5",	 --store 245 r0
	 x"002000",	 --ldi r0 32767
	 x"007fff",
	 x"0800f4",	 --store 244 r0
	 x"002000",	 --ldi r0 1
	 x"000001",
	 x"0800f3",	 --store 243 r0
	 x"002000",	 --ldi r0 14
	 x"00000e",
	 x"0800f2",	 --store 242 r0
	 x"002000",	 --ldi r0 19
	 x"000013",
	 x"0800f1",	 --store 241 r0
	 x"002000",	 --ldi r0 3
	 x"000003",
	 x"0800f0",	 --store 240 r0
	 x"002000",	 --ldi r0 0
	 x"000000",
	 x"0800ef",	 --store 239 r0
	 x"002000",	 --ldi r0 8
	 x"000008",
	 x"0800c8",	 --store 200 r0
	 x"002000",	 --ldi r0 8
	 x"000008",
	 x"0800c9",	 --store 201 r0
	 x"002000",	 --ldi r0 8
	 x"000008",
	 x"012000",	 --ldi r1 14
	 x"00000e",
	 x"702000",	 --mul r0 r1
	 x"1000f1",	 --add r0 241
	 x"1000ef",	 --add r0 239
	 x"0800ca",	 --store 202 r0
	 x"072000",	 --ldi r7 0
	 x"000000",
	 x"012000",	 --ldi r1 3
	 x"000003",
	 x"410002",	 --out vga_tile r1
	 x"980008",	 --in r0 joystick
	 x"900001",	 --cmp r0 1
	 x"580041",	 --beq 65
	 x"900002",	 --cmp r0 2
	 x"580041",	 --beq 65
	 x"900003",	 --cmp r0 3
	 x"580041",	 --beq 65
	 x"900004",	 --cmp r0 4
	 x"580041",	 --beq 65
	 x"900005",	 --cmp r0 5
	 x"580036",	 --beq 54
	 x"300072",	 --bra 114
	 x"1700f3",	 --add r7 243
	 x"470002",	 --out vga_tile r7
	 x"0000c8",	 --load r0 200
	 x"400000",	 --out vga_x r0
	 x"0000c9",	 --load r0 201
	 x"400001",	 --out vga_y r0
	 x"500000",	 --draw
	 x"002000",	 --ldi r0 75
	 x"00004b",
	 x"0800ff",	 --store 255 r0
	 x"300072",	 --bra 114
	 x"0900f8",	 --store 248 r1
	 x"0a00f7",	 --store 247 r2
	 x"0100c8",	 --load r1 200
	 x"0200c9",	 --load r2 201
	 x"900001",	 --cmp r0 1
	 x"58004d",	 --beq 77
	 x"900002",	 --cmp r0 2
	 x"580053",	 --beq 83
	 x"900003",	 --cmp r0 3
	 x"580059",	 --beq 89
	 x"900004",	 --cmp r0 4
	 x"58005f",	 --beq 95
	 x"910000",	 --cmp r1 0
	 x"380051",	 --bne 81
	 x"012000",	 --ldi r1 20
	 x"000014",
	 x"2100f3",	 --sub r1 243
	 x"300065",	 --bra 101
	 x"910013",	 --cmp r1 19
	 x"380057",	 --bne 87
	 x"012000",	 --ldi r1 65535
	 x"00ffff",
	 x"1100f3",	 --add r1 243
	 x"300065",	 --bra 101
	 x"920000",	 --cmp r2 0
	 x"38005d",	 --bne 93
	 x"022000",	 --ldi r2 15
	 x"00000f",
	 x"2200f3",	 --sub r2 243
	 x"300065",	 --bra 101
	 x"92000e",	 --cmp r2 14
	 x"380063",	 --bne 99
	 x"022000",	 --ldi r2 65535
	 x"00ffff",
	 x"1200f3",	 --add r2 243
	 x"300065",	 --bra 101
	 x"410000",	 --out vga_x r1
	 x"420001",	 --out vga_y r2
	 x"a80018",	 --in r0 random
	 x"400002",	 --out vga_tile r0
	 x"b80000",	 --drawcursor
	 x"0900c8",	 --store 200 r1
	 x"0a00c9",	 --store 201 r2
	 x"0200f7",	 --load r2 247
	 x"0100f8",	 --load r1 248
	 x"002000",	 --ldi r0 1000
	 x"0003e8",
	 x"0800ff",	 --store 255 r0
	 x"300076",	 --bra 118
	 x"002000",	 --ldi r0 15
	 x"00000f",
	 x"0800ff",	 --store 255 r0
	 x"300076",	 --bra 118
	 x"0800f8",	 --store 248 r0
	 x"0900f7",	 --store 247 r1
	 x"0a00f6",	 --store 246 r2
	 x"0000ff",	 --load r0 255
	 x"022000",	 --ldi r2 0
	 x"000000",
	 x"012000",	 --ldi r1 0
	 x"000000",
	 x"1100f3",	 --add r1 243
	 x"690000",	 --cmp r1 r0
	 x"38007e",	 --bne 126
	 x"012000",	 --ldi r1 0
	 x"000000",
	 x"1200f3",	 --add r2 243
	 x"6a0000",	 --cmp r2 r0
	 x"38007e",	 --bne 126
	 x"0200f6",	 --load r2 246
	 x"0100f7",	 --load r1 247
	 x"0000f8",	 --load r0 248
	 x"30002a",	 --bra 42

   others => (others=> '0'));
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

    