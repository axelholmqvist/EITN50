from conversions import *

image_file = open('image.dat', 'rb')
boot_data = image_file.read(512 * 1).hex()

def FAT_table():
	fat_data = {}
	for i in range(512 * 18):
		fat_data[i] = image_file.read(1).hex()

	fat_table = []
	for i in range(0, len(fat_data), 3):
		three_bytes = str(fat_data[i]) + str(fat_data[i+1]) + str(fat_data[i+2])
		fat_table.append(three_bytes[3] + three_bytes[0] + three_bytes[1])
		fat_table.append(three_bytes[4] + three_bytes[5] + three_bytes[2])
	
	print_fat_top()
	for i in range(275):
		print('\t\t' + str(i) + '\t──────»\t' + str(fat_table[i]) + ' / ' + hex_to_decimal(fat_table[i]))
	print_fat_bot()

def print_fat_top():
	print(
		'\n\n' + '▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒'
		+ '\n' + '===================== FAT TABLE INFO =====================' + '\n'
	)

def print_fat_bot():
	print(
		'\n' + '======================== © KINGEN ========================' 
		+ '\n' + '▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒'
        + '\n\n'
	)

    