'''
Created on Oct 18, 2018

Rename and edit diversity youtube mp3 rips to have metadata 

@author: Kyle
'''
import os, sys, re, pprint
import mutagen
from mutagen.mp3  import MP3
from mutagen.id3 import ID3, TIT2, TALB, TOPE, TPE2, TPE1, TCOM

dirpathDiver = r'C:\_KM_root_lap\Music\Youtube\YoutubeRandom'

#sample
filename = r'AZEDIA - Something (Keeno Remix).mp3'
aReg = re.search('(.*) - (.*)\.', filename)
homestuckpath= r'C:\_KM_root_lap\Music\Homestuck Vol. 6 - Heir Transparent\track02.mp3'
somethingWrongPath = dirpathDiver + os.sep + filename
starpath= r'C:\_KM_root_lap\Music\Starbound Soundtrack\Atlas.mp3'
#### All code below works. Simply kept to showcase multiple files and their encodings
#===============================================================================
# ##############
# aMutFile = mutagen.File(homestuckpath)
# print(aMutFile.keys())
# print(aMutFile.pprint())
# ##############
# aMutFile = mutagen.File(starpath)
# print(aMutFile.keys())
# print(aMutFile.pprint())
# ##############
# #Now to test a change on "something wrong"
# aMutFile = mutagen.File(somethingWrongPath)
# print(aMutFile.keys())
# print(aMutFile.pprint())
# ### Functional code to apply changes to above file.
# # audio = ID3(somethingWrongPath)
# # audio.add(TIT2(encoding=3, text=aReg.group(2) ) )
# # audio.add(TOPE(encoding=3, text=aReg.group(1) ) )
# # audio.add(TPE1(encoding=3, text=aReg.group(1) ) )
# # audio.add(TPE2(encoding=3, text=aReg.group(1) ) )
# # audio.add(TCOM(encoding=3, text=aReg.group(1) ) )
# # audio.save()
# #######
#===============================================================================


#===============================================================================
# aMutFile = mutagen.File(somethingWrongPath)
# print(aMutFile.keys())
# print(aMutFile.pprint())
#===============================================================================

print(os.listdir(dirpathDiver))
for fname in os.listdir(dirpathDiver):
    aReg = re.search('(.*) - (.*)\.', fname)
    audio = ID3(dirpathDiver+os.sep+fname)
    print(fname)
    #  Japanese characters are not supported and will cause an error.
    audio.add(TIT2(encoding=3, text=aReg.group(2) ) )
    audio.add(TOPE(encoding=3, text=aReg.group(1) ) )
    audio.add(TPE1(encoding=3, text=aReg.group(1) ) )
    audio.add(TPE2(encoding=3, text=aReg.group(1) ) )
    audio.add(TCOM(encoding=3, text=aReg.group(1) ) )
    audio.save()
#if os.path.isdir(user_path+ os.sep+fname):

# for file in dirpathDiver:



print('--set')


