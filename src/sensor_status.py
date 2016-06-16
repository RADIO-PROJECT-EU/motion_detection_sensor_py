#!/usr/bin/env python
import roslib, rospy
import requests
from motion_detection_sensor_status_publisher.msg import SensorStatusMsg

url = 'http://localhost:8080/radioMC/radio/getSensorStatus'
publisher = None
topic = ''

def init():
    global url, publisher, topic
    rospy.init_node('motion_detection_sensor_status_publisher')
    url = rospy.get_param('~api_url', 'http://localhost:8080/radioMC/radio/getSensorStatus')
    topic = '~'+rospy.get_param('~publish_topic', 'status')
    publisher = rospy.Publisher(topic, SensorStatusMsg, queue_size=10)
    rospy.Timer(rospy.Duration(0.5), requestAndPublish)
    while not rospy.is_shutdown():  
        rospy.spin()


def requestAndPublish(timeEvent):
    global url, publisher
    
    r = requests.get(url)
    js = r.json()

    msg = SensorStatusMsg()
    msg.header.stamp = rospy.Time.now()
    msg.sensor_id = js['id']
    msg.status = js['status']
    msg.date = js['date']
    msg.trigger = js['trigger']
    msg.triggerName = js['triggerName']

    publisher.publish(msg)

if __name__ == '__main__':
    init()
