import tkinter as tk
from tkinter import filedialog
import os
from pdf2image import convert_from_path
import threading
from concurrent.futures import ThreadPoolExecutor
import time
from PIL import Image
import sys
# ====== 配置项 ======
TP2_PATH = r"C:\Users\Administrator\Desktop\ele_yinzhang\tp2.png"
MAX_WORK = 4

# =====================
def get_tp2_path():
    """
    检测运行模式（源码/打包exe），返回同目录下tp2.png的绝对路径
    """
    if getattr(sys, 'frozen', False):
        # exe模式（PyInstaller等打包后）
        base_path = sys._MEIPASS if hasattr(sys, '_MEIPASS') else os.path.dirname(sys.executable)
    else:
        # 源码模式
        base_path = os.path.dirname(os.path.abspath(__file__))
    
    # 拼接tp2.png路径
    tp2_path = os.path.join(base_path, "tp2.png")
    return os.path.abspath(tp2_path)

def convert_pdf_first_page_to_png(): 
    """
    使用Tkinter选择PDF文件，将每个PDF文件的首页转换为PNG图片
    使用多线程提高转换效率
    返回生成的PNG图片绝对路径列表
    """
    # 初始化Tkinter并隐藏主窗口
    root = tk.Tk()
    root.withdraw()
    
    # ① 使用Tkinter选择PDF文件
    pdf_files = filedialog.askopenfilenames(
        title="选择PDF文件",
        filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
    )
    
    if not pdf_files:
        print("未选择任何PDF文件")
        return []
    
    # ② 保存选择的PDF路径作为list1
    list1 = list(pdf_files)
    print(f"已选择 {len(list1)} 个PDF文件")
    
    # 初始化list2用于保存图片绝对路径
    list2 = []
    
    # 创建线程锁以确保列表操作的线程安全
    list_lock = threading.Lock()
    
    def convert_single_pdf(pdf_path):
        """转换单个PDF文件的函数"""
        try:
            # 获取PDF文件所在目录和文件名（不含扩展名）
            pdf_dir = os.path.dirname(pdf_path)
            pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
            
            # 设置输出图片名称：GZ_源pdf名称.png
            output_image_name = f"GZ_{pdf_name}.png"
            output_image_path = os.path.join(pdf_dir, output_image_name)
            
            # 将PDF首页转换为PNG图片
            images = convert_from_path(pdf_path, first_page=1, last_page=1, dpi=300)
            
            if images:
                # 保存第一页为PNG图片
                images[0].save(output_image_path, 'PNG')
                
                # 使用线程锁安全地将图片**绝对路径**添加到list2
                with list_lock:
                    list2.append(output_image_path)
                return True
            else:
                return False
                
        except Exception as e:
            return False
    
    # 记录开始时间
    start_time = time.time()
    
    # ③ 使用线程池并行处理PDF转换
    with ThreadPoolExecutor(max_workers=4, thread_name_prefix="PDF_Converter") as executor:
        futures = [executor.submit(convert_single_pdf, pdf_path) for pdf_path in list1]
        results = [future.result() for future in futures]
    
    # 计算总耗时
    end_time = time.time()
    total_time = end_time - start_time
    
    print(f"\n转换完成! 成功转换 {len(list2)}/{len(list1)} 个文件")
    print(f"总耗时: {total_time:.2f} 秒,平均每个文件: {total_time/len(list1) if list1 else 0:.2f} 秒.")
    
    return list2


def add_gz_prefix(abs_path: str) -> str:
    """
    给文件的文件名加上 'GZ_' 前缀，并返回新的绝对路径。
    不会改动原文件，仅返回新路径。

    参数:(abs_path)=原始文件的绝对路径


    返回:加上 'GZ_' 前缀的新文件绝对路径
    """
    if not os.path.isabs(abs_path):
        raise ValueError(f"必须传入绝对路径, 当前是: {abs_path}")

    dir_name = os.path.dirname(abs_path)                  # 文件所在目录
    file_name = os.path.basename(abs_path)                # 文件名
    new_name = f"GZ_{file_name}"                          # 加前缀
    new_abs_path = os.path.join(dir_name, new_name)       # 拼接成新的绝对路径
    return new_abs_path


def combine_images(bottom_image_path, top_image_path, output_path=None):
    """
    将两张图片组合在一起，底层图片在底部，顶层图片在顶部
    
    参数:
        bottom_image_path: 底层图片路径
        top_image_path: 顶层图片路径  
        output_path: 输出图片路径，默认为'combined_result.png'
    """
    try:
        # 打开图片
        bottom_img = Image.open(bottom_image_path)
        top_img = Image.open(top_image_path)
        
        print(f"底层图片尺寸: {bottom_img.size}")
        print(f"顶层图片尺寸: {top_img.size}")
        
        # 确保两张图片尺寸一致（将顶层图片调整为底层图片的尺寸）
        if bottom_img.size != top_img.size:
            print("调整顶层图片尺寸以匹配底层图片...")
            top_img = top_img.resize(bottom_img.size, Image.Resampling.LANCZOS)
        
        # 确保图片都是RGBA模式以支持透明度
        if bottom_img.mode != 'RGBA':
            bottom_img = bottom_img.convert('RGBA')
        if top_img.mode != 'RGBA':
            top_img = top_img.convert('RGBA')
        
        # 创建新图片，底层图片作为背景
        combined = Image.new('RGBA', bottom_img.size)
        combined.paste(bottom_img, (0, 0))
        
        # 将顶层图片叠加到底层图片上
        combined = Image.alpha_composite(combined, top_img)
        
        # 保存结果
        if output_path is None:
            output_path = 'combined_result.png'
        
        combined.save(output_path, 'PNG')
        print(f"图片组合完成！保存为: {output_path}")
        
        # 显示结果图片信息
        print(f"输出图片尺寸: {combined.size}")
        
        return combined
        
    except FileNotFoundError as e:
        print(f"错误: 找不到图片文件 - {e}")
    except Exception as e:
        print(f"处理图片时发生错误: {e}")



# 使用示例
if __name__ == "__main__":
    # 调用函数并获取结果
    result_list = convert_pdf_first_page_to_png()
    tp2_cunzai = True
    #print(result_list)
    
    if not os.path.isfile(TP2_PATH):
        print("tp2.png(透明图层)不存在,尝试获取同级文件夹下的TP2.png文件")
        TP2_PATH = get_tp2_path()
        if not os.path.isfile(TP2_PATH):
            print("tp2文件不存在,无法使用")
            tp2_cunzai = False
        else:
            tp2_cunzai = True
    else:
        tp2_cunzai = True
        
    if tp2_cunzai:
        for i in result_list:
            combine_images(i,TP2_PATH,i)

