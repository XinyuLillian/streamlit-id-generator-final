import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import os
import datetime

# 配置路径
SAVE_FILE = "id_no_log.csv"
IMAGE_PATH = "image.jpg"  # 替换成你实际的图片名

# 字体路径（放到项目文件夹内）
FONT_PATH_NO = "Blackbox.ttf"            # Blackbox字体文件
FONT_PATH_ID = "SourceHanSerifCN-Regular-1.otf"    # 思源宋体字体文件

FONT_SIZE_NO = 48
FONT_SIZE_ID = 60

# 初始化日志
if not os.path.exists(SAVE_FILE):
    with open(SAVE_FILE, "w") as f:
        f.write("id,no,timestamp\n")

def load_log():
    log = {}
    with open(SAVE_FILE, "r") as f:
        next(f)
        for line in f:
            id_, no, _ = line.strip().split(",")
            log[id_] = int(no)
    return log

def save_log(user_id, no):
    timestamp = datetime.datetime.now().isoformat()
    with open(SAVE_FILE, "a") as f:
        f.write(f"{user_id},{no},{timestamp}\n")

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

        # 打开图片
        image = Image.open(IMAGE_PATH).convert("RGB")
        draw = ImageDraw.Draw(image)

        # 加载字体
        try:
            font_no = ImageFont.truetype(FONT_PATH_NO, FONT_SIZE_NO)
            font_id = ImageFont.truetype(FONT_PATH_ID, FONT_SIZE_ID)
        except Exception as e:
            st.warning(f"⚠️ 自定义字体加载失败，将使用默认字体。\n错误信息：{e}")
            font_no = ImageFont.load_default()
            font_id = ImageFont.load_default()

        # 画 NO.
        text_no = f"No. {no}"
        position_no = (30, 20)  # 向右下角移动
        draw.text(position_no, text_no, fill="white", font=font_no)

        # 画 ID
        position_id = (850, 1870)  # 你可以再调这个位置
        draw.text(position_id, user_id, fill=(255, 0, 250), font=font_id)

        # 显示和下载
        st.image(image, caption=f"已生成编号：No. {no}", use_container_width=True)

        img_bytes = io.BytesIO()
        image.save(img_bytes, format='JPEG')
        img_bytes.seek(0)

        st.download_button(
            label="下载你的表彰图片",
            data=img_bytes,
            file_name=f"Your_Image_No_{no}.jpg",
            mime="image/jpeg"
        )

if __name__ == "__main__":
    main()
