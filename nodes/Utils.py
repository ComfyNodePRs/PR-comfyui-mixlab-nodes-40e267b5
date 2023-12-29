import os
import re,random
from PIL import Image
import numpy as np
# FONT_PATH= os.path.abspath(os.path.join(os.path.dirname(__file__),'../assets/王汉宗颜楷体繁.ttf'))
import folder_paths
import matplotlib.font_manager as fm

# import json
# import hashlib


# def get_json_hash(json_content):
#     json_string = json.dumps(json_content, sort_keys=True)
#     hash_object = hashlib.sha256(json_string.encode())
#     hash_value = hash_object.hexdigest()
#     return hash_value
    


def tensor2pil(image):
    return Image.fromarray(np.clip(255. * image.cpu().numpy().squeeze(), 0, 255).astype(np.uint8))


def create_temp_file(image):
    output_dir = folder_paths.get_temp_directory()

    (
            full_output_folder,
            filename,
            counter,
            subfolder,
            _,
        ) = folder_paths.get_save_image_path('tmp', output_dir)

    
    image=tensor2pil(image)
 
    image_file = f"{filename}_{counter:05}.png"
     
    image_path=os.path.join(full_output_folder, image_file)

    image.save(image_path,compress_level=4)

    return [{
                "filename": image_file,
                "subfolder": subfolder,
                "type": "temp"
                }]

def get_font_files(directory):
    font_files = {}

    # 从指定目录加载字体
    for file in os.listdir(directory):
        if file.endswith('.ttf') or file.endswith('.otf'):
            font_name = os.path.splitext(file)[0]
            font_path = os.path.join(directory, file)
            font_files[font_name] = os.path.abspath(font_path)

    # 尝试获取系统字体
    try:
        font_paths = fm.findSystemFonts()
        for path in font_paths:
            try:
                font_prop = fm.FontProperties(fname=path)
                font_name = font_prop.get_name()
                font_files[font_name] = path
            except Exception as e:
                print(f"Error processing font {path}: {e}")
    except Exception as e:
        print(f"Error finding system fonts: {e}")

    return font_files

r_directory = os.path.join(os.path.dirname(__file__), '../assets/')

font_files = get_font_files(r_directory)
# print(font_files)


class ColorInput:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": { 
             
                    "color":("TCOLOR",), 
                             },
                }
    
    RETURN_TYPES = ("STRING",)
    # RETURN_NAMES = ("WIDTH","HEIGHT","X","Y",)

    FUNCTION = "run"

    CATEGORY = "♾️Mixlab/utils"

    INPUT_IS_LIST = False
    OUTPUT_IS_LIST = (False,False,)

    def run(self,color):
        return (color,)



class FontInput:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": { 
             
                    "font": (list(font_files.keys()),),
                             },
                }
    
    RETURN_TYPES = ("STRING",)
    # RETURN_NAMES = ("WIDTH","HEIGHT","X","Y",)

    FUNCTION = "run"

    CATEGORY = "♾️Mixlab/utils"

    INPUT_IS_LIST = False
    OUTPUT_IS_LIST = (False,False,)

    def run(self,font):

        return (font_files[font],)
    
class TextToNumber:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": { 
                    "text": ("STRING",{"multiline": False,"default": "1"}),
                    "random_number": (["enable", "disable"],),
                    "number":("INT", {
                        "default": 0, 
                        "min": 0, #Minimum value
                        "max": 10000000000, #Maximum value
                        "step": 1, #Slider's step
                        "display": "number" # Cosmetic only: display as "number" or "slider"
                    }),
                             },
                }
    
    RETURN_TYPES = ("INT",)
    # RETURN_NAMES = ("WIDTH","HEIGHT","X","Y",)

    FUNCTION = "run"

    CATEGORY = "♾️Mixlab/utils"

    INPUT_IS_LIST = False
    OUTPUT_IS_LIST = (False,)

    def run(self,text,random_number,number):
        
        numbers = re.findall(r'\d+', text)
        result=0
        for n in numbers:
            result = int(n)
            # print(result)
        
        if random_number=='enable' and result>0:
            result= random.randint(1, 10000000000)
        return {"ui": {"text": [text],"num":[result]}, "result": (result,)}
    

   
class FloatSlider:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
                    "number":("FLOAT", {
                        "default": 0, 
                        "min": 0, #Minimum value
                        "max": 1, #Maximum value
                        "step": 0.001, #Slider's step
                        "display": "slider" # Cosmetic only: display as "number" or "slider"
                    }),
                             },
                }
    
    RETURN_TYPES = ("FLOAT",) 

    FUNCTION = "run"

    CATEGORY = "♾️Mixlab/utils"

    INPUT_IS_LIST = False
    OUTPUT_IS_LIST = (False,)

    def run(self,number):
       
        return (number,)
    
  
class IntNumber:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
                    "number":("INT", {
                        "default": 0, 
                        "min": -1, #Minimum value
                        "max": 0xffffffffffffffff,
                        "step": 1, #Slider's step
                        "display": "number" # Cosmetic only: display as "number" or "slider"
                    }),
                             },
                }
    
    RETURN_TYPES = ("INT",) 

    FUNCTION = "run"

    CATEGORY = "♾️Mixlab/utils"

    INPUT_IS_LIST = False
    OUTPUT_IS_LIST = (False,)

    def run(self,number):
       
        return (number,)

class MultiplicationNode:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
                    "numberA":(any_type,),
                    "numberB":("FLOAT", {
                        "default": 0, 
                        "min": -1, #Minimum value
                        "max": 0xffffffffffffffff,
                        "step": 0.1, #Slider's step
                        "display": "number" # Cosmetic only: display as "number" or "slider"
                    })
                             },
                }
    
    RETURN_TYPES = ("FLOAT","INT",) 

    FUNCTION = "run"

    CATEGORY = "♾️Mixlab/utils"

    INPUT_IS_LIST = False
    OUTPUT_IS_LIST = (False,False,)

    def run(self,numberA,numberB):
        b=int(numberA*numberB)
        a=float(numberA*numberB)
        return (a,b,) 

class TextInput:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
                    "text": ("STRING",{"multiline": True,"default": ""}),
                             },
                }
    
    RETURN_TYPES = ("STRING",) 

    FUNCTION = "run"

    CATEGORY = "♾️Mixlab/utils"

    INPUT_IS_LIST = False
    OUTPUT_IS_LIST = (False,)

    def run(self,text):
       
        return (text,)
    
# 接收一个值，然后根据字符串或数值长度计算延迟时间，用户可以自定义延迟"字/s"，延迟之后将转化

import comfy.samplers
import folder_paths
 
# import time


class AnyType(str):
  """A special class that is always equal in not equal comparisons. Credit to pythongosssss"""

  def __ne__(self, __value: object) -> bool:
    return False

any_type = AnyType("*")
import time

class DynamicDelayProcessor:

    @classmethod
    def INPUT_TYPES(cls):
        # print("print INPUT_TYPES",cls)
        return {
            "required":{
                    "delay_seconds":("INT",{
                    "default":1,
                    "min": 0,
                    "max": 1000000,
                    }),
            },
            "optional":{
                "any_input":(any_type,),
                "delay_by_text":("STRING",{"multiline":True,}),
                "words_per_seconds":("FLOAT",{ "default":1.50,"min": 0.0,"max": 1000.00,"display":"Chars per second?"}),
                "replace_output": (["disable","enable"],),
                "replace_value":("INT",{ "default":-1,"min": 0,"max": 1000000,"display":"Replacement value"})
                }
            }
  
    @classmethod
    def calculate_words_length(cls,text):
        chinese_char_pattern = re.compile(r'[\u4e00-\u9fff]')
        english_word_pattern = re.compile(r'\b[a-zA-Z]+\b')
        number_pattern = re.compile(r'\b[0-9]+\b')

        words_length = 0
        for segment in text.split():
            if chinese_char_pattern.search(segment):
                # 中文字符，每个字符计为 1
                words_length += len(segment)
            elif number_pattern.match(segment):
                # 数字，每个字符计为 1
                words_length += len(segment)
            elif english_word_pattern.match(segment):
                # 英文单词，整个单词计为 1
                words_length += 1

        return words_length



    FUNCTION = "run"
    RETURN_TYPES = (any_type,)
    RETURN_NAMES = ('output',)

    CATEGORY = "♾️Mixlab/utils"
    def run(self,any_input,delay_seconds,delay_by_text,words_per_seconds,replace_output,replace_value):
        # print(f"Delay text:",delay_by_text )
        # 获取开始时间戳
        start_time = time.time()

        # 计算延迟时间
        delay_time = delay_seconds
        if delay_by_text and isinstance(delay_by_text, str) and words_per_seconds > 0:
            words_length = self.calculate_words_length(delay_by_text)
            print(f"Delay text: {delay_by_text}, Length: {words_length}")
            delay_time += words_length / words_per_seconds
            
        # 延迟执行
        print(f"延迟执行: {delay_time}")
        time.sleep(delay_time)

        # 获取结束时间戳并计算间隔
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"实际延迟时间: {elapsed_time} 秒")        

        # 根据 replace_output 决定输出值
        return (max(0, replace_value),) if replace_output == "enable" else (any_input,)
        



# app 配置节点
class AppInfo:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": { 
                    "name": ("STRING",{"multiline": False,"default": "Mixlab-App"}),
                    "image": ("IMAGE",),
                    "input_ids":("STRING",{"multiline": True,"default": "\n".join(["1","2","3"])}),
                    "output_ids":("STRING",{"multiline": True,"default": "\n".join(["5","9"])}),
                             },

                "optional":{
                    "description":("STRING",{"multiline": True,"default": ""}),
                    "version":("INT", {
                        "default": 1, 
                        "min": 1, 
                        "max": 10000, 
                        "step": 1, 
                        "display": "number"  
                    }),
                }

                }
    
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("IMAGE",)

    FUNCTION = "run"

    CATEGORY = "♾️Mixlab"

    INPUT_IS_LIST = False
    OUTPUT_IS_LIST = (False,)
    OUTPUT_NODE = True

    def run(self,name,image,input_ids,output_ids,description,version):

        im=create_temp_file(image)
        
        # id=get_json_hash([name,im,input_ids,output_ids,description,version])

        return {"ui": {"json": [name,im,input_ids,output_ids,description,version]}, "result": (image,)}
    

    

class GetImageSize_:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
            }
        }

    RETURN_TYPES = ("INT", "INT")
    RETURN_NAMES = ("width", "height")

    FUNCTION = "get_size"

    CATEGORY = "♾️Mixlab/utils"

    def get_size(self, image):
        _, height, width, _ = image.shape
        return (width, height)



class SwitchByIndex:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "A":(any_type,),
                "B":(any_type,),
                "index":("INT", {
                        "default": -1, 
                        "min": -1, 
                        "max": 1000, 
                        "step": 1, 
                        "display": "number"  
                    }),
            }
        }

    RETURN_TYPES = (any_type,)
    RETURN_NAMES = ("C",)

    FUNCTION = "run"

    CATEGORY = "♾️Mixlab/utils"

    INPUT_IS_LIST = True
    OUTPUT_IS_LIST = (True,)

    def run(self, A,B,index):
        C=[]
        index=index[0]
        for a in A:
            C.append(a)
        for b in B:
            C.append(b)
        if index>-1:
            try:
                C=[C[index]]
            except Exception as e:
                C=[]
        return (C,)



class LimitNumber:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "number":(any_type,),
                "min_value":("INT", {
                        "default": 0, 
                        "min": 0, 
                        "max": 0xffffffffffffffff,
                        "step": 1, 
                        "display": "number"  
                    }),
                "max_value":("INT", {
                        "default": 1, 
                        "min": 1, 
                        "max": 0xffffffffffffffff,
                        "step": 1, 
                        "display": "number"  
                    }),
            }
        }

    RETURN_TYPES = (any_type,)
    RETURN_NAMES = ("number",)

    FUNCTION = "run"

    CATEGORY = "♾️Mixlab/utils"

    INPUT_IS_LIST = False
    OUTPUT_IS_LIST = (False,)

    def run(self, number, min_value, max_value):
        nn=number

        if isinstance(number, int):
            min_value=int(min_value)
            max_value=int(max_value)
        if isinstance(number, float):
            min_value=float(min_value)
            max_value=float(max_value)

        if number < min_value:
            nn= min_value
        elif number > max_value:
            nn= max_value
        
        return (nn,)


 