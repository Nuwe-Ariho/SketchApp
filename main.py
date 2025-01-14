import flet as ft
import math

# my pandas
class Data_Frame(dict):
    def __init__(self,dt) -> None:
        if not isinstance(dt, dict):
            raise TypeError(f'The input is not a dictionary... Please input a dictionary.')
        self.data = dt

    # Method to display the DataFrame in a tabular format
    def __repr__(self):
        # Create a table-like string
        headers = list(self.data.keys())
        rows = zip(*[self.data[col] for col in headers])
        table = " | ".join(headers) + "\n"
        table += "-" * len(table) + "\n"
        for row in rows:
            table += " | ".join(str(item) for item in row) + "\n"
        return table

    #  validate row 
    def _validate_row(self,row):
        if row not in range(len(self.data[list(self.data.keys())[0]])):
            raise ValueError('The index provided is not present in the DataFrame...')
        
    #  validate col 
    def _validate_col(self,col):
        if col not in self.data.keys():
            raise ValueError('The column provided is not present in the DataFrame...')
        
    # Get value on the index provided.
    def loc(self,row,col):
        self._validate_row(row)
        self._validate_col(col)
        return self.data[col][row]
    
    # Update a value
    def update_loc(self, row, col, value):
        self.data[col][row] = value

    #  Returns the mean of a column selected.
    def mean(self,col):
        self._validate_col(col)
        column=self.data[col]
        return sum(column)/len(column)
    
    #  Returns the max value of a column selected.
    def max(self,col):
        self._validate_col(col)
        column=self.data[col]
        max_val = max(column)
        id = self.data[col].index(max(column))
        return id, max_val
    
    #  Returns the min value of a column selected.
    def min(self,col):
        self._validate_col(col)
        column=self.data[col]
        min_val = min(column)
        id = self.data[col].index(max(column))
        return id, min_val
    
    # Return shape of df
    def shape(self):
        rows= len(self.data[list(self.data.keys())[0]])
        cols= len(self.data.keys())
        return [rows, cols]
    
    #  Return true if any of the values in the column is true and above 1
    def any(self,col):
        self._validate_col(col)
        if self.shape()[0] == 0:
            raise IndexError('The DataFrame is empt...')
        
        check = ['True' if i > 0 else 'False' for i in self.data[col]]
        if check.__contains__('True'):
            return True
        else:
            return False
        
    #  Return true if all of the values in the column is true above 1
    def all(self,col):
        self._validate_col(col)
        if self.shape()[0] == 0:
            raise IndexError('The DataFrame is empt...')
        
        check = ['True' if i > 0 else 'False' for i in self.data[col]]
        if check.__contains__('False'):
            return False
        else:
            return True
        
    def add_data(self,dictionary:dict):
        if len(dictionary) != len(self.data.keys()):
            raise ValueError('The columns are not equal....')

        for i in dictionary:
            self.data[i].append(dictionary[i])
    
    def point_exists(self,x_cord:tuple):
        if not self.data.__contains__(x_cord[0]):
            raise ValueError(f'Column {x_cord[0]} doesnt exist...')
        if self.shape()[0] == 0:
            raise IndexError('The DataFrame is empty...')
        
        if x_cord[1] in self.data[x_cord[0]]:
            return True
        else:
            return False
        
    def delete_row(self,rows:list):
        for i in rows:
            self._validate_row(i)

            for j in range(len(list(self.data.values())[0])):
                if i == j:
                    for k in self.data.keys():
                        self.data[k].remove(self.data[k][j])
        return self

    def get_val_index(self,col,val):
        self._validate_col(col)

        ids = []
        for i,value in enumerate(self.data[col]):
            if value == val:
                ids.append(i)
        
        return ids
    
    def index(self):
        if self.shape()[0] == 0:
            raise IndexError('The DataFrame is empt...')
        
        return list(range(self.shape()[0]))
    
    def return_col(self,col):
        self._validate_col(col)

        return list(self.data[col])

# ======================


def main(page : ft.Page):
    page.title = 'This is a test app'

    page.bgcolor = '#205b7a'
    # page.bgcolor =  '#7ca4d9'
    page.padding = 10
    page.horizontal_alignment=ft.CrossAxisAlignment.CENTER 

    pts=Data_Frame(dt={'x':[100,100,200,200,150],'y':[100,200,200,100,50], 'state':[0,0,0,0,0]})
  
    def point_paint(state):
        if state == 1:
            return ft.Paint(stroke_width=9,color='purple' ,style=ft.PaintingStyle.STROKE,stroke_cap=ft.StrokeCap.ROUND)
        else:
            return ft.Paint(stroke_width=6,color='black' ,style=ft.PaintingStyle.FILL,stroke_cap=ft.StrokeCap.ROUND)
        
        
    cw=page.width-21
    ch=page.height*0.8

    offset_x, offset_y = 0, 0
    class Scale():
        scale = 1 # Stores current scale on every update
        scale_initial = 1 # Store the scale after a zooming action.
    scale = Scale.scale

    modify = False
    class Unit():
        selected_unit = 1

    selected_unit =Unit.selected_unit



    # ----------Canvas_Functions------------------Canvas_Functions-------------

    # Update the controls attribute of the canvas.
    def updt_controls(offset_x,offset_y,scale,draw=True):
        if draw:
            # Ensure dataframe has some points.
            if pts.shape()[0] == 0:
                return
            # point_features = [ft.canvas.Points(points=[ft.Offset((pts.loc(i,'x')+offset_x)*scale, (pts.loc(i,'y')+offset_y)*scale)],paint=point_paint(pts.loc(i,'state'))) for i in pts.index()]
            point_features = [ft.canvas.Points(points=[ft.Offset((pts.loc(i,'x')+offset_x)*scale, (pts.loc(i,'y')+offset_y)*scale)],paint=point_paint(pts.loc(i,'state'))) for i in pts.index()]

            # Get the Area, boundary and dimensions.
            Area_text = get_area(pts)
            boundary_features = get_boundary_and_dimensions(pts)

            # Combine point and path features
            features = boundary_features+ point_features+ Area_text
            return features
        else:
            return []

    # Capture the scale value after zooming - to be used later in the actual zooming action.
    def scale_initial(e:ft.ScaleEndEvent):
        Scale.scale_initial = Scale.scale

    # Handles zooming and panning.
    def pan_zoom(e: ft.ScaleUpdateEvent):
        nonlocal offset_x, offset_y, scale, modify
        # Ensure dataframe has some points.
        if pts.shape()[0] == 0:
            return
        
        # Panning starts here......
        if e.pointer_count == 1 and modify == False:
            # Panning every shape - here the scale helps to keep a constant panning movement even after zooming.
            offset_x += e.focal_point_delta_x/scale
            offset_y += e.focal_point_delta_y/scale

            # Update shapes with new pan position
            canvas.shapes = []
            canvas.shapes= updt_controls(offset_x, offset_y, scale)
            canvas.update()
            return
        
        elif e.pointer_count == 1 and modify == True:
            # Panning every active point - here the scale helps to keep a constant panning movement even after zooming.
            off_x, off_y = 0, 0
            off_x += e.focal_point_delta_x/scale
            off_y += e.focal_point_delta_y/scale

            # active = pts[pts['state']==1].index.values
            active = pts.get_val_index('state',1)

            for a in active:
                x_update = off_x + pts.loc(a,'x')
                y_update = off_y + pts.loc(a,'y')
                pts.update_loc(a,'x',x_update) 
                pts.update_loc(a,'y',y_update) 
            
            canvas.shapes = []
            canvas.shapes= updt_controls(offset_x, offset_y, scale)
            canvas.update()
            return
        
        # Zooming starts here by adjusting the scale variable.
        Scale.scale = e.scale * Scale.scale_initial 
        scale = Scale.scale

        canvas.shapes=[]
        canvas.shapes= updt_controls(offset_x, offset_y, scale)
        canvas.update()

    # Zoom extents function.
    def zoom_extents(e):
        nonlocal offset_x, offset_y
        # Ensure dataframe has some points.
        if pts.shape()[0] == 0:
            return
        
        center_x = pts.mean('x')
        center_y = pts.mean('y')

        offset_x = float((cw/scale)/2 - center_x)
        offset_y = float((ch/scale)/2 - center_y)
        
        canvas.shapes = []
        canvas.shapes= updt_controls(offset_x, offset_y, scale)
        canvas.update()

    # Selection function to activate a point.
    def select_point(e: ft.LongPressStartEvent ):
        nonlocal offset_x, offset_y, modify
        # Ensure dataframe has some points.
        # print(f'Are there any points: {pts.any('x')}')
        if pts.shape()[0] == 0:
            return
        
        search_x = e.local_x 
        search_y = e.local_y

        dists = list(map(lambda i: math.sqrt(((pts.loc(i,'x') + offset_x)*scale - search_x)**2 + ((pts.loc(i,'y') + offset_y)*scale - search_y)**2) ,  pts.index()))
        index = dists.index(min(dists))

        # To togle the state if its 0 then turn to 1 and vice versa.
        if pts.loc(index,'state') == 0:
            pts.update_loc(index,'state',1) 
        else:
            pts.update_loc(index,'state',0) 

        if pts.any('state'):
            modify = True
        
        # print(pts)
        # print(f'dists_index: {dists.to_list().index(dists.min())}, distance: {dists.min()}')
        # canvas.shapes.append(ft.canvas.Points(points=[ft.Offset((float(pts.loc(index,'x'])+offset_x)*scale, (float(pts.loc(index,'y'])+offset_y)*scale)],paint=point_paint2))
        canvas.shapes= updt_controls(offset_x, offset_y, scale)
        canvas.update()

    # delete points selected.
    def delete_point(e):
        nonlocal pts, modify
        # Ensure dataframe has some points.
        if pts.shape()[0] == 0:
            canvas.shapes=[]
            canvas.shapes= updt_controls(offset_x, offset_y, scale,draw=False)
            canvas.update()
            return
        
        del_index = pts.get_val_index('state',1)
        pts.delete_row(del_index)

        if pts.shape()[0] == 0:
            canvas.shapes=[]
            canvas.shapes= updt_controls(offset_x, offset_y, scale,draw=False)
            canvas.update()
            return
        
        # print(pts)
        modify = False
        canvas.shapes=[]
        canvas.shapes= updt_controls(offset_x, offset_y, scale)
        canvas.update()

    def add_point(e):
        nonlocal pts, modify
        # Ensure dataframe has some points.

        if pts.shape()[0] == 0:
            center_x = (cw/scale)/2
            center_y = (ch/scale)/2
        else:
            center_x = pts.mean('x')
            center_y = pts.mean('y')

        pts.add_data({'x':center_x,'y':center_y,'state':1})
        modify = True
        canvas.shapes=[]
        canvas.shapes= updt_controls(offset_x, offset_y, scale)
        canvas.update()


    # Reset some of the variales once the user taps the canvas.
    def revert(e: ft.TapEvent):
        nonlocal offset_x, offset_y, scale ,modify
        modify = False
        
        for i,value in enumerate(pts.data['state']):
            pts.update_loc(i,'state',0)

        
        canvas.shapes=[]
        canvas.shapes= updt_controls(offset_x, offset_y, scale)
        canvas.update()

    def update_units(e):
        nonlocal offset_x, offset_y, scale
        Unit.selected_unit = int(e.data)
        # Optionally: update canvas here
        canvas.shapes=[]
        canvas.shapes= updt_controls(offset_x, offset_y, scale)
        canvas.update()


    def convert_units(value):
        """
        Convert the given value to meters or feet based on the selected unit.
        """
        if Unit.selected_unit == 1:  # For meters
            return value / 10
        elif Unit.selected_unit == 0:  # For feet
            return value * 3.2808399 / 10

    def get_area(pts):
        """
        Calculate the area of the polygon formed by the points in the pts object.
        """
        if pts.shape()[0] < 3:
            return []
        x_cords = pts.data['x']
        y_cords = pts.data['y']

        n = len(x_cords)
        area = 0.0
        for i in range(n):
            j = (i + 1) % n
            area += x_cords[i] * y_cords[j]
            area -= y_cords[i] * x_cords[j]
        area = abs(area) / 2.0
        area = area / 100 # Converted to meters squared from pixels squared.

        center_x = pts.mean('x')
        center_y = pts.mean('y')

        Area_text = [ft.canvas.Text(x=(center_x+offset_x)*scale,y=(center_y+offset_y)*scale,text=f'{round(area/4046,3)} a',style=ft.TextStyle(size=15,decoration=ft.TextDecorationStyle.WAVY,decoration_color='blue'))]
        return Area_text
    

    def get_dimension_data(row,col1,col2):
        nonlocal offset_x, offset_y, scale
        if row+1 in pts.index():
            x0=pts.loc(row, col1)
            x1=pts.loc(row+1, col1)
            y0=pts.loc(row, col2)
            y1=pts.loc(row+1, col2)
        else:
            x0=pts.loc(row, col1)
            x1=pts.loc(0, col1)
            y0=pts.loc(row, col2)
            y1=pts.loc(0, col2)
        

        pos_x, pos_y = ((x1+x0)/2+offset_x)*scale , ((y1+y0)/2+offset_y)*scale
        dx = x1-x0+1
        dy = y1-y0+1
        orientation = math.atan(dy/dx)
        dist=round(convert_units(math.sqrt(dx**2+dy**2)), 2)
        return pos_x, pos_y, orientation, dist

    def get_boundary_and_dimensions(pts):
        nonlocal scale
        if pts.shape()[0] < 3:
            return []
    # Create a path feature by connecting the points
        boundary=[]
        dimensions = []
        boundary.append(ft.canvas.Path.MoveTo((int(pts.loc(0, 'x')) + offset_x) * scale, (int(pts.loc(0, 'y')) + offset_y) * scale)) 
        
        pos_x0, pos_y0, orientation0, dist0 = get_dimension_data(0,'x', 'y')
        dimensions.append(ft.canvas.Text(pos_x0,pos_y0,dist0,rotate=orientation0 ,style=ft.TextStyle(color='#edf2ff')))

        # Connect the points
        for i in pts.index()[1:]:  # Skip the first point since we've already moved there
            boundary.append(ft.canvas.Path.LineTo(
                (int(pts.loc(i, 'x')) + offset_x) * scale, 
                (int(pts.loc(i, 'y')) + offset_y) * scale
            ))

            pos_x1, pos_y1, orientation1, dist1 = get_dimension_data(i,'x', 'y')
            dimensions.append(ft.canvas.Text(pos_x1,pos_y1,dist1,rotate=orientation1,style=ft.TextStyle(color='#edf2ff')))
        
        boundary.append(ft.canvas.Path.Close())
        boundary_features = [ft.canvas.Path(boundary, 
                                            paint=ft.Paint(color=ft.colors.with_opacity(0.5, 'blue'), stroke_width=10, 
                                                        style=ft.PaintingStyle.FILL),
                                            ),
                            ] + dimensions
        
        return boundary_features





    canvas = ft.canvas.Canvas(updt_controls(0,0,1),
                              content=ft.GestureDetector(
                                                         drag_interval = 50,
                                                         on_scale_update = pan_zoom,
                                                         on_scale_end= scale_initial,
                                                         on_long_press_start= select_point,
                                                         on_tap= revert
                                                        )
                            )



    page.add(
        ft.Column(
            controls=[
                    ft.Container(content=ft.Text('Sketch App'),
                                 border=ft.border.all(1,'orange'),
                                 height=60,
                                 border_radius=5,padding=ft.Padding(0,20,0,10),
                                 alignment=ft.alignment.center,
                                 ink=True,
                                 on_click= lambda e: print(f'I have been clicked!\nahh event !{e}')
                                 ),
                    ft.Container(content=canvas,
                                border=ft.border.all(1,'orange'),
                                bgcolor='#a2bbcf',
                                border_radius=5,
                                expand=True,
                                width=page.width,
                                clip_behavior=ft.ClipBehavior.ANTI_ALIAS
                                ),
                    ft.Row(controls=[ # ADD_LOCATION, ADJUST
                                        ft.IconButton(icon=ft.icons.ADD_LOCATION_ALT_OUTLINED,
                                                      icon_size=35,
                                                      icon_color=ft.colors.GREEN_ACCENT_200,
                                                      on_click=add_point),
                                        ft.IconButton(icon=ft.icons.WRONG_LOCATION_OUTLINED,
                                                      icon_size=35,
                                                      icon_color=ft.colors.RED_ACCENT_200,
                                                      on_click=delete_point),
                                        ft.IconButton(icon=ft.icons.ZOOM_OUT_MAP_OUTLINED,
                                                      icon_size=35,
                                                      icon_color=ft.colors.GREEN_ACCENT_200,
                                                      on_click=zoom_extents),
                                        ft.CupertinoSlidingSegmentedButton(
                                                                            selected_index=selected_unit,
                                                                            thumb_color=ft.colors.BLUE_400,
                                                                            on_change= update_units,
                                                                            # padding=ft.padding.symmetric(0, 10),
                                                                            controls=[
                                                                                ft.Text("feet"),
                                                                                ft.Text("meters"),
                                                                            ],
                                                                        )
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                    )
                    ],
                    expand=True
                )
            )

ft.app(target=main)
