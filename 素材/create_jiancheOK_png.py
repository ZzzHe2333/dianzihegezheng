from PIL import Image, ImageDraw, ImageFont
import os

def create_horizontal_transparent_image():
    """
    创建横向1:4比例的透明图片，带有红色边框和红色文字
    图片比例：高度:宽度 = 1:4
    边框和文字均为红色
    文字尽可能占满方框的85%空间
    """
    try:
        # 设置1:4比例的尺寸 (高度:宽度 = 1:4)
        # 例如：高度150像素，宽度600像素
        height = 150
        width = height * 4  # 1:4比例
        
        # 创建透明背景的RGBA图像
        image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        
        # 设置红色方框参数
        margin = int(min(width, height) * 0.05)  # 边距为图片最小尺寸的5%
        border_width = max(2, int(min(width, height) * 0.01))  # 边框宽度自适应
        
        # 方框坐标 (左上角x, 左上角y, 右下角x, 右下角y)
        box_coords = [
            margin,  # 左上角x
            margin,  # 左上角y
            width - margin,  # 右下角x
            height - margin   # 右下角y
        ]
        
        # 绘制红色方框
        draw.rectangle(box_coords, outline='red', width=border_width)
        
        # 计算方框内部可用区域 (用于放置文字)
        box_width = box_coords[2] - box_coords[0]  # 方框宽度
        box_height = box_coords[3] - box_coords[1]  # 方框高度
        
        # 文字区域占方框的85%
        text_area_width = int(box_width * 0.85)
        text_area_height = int(box_height * 0.85)
        
        # 设置文字
        text = "检 测 合 格"
        
        # 尝试加载宋体，如果失败则使用默认字体
        font = None
        font_paths = [
            "C:/Windows/Fonts/simsun.ttc",  # Windows 宋体
            "C:/Windows/Fonts/simsun.ttf",  # Windows 宋体
            "/System/Library/Fonts/STHeiti Light.ttc",  # macOS
            "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf"  # Linux
        ]
        
        for font_path in font_paths:
            if os.path.exists(font_path):
                # 初始字体大小设为方框高度的70%
                initial_font_size = int(box_height * 0.7)
                try:
                    font = ImageFont.truetype(font_path, initial_font_size)
                    break
                except:
                    continue
        
        if font is None:
            # 如果找不到系统字体，使用默认字体
            initial_font_size = int(box_height * 0.7)
            font = ImageFont.load_default()
            print("警告: 未找到宋体字体，使用默认字体")
        
        # 调整字体大小，使文字尽可能占满方框的85%
        optimal_font_size = find_optimal_font_size(draw, text, font, text_area_width, text_area_height, initial_font_size)
        
        # 使用调整后的字体大小重新加载字体
        if optimal_font_size != initial_font_size:
            try:
                for font_path in font_paths:
                    if os.path.exists(font_path):
                        font = ImageFont.truetype(font_path, optimal_font_size)
                        break
            except:
                # 如果重新加载失败，保持原字体
                pass
        
        # 计算文字位置（居中）
        try:
            # 新版本PIL使用textbbox
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
        except AttributeError:
            # 旧版本PIL使用textsize
            text_width, text_height = draw.textsize(text, font=font)
        
        text_x = (width - text_width) // 2
        text_y = (height - text_height) // 2
        
        # 绘制红色文字
        draw.text((text_x, text_y), text, fill='red', font=font)
        
        # 保存图片
        output_filename = "transparent_horizontal_1_4.png"
        image.save(output_filename, 'PNG')
        
        print(f"成功创建图片: {output_filename}")
        print(f"图片尺寸: {width} x {height} 像素")
        print(f"边框边距: {margin} 像素")
        print(f"边框宽度: {border_width} 像素")
        print(f"文字区域: {text_area_width} x {text_area_height} 像素")
        print(f"最终字体大小: {optimal_font_size} 点")
        print(f"文件大小: {os.path.getsize(output_filename)} 字节")
        
        return output_filename
        
    except Exception as e:
        print(f"创建图片时出错: {e}")
        return None

def find_optimal_font_size(draw, text, font, max_width, max_height, initial_size):
    """
    查找最佳字体大小，使文字尽可能占满指定区域
    
    参数:
    draw: ImageDraw对象
    text: 要绘制的文字
    font: 初始字体对象
    max_width: 最大宽度
    max_height: 最大高度
    initial_size: 初始字体大小
    
    返回:
    最佳字体大小
    """
    font_size = initial_size
    
    # 尝试减小字体大小，直到文字适合指定区域
    for size in range(initial_size, 10, -1):  # 从初始大小递减到10
        try:
            # 尝试使用新字体大小
            temp_font = font.font_variant(size=size)
            
            # 计算文字尺寸
            try:
                bbox = draw.textbbox((0, 0), text, font=temp_font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
            except AttributeError:
                text_width, text_height = draw.textsize(text, font=temp_font)
            
            # 检查是否适合指定区域
            if text_width <= max_width and text_height <= max_height:
                font_size = size
                break
        except:
            continue
    
    return font_size

def create_multiple_sizes():
    """创建不同尺寸的横向1:4比例图片"""
    #heights = [100, 150, 200]  # 不同高度，宽度会自动计算为高度的4倍
    heights = [200]
    for h in heights:
        try:
            w = h * 4  # 1:4比例 (800 200)
            
            # 创建透明图像
            image = Image.new('RGBA', (w, h), (0, 0, 0, 0))
            draw = ImageDraw.Draw(image)
            
            # 设置红色方框参数
            margin = int(min(w, h) * 0.05) 
            border_width = max(6, int(min(w, h) * 0.01)) #6-2
            box_coords = [10*margin, margin, w - 10*margin, h - margin]
            
            # 绘制红色方框
            draw.rectangle(box_coords, outline='red', width=border_width)
            
            # 计算方框内部可用区域
            box_width = box_coords[2] - box_coords[0]
            box_height = box_coords[3] - box_coords[1]
            text_area_width = int(box_width * 0.85)
            text_area_height = int(box_height * 0.85)
            
            # 设置文字
            text = "检测合格"
            
            # 加载字体
            font_paths = [
                "C:/Windows/Fonts/simsun.ttc",
                "C:/Windows/Fonts/simsun.ttf",
                "/System/Library/Fonts/STHeiti Light.ttc",
                "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf"
            ]
            
            font = None
            initial_font_size = int(box_height * 0.7)
            for font_path in font_paths:
                if os.path.exists(font_path):
                    try:
                        font = ImageFont.truetype(font_path, initial_font_size)
                        break
                    except:
                        continue
            
            if font is None:
                font = ImageFont.load_default()
            
            # 调整字体大小
            optimal_font_size = find_optimal_font_size(draw, text, font, text_area_width, text_area_height, initial_font_size)
            
            # 使用调整后的字体大小
            if optimal_font_size != initial_font_size:
                try:
                    for font_path in font_paths:
                        if os.path.exists(font_path):
                            font = ImageFont.truetype(font_path, optimal_font_size)
                            break
                except:
                    pass
            
            # 计算文字位置
            try:
                bbox = draw.textbbox((0, 0), text, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
            except AttributeError:
                text_width, text_height = draw.textsize(text, font=font)
            
            text_x = (w - text_width) // 2
            text_y = (h - text_height) // 2
            
            # 绘制红色文字
            draw.text((text_x, text_y), text, fill='red', font=font)
            
            filename = f"transparent_horizontal_1_4_{h}x{w}.png"
            image.save(filename, 'PNG')
            print(f"创建: {filename} - {h}x{w}像素, 字体大小: {optimal_font_size}点")
            
        except Exception as e:
            print(f"创建尺寸 {h}x{w} 时出错: {e}")

if __name__ == "__main__":
    # 创建主要图片
    print("创建横向1:4比例透明图片...")
    print("特点:")
    print("- 高度:宽度 = 1:4")
    print("- 透明背景")
    print("- 红色边框")
    print("- 红色'检测合格'文字(宋体)")
    print("- 文字占方框约85%空间")
    print()
    
    #create_horizontal_transparent_image()
    
    print("\n" + "="*50 + "\n")
    
    # 创建多个尺寸版本
    print("创建不同尺寸的横向1:4比例图片...")
    create_multiple_sizes()