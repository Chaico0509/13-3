import io

import streamlit as st
from rembg import remove
from PIL import Image


def main():
    st.set_page_config(
        page_title="Image Background Remover",
        page_icon="🪄",
        layout="centered"
    )

    st.title("🪄 Image Background Remover")
    st.write(
        "이미지를 업로드하면 **배경을 자동으로 제거**하고, "
        "배경이 투명한 PNG 파일로 다운로드할 수 있습니다."
    )

    uploaded_file = st.file_uploader(
        "이미지를 업로드하세요 (PNG / JPG / JPEG)",
        type=["png", "jpg", "jpeg"]
    )

    if uploaded_file is not None:
        # 원본 이미지 표시
        input_image = Image.open(uploaded_file).convert("RGBA")
        st.subheader("원본 이미지")
        st.image(input_image, use_column_width=True)

        with st.spinner("배경 제거 중입니다. 잠시만 기다려주세요..."):
            # rembg로 배경 제거 (PIL 이미지를 직접 넘길 수 있음)
            output_image = remove(input_image)

        st.subheader("배경 제거 결과")
        st.image(output_image, use_column_width=True)

        # 다운로드용 버퍼에 PNG로 저장
        buf = io.BytesIO()
        output_image.save(buf, format="PNG")
        byte_im = buf.getvalue()

        st.download_button(
            label="배경 제거된 이미지 다운로드 (PNG)",
            data=byte_im,
            file_name="output_no_bg.png",
            mime="image/png"
        )

        st.info(
            "결과 이미지는 **투명 배경의 PNG** 형식입니다. "
            "PPT, 문서, 썸네일 제작 등에 바로 활용할 수 있습니다."
        )


if __name__ == "__main__":
    main()
