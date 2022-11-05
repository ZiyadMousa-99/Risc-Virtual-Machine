
import sys
import CPU
import Memory
def main():


    cpu=CPU.CPU()
    memory=Memory.Memory()
    memory.loadFile("code-binary.bin","data-binary.bin")
    cpu.memory=memory
    cpu.loop()



if __name__ == "__main__":
    main()


def startVM(Cpu):
    Cpu.main()


