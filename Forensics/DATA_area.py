from conversions import *

image_file = open('image.dat', 'rb')
data = image_file.read() 

def print_data_block():
    # print(data[144384:144896].hex()) # (33+251-2)*512, from discovered FAT-entry at 251
    # A subdirectory that contains the .- and the ..-directory, SYSTEM.DAT and TEST.TXT
    # TEST.TXT has first logical cluster at 253.
    # SYSTEM.DAT has first logical cluster at 260 and is 2029 bytes.
    # =>
    print(data[148992:151021].hex()) # (33+260-2)*512 -> (33+260-2*512)+2029)
    # JACKPOT!!! A zip-file with a xxx.doc.
    #zip_file = open("system.zip", "wb")
    #zip_file.write(data[148992:151021])
    #zip_file.close()
    # Password: Bg%4! (from John the Ripper)

    # print(data[144896:145408].hex()) # (33+252-2)*512, from discovered FAT-entry at 252
    # A subdirectory that contains the .- and the ..-directory. Nothing more.

    # print(data[145408:145920]) # (33+253-2)*512, from discovered FAT-entry at 253 / deleted file in ROOT at 253
    # Contains "This is text"

    # print(data[148480:148992].hex()) # (33+259-2)*512, from deleted file in ROOT at 259
    # A subdirectory that contains the .- and the ..-directory. Nothing more.

def print_data_top():
	print(
		'\n\n' + '▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒'
		+ '\n' + '======================= DATA BLOCK =======================...' + '\n'
	)

def print_data_bot():
	print(
		'\n' + '======================== © KINGEN ========================' 
		+ '\n' + '▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒...'
        + '\n\n'
	)

def DATA_area():
    print_data_top()
    print_data_block()
    print_data_bot()