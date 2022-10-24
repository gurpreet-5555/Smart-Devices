# Smart-Devices
Solution that enables IoT supported devices to "see" human activity and automatically turn on/off. <br>Computer Vision &amp; Object Detection is used to detect human presence and send a signal to an IoT device so that it can operate automatically.

<img src="output/output.gif" width="1100" height="500" />

<br>

For quite some time, one of the primary use cases for AI has been automation.<br>
There are several methods for devices to detect human presence in a region using sensors and act accordingly.
One method that allows us to do so is through computer vision and object detection (or person detection).

<br>
In this project, we'll utilize a neural network based object detection architecture known as 'ssd-mobilenet-v2'.<br>
SSD or Single Shot Detector is used to perform object detection by dividing an image into a number of regions/cells using a grid and then assigning detected class and its confidence score to the detection region. 

<br> <br>
'ssd-mobilenet-v2' is available for use on Tensorflow object detection model zoo.<br>
Depending on the usecase, there are several object detection models to choose from. The 'ssd-mobilenet-v2' is capable of detecting over 90 classes, including person detection in images.

<br>You can explore more object detection models through below link:<br>
<a href="https://github.com/tensorflow/models/tree/master/research/object_detection">Explore Tensorflow Object Detection Models</a>

<h2>Features:</h2>
<ul>
  <li>Control an IoT enabled device automatically by detecting human activity</li>
  <li>Real-time person detection</li>
  <li>Specify confidence threshold for detection to compensate for poor lighting/image quality</li>
  <li>Set countdown timers for starting & stopping a device</li>
  <li>Support for multiple streaming protocols from IP cameras such as rtsp, http. Can also be used with static video file depending on installed codecs(.mp4, .avi etc..)</li>
  <li>Supports in-built webcams</li>
</ul>  

<h2>Requirements:</h2>
<ul>
  <li>Python 3.6</li>
  <li>OpenCV 4.2.0</li>
  <li>Tensorflow 1.15</li>
  <li>NumPy 1.18.2</li>  
</ul>

<h2>How to use?</h2>
<ul>
  <li>Clone Repository</li>
  <pre>git clone https://github.com/gurpreet-5555/Smart-Devices.git</pre>  </ul>
<ul>  <li>Navigate to main directory</li>
  <pre>cd Smart-Devices</pre> </ul>
<ul><li>Specify your code in <b>device_controller.py</b> to start and stop IoT powered device.</li>
<pre>Sample code is included to turn on/off Philips Hue Lamps</pre></ul>
<ul><li>Execute Program</li>
<pre>python start_detection.py --confidence 0.4 --stream http://192.168.1.43:8080/video --startthreshold 10 --stopthreshold 60</pre>
<pre>Arguments -
confidence : Confidence threshold (0.0 to 1.0) for person detection. Use a lower value to compensate for poor lighting or image quality(Optional)
stream : Source of video feed (http, rtsp etc) or video file. Specify this parameter as 0 to use in-built webcams. (Required)
startthreshold: Time to wait in seconds before device starts once human activity is detected. Default value is 5 seconds. (Optional)
stopthreshold: Time to wait in seconds before device stops once no human activity is detected in video stream. Default value is 30 seconds. (Optional)
</pre></ul>


 
  
