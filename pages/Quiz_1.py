import cv2 as cv
import numpy as np
import streamlit as st
from PIL import Image


def translate(img, Tx, Ty, Bx_o, By_o):
    wdth = img.shape[1]
    hght = img.shape[0]
    Bx_n = Bx_o + Tx
    By_n = By_o + Ty
    m_translation = np.float32([
        [1, 0, Bx_n],
        [0, 1, By_n],
        [0, 0, 1]])
    translated_img = cv.warpPerspective(img, m_translation, (wdth, hght))
    return translated_img


def manipSingleImg():
    x_o_px = 0
    y_o_px = 0

    col1, col2 = st.columns(2)
    x_t_px = col1.number_input(
        "Pixels to translate on X-Axis?", value=0, step=1)
    y_t_px = col2.number_input(
        "Pixels to translate on Y-Axis?", value=0, step=1)
    img_file = st.file_uploader("Upload single image...")

    if img_file and x_t_px is not None and y_t_px is not None:
        img = Image.open(img_file)
        np_img = np.array(img)
        col1, col2 = st.columns(2)
        col1.markdown("Image Width: **" +
                      str(np_img.shape[1]) + "** px")
        col2.markdown("Image Height: **" +
                      str(np_img.shape[0]) + "** px")
        manip_img = translate(np_img, x_t_px, y_t_px, x_o_px, y_o_px)
        st.image(manip_img, channels="RGB")

        x_o_px = x_t_px
        y_o_px = y_t_px


def manipMultiImg():
    img_files = st.file_uploader(
        "Upload multiple images...", accept_multiple_files=True)

    t_step = st.number_input(
        "Translation step?", value=0)
    st.write("Translation step is added five times, resulting in five of the same images with compounding translation values.")
    st.write("---")

    cols1 = st.columns(2)
    x_o_px = cols1[0].number_input("X-Origin in pixels?", value=0)
    y_o_px = cols1[1].number_input("Y-Origin in pixels?", value=0)

    cols2 = st.columns(2)
    x_t_px = cols2[0].number_input(
        "Pixels to translate on X-Axis?", value=0)
    y_t_px = cols2[1].number_input(
        "Pixels to translate on Y-Axis?", value=0)

    if img_files is not None and t_step:
        for i in range(len(img_files)):
            img = Image.open(img_files[i])
            np_img = np.array(img)
            col1, col2 = st.columns(2)
            col1.markdown("Image Width: **" +
                          str(np_img.shape[1]) + "** px")
            col2.markdown("Image Height: **" +
                          str(np_img.shape[0]) + "** px")
            cols = st.columns(5)

            for j in range(5):
                manip_img = translate(
                    np_img, x_t_px, y_t_px, x_o_px, y_o_px)
                cols[j].image(manip_img, channels="RGB")
                x_o_px += t_step
                y_o_px += t_step
                x_t_px += t_step
                y_t_px += t_step

            x_o_px -= t_step * 5
            y_o_px -= t_step * 5
            x_t_px -= t_step * 5
            y_t_px -= t_step * 5


def main():
    st.write("# Quiz 1: Image Translation")
    img_manip = st.selectbox("Manipulate single or multiple images?", [
                             "Single", "Multiple"])

    if img_manip == "Single":
        manipSingleImg()
    else:
        manipMultiImg()


if __name__ == "__main__":
    main()
