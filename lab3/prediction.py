import matplotlib.pyplot as plt
import glob
from sklearn.ensemble import RandomForestClassifier
from constants import *


def predict(train_data, train_labels):
    clf = RandomForestClassifier(n_estimators=NUM_TREES, random_state=SEED, n_jobs=-1)

    clf.fit(train_data, train_labels)

    # loop through the test images
    for ind, file in enumerate(glob.glob(TEST_PATH + "/*.*")):
        # read the image
        image = cv2.imread(file)
        image = cv2.resize(image, FIXED_SIZE)

        global_feature = get_feature(image)

        # predict label of test image
        prediction = clf.predict(global_feature.reshape(1, -1))[0]

        # display the output image
        fig = plt.figure()
        fig.suptitle(TRAIN_LABELS[prediction])
        plt.axis('off')
        plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        plt.savefig(f'data/result/{ind}.png')
