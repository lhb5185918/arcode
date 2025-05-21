import arcade

def draw_coordinate_system(width, height, mouse_x=0, mouse_y=0, grid_spacing=50):
    """
    绘制坐标轴、网格和鼠标位置
    
    参数:
        width (int): 屏幕宽度
        height (int): 屏幕高度
        mouse_x (int): 鼠标X坐标
        mouse_y (int): 鼠标Y坐标
        grid_spacing (int): 网格间距
    """
    # 绘制网格线
    for x in range(0, width + 1, grid_spacing):
        arcade.draw_line(x, 0, x, height, arcade.color.GRAY, 1)
        arcade.draw_text(
            str(x), 
            start_x=x, start_y=10, 
            color=arcade.color.RED, 
            font_size=10
        )
    
    for y in range(0, height + 1, grid_spacing):
        arcade.draw_line(0, y, width, y, arcade.color.GRAY, 1)
        arcade.draw_text(
            str(y), 
            start_x=10, start_y=y, 
            color=arcade.color.RED, 
            font_size=10
        )
    
    # 在主要的坐标轴上使用更粗的线
    arcade.draw_line(0, 0, width, 0, arcade.color.RED, 2)  # X轴
    arcade.draw_line(0, 0, 0, height, arcade.color.GREEN, 2)  # Y轴
    
    # 绘制当前鼠标位置
    arcade.draw_circle_filled(mouse_x, mouse_y, 5, arcade.color.YELLOW)
    
    # 为鼠标坐标文本添加背景
    text = f"X: {mouse_x}, Y: {mouse_y}"
    text_width = len(text) * 8  # 估计文本宽度
    arcade.draw_rectangle_filled(
        mouse_x + 10 + text_width/2, 
        mouse_y + 10 + 8, 
        text_width, 20, 
        (0, 0, 0, 150)
    )
    
    # 显示鼠标坐标
    arcade.draw_text(
        text, 
        start_x=mouse_x + 10, 
        start_y=mouse_y + 10, 
        color=arcade.color.WHITE, 
        font_size=12
    ) 