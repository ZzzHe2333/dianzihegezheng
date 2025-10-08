from PIL import Image
import os

def create_transparent_a4_png(output_path="transparent_a4.png", dpi=72):
    """
    创建一个透明背景的A4大小PNG图片
    
    参数:
    output_path: 输出文件路径
    dpi: 分辨率 (默认为72 DPI)
    """
    try:
        # A4纸张尺寸 (毫米)
        a4_width_mm = 210
        a4_height_mm = 297
        
        # 将毫米转换为像素 (1英寸 = 25.4毫米)
        width_px = int(a4_width_mm * dpi / 25.4)
        height_px = int(a4_height_mm * dpi / 25.4)
        
        print(f"创建A4透明图片: {width_px} x {height_px} 像素 ({dpi} DPI)")
        
        # 创建RGBA模式的透明图像
        # RGBA: Red, Green, Blue, Alpha (透明度)
        image = Image.new('RGBA', (width_px, height_px), (0, 0, 0, 0))
        
        # 保存为PNG格式
        image.save(output_path, 'PNG')
        
        print(f"成功创建透明A4图片: {output_path}")
        print(f"文件大小: {os.path.getsize(output_path)} 字节")
        
        return output_path
        
    except Exception as e:
        print(f"创建图片时出错: {e}")
        return None

def create_a4_with_different_dpi():
    """创建不同DPI的A4透明图片"""
    dpi_options = {
        '72_dpi': 72,      # 屏幕显示
        '150_dpi': 150,    # 普通打印
        '300_dpi': 300     # 高质量打印
    }
    
    for name, dpi in dpi_options.items():
        filename = f"transparent_a4_{name}.png"
        create_transparent_a4_png(filename, dpi)
        print()

if __name__ == "__main__":
    # 创建默认72 DPI的透明A4图片
    create_transparent_a4_png()
    
    print("\n" + "="*50 + "\n")
    
    # 创建不同DPI的版本
    create_a4_with_different_dpi()