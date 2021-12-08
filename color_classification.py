import numpy as np 
from PIL import Image 
import matplotlib.pyplot as plt 

from sklearn.cluster import KMeans


class ColorClassification:
    def __init__(self, dark=False):
        if not dark:
            img = Image.open('model.png').convert('RGB')
            
            img.thumbnail((25, 50))
        else:
            img = Image.open('dark_model.png').convert('RGB')
        self.arr = np.array(img)
        self.X = self.arr.reshape(self.arr.shape[0] * self.arr.shape[1], 3)
        if not dark:
            self.est = KMeans(n_clusters=2, random_state=42)
        else: 
            self.est = KMeans(n_clusters=4, random_state=42)
        self.est.fit(self.X)
    
    def show_model(self):
        plt.figure(figsize=(4, 3))
        plt.imshow(self.arr)
                
        labels = self.est.labels_
        ans = labels.reshape(self.arr.shape[0], self.arr.shape[1])
        plt.figure(figsize=(4, 3))
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
    # img = Image.open('test/Screenshot_1638873926.png').convert('RGB')
    img = Image.open('d.png').convert('RGB')
    img.thumbnail((500, 500))
    model = ColorClassification(dark=True) 
    model.show_model()
    model.test(img)
    
    