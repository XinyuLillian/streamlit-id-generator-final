
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import os
import datetime

# 设置文件保存路径（可以使用本地 CSV 文件记录 ID 与顺序）
SAVE_FILE = "id_no_log.csv"
IMAGE_PATH = "image.jpg"  # 你自己的图片名
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"  # 可替换为你自己的字体路径
FONT_SIZE = 48

# 初始化 log 文件
if not os.path.exists(SAVE_FILE):
    with open(SAVE_FILE, "w") as f:
        f.write("id,no,timestamp\n")

# 加载现有记录
def load_log():
    log = {}
    with open(SAVE_FILE, "r") as f:
        next(f)
        for line in f:
            id_, no, _ = line.strip().split(",")
            log[id_] = int(no)
    return log

# 保存新的记录
def save_log(user_id, no):
    timestamp = datetime.datetime.now().isoformat()
    with open(SAVE_FILE, "a") as f:
        f.write(f"{user_id},{no},{timestamp}\n")

# 主函数
def main():
    st.title("亲爱的小锹，生成你的专属表彰！")

    user_id = st.text_input("请输入你的 ID：")

    if user_id:
        log = load_log()

        if user_id in log:
            no = log[user_id]
        else:
            no = len(log) + 1
            save_log(user_id, no)

        st.success(f"你好，{user_id}！你的专属证书编号是：No. {no}")

        # 加载图片
        image = Image.open(IMAGE_PATH).convert("RGB")
        draw = ImageDraw.Draw(image)

        # 添加编号到图片上（可以根据需要调整坐标）
        try:
            font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
        except:
            font = ImageFont.load_default()

        text = f"No. {no}"
        text_position = (50, 50)  # 你可以改成图片中留出的区域坐标
        draw.text(text_position, text, fill="black", font=font)

        # 显示图片
        st.image(image, caption=f"含编号的图片：No. {no}", use_column_width=True)

        # 下载链接
        img_bytes = io.BytesIO()
        image.save(img_bytes, format='JPEG')
        img_bytes.seek(0)

        st.download_button(
            label="下载你的图片",
            data=img_bytes,
            file_name=f"Your_Image_No_{no}.jpg",
            mime="image/jpeg"
        )

if __name__ == "__main__":
    main()
