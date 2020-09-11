from conversions import *

image_file = open('image.dat', 'rb')
boot_fat = image_file.read(512 * 19).hex()

files = {}
for i in range(224):
	files[i] = image_file.read(32).hex()

def file_info(file_x, x):
	hex_data = []
	for i in range (0, len(file_x), 2):
		hex_data.append(file_x[i : i + 2])
	
	if str(hex_data[0]) != '00':
		if str(hex_data[0]) == 'e5':
			print (
				'\n──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────' +
				'\nFile ' + str(x) + ':'
				+ '\n\t ╔ 0xE5: File has been deleted. Interesting!'
				+ '\n\t ╚ (First byte in Directory/Filename is missing)'

				+ '\n\n\t' + 'Directory/Filename: \t' + ' '.join(hex_data[1:7+1])
							+ '\t\t ──» ' + hex_to_ascii(hex_data[1:7+1])
				)
		else:
			print(
				'\n──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────' +
				'\nFile ' + str(x) + ':' +
				'\n\n\t' + 'Directory/Filename: \t' + ' '.join(hex_data[0:7+1])
							+ '\t\t ──» ' + hex_to_ascii(hex_data[0:7+1])
			)
		print(
			'\t' + '└─» Additional: \t' + ' '.join(hex_data[8:10+1])
						+ '\t\t\t ──» ' + hex_to_ascii(hex_data[8:10+1])

			+ '\n\t' + 'Attributes: \t\t' + hex_data[11]
						+ '\t ──» ' + binary_block_form(hex_to_binary(hex_data[11]))
						+ '\t\t ──» ' + get_attribute(hex_data[11])

			+ '\n\t' + 'Reserved: \t\t' + ' '.join(hex_data[12:13+1])
						+ '\t ──» ' + binary_block_form(hex_to_binary(hex_data[12:13+1]))
						+ ' ─────────────┐ '

			+ '\n\t' + 'Creation time: \t\t' + ' '.join(little_endian(hex_data[14:15+1]))
						+ '\t ──» ' + binary_block_form(hex_to_binary(little_endian(hex_data[14:15+1])))
						+ ' ──» ' + hex_to_time(hex_data[14:15+1]) + ' + ' + str(int(hex_data[15],16)*0.01) + 's'

			+ '\n\t' + 'Creation date: \t\t' + ' '.join(little_endian(hex_data[16:17+1]))
						+ '\t ──» ' + binary_block_form(hex_to_binary(little_endian(hex_data[16:17+1])))
						+ ' ──» ' + hex_to_date(hex_data[16:17+1])

			+ '\n\t' + 'Last access date: \t' + ' '.join(little_endian(hex_data[18:19+1]))
						+ '\t ──» ' + binary_block_form(hex_to_binary(little_endian(hex_data[18:19+1])))
						+ ' ──» ' + hex_to_date(hex_data[18:19+1])

			+ '\n\t' + 'Ignore in FAT12: \t' + ' '.join(hex_data[20:21+1])
			
			+ '\n\t' + 'Last write time: \t' + ' '.join(little_endian(hex_data[22:23+1])) 
						+ '\t ──» ' + binary_block_form(hex_to_binary(little_endian(hex_data[22:23+1])))
						+ ' ──» ' + hex_to_time(hex_data[22:23+1])
						+ ' (No fine resolution time)'

			+ '\n\t' + 'Last write date: \t' + ' '.join(little_endian(hex_data[24:25+1]))	
						+ '\t ──» ' + binary_block_form(hex_to_binary(little_endian(hex_data[24:25+1])))
						+ ' ──» ' + hex_to_date(hex_data[18:19+1])

			+ '\n\t' + 'First logical cluster: \t' + ' '.join(little_endian(hex_data[26:27+1])) 
						+ '\t\t\t\t ──» ' + hex_to_decimal(little_endian(hex_data[26:27+1]))
			
			+ '\n\t' + 'File size: \t\t' + ' '.join(little_endian(hex_data[28:31+1]))
						+ '\t\t\t ──» ' + hex_to_decimal(little_endian(hex_data[28:31+1])) + ' bytes'
			)

def print_top_frame():
	print(
		'\n\n' + '▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒'
		+ '\n' + '==================================================== ROOT DIR INFO ==================================================== ' + '\n'
	)

def print_bot_frame():
	print(
		'\n\n' + '====================================================== © KINGEN ======================================================' 
		+ '\n' + '▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒'
        + '\n\n'
	)

def print_entire_root_dir():
    print_top_frame()
    for i in range(224):
        file_info(files[i], i)
    print_bot_frame()

def print_file_info(i):
    file_info(files[i], i)

def ROOT_dir():
    print_entire_root_dir()
	#print_file_info(259)