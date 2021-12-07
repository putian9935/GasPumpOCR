import numpy as np 
from PIL import Image 
import matplotlib.pyplot as plt 

from sklearn.cluster import KMeans
from mpl_toolkits.mplot3d import Axes3D


class ColorClassification:
    def __init__(self):

        img = Image.open('f.png').convert('RGB')
        img.thumbnail((25, 50))
        self.arr = np.array(img)
        self.X = self.arr.reshape(self.arr.shape[0] * self.arr.shape[1], 3)
        self.est = KMeans(n_clusters=2, random_state=42)
        self.est.fit(self.X)
    
    def show_model(self):
        fig = plt.figure(figsize=(4, 3))
        ax = Axes3D(fig, rect=[0, 0, 0.95, 1])

        labels = self.est.labels_
        plt.scatter(self.X[:,0], self.X[:,1], self.X[:,2], c=labels.astype(float))
        ans = labels.reshape(self.arr.shape[0], self.arr.shape[1])
        plt.figure()
        plt.imshow(ans)
        plt.show() 
    
    def test(self, img):
        """Test model on arbitrary image; 

        img is expected to have mode RGB
        """
        arr = np.array(img)
        y = arr.reshape(arr.shape[0] * arr.shape[1], 3)
        plt.figure()
        plt.imshow(
            self.est.predict(y).reshape(arr.shape[0] , arr.shape[1])
        )
        plt.show()

    def convert_to_01(self, img):
        arr = np.array(img)
        y = arr.reshape(arr.shape[0] * arr.shape[1], 3)
        return (self.est.predict(y) == 1).reshape(arr.shape[0] , arr.shape[1])


if __name__ == '__main__':
    img = Image.open('Screenshot_1638873926.png').convert('RGB')
    img.thumbnail((500, 500))
    model = ColorClassification() 
    model.test(img)