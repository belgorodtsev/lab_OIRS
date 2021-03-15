import image_generator as ig
import imutils
import cv2
import os


def get_shape_info(contour):
	# точность, максимальное расстояние от контура до апроксимирующего контура
	epsilon = 0.05 * cv2.arcLength(contour, True)
	approx = cv2.approxPolyDP(contour, epsilon, True)
	if len(approx) == 3:
		shape = "triangle"
	elif len(approx) == 4:
		(_, _, w, h) = cv2.boundingRect(approx)
		ar = w / float(h)
		shape = "square" if 0.95 <= ar <= 1.05 else "rectangle"
	elif len(approx) == 5:
		shape = "pentagon"
	else:
		shape = "circle"
	return approx, shape


def image_detector(n_image):
	if not os.path.exists("threshold_image"):
		os.mkdir("threshold_image")

	if not os.path.exists("result"):
		os.mkdir("result")

	for i in range(n_image):
		image = cv2.imread(f"init/{i + 1}.jpg")

		# преобразуем RGB в серое
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		# сегментация
		thresh = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY)[1]

		cv2.imwrite(f"threshold_image/{i + 1}.jpg", thresh)

		# извлекаем крайние внешние контуры, запоминаем не все точки
		contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		contours = imutils.grab_contours(contours)

		for cnt in contours:
			approx, shape_name = get_shape_info(cnt)
			x = approx.ravel()[0]
			y = approx.ravel()[1] - 5

			cv2.drawContours(image, [cnt], -1, (0, 0, 255), 2)
			cv2.putText(image, shape_name, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

		cv2.imwrite(f"result/{i + 1}.jpg", image)


if __name__ == "__main__":
	number_images = int(input("Введите количество изображений:"))
	ig.generate_random_images(number_images)
	image_detector(number_images)
