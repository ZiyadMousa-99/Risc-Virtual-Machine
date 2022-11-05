
class Inst(object):
    def __init__(self,type,opcode=0,rs1=0,rs2=0,funct3=0,funct7=0,rd=0,imm=0):
        self.type=type
        self.opcode=opcode
        self.rs1=rs1
        self.rs2=rs2
        self.funct3=funct3
        self.funct7=funct7
        self.rd=rd
        self.imm=imm
