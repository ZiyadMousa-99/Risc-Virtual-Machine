import Memory
import Inst
from myhdl import intbv



class CPU:
    def __init__(self):
        self.registers = [intbv(0)[32:]]*32
        self.memory = Memory.Memory()
        self.pc = 0x400000

    # ===================================================[MAIN LOOP]=========================================================
    """
    In this section, the implementation of the main loop where the five stages of a CPU are illustrated, the five stages
    are as follows:
    1) Instruction Fetch Stage (IF Stage)
    2) Instruction Decode Stage (ID Stage)
    3) Execution Stage (EX Stage)
    4) Memory Access Stage (MEM Stage)
    5) Write-Back Stage (WB Stage)

    Although in the following, it shows a main loop with only the first three stages, it should be clear that the other 
    two stages were embedded with-in the execution stage.

    The loop will keep running, until the breaking condition is met, here in this implementation it is assumed to have 
    a breaking condition of all ones, indicating the end of the program.

    """

    # -----------------------------------------------------------------------------------------------------------------------
    def loop(self):
        self.isRunning = True

        file=open("regsiter_history.txt", "w")
        while self.isRunning:

            self.printRegisters(file)
            # 1) Instruction Fetch Stage (IF Stage)
            read_inst = self.fetch_inst()

            if read_inst == "0"*32: # finally output the content of the memory to a file
                self.memory.printData()
                break

            # 2) Instruction Decode Stage (ID Stage)
            decoded_inst = self.decode_inst(read_inst)

            # 3) Execution Stage (EX Stage)
            self.execute_inst(decoded_inst)

            # 4) Memory Access Stage (MEM Stage) - embedded with-in execution stage
            # 5) Write-Back Stage (WB Stage) - embedded with-in execution stage


        file.close()
    # ---------------------------------------------------[IF-Stage]---------------------------------------------------------
    """
    In this stage, the CPU reads instructions from the address in the memory whose value is present in the program 
    counter (PC).
    """

    # -----------------------------------------------------------------------------------------------------------------------
    def fetch_inst(self):
        return self.memory.read_inst(self.pc)

        # ---------------------------------------------------[ID-Stage]---------------------------------------------------------
        """
        In this stage, instruction is decoded and the register file is accessed to get the values from the registers
         used in the instruction, the decoded instruction is passed then to the next stage.
        """

    # -----------------------------------------------------------------------------------------------------------------------
    def decode_inst(self, inst):
        # R-type
        if inst[25:] == "0110011":
            opcode = inst[25:]
            rd = inst[20:25]
            rs1 = inst[12:17]
            rs2 = inst[7:12]
            funct3 = inst[17:20]
            funct7 = inst[0:7]
            return Inst.Inst("R", opcode=opcode, rs1=rs1, rs2=rs2, funct3=funct3, funct7=funct7, rd=rd)


        # I-type
        elif inst[25:] == "0010011" or inst[25:] == "0000011" or inst[25:] == "1100111" or inst[25:] == "1110011":
            opcode = inst[25:]
            rd = inst[20:25]
            rs1 = inst[12:17]
            funct3 = inst[17:20]
            imm = inst[0:12]
            return Inst.Inst("I", opcode=opcode, rs1=rs1, funct3=funct3, rd=rd, imm=imm)
        # S-type
        elif inst[25:] == "0100011":
            opcode = inst[25:]
            rs1 = inst[12:17]
            rs2 = inst[7:12]
            funct3 = inst[17:20]
            imm = inst[0:7] + inst[20:25]
            return Inst.Inst("S", opcode=opcode, rs1=rs1, rs2=rs2, funct3=funct3, imm=imm)
        # B-type
        elif inst[25:] == "1100011":
            opcode = inst[25:]
            rs1 = inst[12:17]
            rs2 = inst[7:12]
            funct3 = inst[17:20]
            imm = inst[0] + inst[24] + inst[1:7] + inst[20:24]
            return Inst.Inst("B", opcode=opcode, rs1=rs1, rs2=rs2, funct3=funct3, imm=imm)
        # U-type
        elif inst[25:] == "0110111" or inst[25:] == "0010111":
            opcode = inst[25:]
            rd = inst[20:25]
            imm = inst[0:20]
            return Inst.Inst("U", opcode=opcode, rd=rd, imm=imm)



        # J-type
        elif inst[25:] == "1101111":
            opcode = inst[25:]
            rd = inst[20:25]
            imm = inst[0] + inst[12:20] + inst[11] + inst[1:11]
            return Inst.Inst("J", opcode=opcode, rd=rd, imm=imm)

        # ---------------------------------------------------[EX-Stage]---------------------------------------------------------
        """
        In this stage, ALU operations are performed, here it includes the next two stages Memory Access Stage and the 
        Write-Back Stage depending on the decoded instruction received from previous stage 
        """

    # ----------------------------------------------------------------------------------------------------------------------

    def execute_inst(self, decoded_inst):
        self.registers[0]=intbv(0)[32:]


        # -----------------------------------------------[R-Type]---------------------------------------------------------------
        if decoded_inst.type == "R":

            rd = int(decoded_inst.rd, 2)
            rs1 = int(decoded_inst.rs1, 2)
            rs2 = int(decoded_inst.rs2, 2)

            if decoded_inst.funct3 == "000":
                if decoded_inst.funct7 == "0000000":  # ADD
                    self.registers[rd] = intbv(self.registers[rs1]).signed() + intbv(self.registers[rs2]).signed()
                    self.pc += 4
                elif decoded_inst.funct7 == "0100000":  # SUB
                    self.registers[rd] = intbv(self.registers[rs1]).signed() - intbv(self.registers[rs2]).signed()
                    self.pc += 4


            elif decoded_inst.funct3 == "100":  # XOR
                self.registers[rd] = intbv(self.registers[rs1]).signed() ^ intbv(self.registers[rs2]).signed()
                self.pc += 4

            elif decoded_inst.funct3 == "110":  # OR
                self.registers[rd] = intbv(self.registers[rs1]).signed() | intbv(self.registers[rs2]).signed()
                self.pc += 4

            elif decoded_inst.funct3 == "111":  # AND
                self.registers[rd] = intbv(self.registers[rs1]).signed() & intbv(self.registers[rs2]).signed()
                self.pc += 4

            elif decoded_inst.funct3 == "001":  # SLL
                self.registers[rd] = intbv(self.registers[rs1]).signed() << intbv(self.registers[rs2]).signed()
                self.pc += 4

            elif decoded_inst.funct3 == "101":
                if decoded_inst.funct7 == "0000000":  # SRL
                    self.registers[rd] = r_logical_shift(intbv(self.registers[rs1]).signed(), intbv(self.registers[rs2]).signed())
                    self.pc += 4
                elif decoded_inst.funct7 == "0100000":  # SRA
                    self.registers[rd] = intbv(self.registers[rs1]).signed() >> intbv(self.registers[rs2]).signed()
                    self.pc += 4

            elif decoded_inst.funct3 == "010":  # SLT
                self.registers[rd] = 1 if intbv(self.registers[rs1]).signed() < intbv(self.registers[rs2]).signed() else 0
                self.pc += 4

            elif decoded_inst.funct3 == "011":  # SLTU
                self.registers[rd] = 1 if intbv(self.registers[rs1]).unsigned() < intbv(self.registers[rs2]).unsigned() else 0
                self.pc += 4




        # ------------------------------------------------------[I-Type]-----------------------------------------------------------

        elif decoded_inst.type == "I":

            rd = int(decoded_inst.rd, 2)
            rs1 = int(decoded_inst.rs1, 2)
            imm = decoded_inst.imm

            if decoded_inst.opcode == "0010011":

                if decoded_inst.funct3 == "000":  # ADDI
                    self.registers[rd] = intbv(self.registers[rs1]).signed() + self.signed(imm,12)
                    self.pc += 4

                elif decoded_inst.funct3 == "100":  # XORI
                    self.registers[rd] = intbv(self.registers[rs1]).signed() ^ self.signed(imm,12)
                    self.pc += 4

                elif decoded_inst.funct3 == "110":  # ORI
                    self.registers[rd] = intbv(self.registers[rs1]).signed() | self.signed(imm,12)
                    self.pc += 4

                elif decoded_inst.funct3 == "111":  # ANDI
                    self.registers[rd] = intbv(self.registers[rs1]).signed() & self.signed(imm,12)
                    self.pc += 4

                elif decoded_inst.funct3 == "001":  # SLLI
                    self.registers[rd] = intbv(self.registers[rs1]).signed() << imm[12:5]
                    self.pc += 4

                elif decoded_inst.funct3 == "101":
                    if decoded_inst.funct7 == "0000000":  # SRLI
                        self.registers[rd] = r_logical_shift(intbv(self.registers[rs1]).signed(), imm[12:5])
                        self.pc += 4
                    elif decoded_inst.funct7 == "0100000":  # SRAI
                        self.registers[rd] = intbv(self.registers[rs1]).signed() >> imm[12:5]
                        self.pc += 4

                elif decoded_inst.funct3 == "010":  # SLTI
                    self.registers[rd] = 1 if intbv(self.registers[rs1]).signed() < imm.signed() else 0
                    self.pc += 4

                elif decoded_inst.funct3 == "011":  # SLTUI
                    self.registers[rd] = 1 if intbv(self.registers[rs1]).unsigned() < imm.unsigned() else 0
                    self.pc += 4



            elif decoded_inst.opcode == "0000011":
                if decoded_inst.funct3 == "000":
                    address = self.registers[rs1] + imm.signed()
                    self.registers[rd] = self.memory.ReadData(address, 1)
                    self.pc += 4

                elif decoded_inst.funct3 == "001":
                    address = self.registers[rs1] + imm.signed()
                    self.registers[rd] = self.memory.ReadData(address, 2)
                    self.pc += 4

                elif decoded_inst.funct3 == "010":
                    address = self.registers[rs1] + self.signed(imm,12)
                    self.registers[rd] = self.memory.read_data(address,1)
                    self.pc += 4
                elif decoded_inst.funct3 == "100":
                    address = self.registers[rs1] + imm.unsigned()
                    self.registers[rd] = self.memory.ReadData(address, 1)
                    self.pc += 4
                elif decoded_inst.funct3 == "101":
                    address = self.registers[rs1] + imm.unsigned()
                    self.registers[rd] = self.memory.ReadData(address, 2)
                    self.pc += 4



            elif decoded_inst.opcode == "1100111":  # JALR
                self.registers[rd] = self.pc + 4
                self.pc = intbv(self.registers[rs1])[32:].signed() + self.signed(imm,12)

            elif decoded_inst.opcode == "1110011":  # ecall
                if self.registers[17] == 93:  # exit
                    self.isRunning = False

                elif self.registers[17] == 64:
                    self.pc += 4





        # ------------------------------------------------------[S-Type]-----------------------------------------------------------

        elif decoded_inst.type == "S":

            rs1 = int(decoded_inst.rs1, 2)
            rs2 = int(decoded_inst.rs2, 2)
            imm = decoded_inst.imm

            if decoded_inst.funct3 == "000":  # SB
                address = self.registers[rs1] + imm.signed()
                data = self.registers[rs2][8:0]
                self.registers[rd] = self.memory.write(address, data)
                self.pc += 4


            elif decoded_inst.funct3 == "001":  # SH
                address = self.registers[rs1] + imm.signed()
                data = self.registers[rs2][7:0]
                self.registers[rd] = self.memory.write(address, data)
                data = self.registers[rs2][16:8]
                self.registers[rd] = self.memory.write(address + 4, data)
                self.pc += 4


            elif decoded_inst.funct3 == "010":  # SW

                address = self.registers[rs1] + self.signed(imm,12)

                data = int(str(intbv(self.registers[rs2])[7:0]),16)
                self.memory.write(address, data)


                data = int(str(intbv(self.registers[rs2])[16:8]), 16)
                self.memory.write(address + 1, data)

                data = int(str(intbv(self.registers[rs2])[24:16]), 16)
                self.memory.write(address + 2, data)

                data = int(str(intbv(self.registers[rs2])[32:24]), 16)
                self.memory.write(address + 3, data)

                self.pc += 4



        # ------------------------------------------------------[B-Type]-----------------------------------------------------------

        elif decoded_inst.type == "B":

            rs1 = int(decoded_inst.rs1, 2)
            rs2 = int(decoded_inst.rs2, 2)
            imm=self.signed(decoded_inst.imm,12)*2
            if decoded_inst.funct3 == "000":  # beq
                if intbv(self.registers[rs1]).signed() == intbv(self.registers[rs2]).signed():
                    self.pc += imm

                else:
                    self.pc += 4


            elif decoded_inst.funct3 == "001":  # bne

                if intbv(self.registers[rs1])[32:].signed() != intbv(self.registers[rs2])[32:].signed():
                    self.pc += imm
                else:
                    self.pc += 4


            elif decoded_inst.funct3 == "100":  # blt

                if intbv(self.registers[rs1]).signed() < intbv(self.registers[rs2]).signed():
                    self.pc += imm
                else:
                    self.pc += 4


            elif decoded_inst.funct3 == "101":  # bge
                if intbv(self.registers[rs1])[32:].signed() >= intbv(self.registers[rs2])[32:].signed():
                    self.pc += imm
                else:
                    self.pc += 4


            elif decoded_inst.funct3 == "110":  # bltu
                if intbv(self.registers[rs1]).unsigned() < intbv(self.registers[rs2]).unsigned():
                    self.pc += imm
                else:
                    self.pc += 4


            elif decoded_inst.funct3 == "111":  # bgeu
                if intbv(self.registers[rs1]).unsigned() >= intbv(self.registers[rs1]).unsigned():
                    self.pc += imm
                else:
                    self.pc += 4

        # ------------------------------------------------------[U-Type]-----------------------------------------------------------

        elif decoded_inst.type == "U":

            rd = int(decoded_inst.rd, 2)
            imm = intbv(decoded_inst.imm)[32:]

        if decoded_inst.opcode == "0110111":  # lui
            self.registers[rd] = (imm << 12)
            self.pc += 4


        elif decoded_inst.opcode == "0010111":  # auipc
            self.registers[rd] = self.pc + (imm << 12)
            self.pc += 4


        # ------------------------------------------------------[J-Type]-----------------------------------------------------------

        elif decoded_inst.type == "J":

            rd = int(decoded_inst.rd, 2)
            imm = decoded_inst.imm

            if decoded_inst.opcode == "1101111":  # jal
                self.registers[rd] = self.pc + 4
                self.pc += (self.signed(imm,20)<<1)
        self.registers[0] = intbv(0)[32:]
    # ----------------------------------------------------------------------------------------------------------------------

    """
    as in python we only have arithmetic shift thus to have 
    logical shift,must be implemented from scratch.
    """

    def r_logical_shift(self, val, n):
        return val >> n if val >= 0 else (val + 0x100000000) >> n


    def printRegisters(self,file):
            counter=0
            file.write(f"===============[Registers]=============\n")
            for reg in self.registers:
                file.write("x"+str(counter)+": "+str(reg)+"\n")
                counter+=1
            file.write("=======================================\n")





    def signed(self,val, bits):
        """compute the 2's complement of int value val"""
        val=int(val,2)
        if (val & (1 << (bits - 1))) != 0:  # if sign bit is set e.g., 8bit: 128-255
            val = val - (1 << bits)  # compute negative value
        return val  # return positive value as is