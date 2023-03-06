import streamlit as st
import matplotlib.pyplot as plt

class LineTemp:

  def __init__(self, x1, y1, x2, y2):
    self.strt_pnt = [x1, y1]
    self.end_pnt = [x2, y2]


  def dda(self):
    fig, ax = plt.subplots()
    fig.suptitle('Digital Differential Analyzer')
    ax.set_xlabel('X-Axis')
    ax.set_ylabel('Y-Axis')

    strt_x = self.strt_pnt[0]
    strt_y = self.strt_pnt[1]

    dx = abs(self.end_pnt[0] - strt_x) 
    dy = abs(self.end_pnt[1] - strt_y) 

    steps = dx if dx >= dy else dy
   
    x_inc = float(dx / steps)
    y_inc = float(dy / steps)

    x_data = []
    y_data = []

    for i in range(steps):
      x_data.append(strt_x)
      y_data.append(strt_y)

      strt_x += x_inc
      strt_y += y_inc

    ax.plot(x_data, y_data, color='blue', linestyle='solid')

    midpoint_x = (self.strt_pnt[0] + self.end_pnt[0]) / 2
    midpoint_y = (self.strt_pnt[1] + self.end_pnt[1]) / 2

    ax.plot(midpoint_x, midpoint_y, color='green', marker='*')
    return fig  
  


  def bresenhams(self):
    fig, ax = plt.subplots()
    fig.suptitle('Bresenham\'s')
    ax.set_xlabel('X-Axis')
    ax.set_ylabel('Y-Axis')

    strt_x = self.strt_pnt[0] 
    strt_y = self.strt_pnt[1]

    dx = self.end_pnt[0] - strt_x 
    dy = self.end_pnt[1] - strt_y 

    decision = (2 * dy) - dx 

    x_data = []
    y_data = []
    
    while(strt_x <= self.end_pnt[0]):
      x_data.append(strt_x)
      y_data.append(strt_y)
      strt_x += 1

      if decision < 0: 
        decision = decision + (2 * dy) 
      else:
        decision = decision + (2 * dy) - (2 * dx) 
        strt_y += 1 

    ax.plot(x_data, y_data, color='red', linestyle='solid')
    
    midpoint_x = (self.strt_pnt[0] + self.end_pnt[0]) / 2
    midpoint_y = (self.strt_pnt[1] + self.end_pnt[1]) / 2

    ax.plot(midpoint_x, midpoint_y, color='green', marker='*')

    return fig  
  

  def midpoint(self):
    fig, ax = plt.subplots()
    fig.suptitle('Midpoint')
    ax.set_xlabel('X-Axis')
    ax.set_ylabel('Y-Axis')

    strt_x = self.strt_pnt[0]
    strt_y = self.strt_pnt[1]

    dx = self.end_pnt[0] - strt_x 
    dy = self.end_pnt[1] - strt_y 

    decision = (2 * dy) - dx 

    x_data = []
    y_data = []

    while(strt_x <= self.end_pnt[0]):
      x_data.append(strt_x)
      y_data.append(strt_y)
      strt_x += 1

      if decision < 0: 
        decision = decision + (2 * dy) 
      else:
        decision = decision + 2 * (dy - dx) 
        strt_y += 1 
    
    
    ax.plot(x_data, y_data, color='yellow', linestyle='solid')

    midpoint_x = (self.strt_pnt[0] + self.end_pnt[0]) / 2
    midpoint_y = (self.strt_pnt[1] + self.end_pnt[1]) / 2
    ax.plot(midpoint_x, midpoint_y, color='green', marker='*')

    return fig
  
def main():
  st.title('Create A Line')
  col1, col2 = st.columns(2)
  figure = False

  with col1:
    strt_x = st.number_input('Start X-Coordinate: ', min_value=0, value=0)
    strt_y = st.number_input('Start Y-Coordinate: ', min_value=0, value=0)

    end_x = st.number_input('End X-Coordinate: ', min_value=0, value=5)
    end_y = st.number_input('End Y-Coordinate: ', min_value=0, value=5)

    line = LineTemp(strt_x, strt_y, end_x, end_y)

    algo = st.selectbox('Algorithm to plot line...', ('Digital Differential Analyzer', 'Bresenham\'s', 'Midpoint'))

    if (algo == 'Digital Differential Analyzer'):
      figure = line.dda()
      with col2:
       st.pyplot(figure)
    elif (algo == 'Bresenham\'s'):
      figure = line.bresenhams()
      with col2:
       st.pyplot(figure)
    elif (algo == 'Midpoint'):
      figure = line.midpoint()
      with col2:
       st.pyplot(figure)

if __name__ == '__main__':
  main()
