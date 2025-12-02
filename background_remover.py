import io
import streamlit as st
from rembg import remove
from PIL import Image


def overlay_image(background, foreground, scale, pos_x, pos_y):
    """배경 위에 전경 이미지 합성"""
    bg = background.convert("RGBA")
    fg = foreground.convert("RGBA")

    # 전경 이미지 확대/축소
    new_width = int(fg.width * scale)
    new_height = int(fg.height * scale)
    fg = fg.resize((new_width, new_height), Image.LANCZOS)

    # 전경 이미지 위치 이동
    bg.paste(fg, (pos_x, pos_y), fg)

    return bg


# --------------------------
# Streamlit App
# --------------------------
def main():
    st.set_page_config(page_title="Background Replace Pro", page_icon="🪄")

    st.title("🪄 내맘대로 이미지를 합성해보자!")
    st.write("이미지 크기 조절과 위치 이동이 가능해요.")

    fg_file = st.file_uploader("전경 이미지 업로드", type=["png", "jpg", "jpeg"])
    bg_file = st.file_uploader("배경 이미지 업로드", type=["png", "jpg", "jpeg"])

    # UI 세팅
    st.sidebar.title("⚙️ 이미지 조정 옵션")

    scale = st.sidebar.slider("전경 이미지 크기 조절 (작게 ↔ 크게)", 0.1, 3.0, 1.0, 0.05)

    # 직관적인 위치 이동 슬라이더
    pos_x = st.sidebar.slider("좌우 이동 (← 왼쪽 / 오른쪽 →)", -500, 500, 0, 5)
    pos_y = st.sidebar.slider("상하 이동 (↑ 위 / 아래 ↓)", -500, 500, 0, 5)

    if fg_file:
        fg_image = Image.open(fg_file).convert("RGBA")
        st.subheader("전경 원본")
        st.image(fg_image)

        with st.spinner("배경 제거 중…"):
            removed_fg = remove(fg_image)

        st.subheader("배경제거 결과")
        st.image(removed_fg)

    if fg_file and bg_file:
        bg_image = Image.open(bg_file).convert("RGBA").copy()

        st.subheader("배경 이미지")
        st.image(bg_image)

        st.subheader("🧩 합성 결과")

        # 중앙 기준 + 사용자 조정값 적용
        pos_x_adj = (bg_image.width - removed_fg.width) // 2 + pos_x
        pos_y_adj = (bg_image.height - removed_fg.height) // 2 + pos_y

        with st.spinner("이미지를 합성 중…"):
            result = overlay_image(
                bg_image, removed_fg, scale, pos_x_adj, pos_y_adj
            )

        st.image(result, use_column_width=True)

        # 다운로드
        buf = io.BytesIO()
        result.save(buf, format="PNG")
        st.download_button(
            label="🎉 합성 이미지 다운로드",
            data=buf.getvalue(),
            file_name="result.png",
            mime="image/png"
        )


if __name__ == "__main__":
    main()
