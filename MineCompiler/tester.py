import unittest
from typing import *
import compiling.compiler as compiler
import validation.input_check as validate


class testInput(unittest.TestCase):

    #Test compiler
    def test_ldi(self):
        self.assertTrue(compiler.compiled_line("ldi gr2 2") == "000000100010000000000000\n000000000000000000000010")
        self.assertTrue(compiler.compiled_line("ldi gr2 9") == "000000100010000000000000\n000000000000000000001001")
        self.assertTrue(compiler.compiled_line("ldi gr2 7") == "000000100010000000000000\n000000000000000000000111")

    def test_load(self):
        self.assertTrue(compiler.compiled_line("load gr2 2") == "000000100000000000000010")
        self.assertTrue(compiler.compiled_line("load gr1 gr0") == "100000010000000000000000")
        self.assertFalse(compiler.compiled_line("load gr2 2") == "000000100010000000000000\n000000000000000000000010")


    def test_store(self):
        self.assertTrue(compiler.compiled_line("store 255 gr4") == "000011000000000011111111")
        self.assertTrue(compiler.compiled_line("store gr0 gr7") == "100010001110000000000000")

    def test_add(self):
        self.assertTrue(compiler.compiled_line("add gr5 gr3") == "010011010110000000000000")
        self.assertTrue(compiler.compiled_line("add gr5 gr4") == "010011011000000000000000")
        self.assertTrue(compiler.compiled_line("add gr4 255") == "000101000000000011111111")

    def test_out(self):
        self.assertTrue(compiler.compiled_line("out vga_x gr7") == "010001110000000000000000")
        self.assertTrue(compiler.compiled_line("out vga_y gr7") == "010001110000000000000001")
        self.assertTrue(compiler.compiled_line("out vga_tile gr7") == "010001110000000000000010")

    def test_sub(self):
        self.assertTrue(compiler.compiled_line("sub gr5 255") == "001001010000000011111111")
    def test_and(self):
        self.assertTrue(compiler.compiled_line("and gr5 255") == "000111010000000011111111")
    def test_halt(self):
        self.assertTrue(compiler.compiled_line("halt") == "011110000000000000000000")
    def test_bra(self):
        self.assertTrue(compiler.compiled_line("bra 33") == "001100000000000000100001")

    def test_cmp(self):
        self.assertTrue(compiler.compiled_line("cmp gr1 gr2") == "011010010100000000000000")
        self.assertTrue(compiler.compiled_line("cmp gr1 1") == "100100010000000000000001")

    def test_bne(self):
        self.assertTrue(compiler.compiled_line("bne 28") == "001110000000000000011100")
    
    def test_draw(self):
        self.assertTrue(compiler.compiled_line("draw") == "010100000000000000000000")

    def test_drawCursor(self):
        self.assertTrue(compiler.compiled_line("drawCursor") == "101110000000000000000000")

    def test_bra(self):
        self.assertTrue(compiler.compiled_line("bra 33") == "001100000000000000100001")
    def test_in(self):
        self.assertTrue(compiler.compiled_line("in r1 joystick") == "100110010000000000001000")




    #Test input checker
    def test_correct_argc(self):
        self.assertTrue(validate.correct_argc("hejsan:", []))
        self.assertFalse(validate.correct_argc("hejsan:", ["2"]))
        self.assertFalse(validate.correct_argc("hejsan:", ["blabla ", "hej"]))
        self.assertTrue(validate.correct_argc("bra", ["non_digit _adress"]))
        self.assertTrue(validate.correct_argc("bra", ["59"]))
        self.assertFalse(validate.correct_argc("bra", []))
        self.assertFalse(validate.correct_argc("bra", [2, 5]))
        self.assertFalse(validate.correct_argc("inc", [5, 1 ,3]))
        self.assertFalse(validate.correct_argc("inc", []))
        self.assertTrue(validate.correct_argc("inc", ["r1"]))
        self.assertTrue(validate.correct_argc("add", ["ett", "två"]))
        self.assertFalse(validate.correct_argc("add", []))
        self.assertFalse(validate.correct_argc("add", ["test"]))
        self.assertFalse(validate.correct_argc("add", ["test", "hej", "då"]))

if __name__ == '__main__':
    unittest.main()