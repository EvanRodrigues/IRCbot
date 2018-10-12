import threading
import time

from Tools import update_file

POINTS_FILE = './Data/Points.txt'

class AutoPoints:
	def __init__(self):
		self.chatters = []


	def run(self):
		MissionThread = threading.Thread(target = self.start, args = ())
		MissionThread.daemon = True
		MissionThread.start()
		return


	def start(self):
		while True:
			time.sleep(60)
			self.award_all(1)


	def updateChatters(self, line):
		parts = line.split("\\r\\n")

		for part in parts:
			try:
				if "JOIN" in part:
					user = part.split(":")[1].split("!")[0]
					self.chatters.append(user)
				elif "PART" in part:
					user = part.split(":")[1].split("!")[0]
					self.chatters.remove(user)
				else:
					continue
			except:
				continue		


	def award_all(self, total):
		for user in self.chatters:
			print("added 1 dd to " + user)
			update_file(POINTS_FILE, user, total)
		
		return


def rem_extra_info(userInfo):
	userInfo = userInfo.split(":")[1]
	userInfo = userInfo.split("!")[0]
	return userInfo