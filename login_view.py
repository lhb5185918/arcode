import arcade
import arcade.gui
import random
import math
# 删除以下导入，因为它们可能在导入时创建窗口
# from enhanced_game import EnhancedChildhoodRoom
# from interactive_room_game import ChildhoodRoom, SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE
# 只导入必要的常量
from interactive_room_game import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE
from bedroom_view import BedroomView

# 定义一个随机颜色生成函数，替代arcade.color.random_color()
def random_color():
    """生成随机RGB颜色"""
    return (
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255)
    )

# 定义90后经典的亮色调
NINETIES_COLORS = [
    (255, 105, 180),  # 热粉红
    (50, 205, 50),    # 浅绿
    (255, 165, 0),    # 橙色
    (106, 90, 205),   # 石板蓝
    (255, 215, 0),    # 金色
    (0, 191, 255),    # 深天蓝
    (138, 43, 226),   # 紫罗兰
    (255, 69, 0),     # 橙红色
    (30, 144, 255),   # 道奇蓝
    (50, 205, 50)     # 石灰绿
]

class LoginView(arcade.View):
    """游戏登录页视图"""
    
    def __init__(self):
        super().__init__()
        
        # 设置背景颜色
        arcade.set_background_color(arcade.color.LIGHT_BLUE)
        
        # 创建一些动画元素
        self.stars = []
        for _ in range(50):
            self.stars.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT),
                'size': random.uniform(1, 3),
                'speed': random.uniform(0.5, 2)
            })
        
        # 创建动画计时器
        self.total_time = 0.0
        
        # 创建UI管理器
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        
        # 创建一个垂直布局容器
        self.v_box = arcade.gui.UIBoxLayout()
        
        # 添加标题标签
        title_label = arcade.gui.UILabel(
            text="90后童年互动房间",
            font_size=40,
            width=500,
            align="center"
        )
        self.v_box.add(title_label.with_space_around(bottom=30))
        
        # 创建一个装饰性分隔线
        line_box = arcade.gui.UIBoxLayout(vertical=False)
        for i in range(10):
            color = NINETIES_COLORS[i]
            line = arcade.gui.UILabel(
                text="●",
                width=40,
                font_size=24,
                text_color=color
            )
            line_box.add(line)
        self.v_box.add(line_box.with_space_around(bottom=30))
        
        # 创建用户名输入框
        username_layout = arcade.gui.UIBoxLayout(vertical=False)
        username_field = arcade.gui.UILabel(
            text="用户名:",
            width=100,
            text_color=arcade.color.DARK_BLUE,
            font_size=18
        )
        self.username_input = arcade.gui.UIInputText(
            text="玩家1",
            width=300,
            height=40,
            font_size=16,
            text_color=arcade.color.BLACK
        )
        username_layout.add(username_field)
        username_layout.add(self.username_input)
        self.v_box.add(username_layout.with_space_around(bottom=20))
        
        # 创建密码输入框
        password_layout = arcade.gui.UIBoxLayout(vertical=False)
        password_field = arcade.gui.UILabel(
            text="密码:",
            width=100,
            text_color=arcade.color.DARK_BLUE,
            font_size=18
        )
        self.password_input = arcade.gui.UIInputText(
            text="",
            width=300,
            height=40,
            font_size=16,
            text_color=arcade.color.BLACK,
            password=True
        )
        password_layout.add(password_field)
        password_layout.add(self.password_input)
        self.v_box.add(password_layout.with_space_around(bottom=30))
        
        # 登录按钮 - 更漂亮的样式
        login_button = arcade.gui.UIFlatButton(
            text="登录",
            width=200,
            height=50,
            font_size=18,
            style={
                "font_color": arcade.color.WHITE,
                "bg_color": arcade.color.PURPLE,
                "border_color": arcade.color.DARK_BLUE,
                "border_width": 2,
                "bg_color_pressed": arcade.color.BLUE,
            }
        )
        
        # 将使用原始版本还是增强版的标志
        self.use_enhanced_version = False
        
        # 设置版本选择切换按钮 - 更漂亮的样式
        version_switch = arcade.gui.UIFlatButton(
            text="切换到增强版",
            width=200,
            height=50,
            font_size=18,
            style={
                "font_color": arcade.color.WHITE,
                "bg_color": arcade.color.DARK_GREEN,
                "border_color": arcade.color.BLACK,
                "border_width": 2,
                "bg_color_pressed": arcade.color.DARK_PASTEL_GREEN,
            }
        )
        
        # 版本切换按钮事件处理
        @version_switch.event("on_click")
        def on_version_switch(event):
            self.use_enhanced_version = not self.use_enhanced_version
            if self.use_enhanced_version:
                version_switch.text = "切换到基础版"
                version_switch.style["bg_color"] = arcade.color.DARK_RED
                version_switch.style["bg_color_pressed"] = arcade.color.DARK_PINK
            else:
                version_switch.text = "切换到增强版"
                version_switch.style["bg_color"] = arcade.color.DARK_GREEN
                version_switch.style["bg_color_pressed"] = arcade.color.DARK_PASTEL_GREEN
        
        # 用于防止重复点击的标志
        self.is_transitioning = False
        
        # 登录按钮事件处理
        @login_button.event("on_click")
        def on_login_button_click(event):
            # 如果正在切换视图，则忽略重复点击
            if self.is_transitioning:
                print("正在切换视图，忽略重复点击")
                return
            
            # 标记正在切换视图
            self.is_transitioning = True
            print("开始登录流程...")
            
            # 获取用户名
            username = self.username_input.text if self.username_input.text else "玩家"
            print(f"用户名: {username}")
            
            try:
                # 禁用UI管理器，防止再次点击
                print("禁用UI管理器")
                self.manager.disable()
                
                # 获取当前窗口对象
                current_window = self.window
                print(f"当前窗口ID: {id(current_window)}")
                
                # 使用延迟导入
                import importlib
                bedroom_module = importlib.import_module('bedroom_view')
                
                # 创建新的卧室视图
                print("创建卧室视图")
                bedroom_view = bedroom_module.BedroomView(self.use_enhanced_version, username)
                print(f"卧室视图ID: {id(bedroom_view)}")
                
                # 跳转到卧室页面，关闭防重复点击标记
                print("准备切换到卧室视图")
                self.is_transitioning = False
                current_window.show_view(bedroom_view)
                print("已切换到卧室视图")
            except Exception as e:
                print(f"切换视图时出错: {e}")
                import traceback
                traceback.print_exc()
                # 如果出错，重新启用UI管理器
                self.manager.enable()
                # 取消正在切换的标记
                self.is_transitioning = False
        
        # 添加一个按钮容器，使按钮并排显示
        button_row = arcade.gui.UIBoxLayout(vertical=False, space_between=20)
        button_row.add(login_button)
        button_row.add(version_switch)
        
        # 将按钮行添加到布局中
        self.v_box.add(button_row.with_space_around(bottom=30))
        
        # 将垂直框添加到管理器中
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box
            )
        )
    
    def on_update(self, delta_time):
        """更新动画"""
        self.total_time += delta_time
        
        # 更新星星位置
        for star in self.stars:
            star['y'] -= star['speed']
            if star['y'] < 0:
                star['y'] = SCREEN_HEIGHT
                star['x'] = random.randint(0, SCREEN_WIDTH)
    
    def on_draw(self):
        """渲染登录页面"""
        arcade.start_render()
        
        # 绘制渐变背景
        arcade.draw_lrtb_rectangle_filled(
            0, SCREEN_WIDTH, SCREEN_HEIGHT, 0,
            arcade.color.SKY_BLUE
        )
        arcade.draw_lrtb_rectangle_filled(
            0, SCREEN_WIDTH, SCREEN_HEIGHT * 0.6, 0,
            arcade.color.LIGHT_BLUE
        )
        
        # 绘制星星
        for star in self.stars:
            arcade.draw_circle_filled(
                star['x'], star['y'], star['size'],
                arcade.color.WHITE
            )
        
        # 绘制底部装饰
        # 绘制草地
        arcade.draw_lrtb_rectangle_filled(
            0, SCREEN_WIDTH, SCREEN_HEIGHT * 0.15, 0,
            arcade.color.APPLE_GREEN
        )
        
        # 绘制云朵
        self.draw_cloud(100, SCREEN_HEIGHT - 100, 40)
        self.draw_cloud(300, SCREEN_HEIGHT - 150, 50)
        self.draw_cloud(600, SCREEN_HEIGHT - 120, 45)
        self.draw_cloud(800, SCREEN_HEIGHT - 180, 55)
        
        # 绘制彩色气球
        for i in range(10):
            x = 50 + i * 100
            y = SCREEN_HEIGHT - 50
            self.draw_balloon(x, y, NINETIES_COLORS[i])
        
        # 绘制UI元素
        self.manager.draw()
        
        # 绘制底部提示文字
        arcade.draw_text(
            "登录以体验90后童年的回忆",
            start_x=SCREEN_WIDTH / 2,
            start_y=70,
            color=arcade.color.DARK_BLUE,
            font_size=16,
            anchor_x="center",
            bold=True
        )
    
    def draw_balloon(self, x, y, color):
        """绘制气球"""
        # 气球线
        line_bob = 5 * math.sin(self.total_time * 2 + x / 50)
        arcade.draw_line(
            x, y - 20 + line_bob, 
            x, y - 90 + line_bob * 0.5, 
            arcade.color.BLACK, 2
        )
        
        # 气球本身
        arcade.draw_circle_filled(
            x, y, 25, color
        )
        # 气球反光
        arcade.draw_circle_filled(
            x - 8, y + 8, 5, (255, 255, 255, 120)
        )
    
    def draw_cloud(self, x, y, size):
        """绘制云朵"""
        arcade.draw_circle_filled(x, y, size, arcade.color.WHITE)
        arcade.draw_circle_filled(x + size*0.8, y, size*0.7, arcade.color.WHITE)
        arcade.draw_circle_filled(x - size*0.8, y, size*0.7, arcade.color.WHITE)
        arcade.draw_circle_filled(x + size*0.4, y + size*0.4, size*0.7, arcade.color.WHITE)
        arcade.draw_circle_filled(x - size*0.4, y + size*0.4, size*0.7, arcade.color.WHITE)
    
    def on_show_view(self):
        """显示视图时的处理"""
        arcade.set_background_color(arcade.color.LIGHT_BLUE)
        self.manager.enable()
        # 重置切换标记
        self.is_transitioning = False
    
    def on_hide_view(self):
        """隐藏视图时的处理"""
        self.manager.disable()

# 这里删除了原来的main函数，只使用main.py作为入口点 