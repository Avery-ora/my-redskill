import sys
import os
import io
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import rembg

def create_heytea_style_poster(image_path, title, mode):
    os.makedirs("output", exist_ok=True)
    
    original = Image.open(f"input/{image_path}").convert("RGBA")
    w, h = original.size
    
    # 抠图提取主体
    with open(f"input/{image_path}", "rb") as f:
        input_bytes = f.read()
    output_bytes = rembg.remove(input_bytes)
    subject = Image.open(io.BytesIO(output_bytes)).convert("RGBA")
    subject = subject.resize((w, h))
    
    # 处理成干净的白底背景
    background = Image.new("RGBA", (w, h), (255, 255, 255, 255))
    
    # 把主体放在画面中合适的位置
    result = Image.alpha_composite(background, subject)
    
    # 画涂鸦小人（粗黑、笨拙的线条）
    draw = ImageDraw.Draw(result)
    
    # 小人位置（右下角区域）
    cx, cy = int(w * 0.8), int(h * 0.75)
    
    # 头
    draw.ellipse([cx-20, cy-40, cx+20, cy], fill=None, outline="black", width=3)
    # 眼睛（两个小点）
    draw.ellipse([cx-8, cy-28, cx-4, cy-24], fill="black")
    draw.ellipse([cx+4, cy-28, cx+8, cy-24], fill="black")
    # 嘴巴（一条歪歪的弧线）
    draw.arc([cx-8, cy-18, cx+8, cy-8], start=0, end=180, fill="black", width=2)
    # 身体
    draw.line([cx, cy, cx, cy+50], fill="black", width=3)
    # 胳膊
    draw.line([cx, cy+15, cx-25, cy+35], fill="black", width=2)
    draw.line([cx, cy+15, cx+25, cy+35], fill="black", width=2)
    # 腿
    draw.line([cx, cy+50, cx-15, cy+80], fill="black", width=2)
    draw.line([cx, cy+50, cx+15, cy+80], fill="black", width=2)
    
    # 带字版处理
    if mode == "with_title" and title:
        try:
            font_title = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", size=int(h * 0.06))
        except:
            font_title = ImageFont.load_default()
        
        # 文字区域
        tw, th = draw.textbbox((0, 0), title, font=font_title)[2:]
        tx, ty = int((w - tw) / 2), int(h * 0.08)
        
        # 白底文字背景
        draw.rectangle([tx-20, ty-10, tx+tw+20, ty+th+10], fill=(255, 255, 255, 240))
        draw.text((tx, ty), title, fill="black", font=font_title)
        
        result.convert("RGB").save("output/with_title.jpg", quality=95)
        print("✅ 带字版海报生成完成")
    
    # 无字版处理
    elif mode == "without_title":
        result.convert("RGB").save("output/without_title.jpg", quality=95)
        print("✅ 无字版海报生成完成")

if __name__ == "__main__":
    image_name = sys.argv[1]
    title = sys.argv[2] if len(sys.argv) > 2 else ""
    mode = sys.argv[3] if len(sys.argv) > 3 else "both"
    create_heytea_style_poster(image_name, title, mode)
