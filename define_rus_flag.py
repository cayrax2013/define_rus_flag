import cv2
import numpy as np
import base64

colors = {
    (255, 255, 255): "белый",             
    (0, 0, 255): "красный",               
    (0, 255, 0): "зеленый",               
    (255, 0, 0): "синий",                 
    (0, 255, 255): "желтый",              
    (255, 0, 255): "пурпурный",           
    (255, 255, 0): "голубой",             
    (0, 0, 0): "черный",                  
    (128, 128, 128): "серый",             
    (0, 0, 128): "темно-красный",         
    (0, 128, 0): "темно-зеленый",         
    (128, 0, 0): "темно-синий",           
    (0, 128, 128): "оливковый",           
    (128, 0, 128): "темно-пурпурный",     
    (128, 128, 0): "темно-голубой",       
    (255, 128, 255): "розово-фиолетовый", 
    (255, 128, 128): "светло-синий",      
    (128, 255, 255): "светло-желтый",     
    (128, 128, 255): "розовый",           
    (128, 255, 128): "салатовый",         
    (0, 128, 255): "оранжевый",           
    (0, 255, 128): "светло-зеленый",      
    (128, 255, 0): "бирюзовый",           
    (128, 0, 255): "фиолетовый",          
    (255, 128, 0): "аквамарин",           
    (255, 255, 128): "лавандовый",        
    (255, 0, 128): "индиго",          
}

def read_image(input_text):
    # img = cv2.imdecode(np.frombuffer(base64.b64decode(input_text), dtype=np.uint8), cv2.IMREAD_COLOR)
    img = cv2.imread(input_text)
    return img

def split_image_vertically(img, num_parts=3):
    height, width, _ = img.shape
    part_height = height // num_parts
    
    parts = []
    for i in range(num_parts):
        start_y = i * part_height
        end_y = (i + 1) * part_height if i < num_parts - 1 else height
        
        part = img[start_y:end_y, :]
        parts.append(part)
    
    return parts

def get_color(img, colors):
    result = ""
    for i in colors:
        if np.all(np.abs(np.array(img) - np.array(i)) < 20):
            result = i
            break
    if tuple(result) in colors:
        result = colors[tuple(result)]
    return result

def check_aspect_ratio(width, height, target_ratio=3/2, tolerance=0.05):
    actual_ratio = width / height
    ratio_diff = abs(actual_ratio - target_ratio) / target_ratio
    
    return ratio_diff <= tolerance

img = read_image(input(""))
height, width, _ = img.shape
condition = check_aspect_ratio(width, height, target_ratio=3/2, tolerance=0.05)
parts = split_image_vertically(img, 3)

avg_color = parts[0].mean(axis=(0, 1))

result1 = get_color(parts[0].mean(axis=(0, 1)), colors)
result2 = get_color(parts[1].mean(axis=(0, 1)), colors)
result3 = get_color(parts[2].mean(axis=(0, 1)), colors)

for i in colors:
    if np.all(np.abs(np.array(parts[0]) - np.array(i)) < 40):
        result1 = i
        break
if tuple(result1) in colors:
    result1 = colors[tuple(result1)]

if (result1 == "белый" and result2 == "синий" and result3 == "красный" and condition):
    print("Это изображение - флаг России")
else:
    print("Это не флаг России")