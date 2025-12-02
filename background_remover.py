import io
import streamlit as st
from rembg import remove
from PIL import Image

def overlay_image(background, foreground):
    """배경 이미지 위에 전경 이미지를 중앙에 합성"""
    bg = background.convert("RGBA")
    fg = foreground.convert("RGBA")

    # 전경 이미지를 배경 크기에 맞게 비율 유지하며 축소
    fg.thumbnail((bg.width, bg.height), Image.LANCZOS)

    # 합성 위치(중앙)
    x = (bg.width - fg.width) // 2
    y = (bg.height - fg.height) // 2

    bg.paste(fg, (x, y), fg)
    return bg

def main():
    st.set_page_config(
        page_title="Image Background Remover + Replacer",
        page_icon="🪄",
        layout="centered"
    )

    st.title("🪄 배경 제거 + 새 배경 합성기")

    st.write("두 가지 이미지를 업로드하세요.")
    st.write("- **전경 이미지**: 배경을 제거할 인물/제품 사진")
    st.write("- **배경 이미지**: 삽입하고 싶은 새 배경")

    # -----------------------------
    # ① 전경 이미지 업로드 (배경 제거)
    # -----------------------------
    fg_file = st.file_uploader(
        "전경 이미지 업로드 (PNG/JPG/JPEG)",
        type=["png", "jpg", "jpeg"],
        key="fg"
    )

    # -----------------------------
    # ② 배경 이미지 업로드
    # -----------------------------
    bg_file = st.file_uploader(
        "배경 이미지 업로드 (PNG/JPG/JPEG)",
        type=["png", "jpg", "jpeg"],
        key="bg"
    )

    if fg_file:
        fg_image = Image.open(fg_file).convert("RGBA")
        st.subheader("전경 원본 이미지")
        st.image(fg_image, use_column_width=True)

        with st.spinner("배경 제거 중…"):
            removed_fg = remove(fg_image)

        st.subheader("배경제거 결과")
        st.image(removed_fg, use_column_width=True)

    # -------------------------------------
    # ③ 두 이미지가 모두 업로드되면 합성 실행
    # -------------------------------------
    if fg_file and bg_file:
        bg_image = Image.open(bg_file).convert("RGBA")
        st.subheader("배경 이미지")
        st.image(bg_image, use_column_width=True)

        with st.spinner("새 배경에 합성 중…"):
            result = overlay_image(bg_image, removed_fg)

        st.subheader("합성 결과")
        st.image(result, use_column_width=True)

        # 다운로드
        buffer = io.BytesIO()
        result.save(buffer, format="PNG")
        result_bytes = buffer.getvalue()

        st.download_button(
            label="🎉 합성된 이미지 다운로드 (PNG)",
            data=result_bytes,
            file_name="merged_result.png",
            mime="image/png"
        )

if __name__ == "__main__":
    main()
