import streamlit as st
from PIL import Image
import numpy as np
from streamlit_image_coordinates import streamlit_image_coordinates

st.set_page_config(layout="wide")
st.title("専用 色違い生成ツール")

uploaded_file = st.file_uploader("ベース画像をアップロードしてください", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("👆 画像内の変更したい色をタップしてください")
        value = streamlit_image_coordinates(image, key="pil")

    if value is not None:
        x, y = value["x"], value["y"]
        img_array = np.array(image)
        target_color = img_array[y, x]
        
        hex_color = '#%02x%02x%02x' % tuple(target_color)
        
        with col2:
            st.write("抽出した色:")
            st.color_picker("元の色", hex_color, disabled=True)
            new_hex_color = st.color_picker("🎨 新しく塗る色を選んでください", "#0000FF")
            tolerance = st.slider("色の許容範囲（数値を上げると似た色もまとめて変更します）", 0, 100, 10)

            if st.button("色違いを生成する"):
                new_color = tuple(int(new_hex_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
                diff = np.abs(img_array.astype(int) - target_color.astype(int))
                mask = np.all(diff <= tolerance, axis=-1)
                
                result_array = img_array.copy()
                result_array[mask] = new_color
                
                result_image = Image.fromarray(result_array)
                st.success("完成！画像を長押しして保存してください。")
                st.image(result_image, use_container_width=True)
