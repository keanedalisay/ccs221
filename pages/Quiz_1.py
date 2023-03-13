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
    translated_img = cv.warpPerspective(img, m_translation, (wdth,
                                                             hght))
    return translated_img


# def translateImages(imgs):
#     orig_img = cv.imread(imgs[0])
#     cv.imshow('Original Image', orig_img)
#     cv.waitKey(0)
#     orig_img_wdth = orig_img.shape[1]
#     orig_img_hght = orig_img.shape[0]
#     comb_img = orig_img
#     Bx = 20
#     By = 50
#     Tx = 60
#     Ty = 70
#     for i in range(len(imgs)):
#         trgt_img = cv.imread(imgs[i])
#         manip_img = translate(trgt_img, Bx, By, Tx, Ty)
#         cv.imshow("Manipulated Image", manip_img)
#         cv.waitKey(0)
#         Bx += 25
#         By += 25
#         Tx += 25
#         Ty += 25
#         resized_img = cv.resize(manip_img,
#                                 (orig_img_wdth, orig_img_hght),
#                                 interpolation=cv.INTER_AREA)
#         comb_img = np.concatenate((comb_img, resized_img), axis=1)

#     cv.imshow("Manipualted Images", comb_img)
#     cv.waitKey(0)


def main():
    st.write("# Quiz 1: Image Translation")
    img_manip = st.selectbox("Manipulate single or multiple images", [
                             "Single", "Multiple"])

    x_o_px = 0
    y_o_px = 0

    if img_manip == "Single":
        col1, col2 = st.columns(2)
        x_t_px = col1.number_input(
            "Pixels to translate on X-Axis", value=0, step=1)
        y_t_px = col2.number_input(
            "Pixels to translate on Y-Axis", value=0, step=1)
        img_file = st.file_uploader("Upload single image")

        if img_file and x_t_px is not None and y_t_px is not None:
            img = Image.open(img_file)
            np_img = np.array(img)
            manip_img = translate(np_img, x_t_px, y_t_px, x_o_px, y_o_px)
            st.image(manip_img, channels="RGB")

            x_o_px = x_t_px
            y_o_px = y_t_px

    else:
        pass


if __name__ == "__main__":
    main()
