import cv2
import math
from datetime import datetime
from modules.HandTrackingModule import HandDetector
from modules.VolumeHandControl import VolumeController
from dao.mongodb_dao import MongoDAO

def main():
    cap = cv2.VideoCapture(0)
    detector = HandDetector(detectionCon=0.7)
    vol_ctrl = VolumeController()
    dao = MongoDAO()
    
    db_status = "OK" if dao.db is not None else "--"
    
    if dao.db is not None:
        dao.insertar_sesion({"inicio": datetime.now(), "usuario": "Gabriel Herrador"})

    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img, draw=False)

        if len(lmList) != 0:
            fingers = detector.fingersUp()
            
            # REQUISITO: Meñique (fingers[4]) bajado para actuar
            if fingers[4] == 0:
                # Pulgar (id 4) e Índice (id 8)
                x1, y1 = lmList[4][1], lmList[4][2]
                x2, y2 = lmList[8][1], lmList[8][2]
                distancia = math.hypot(x2 - x1, y2 - y1)
                
                volBar, volPer = vol_ctrl.set_volume(distancia)

                if dao.db is not None:
                    dao.insertar_evento({
                        "timestamp": datetime.now(),
                        "volumen": volPer
                    })
                
                cv2.circle(img, (x1, y1), 10, (255, 0, 0), cv2.FILLED)
                cv2.circle(img, (x2, y2), 10, (255, 0, 0), cv2.FILLED)
                cv2.putText(img, f"Vol: {volPer}%", (40, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

        cv2.putText(img, f"DB: {db_status}", (10, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
        cv2.imshow("Control de Volumen - Gabriel", img)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()