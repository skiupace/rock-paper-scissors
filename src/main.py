import time
import random
import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector


cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

detector = HandDetector(maxHands=1)

timer = 0
startGame = False
resultState = False
scores = [0,0] # [AI, Player]

while True:
    bgImage = cv2.imread("resources/bg.png")
    success, img = cap.read()
    img = cv2.flip(img, 1)
    
    scaledImage = cv2.resize(img, (0, 0), None, 0.875, 0.875)
    scaledImage = scaledImage[:,80:480]
    
    # Find hands
    hands, img = detector.findHands(scaledImage)

    if startGame:
        if resultState is False:
            timer = time.time() - initialTime
            cv2.putText(bgImage, str(int(timer)), (605, 435), cv2.FONT_HERSHEY_PLAIN, 6, (255, 0, 255), 4)

            if timer > 3:
                resultState = True
                timer = 0

                if hands:
                    hand = hands[0]
                    fingers = detector.fingersUp(hand)

                    if fingers == [0,0,0,0,0]:
                        playerMove = 1
                    elif fingers == [1,1,1,1,1]:
                        playerMove = 2
                    elif fingers == [0,1,1,0,0]:
                        playerMove = 3

                    randomNumber = random.randint(1, 3)
                    aiImage = cv2.imread(f'resources/{randomNumber}.png', cv2.IMREAD_UNCHANGED)
                    bgImage = cvzone.overlayPNG(bgImage, aiImage, (149, 310))

                    # when PLayer wins
                    if  (playerMove == 1 and randomNumber == 3) or \
                        (playerMove == 2 and randomNumber == 1) or \
                        (playerMove == 3 and randomNumber == 2):
                        scores[1] += 1

                    # when AI wins
                    if  (playerMove == 3 and randomNumber == 1) or \
                        (playerMove == 1 and randomNumber == 2) or \
                        (playerMove == 2 and randomNumber == 3):
                        scores[0] += 1

    bgImage[234:654,795:1195] = scaledImage

    if resultState:
        bgImage = cvzone.overlayPNG(bgImage, aiImage, (149, 310))

    cv2.putText(bgImage, str(scores[0]), (410, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)
    cv2.putText(bgImage, str(scores[1]), (1112, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)
    cv2.imshow("Rock Paper Scissors!", bgImage)
    
    key = cv2.waitKey(1)
    if key == ord('s'):
        startGame = True
        initialTime = time.time()
        resultState = False
    elif key & 0xFF == ord('q'):
        break
