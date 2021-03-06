import dlib, cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.patheffects as path_effects


# model
detector = dlib.get_frontal_face_detector()
sp = dlib.shape_predictor('models/shape_predictor_68_face_landmarks.dat')
facerec = dlib.face_recognition_model_v1('models/dlib_face_recognition_resnet_model_v1.dat')

def find_faces(img):
    dets = detector(img, 1)

    # can not find face
    if len(dets) == 0:
        return np.empty(0), np.empty(0), np.empty(0)
    
    rects, shapes = [], []
    shapes_np = np.zeros((len(dets), 68, 2), dtype=np.int)
    
    for k, d in enumerate(dets):
        rect = ((d.left(), d.top()), (d.right(), d.bottom()))
        rects.append(rect)

        # 이미지랑, 얼굴 상화좌우좌표 기반으로 나온 사각형을 대입 -> 68개 점.
        shape = sp(img, d)
        
        # convert dlib shape to numpy array
        for i in range(0, 68):
            shapes_np[k][i] = (shape.part(i).x, shape.part(i).y)

        shapes.append(shape)
        
    # rects(사각형 얼굴), shapes(68개점), shapes_np(dlib를 np array로 변환한 것)
    return rects, shapes, shapes_np

# shape로 128개 얼굴패턴 data추출
def encode_faces(img, shapes):
    face_descriptors = []

    for shape in shapes:
        # facerec -> facerecognition
        face_descriptor = facerec.compute_face_descriptor(img, shape)
        face_descriptors.append(np.array(face_descriptor))

    return np.array(face_descriptors)



def makeDescs(img_paths, descs):
    for name, img_path in img_paths.items():
        img_bgr = cv2.imread(img_path)
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

        _, img_shapes, _ = find_faces(img_rgb)
        # shape(68개 점)을 넣어 데이터를 ㅇ얻는다.
        descs[name] = encode_faces(img_rgb, img_shapes)[0]


    np.save('img/descs.npy', descs)
    # print("I Found " + str(len(img_shapes)) + " faces")
    # print(descs)

    return descs


def recogFace(descs, compare_img_path, n):
    img_bgr = cv2.imread(compare_img_path)
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

    rects, shapes, _ = find_faces(img_rgb)
    descriptors = encode_faces(img_rgb, shapes)

    # Visualize Output
    fig, ax = plt.subplots(1, figsize=(20, 20))
    ax.imshow(img_rgb)

    for i, desc in enumerate(descriptors):
        found = False
        
        for name, saved_desc in descs.items():
            dist = np.linalg.norm([desc] - saved_desc, axis=1)

            if dist < 0.6:
                found = True

                # drawing part
                text = ax.text(rects[i][0][0], rects[i][0][1], name,
                        color='b', fontsize=40, fontweight='bold')
                text.set_path_effects([path_effects.Stroke(linewidth=10, foreground='white'), path_effects.Normal()])
                rect = patches.Rectangle(rects[i][0], rects[i][1][1] - rects[i][0][1], rects[i][1][0] - rects[i][0][0],linewidth=2, edgecolor='w', facecolor='none')
                ax.add_patch(rect)

                break
        
        if not found:
            ax.text(rects[i][0][0], rects[i][0][1], 'unknown',
                    color='r', fontsize=20, fontweight='bold')
            rect = patches.Rectangle(rects[i][0], rects[i][1][1] - rects[i][0][1], rects[i][1][0] - rects[i][0][0], linewidth=2, edgecolor='r', facecolor='none')
            ax.add_patch(rect)

    plt.axis('off')
    plt.savefig(f'img/output{n}.png')
    # plt.show()



img_paths = {
    'conan' : 'img/conan.jpg'
}
# eccode된 얼굴패턴이 저장될 곳.
descs = {
    'conan' : None
}


compare_img_path1 = 'img/ctest1.jpg'
compare_img_path2 = 'img/ctest2.jpg'
descs = makeDescs(img_paths, descs)
recogFace(descs, compare_img_path1, 1)
recogFace(descs, compare_img_path2, 2)




