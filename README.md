# NES_Emulator

This is a **very** experimental attempt at building an emulator capable of running NES ROMs.
While I've found a handful of different emulators that much more experienced developers have
made in the past, it seems most of them are either not entirely complete/functional or they 
are only partially written using Python. 

This project is purely for fun, and its completion may be dependent on whether it remains fun.
So far, learning about the architecture of the 6502 microprocessor and familiarizing myself
with the instruction set has been enjoyable, so I hope that continues to be the case and I end
up with a somewhat usable finished product.

While I do welcome collaboration from anyone interested, this project is meant to be educational.
If you see anything that's terribly wrong with the design or implementation, feel free to submit
a pull request, preferably with a detailed explanation of why it should be done differently.

I've done a few (very simple) projects with IA-32 assembly and have studied x86 architecture at a
high level, so the basic concepts are not completely foreign to me. However, this is definitely
beyond my level of expertise, but hopefully with some humility and patience, I'll develop some
new skills and learn a few things.

## Update #1

After a bit of experimenting with potential designs and a bit more research, it has become clear
that the short-term scope of the project must change a bit. Before being able to dive head-first 
into building a NES Emulator, I'll need to make a somewhat-functional 6502 assembler. This may have
been obvious to some, but I guess I assumed that, since any ROMs are going to be already-written
and fully-tested pieces of software, I would only need to be able to run nice, neat code. Of course,
it isn't that simple. In order to test and ensure that everything works as intended, I'll have to be
able to run much smaller pieces of software designed to test the emulated hardware for bugs. I think
I should be able to start pretty simply and only implement a handful of instructions to test the
basic design of the emulated machine. Hopefully, any major flaws will become evident quickly...

## Update #2

I've decided to make a design change for the time being. To keep from having to refactor and redesign
as many components of the NES as I get the CPU and instruction set working, I'm going to make a single
file that contains the emulated CPU and the necessary functions to carry out all the instructions. The
end result of this step should **hopefully** be what is essentially a 6502 emulator/assembler. Once 
that is working as intended, I may break that file into sensible components to use where necessary in
the larger program. Still learning a lot about this neat microprocessor, and now I'm learning some more
about the software development process as well.