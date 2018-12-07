import os
import cv2

def crop_images():
    # 裁剪该目录下的所有图片
    img_files = os.listdir("./images")
    for img_file in img_files:
        out_name = "new_" + img_file
        img_path = os.path.join("./images", img_file)
        out_path = os.path.join("./images", out_name)
        print(img_path, out_path)
        img = cv2.imread(img_path)
        crop_img = img[:2000, :550]
        cv2.imwrite(out_path, crop_img)

if __name__ == "__main__":
    crop_images()
