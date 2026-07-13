python
import sys
import os
import io
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import rembg

def create_heytea_poster(image_path, title=""):
    os.makedirs("output", exist_ok=True)
    
    original = Image.open(f"input/{image_path}").convert("RGBA")
    w, h = original.size
    
    # 抠图
    with open(f"input/{image_path}", "rb") as f:
        input_bytes = f.read()
    output_bytes = rembg.remove(input_bytes)
    subject = Image.open(io.BytesIO(output_bytes)).convert("RGBA")
    subject = subject.resize((w, h))
    
    # 背景虚化 + 暖色调
    background = original.filter(ImageFilter.GaussianBlur(radius=15))
    overlay = Image.new("RGBA", (w, h), (255, 200, 150, 80))
    background = Image.alpha_composite(background, overlay)
    
    # 合成
    result = Image.alpha_composite(background, subject)
    
    # 手写风字体（尝试系统字体，没有则用默认）
    try:
        font_title = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", size=int(h * 0.06))
        font_doodle = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", size=int(h * 0.03))
    except:
        font_title = ImageFont.load_default()
        font_doodle = ImageFont.load_default()
    
    draw = ImageDraw.Draw(result)
    
    # 涂鸦小人
    cx, cy = int(w * 0.85), int(h * 0.75)
    draw.ellipse([cx-20, cy-40, cx+20, cy], fill=None, outline="black", width=3)
    draw.ellipse([cx-8, cy-28, cx-4, cy-24], fill="black")
    draw.ellipse([cx+4, cy-28, cx+8, cy-24], fill="black")
    draw.arc([cx-8, cy-18, cx+8, cy-8], start=0, end=180, fill="black", width=2)
    draw.line([cx, cy, cx, cy+50], fill="black", width=3)
    draw.line([cx, cy+15, cx-25, cy+35], fill="black", width=2)
    draw.line([cx, cy+15, cx+25, cy+35], fill="black", width=2)
    draw.line([cx, cy+50, cx-15, cy+80], fill="black", width=2)
    draw.line([cx, cy+50, cx+15, cy+80], fill="black", width=2)
    
    # 星星
    star_positions = [(int(w*0.1), int(h*0.2)), (int(w*0.3), int(h*0.85)), (int(w*0.75), int(h*0.15))]
    for sx, sy in star_positions:
        draw.text((sx, sy), "★", fill="black", font=font_doodle)
    
    # 标题
    if title:
        tw, th = draw.textbbox((0, 0), title, font=font_title)[2:]
        tx, ty = int((w - tw) / 2), int(h * 0.08)
        draw.rectangle([tx-20, ty-10, tx+tw+20, ty+th+10], fill=(255, 255, 255, 200))
        draw.text((tx, ty), title, fill="black", font=font_title)
    
    result.convert("RGB").save("output/with_title.jpg", quality=95)
    
    # 不带标题版（复制涂鸦）
    result_no = Image.alpha_composite(background, subject)
    draw2 = ImageDraw.Draw(result_no)
    draw2.ellipse([cx-20, cy-40, cx+20, cy], fill=None, outline="black", width=3)
    draw2.ellipse([cx-8, cy-28, cx-4, cy-24], fill="black")
    draw2.ellipse([cx+4, cy-28, cx+8, cy-24], fill="black")
    draw2.arc([cx-8, cy-18, cx+8, cy-8], start=0, end=180, fill="black", width=2)
    draw2.line([cx, cy, cx, cy+50], fill="black", width=3)
    draw2.line([cx, cy+15, cx-25, cy+35], fill="black", width=2)
    draw2.line([cx, cy+15, cx+25, cy+35], fill="black", width=2)
    draw2.line([cx, cy+50, cx-15, cy+80], fill="black", width=2)
    draw2.line([cx, cy+50, cx+15, cy+80], fill="black", width=2)
    for sx, sy in star_positions:
        draw2.text((sx, sy), "★", fill="black", font=font_doodle)
    result_no.convert("RGB").save("output/without_title.jpg", quality=95)
    
    print("✅ 海报生成完成！")
    print(f"  - 带标题版: output/with_title.jpg")
    print(f"  - 不带标题版: output/without_title.jpg")

if __name__ == "__main__":
    image_name = sys.argv[1] if len(sys.argv) > 1 else "photo.jpg"
    title = sys.argv[2] if len(sys.argv) > 2 else ""
    create_heytea_poster(image_name, title)
