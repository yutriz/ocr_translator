from .snipper import snipper
import cv2

class multi_blocks():
    def __init__(self):
        self.snippers = list()
        self.snippers_num = input('enter num of your ROI(s): ')
        self.snippers_num = int(self.snippers_num)
        
        for _ in range(0, self.snippers_num):
            self.snippers.append(snipper(mode='block'))
        cv2.destroyAllWindows()
        print(self.snippers)

    
    def snipper_info(self, index):
        if 0 <= index and index < self.snippers_num:
            return self.snippers[index].snip_pos
        else: 
            return None
        
    def snippers_pos(self):
        """
        output: list of pos tuples
        """
        positions = list()
        for num in range(0, self.snippers_num):
            positions.append(self.snippers[num].snip_pos)
        
        return positions
    
    def snippers_images(self):
        images = list()
        for num in range(0, self.snippers_num):
            im = self.snippers[num].get_snip()
            images.append(im)
        return images
    
    def snipper_update(self):
        self.snippers_images
    
    
