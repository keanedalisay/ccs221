import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import streamlit as st

class createPolygon:
    def __init__(self, max_range, rows, columns):
        self.two_d_arr = np.random.randint(max_range, size=(rows, columns))
        self.max_clr_rng = max_range

    def boundaryFill(self, row, column, border_color):
        arr_dim = self.two_d_arr.shape
        if  row >= arr_dim[0] or  row < 0 : return
        if  column >= arr_dim[1] or column < 0: return

        value = self.two_d_arr[row][column]
        if value == border_color: return

        self.two_d_arr[row][column] = border_color

        self.boundaryFill(row - 1, column, border_color) # top
        self.boundaryFill(row, column + 1, border_color) # right
        self.boundaryFill(row + 1, column, border_color)# bottom 
        self.boundaryFill(row, column - 1, border_color) # left
        return

    def floodFill(self, row, column, target_color, replcmnt_color):
        arr_dim = self.two_d_arr.shape
        if  row >= arr_dim[0] or  row < 0 : return
        if  column >= arr_dim[1] or column < 0: return

        value = self.two_d_arr[row][column]
        if value == target_color: 
            self.two_d_arr[row][column] = replcmnt_color
            self.floodFill(row, column - 1, target_color, replcmnt_color)
            self.floodFill(row + 1, column, target_color, replcmnt_color)
            self.floodFill(row, column + 1, target_color, replcmnt_color)
            self.floodFill(row - 1, column, target_color, replcmnt_color)
            
        return

    def displayPolygon(self, label, elem):
        fig, ax = plt.subplots()
        fig.suptitle(label)
        ax.set_xlabel('X-Axis')
        ax.set_ylabel('Y-Axis')

        norm = mpl.colors.Normalize(0, self.max_clr_rng)

        fig.colorbar(mpl.cm.ScalarMappable(norm = norm, cmap='gist_rainbow'))
        ax.imshow(self.two_d_arr, interpolation='none', cmap='gist_rainbow')
        elem.pyplot(fig)

def main():

    st.write('# Activity 2: Fill Algorithms')
    col1, col2 = st.columns(2)
    rows = col1.number_input('Number of rows', min_value = 3, value = 10)
    columns = col2.number_input('Number of columns', min_value = 3, value = 10)
    max_range = st.number_input('Max value range to fill polygon', min_value = 1, value = 2)
    poly = createPolygon(max_range, rows, columns)

    col1.metric('Width', value = poly.two_d_arr.shape[0])
    col2.metric('Height', value = poly.two_d_arr.shape[1])
    algo = st.selectbox('Fill algorithm to use', options = ('Boundary', 'Flood'))
    
    frm = st.form('fill_config')
    col3, col4 = frm.columns(2)
    row = col3.number_input('Row to start filling', min_value = 0)
    column = col4.number_input('Column to start filling', min_value = 0)

    col5, col6 = st.columns(2)
    if algo == 'Boundary':
        border_color = frm.number_input('Border color (as integer) to lookout', min_value = 0)
        poly.displayPolygon('Before fill...', col5)
        poly.boundaryFill(row, column, border_color)
    elif algo == 'Flood':
        target_color = col3.number_input('Target color (as integer) to replace', min_value = 0)
        replcmnt_color = col4.number_input('Replacement color (as integer)', min_value = 0)
        poly.displayPolygon('Before fill...', col5)
        poly.floodFill(row, column, target_color, replcmnt_color)
  
    submit = frm.form_submit_button('Run')
    if submit:
        poly.displayPolygon('After fill...', col6)

if __name__ == '__main__':
  main()
