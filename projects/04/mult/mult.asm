// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.

	@R1
	D=M
	@i
	M=D

	D=0
(START)
	@SUM
	M=D

	@i
	D=M
	@END
	D;JLE

	@SUM
	D=M
	@R0
	D=D+M

	@i
	M=M-1

	@START
	0;JMP

(END)
	@SUM
	D=M
	@R2
	M=D

	@END
	0;JMP
