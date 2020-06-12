import time
import smbus
from Modules.Pcf8591 import Pcf8591

class Lcd1602:
	def __init__(self, addr):
		self.__bus = smbus.SMBus(1)
		self.__addr = addr
		self.init()

	# 장치 초기화 설정
	def init(self):
		try:
			self.send_command(0x33) # Must initialize to 8-line mode at first
			time.sleep(0.005)
			self.send_command(0x32) # Then initialize to 4-line mode
			time.sleep(0.005)
			self.send_command(0x28) # 2 Lines & 5*7 dots
			time.sleep(0.005)
			self.send_command(0x0C) # Enable display without cursor
			time.sleep(0.005)
			self.send_command(0x01) # Clear Screen
			self.__bus.write_byte(self.__addr, 0x08)
		except:
			return False
		else:
			return True

	# 8비트를 하나의 word로 봐야함 "write_word"는 8비트로 명령어를 보내는 메소드로 생각하자
	def write_word(self, data):
		temp = data | 0x08
		self.__bus.write_byte(self.__addr ,temp)

	# 명령어를 전달할 때는 형식에 맞춰서 해야하며, data sheet에 따라서 작성됨! 장치가 알아들을 수 있는 명령어로 변환해줌
	def send_command(self, comm):
		# Send bit7-4 firstly
		buf = comm & 0xF0
		buf |= 0x04               # RS = 0, RW = 0, EN = 1
		self.write_word(buf)
		time.sleep(0.002)
		buf &= 0xFB               # Make EN = 0
		self.write_word(buf)

		# Send bit3-0 secondly
		buf = (comm & 0x0F) << 4
		buf |= 0x04               # RS = 0, RW = 0, EN = 1
		self.write_word(buf)
		time.sleep(0.002)
		buf &= 0xFB               # Make EN = 0
		self.write_word(buf)

	# 사용자가 출력하고자 하는 데이터 (send_command - 장치에게 어떤 동작을 지시 - 와 send_data - 장치로부터 출력하고자 지시 - 의 차이 주의하기!)
	def send_data(self, data):
		# Send bit7-4 firstly
		buf = data & 0xF0
		buf |= 0x05               # RS = 1, RW = 0, EN = 1
		self.write_word(buf)
		time.sleep(0.002)
		buf &= 0xFB               # Make EN = 0
		self.write_word(buf)

		# Send bit3-0 secondly
		buf = (data & 0x0F) << 4
		buf |= 0x05               # RS = 1, RW = 0, EN = 1
		self.write_word(buf)
		time.sleep(0.002)
		buf &= 0xFB               # Make EN = 0
		self.write_word(buf)

	def clear(self):
		self.send_command(0x01) # Clear Screen

	def openlight(self):  # Enable the backlight 백 라이트를 켜고 끄는 기능 (명령어)
		self.__bus.write_byte(0x27,0x08)
		self.__bus.close()

	# x는 한 라인에 들어갈 수 있는 문자의 수 (16개가 들어갈 수 있으면 x는 0부터 15까지 가질 수 있음)
	# y는 라인 번호 (2줄짜리일 경우 0과 1로 표현)
	def write(self, x, y, str):
		if x < 0:
			x = 0
		if x > 15:
			x = 15
		if y <0:
			y = 0
		if y > 1:
			y = 1

		# Move cursor
		addr = 0x80 + 0x40 * y + x
		self.send_command(addr)

		for chr in str:
			self.send_data(ord(chr))

if __name__ == '__main__':
	lcd = Lcd1602(0x27)
	lcd.write(0, 0, 'Good Morning')
	lcd.write(0, 1, 'This is Yunjis')
	pcf8591 = Pcf8591(0x48)