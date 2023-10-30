from z3 import *


LEN = 40

flag = [BitVec(f"chr_{i}", 8) for i in range(LEN)]
buf = [BitVec(f"buf_{i}", 8) for i in range(0x10)]

# 0x0000000000498040
data = [
	0x73, 0x75, 0x7D, 0x66,		0x77, 0x49, 0x5A, 0x60,
	0x50, 0x7E, 0x67, 0x08,		0x44, 0x66, 0x40, 0x02,
	0x5E, 0x7B, 0x01, 0x7A,		0x66, 0x03, 0x5B, 0x65,
	0x03, 0x47, 0x0F, 0x0D,		0x59, 0x4D, 0x6C, 0x5B,
	0x7F, 0x6B, 0x52, 0x02,		0x7F, 0x13, 0x15, 0x48,
	0x10, 0x09, 0x00, 0x00,		0xC1, 0x6F, 0xF2, 0x86,
	0x23, 0x02, 0x00, 0x00,		0xE1, 0xF5, 0x05, 0x04,
	0x00, 0x00,
]


s = Solver()


for char in flag:
	s.add(And(char >= 0x20, char <= 0x7f))

b = [
	0x31, # '1'
	0x34, # '4'
	0x31, # '1'
	0x35, # '5'
	0x39, # '9'
	0x32, # '2'
	0x36, # '6' guessed
	0x35, # '5'
	0x33, # '3' guessed
	0x35, # '5' guessed
	0x38, # '8' guessed
	0x39, # '9' guessed
	0x37, # '7' guessed
	0x39, # '9' guessed
	0x33, # '3' guessed
	0x32, # '2' guessed
]


for byte in buf:
	s.add(And(byte >= 48, byte <= 57))

for i, byte in enumerate(b):
	if byte:
		s.add(buf[i] == byte)
		
		
for i in range(LEN):
	if b[i & 0xf]:
		print(chr(data[i] ^ b[i & 0xf]), end='')
	else:
		print(' ', end='')
print()




# flag_format =	'BALSN{ U        oO0O_1 P        N_c7F! }'
# flag_format =	'BALSN{                                 }'
flag_format =	'BALSN{ U        oO0O_1 P        N_c7F! }'
assert len(flag_format) == LEN


# banned = " }{`~@?=|+-\\/\'\")(*$$%&<>[]^:;.,"
banned = " }{"


for i, char in enumerate(flag_format):
	if char != ' ':
		s.add(flag[i] == ord(char))
		s.add(buf[i & 0x0F] == (data[i] ^ ord(char)))
	else:
		for c in banned:
			s.add(flag[i] != ord(c))




for i in range(LEN):
	x = data[i] ^ buf[i & 0x0F]
	s.add(flag[i] == x)




if (check := s.check()) == sat:
	m = s.model()
	#print(m)
	try:
		strng = ''.join([chr(m[char].as_long()) for char in flag])
		print(strng)
	except:
		pass

	#s.add(Or([char != m[char] for char in flag[6:-1]]))


else:
	print(check)
