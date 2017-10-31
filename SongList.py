from Song import Song
from Tools import send_message

class SongList:
	def __init__(self, s, irc):
		self.s = s
		self.irc = irc
		self.vipHead = None
		self.vipTail = None
		self.vipLength = 0
		self.head = None
		self.tail = None
		self.length = 0
		self.current = ""



	#prints out the list of songs.
	#starts with the vip list then prints out the normal list
	def getList(self):
		ptr = self.head
		vipPtr = self.vipHead
		output = ""
		count = 1
		vipCount = 1
		

		if vipPtr == None and ptr == None:
			return "Song list is empty! YesHaha"


		#vip list output first
		while vipPtr != None:
			output += "(VIP" + str(vipCount) + ") - "
			output += vipPtr.title
			
			if vipPtr == self.vipTail and ptr == None:
				output += ""
			else:
				output += ", "


			vipPtr = vipPtr.next
			vipCount += 1


		while ptr != None:
			output += "(" + str(count) + ") - "
			output += ptr.title
			
			if ptr != self.tail:
				output += ", "

			ptr = ptr.next
			count += 1

		return output



	#Checks for user duplicates and song name duplicates
	#TODO: check for duplicates in the vip list as well
	def findDuplicates(self, title, user):
		ptr = self.head

		while ptr != None:
			if ptr.title == title:
				return "That song is already on the list " + user
			elif ptr.user == user:
				return "You already have a song on the list " + user

		return ""



	#Normal song list stuff
	def addSong(self, vip, target, username):
		#duplicateError = self.findDuplicates(target, username)

		#if duplicateError != "":
		#	send_message(self.s, self.irc, duplicateError)
		#	return 


		song = Song(target, username)
		
		if vip == True:
			if self.vipHead == None:
				self.vipHead = song
			else:
				self.vipTail.next = song
				
			self.vipTail = song
			self.vipLength += 1
		else:
			if self.head == None:
				self.head = song
			else:
				self.tail.next = song
				
			self.tail = song
			self.length += 1

		send_message(self.s, self.irc, song.title + " has been added!")



	#Mod only command that removes a song based on position on the list
	#todo remove song by song title -> add a try and catch block to check variable type
	def removeSong(self, vip, target):
		ptr = None
		prev = None
		count = 1
		target = int(target)

		if vip == True:
			ptr = self.vipHead
			prev = self.vipHead
		else:
			ptr = self.head
			prev = self.head

		if ptr == None:
			print("Songlist is empty. Theres nothing to remove.")

		while ptr != None:
			if count == target and vip == True:
				if ptr == self.vipHead:
					self.vipHead = self.vipHead.next
					return
				else:
					prev.next = ptr.next

					if ptr == self.vipTail:
						self.vipTail = prev

			elif count == target and vip == False:
				if ptr == self.head:
					self.head = self.head.next
					return
				else:
					prev.next = ptr.next

					if ptr == self.tail:
						self.tail = prev

			count += 1
			prev = ptr
			ptr = ptr.next	