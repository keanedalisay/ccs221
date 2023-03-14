import cv2 as cv
import numpy as np
import streamlit as st

from PIL import Image


def translate(img, x, y):
    wdth = img.shape[1]
    hght = img.shape[0]

    m_translation = np.float32([
        [1, 0, x],
        [0, 1, y],
        [0, 0, 1]])

    translated_img = cv.warpPerspective(
        img, m_translation, (wdth, hght))
    return translated_img


def rotate(img, angle):

    wdth = img.shape[1]
    hght = img.shape[0]

    m_translation = cv.getRotationMatrix2D((wdth / 2, hght / 2), angle, 1)
    rotated_img = cv.warpAffine(
        img, m_translation, (wdth, hght))

    return rotated_img


def scale(img, scale_wdth, scale_hght):
    wdth = img.shape[1]
    hght = img.shape[0]

    m_scaling = np.float32([
        [scale_wdth, 0, 0],
        [0, scale_hght, 0],
        [0, 0, 1]])

    scaled_img = cv.warpPerspective(
        img, m_scaling, (wdth, hght))
    return scaled_img


def resize(img, resize_wdth, resize_hght):

    resized_img = cv.resize(
        img, (resize_wdth, resize_hght), interpolation=cv.INTER_AREA)
    return resized_img


def reflection(img, reflect_hoz, reflect_ver):
    wdth = img.shape[1]
    hght = img.shape[0]

    rflt_hoz_val = -1 if reflect_hoz else 1
    rflt_ver_val = -1 if reflect_ver else 1

    m_reflection_ = np.float32([
        [rflt_hoz_val, 0, wdth],
        [0, rflt_ver_val, hght],
        [0, 0, 1]])

    reflected_image = cv.warpPerspective(
        img, m_reflection_, (wdth * 2, hght * 2))

    return reflected_image


def skew(img, skew_hoz, skew_ver):
    wdth = img.shape[1]
    hght = img.shape[0]

    m_skewing = np.float32([
        [1, skew_hoz, 0],
        [skew_ver, 1, 0],
        [0, 0, 1]])

    skewed_img = cv.warpPerspective(
        img, m_skewing, (wdth, hght))

    return skewed_img


def main():

    st.write("# Activity 3: 2D Image Transformation")

    img_trnsfm = st.selectbox("Transform image/s with?", [
        "Translate", "Rotate", "Scale", "Resize", "Reflection", "Skew"])

    img_files = st.file_uploader(
        "Upload image/s", accept_multiple_files=True)

    col1, col2 = st.columns(2)
    if img_trnsfm == "Translate":
        x = col1.number_input('Pixels to translate horizontally?')
        y = col2.number_input('Pixels to translate vertically?')
    elif img_trnsfm == "Rotate":
        angle = st.number_input('Angle to rotate image? ')
    elif img_trnsfm == "Scale":
        scale_wdth = col1.number_input(
            "Scale percentage of width?", value=1.00)
        scale_hght = col2.number_input(
            "Scale percentage of height?", value=1.00)
    elif img_trnsfm == "Resize":
        resize_wdth = col1.number_input(
            'Pixels to resize image width?', value=100)
        resize_hght = col2.number_input(
            'Pixels to resize image height?', value=100)
    elif img_trnsfm == "Reflection":
        reflect_hoz = col1.checkbox("Flip image horizintally?", value=False)
        reflect_ver = col2.checkbox("Flip image vertically?", value=False)
    elif img_trnsfm == "Skew":
        skew_hoz = col1.number_input("Percentage to skew horizontally?")
        skew_ver = col2.number_input("Percentage to skew vertically?")

    if img_files is not None and len(img_files) > 0:
        cols = st.columns(len(img_files))

        for i in range(len(img_files)):
            img = Image.open(img_files[i])
            np_img = np.array(img)

            cols[i].markdown("Image Width: **" +
                             str(np_img.shape[1]) + "** px")
            cols[i].markdown("Image Height: **" +
                             str(np_img.shape[0]) + "** px")

            if img_trnsfm == "Translate":
                cols[i].image(translate(np_img, x, y))
            elif img_trnsfm == "Rotate":
                cols[i].image(rotate(np_img, angle))
            elif img_trnsfm == "Scale":
                cols[i].image(scale(np_img, scale_wdth, scale_hght))
            elif img_trnsfm == "Resize":
                cols[i].image(resize(np_img, resize_wdth, resize_hght))
            elif img_trnsfm == "Reflection":
                cols[i].image(reflection(np_img, reflect_hoz, reflect_ver))
            elif img_trnsfm == "Skew":
                cols[i].image(skew(np_img, skew_hoz, skew_ver))


if __name__ == '__main__':
    main()
