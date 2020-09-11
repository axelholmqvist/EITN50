from conversions import *

image_file = open('image.dat', 'rb')
boot_data = image_file.read(512 * 1).hex()

def boot_info(boot_data):
	hex_data = []
	for i in range (0, len(boot_data), 2):
		hex_data.append(boot_data[i : i + 2])
	
	print(
        '\n\t' + 'Ignore: \t\t\t' + ' '.join(hex_data[0:11+1])

        + '\n\t' + 'Bytes per sector: \t\t' + ' '.join(little_endian((hex_data[11:12+1])))
                    + '\t\t\t\t\t ──» ' + hex_to_decimal(little_endian(hex_data[11:12+1]))

        + '\n\t' + 'Sectors per cluster : \t\t' + hex_data[13]
                    + '\t\t\t\t\t ──» ' + hex_to_decimal(hex_data[13])

        + '\n\t' + 'Number of reserved sectors: \t' + ' '.join(little_endian(hex_data[14:15+1]))
                    + '\t\t\t\t\t ──» ' + hex_to_decimal(little_endian(hex_data[14:15+1]))

        + '\n\t' + 'Number of FATs: \t\t' + hex_data[16]
                    + '\t\t\t\t\t ──» ' + hex_to_decimal(hex_data[16])

        + '\n\t' + 'Max root directory entries: \t' + ' '.join(little_endian(hex_data[17:18+1]))
                    + '\t\t\t\t\t ──» ' + hex_to_decimal(little_endian(hex_data[17:18+1]))

        + '\n\t' + 'Total sector count: \t\t' + hex_data[19]
                    + '\t\t\t\t\t ──» ' + hex_to_decimal(hex_data[19])

        + '\n\t' + 'Ignore: \t\t\t' + hex_data[21]
        
        + '\n\t' + 'Sectors per FAT: \t\t' + ' '.join(little_endian(hex_data[22:23+1]))
                    + '\t\t\t\t\t ──» ' + hex_to_decimal(little_endian(hex_data[22:23+1]))

        + '\n\t' + 'Sectors per track: \t\t' + ' '.join(little_endian(hex_data[24:25+1]))
                    + '\t\t\t\t\t ──» ' + hex_to_decimal(little_endian(hex_data[24:25+1]))

        + '\n\t' + 'Number of heads: \t\t' + ' '.join(little_endian(hex_data[26:27+1]))
                    + '\t\t\t\t\t ──» ' + hex_to_decimal(little_endian(hex_data[26:27+1]))
        
        + '\n\t' + 'Total sector count (FAT12 = 0): ' + ' '.join(little_endian(hex_data[32:35+1]))
                    + '\t\t\t\t ──» ' + hex_to_decimal(little_endian(hex_data[32:35+1]))

        + '\n\t' + 'Ignore: \t\t\t' + ' '.join(little_endian(hex_data[36:37+1]))

        + '\n\t' + 'Boot signature: \t\t' + hex_data[38]
                    + '\t\t\t\t\t ──» ' + boot_signature(hex_data[38])

        + '\n\t' + 'Volume id: \t\t\t' + ' '.join(little_endian(hex_data[39:42+1]))
                    + '\t\t\t\t ──» ' + hex_to_decimal(little_endian(hex_data[39:42+1]))

        + '\n\t' + 'Volume label: \t\t\t' + ' '.join(hex_data[43:53+1])
                    + '\t ──» ' + hex_to_ascii(hex_data[43:53+1])

        + '\n\t' + 'File system type: \t\t' + ' '.join(hex_data[54:61+1])
                    + '\t\t\t ──» ' + hex_to_ascii(hex_data[54:61+1])

        + '\n\t' + 'Rest of boot sector (ignore): \t' + '-'
        )

def boot_signature(byte):
    if byte == '29':
        return 'True (Extended boot signature exists)'
    else:
        return 'False (Extended boot signature does not exist)'

def print_boot_top():
	print(
		'\n\n' + '▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒'
		+ '\n' + '=================================================== BOOT SECTOR INFO ================================================== '
	)

def print_boot_bot():
	print(
		'\n' + '====================================================== © KINGEN ======================================================' 
		+ '\n' + '▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒'
        + '\n\n'
	)

def BOOT_sector():
    print_boot_top()
    boot_info(boot_data)
    print_boot_bot()