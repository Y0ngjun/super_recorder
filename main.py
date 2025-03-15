import numpy as np
import cv2 as cv

output_filename = input('저장할 동영상 파일 이름을 입력하세요 (예: my video): ')

camera = cv.VideoCapture(0)

if camera.isOpened():
    fourcc = cv.VideoWriter_fourcc(*'XVID')
    fps = float(camera.get(cv.CAP_PROP_FPS))
    frame_width = int(camera.get(cv.CAP_PROP_FRAME_WIDTH))
    frame_height = int(camera.get(cv.CAP_PROP_FRAME_HEIGHT))
    wait_msec = int(1/fps*1000)
    out = None
    recording = False
    mirror_mode = False

    while True:
        valid, img = camera.read()

        if not valid:
            break

        if mirror_mode:
            img = cv.flip(img, 1)

        if recording:
            out.write(img)
            cv.putText(img, 'REC', (10, 30), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 1, cv.LINE_AA)

        cv.imshow('super_recorder', img)

        key = cv.waitKey(wait_msec)
        if key == 27:
            break
        elif key == 32:
            recording = not recording
            if recording:
                out = cv.VideoWriter(output_filename + '.avi', fourcc, fps, (frame_width, frame_height))
                print('녹화 시작: {output_filename}')
            else:
                out.release()
                out = None
                print('녹화 중지')
        elif key == ord('r'):
            mirror_mode = not mirror_mode
            mode = '셀카 모드 활성화' if mirror_mode else '셀카 모드 비활성화'
            print(mode)
    camera.release()
    if out is not None:
        out.release()
    cv.destroyAllWindows()
else:
    print('카메라를 열 수 없습니다.')