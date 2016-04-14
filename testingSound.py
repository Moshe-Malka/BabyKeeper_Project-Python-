import os, glob, ntpath, shutil
import scipy.io.wavfile as wavfile
import scipy.io
import numpy
import matplotlib.pyplot as plt
import sys



def readAudioFile(path):
	'''
	This function returns a numpy array that stores the audio samples
	of a specified WAV of AIFF file
	'''
	extension = os.path.splitext(path)[1]

	try:
		if extension.lower() == '.wav':
			[Fs, x] = wavfile.read(path)
		elif extension.lower() == '.aif' or extension.lower() == '.aiff':
			s = aifc.open(path, 'r')
			nframes = s.getnframes()
			strsig = s.readframes(nframes)
			x = numpy.fromstring(strsig, numpy.short).byteswap()
			Fs = s.getframerate()
		else:
			print "Error in readAudioFile(): Unknown file type!"
			return (-1,-1)
	except IOError:	
		print "Error: file not found or other I/O error."
		return (-1,-1)
	return (Fs, x)

r = readAudioFile('/home/pi/Desktop/MyPyCode/sample3.wav')
print(readAudioFile('/home/pi/Desktop/MyPyCode/sample3.wav'))
print(r[1])
print(max(r[1]))
print(r[1].shape)
plt.plot(r[1])

#print(max(numpy.fromfile(open('/home/pi/Desktop/MyPyCode/sample3.wav'),numpy.int16)[24:]))

