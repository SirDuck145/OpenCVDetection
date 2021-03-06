import cv2
import numpy as np

def nothing(x):
	#any operation while trackbar in use
	pass

cap = cv2.VideoCapture(0)

# Creates a trackbar useful for debugging
cv2.namedWindow("Trackbars")
cv2.createTrackbar("L-H", "Trackbars", 0, 180, nothing)
cv2.createTrackbar("L-S", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("L-V", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("U-H", "Trackbars", 84, 180, nothing)
cv2.createTrackbar("U-S", "Trackbars", 155, 255, nothing)
cv2.createTrackbar("U-V", "Trackbars", 251, 255, nothing)

while(True):
	_, frame = cap.read()
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	l_h = cv2.getTrackbarPos("L-H", "Trackbars")
	l_s = cv2.getTrackbarPos("L-S", "Trackbars")
	l_v = cv2.getTrackbarPos("L-V", "Trackbars")
	u_h = cv2.getTrackbarPos("U-H", "Trackbars")
	u_s = cv2.getTrackbarPos("U-S", "Trackbars")
	u_v = cv2.getTrackbarPos("U-V", "Trackbars")

	lower_red = np.array([l_h,l_s,l_v])
	upper_red = np.array([u_h, u_s, u_v])

	mask = cv2.inRange(hsv, lower_red, upper_red)
	kernel = np.ones((12, 12), np.uint8)
	mask = cv2.erode(mask, kernel)

	# Contours Detection
	contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

	for cnt in contours:
		area = cv2.contourArea(cnt)
		approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)

		if area > 400:
			cv2.drawContours(frame, [approx], 0, (0,0,0), 3)
			if len(approx) == 4:
				print("Rectangle is found")

	cv2.imshow("Frame", frame)
	cv2.imshow("Mask", mask)
	cv2.imshow("kernel", kernel)

	key = cv2.waitKey(1)
	if key == 27:
		break

cap.release()
cv2.destroyAllWindows()
