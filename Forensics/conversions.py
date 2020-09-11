def hex_to_ascii(hex_data):
	return bytearray.fromhex(''.join(hex_data)).decode()

def hex_to_binary(hex_data):
	return bin(int(''.join(hex_data),16))[2:].zfill(int(len(''.join(hex_data))/2)*8)

def binary_to_decimal(binary_data):
	return str(int(binary_data, 2))

def hex_to_decimal(hex_data):
	return str(int(''.join(hex_data), 16))

def binary_block_form(binary_data): #This one is not in little endian. So swap the bytes for the "right" format.
	if len(binary_data) > 8:
		bits = 16
	else:
		bits = 8
	return ' '.join(binary_data[i:i+4] for i in range(0, bits, 4))

def little_endian(hex_data):
	return hex_data[::-1]

def hex_to_time(hex_data):
	hour = binary_to_decimal(hex_to_binary(little_endian(hex_data))[0:4+1])
	minutes = binary_to_decimal(hex_to_binary(little_endian(hex_data))[5:10+1])
	seconds = int(binary_to_decimal(hex_to_binary(little_endian(hex_data))[11:15+1]))*2
	return str(hour) + ':' + str(minutes) + ':' + str(seconds)

def hex_to_date(hex_data):
	year = int(binary_to_decimal(hex_to_binary(little_endian(hex_data))[0:6+1])) + 1980
	month = binary_to_decimal(hex_to_binary(little_endian(hex_data))[7:10+1])
	day = binary_to_decimal(hex_to_binary(little_endian(hex_data))[11:15+1])
	return str(year) + '-' + str(month) + '-' + str(day)

def get_attribute(hex_data):
	attributes = []

	if hex_data[1] == '1':
		attributes.append('Read only')
	if hex_data[1] == '2':
		attributes.append('Hidden')
	if hex_data[1] == '4':
		attributes.append('System')
	if hex_data[1] == '8':
		attributes.append('Volume label')
	if hex_data[0] == '1':
		attributes.append('Subdirectory')
	if hex_data[0] == '2':
		attributes.append('Archive')
	if hex_data[0] == '4':
		attributes.append('Unused')
	
	return str(', '.join(attributes))