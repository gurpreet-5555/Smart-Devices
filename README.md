# Smart-Devices
Solution that enables IoT supported devices to "see" human activity and turn on/off automatically. <br>Computer Vision &amp; Object Detection is used to detect human presence and trigger signal to IoT device for automatic operation.

<br>

Automation has been one of the primary use cases for AI for quite some time now.<br>
Various methods are available to allow devices to detect human prescence in a region using sensors and act accordingly.<br>
One of the methods which allows us to do so includes computer vision and applying it to perform object detection (or person detection).

<br>
In this project, we'll be utilizing a neural network based object detection architecture known as 'ssd-mobilenet-v2'.<br>
SSD or Single Shot Detector is used to perform object detection by dividing an image into a number of regions/cells using a grid and then assigning detected class and its confidence score to the detection region. 

<br> <br>
'ssd-mobilenet-v2' is available for use on Tensorflow object detection model zoo.<br>
There are a no. of object detection models to choose depending on the usecase. 'ssd-mobilenet-v2' is capable of detecting over 90 classes which includes detecting human in an image. 

<br>You can explore more object detection models through below link:

<a href="https://github.com/tensorflow/models/tree/master/research/object_detection">Explore Tensorflow Object Detection Models</a>

<h2>Features:</h2>
<ul>
  <li>Control an IoT enabled device automatically by detecting human activity</li>
  <li>Real-time person detection</li>
  <li>Specify confidence threshold for detection to compensate for poor lighting/image quality</li>
  <li>Countdown Timer for starting & stopping a device</li>
  <li>Support for multiple streaming protocols from IP cameras such as rtsp, http. Can also be used with static video file depending on installed codecs(.mp4, .avi etc..)</li>
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
  <pre>https://github.com/gurpreet-5555/Intelligent-Devices.git</pre>  </ul>
<ul>  <li>Navigate to main directory</li>
  <pre>cd Intelligent-Devices/main</pre> </ul>
<ul><li>Specify your code in <b>device_controller.py</b> to start and stop IoT powered device.</li>
<pre>Sample code is included to turn on/off Philips Hue Lamps</pre></ul>
<ul><li>Execute Program</li>
<pre>python start_controller.py --confidence 0.4 --stream http://192.168.1.43:8080/video --startthreshold 10 --stopthreshold 60</pre>
<pre>Arguments -
confidence : Confidence threshold for person detection. Default value is 0.2 (Optional)
stream : Source of video feed (http, rtsp etc) or video file. (Required)
startthreshold: Time to wait in seconds before device starts once human activity is detected. Default value is 5 seconds. (Optional)
stopthreshold: Time to wait in seconds before device stops once no human activity is detected in video stream. Default value is 30 seconds. (Optional)
</pre></ul>


 
  
