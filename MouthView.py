# -*- coding: ISO-8859-1 -*-
# generated by wxGlade 0.3.5.1 on Fri Apr 15 17:02:14 2005

# Papagayo, a lip-sync tool for use with Lost Marble's Moho
# Copyright (C) 2005 Mike Clifton
# Contact information at http://www.lostmarble.com
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import os
import wx
from utilities import *
# begin wxGlade: dependencies
# end wxGlade

def ProcessMouthDir(mouthView, dirname, names):
	hasImages = False
	for file in names:
		file = file.lower()
		if file.endswith(".jpg") or file.endswith(".jpeg"):
			hasImages = True
	if not hasImages:
		return
	mouthView.AddMouth(os.path.normpath(dirname), names)

class MouthView(wx.Panel):
	def __init__(self, *args, **kwds):
		# begin wxGlade: MouthView.__init__
		kwds["style"] = wx.SUNKEN_BORDER|wx.TAB_TRAVERSAL
		wx.Panel.__init__(self, *args, **kwds)

		self.__set_properties()
		self.__do_layout()
		# end wxGlade

		# Other initialization
		self.doc = None
		self.curFrame = 0
		self.oldFrame = 0
		self.currentPhoneme = "rest"
		self.currentMouth = None
		self.mouths = {}
		self.LoadMouths()

		# Connect event handlers
		# window events
		wx.EVT_PAINT(self, self.OnPaint)

	def __set_properties(self):
		# begin wxGlade: MouthView.__set_properties
		self.SetMinSize((200, 200))
		self.SetBackgroundColour(wx.Colour(255, 255, 255))
		# end wxGlade

	def __do_layout(self):
		# begin wxGlade: MouthView.__do_layout
		pass
		# end wxGlade

	def OnPaint(self, event):
		dc = wx.PaintDC(self)
		dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
		dc.Clear()
		self.DrawMe(dc)

	def DrawMe(self, dc = None):
		if (self.doc is not None) and (self.doc.sound is not None) and (self.doc.sound.IsPlaying()):
			if self.doc.currentVoice is not None:
				phoneme = self.doc.currentVoice.GetPhonemeAtFrame(self.curFrame)
			else:
				phoneme = "rest"
			if phoneme == self.currentPhoneme:
				return
			else:
				self.currentPhoneme = phoneme
		else:
			self.currentPhoneme = "rest"
		if dc is None:
			dc = wx.ClientDC(self)
			freeDC = True
		else:
			freeDC = False
		dc.BeginDrawing()
		try:
			bitmap = self.mouths[self.currentMouth][self.currentPhoneme]
			width, height = self.GetClientSizeTuple()
			dc.DrawBitmap(bitmap, width / 2 - bitmap.GetWidth() / 2, height / 2 - bitmap.GetHeight() / 2)
		except:
			dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
			dc.Clear()
		dc.EndDrawing()
		if freeDC:
			del dc

	def SetFrame(self, frame):
		self.oldFrame = self.curFrame
		self.curFrame = frame
		self.DrawMe()

	def SetDocument(self, doc):
		self.doc = doc
		self.DrawMe()

	def LoadMouths(self):
		os.path.walk(os.path.join(get_main_dir(), "rsrc/mouths"), ProcessMouthDir, self)

	def AddMouth(self, dirname, names):
		bitmaps = {}
		for file in names:
			if ".svn" in file:
				continue
			path = os.path.normpath(os.path.join(dirname, file))
			nolog = wx.LogNull()
			bitmaps[file.split('.')[0]] = wx.Bitmap(path, wx.BITMAP_TYPE_ANY)
			del nolog
		self.mouths[os.path.basename(dirname)] = bitmaps
		if self.currentMouth is None:
			self.currentMouth = os.path.basename(dirname)

# end of class MouthView


