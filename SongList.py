from Song import Song
from Tools import send_message
from Tools import create_log

SONG_LOG = create_log("./Data/Song_Logs/")

#TODO: try to only log when song requests turn on.
#this will reduce the amount of junk files generated.

#Keeps a log of everything requested that session.
#Creates a new log file for each time the bot is on.
def logSong(title):
    file = open(SONG_LOG, "a")
    file.write(title)
    file.write("\r\n")
    file.close()


#Finds Song object in the songlist that matches the username
#Returns a vector containing the Song object and index on the list if found
#Returns None if not found

def findSong(songList, username):
    ptr = songList.head
    song_count = 1

    while ptr != None:
        if ptr.user == username:
            return [ptr, song_count]

        song_count += 1
        ptr = ptr.next

    return None


#LinkedList song list. This simulates a queue for LinkedList practice.
#Nodes are the Song class in Song.py
#Default number of songs a user can add: 1
#Default number of songs printed: 10
#No limit to how big the list can be
class SongList:
    def __init__(self, socket, irc):
        self.s = socket
        self.irc = irc
        self.head = None
        self.user_limit = 1
        self.print_limit = 10
        self.on = False


    #Adds a song to the end of the list.
    #Adds a song to head if head == None
    def addSong(self, title, username):
        if findSong(self, username) != None:
            send_message(self.s, self.irc, "You already have a song on the list " + username)
            return

        newSong = Song(title, username)
        ptr = self.head

        if self.head == None:
            self.head = newSong
        else:
            while ptr.next != None:
                ptr = ptr.next
            ptr.next = newSong

        send_message(self.s, self.irc,"\"" + title + "\"" + " has been added to the list by " + username)


    #Removes current song, logs song as played, prints out new song to play
    def pop(self):
        if self.head == None:
            send_message(self.s, self.irc, "There are no songs on the list.")
            return

        logSong(self.head.title)
        self.head = self.head.next

        if self.head == None:
            send_message(self.s, self.irc, "There are no songs on the list.")
        else:
            send_message(self.s, self.irc, "The next song is \"" + self.head.title + "\" requested by " + self.head.user)


    #Removes a song from the middle of the list.
    #Used when someone has to leave, or you don't have the song, etc.
    #Input: Can take song title, or position on list to remove.
    #Output: Returns True if the index is found, Returns False otherwise.
    def removeSong(self, index):
        ptr = self.head
        prev = self.head
        song_count = 1

        #Delete head.
        if index == 1:
            send_message(self.s, self.irc, "\"" + self.head.title + "\"" + " has been removed.")
            self.head = self.head.next
            return True

        while ptr != None:
            #Found target to delete
            if song_count == index:
                send_message(self.s, self.irc, "\"" + ptr.title + "\"" + " has been removed.")
                prev.next = ptr.next
                return True

            song_count += 1
            prev = ptr
            ptr = ptr.next

        return False


    #Updates song title if user changes their mind.
    #Input: Song index and the new title.
    #Output: Returns True if the index is found, Returns False otherwise.
    def updateSong(self, index, updated_title):
        ptr = self.head
        song_count = 1

        while ptr != None:
            if song_count == index:
                send_message(self.s, self.irc, "\"" + ptr.title + "\"" + " was updated to " + "\""  + updated_title + "\"")
                ptr.title = updated_title
                return True

            song_count += 1
            ptr = ptr.next

        return False


    def currentSong(self):
        if self.head != None:
            send_message(self.s, self.irc, "The current song is \"" + self.head.title + "\" requested by " + self.head.user)
        else:
            send_message(self.s, self.irc, "There are no songs being played.")

    def nextSong(self):
        if self.head.next != None:
            send_message(self.s, self.irc, "The next song is \"" + self.head.next.title + "\" requested by " + self.head.next.user)
        else:
            send_message(self.s, self.irc, "There is no next song on the list.")




    #Prints out the SongList.
    #Prints a custom message if the SongList is empty.
    def printList(self):
        ptr = self.head
        song_count = 1
        output = ""

        while ptr != None:
            output +="(" + str(song_count) + ") - " + ptr.title + ", "
            ptr = ptr.next
            song_count += 1

        if output == "":
            send_message(self.s, self.irc, "The list is empty!")
        else:
            #Send song list to chat, remove comma from end
            send_message(self.s, self.irc, output[0:len(output)-2])


    #Sends a message in chat detailing the user's request
    #Used if user forgets what song they requested or want to know what place in the list their request is.
    #TODO: Add functionality for more than one request per user.
    def mySong(self, username):
        song_info = findSong(self, username)

        if findSong(self, username) == None:
            send_message(self.s, self.irc, "You don't have a song on the list " + username)
            return
        else:
            title = song_info[0].title
            index = str(song_info[1])
            send_message(self.s, self.irc, username + " requested \"" + title +"\" located at position " + index + " on the list.")
