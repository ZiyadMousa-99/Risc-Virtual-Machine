import myhdl
from myhdl import intbv

[

]
class Memory:
    def __init__(self):
        self.printnum=1
        self.size=1024*1024*1024
        self.storage=bytearray(self.size)
        self.textStartAddress=0x400000
        self.dataStartAddress=0x10010000
    """
    loadFile method
    ------------------------inputs--------------------------
    filename1:name of the file to be read ex: Code-Binary.bin
    filename2:name of the file to be read ex: Data-Binary.bin
    ------------------------outputs-------------------------
    ------------------------functionality-------------------
    loads a file into the memory
    """
    def loadFile(self,filename1, filename2):
        file1 = open(filename1, "rb")
        file2 = open(filename2, "rb")
        bytes1 = file1.read()
        bytes2 = file2.read()
        self.storage[self.textStartAddress:self.dataStartAddress - 4] = bytes1
        self.storage[self.dataStartAddress:] = bytes2
        file1.close()
        file2.close()



    """
        write method
        ------------------------inputs--------------------------
        address: where to write in memory
        data: what to write in memory
        ------------------------outputs-------------------------
        ------------------------functionality-------------------
        given address and data we write into the memory at the specified location
        """
    def write(self,address,data):
        self.storage[address]=data
    """
           read_inst method
           ------------------------inputs--------------------------
           address: where to retrieve in memory (4 bytes only)
           ------------------------outputs-------------------------
           string of 32 bits that is the instruction
           ------------------------functionality-------------------
           given address we return that address+4 bytes in the memory
           """
    def read_inst(self,address):
        string=int.from_bytes(self.storage[address:address+4], byteorder='little')
        string=bin(string)
        return string[2:].zfill(32)

    """
              read_data method
              ------------------------inputs--------------------------
              address: where to retrieve in memory (start at address end at n)
              ------------------------outputs-------------------------
              n-bytes of string 
              ------------------------functionality-------------------
              given address we return that address+n bytes in the memory
              """
    def read_data(self,address,n):
        longString = int.from_bytes(self.storage[address:address + n], byteorder='little')
        longString=bin(longString)

        return longString[2:].zfill(32*int((n/4)))

    def printData(self):
        filetext=open("memory_text.txt","w")
        filedata=open("memory_data.txt","w")


        binary_int = int(self.read_data(0x10010040, 8 * 4), 2)
        byte_number = binary_int.bit_length() + 7 // 8
        binary_array = binary_int.to_bytes(byte_number, "little")
        ascii_text = binary_array.decode()
        print(ascii_text)
        filetext.write(f"=======================.Text========================\n")
        filedata.write(f"=======================.Data========================\n")
        for x in range(0x400000,0x400000+0x3FF0,0x4):
            filetext.write(hex(x)+":\t")
            filetext.write(self.read_inst(x))
            filetext.write("\n")
        for x in range(0x10010000,0x10010000+0x3FF0,0x4):
            text=self.read_data(x,1).zfill(32)
            filedata.write(hex(x)+":\t")
            newtext=text[0:8]+" | "+text[8:16]+" | "+text[16:24]+" | "+text[24:32]
            filedata.write(newtext)
            filedata.write("\n")

        self.printnum+=1

        filetext.close()
        filedata.close()

