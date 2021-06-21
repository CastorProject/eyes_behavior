#!/usr/bin/env python

import rospy
import time

from geometry_msgs.msg import Point
from std_msgs.msg import Bool

class eyesManagerNode(object):
	def __init__(self, name):
		self.name = name
		rospy.init_node(self.name)
		self.rate = rospy.Rate(10) # 10hz
		self.initSubscribers()
		self.initPublishers()
		self.initVariables()
		return

	def initSubscribers(self):
		self.subDefEyesBehavior = rospy.Subscriber("/enableDefaultEyes", Bool, self.callbackDefaultEyes)

	def initPublishers(self):
		self.pubLEye = rospy.Publisher("/moveLEye", Point, queue_size = 10)
		self.pubREye = rospy.Publisher("/moveREye", Point, queue_size = 10)
		return

	def initVariables(self):
		self.enableDefaultEyesBehavior = Bool()
		self.enableDefaultEyesBehavior.data = True
		self.eyesDefaultBehavior = Point()
		return

	def callbackDefaultEyes(self, msg):
		self.enableDefaultEyesBehavior.data = msg.data
		return

	def main(self):
		rospy.loginfo("[%s] Facemotor node started ok", self.name)
		x = [i-30 for i in range(60)]
		y = [i-25 for i in range(50)]
		contX = 0
		contY = 0
		directionX = 0
		directionY = 0

		while not (rospy.is_shutdown()):
			if self.enableDefaultEyesBehavior.data:
				self.eyesDefaultBehavior.x = x[contX]
				self.eyesDefaultBehavior.y = y[contY]
				if directionX == 1:
					contX -= 1
				else:
					contX += 1
				if directionY == 1:
					contY -= 1
				else:
					contY += 1
				time.sleep(0.1)
				if(contX == len(x)-2):
					directionX = 1
				elif(contX == 0):
					directionX = 0
				if(contY == len(y)-2):
					directionY = 1
				elif(contY == 0):
					directionY = 0
				self.pubLEye.publish(self.eyesDefaultBehavior)
				self.rate.sleep()

if __name__ == '__main__':
	eyesManager = eyesManagerNode("eyesManager")
	eyesManager.main()
