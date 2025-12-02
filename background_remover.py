import io
import streamlit as st
from rembg import remove
from PIL import Image, ImageFilter, ImageEnhance


def add_shadow(fg, blur=25, offset=(20, 20), shadow_opacity=120):
    """전경 이미지에 그림자 생성"""
    # 전경 이미지 사이즈
    w, h = fg.size

    # 그림자 생성 (검은색 실루엣)
    shadow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    alpha = fg.split()[-1]  # 투명도 채널
    shadow.putalpha(alpha)

    # 그림자 색 진하게
    shadow = ImageEnhance.Brightness(shadow).enhance(0.0)  # 완전 검정색

    # 블러 적용
    shadow = shadow.filter(ImageFilter.GaussianBlur(blur))

    # 그림자 이동 적용된 캔버스
    shadow_canvas = Image.new("RGBA", (w + offset[0], h + offset[1]), (0, 0, 0, 0))
    shadow_canvas.paste(shadow, offset)

    return shadow_canvas


def overlay_image(background, foreground, scale, pos_x, pos_y, add_shadow_flag):
    """배경 위에 전경 이미지 합성"""
    bg = background.convert("RGBA")
    fg = foreground.convert("RGBA")

    # -------------------------
    # ① 전경 이미지 확대/축소
    # -------------------------
    new_width = int(fg.width * scale)
    new_height = int(fg.height * scale)
    fg = fg.resize((new_width, new_height), Image.LANCZOS)

    # 그림자 생성
    if add_shadow_flag:
        shadow = add_shadow(fg)
        # 배경에 그림자 먼저 붙여넣기
        shadow_x = pos_x - 20
        shadow_y = pos_y - 20
        bg.paste(shadow, (shadow_x, shadow_y), shadow)

    # -------------------------
    # ② 전경 이미지 위치 이동
    # -------------------------
    bg.paste(fg, (pos_x, pos_y), fg)

    return bg


# --------------------------
# Streamlit App
# --------------------------
def main():
    st.set_page_config(page_title="Background Replace Pro", page_icon="🪄")

    st.title("🪄 고급 배경제거 + 새 배경 합성기")
    st.write("전경 이미지 크기 조절, 위치 이동, 그림자 기능까지 완벽 지원!")

    fg_file = st.file_uploader("전경 이미지 업로드", type=["png", "jpg", "jpeg"])
    bg_file = st.file_uploader("배경 이미지 업로드", type=["png", "jpg", "jpeg"])

    # UI 세팅
    st.sidebar.title("⚙️ 이미지 조정 옵션")

    scale = st.sidebar.slider("전경 이미지 크기 조절", 0.1, 3.0, 1.0, 0.05)
    pos_x = st.sidebar.slider("X 위치 이동(좌/우)", -500, 500, 0, 5)
    pos_y = st.sidebar.slider("Y 위치 이동(상/하)", -500, 500, 0, 5)
    shadow_flag = st.sidebar.checkbox("그림자 자동 생성", value=True)

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

        # 사용자 위치 기준 보정 (배경 중심 기준)
        pos_x_adj = (bg_image.width - removed_fg.width) // 2 + pos_x
        pos_y_adj = (bg_image.height - removed_fg.height) // 2 + pos_y

        with st.spinner("이미지를 합성 중…"):
            result = overlay_image(
                bg_image, removed_fg, scale, pos_x_adj, pos_y_adj, shadow_flag
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
