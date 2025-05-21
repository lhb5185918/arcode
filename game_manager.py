import arcade
import arcade.gui
import random
import math
import os
import datetime  # 添加datetime模块
from interactive_room_game import Television, RemoteControl, SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE
from bedroom_items import Bed, Desk, Computer, HomeworkBook, Window
from extensions import GameConsole, Radio, Bookshelf
from debug_tools import draw_coordinate_system  # 导入坐标轴绘制函数

# 90后经典的亮色调
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

class GameManager(arcade.Window):
    """统一的游戏管理器，使用状态模式而不是视图切换"""
    
    # 游戏状态常量
    STATE_LOGIN = "login"
    STATE_BEDROOM = "bedroom"
    STATE_GAME = "game"
    
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.BEIGE)
        
        # 当前游戏状态
        self.current_state = self.STATE_LOGIN
        
        # 登录状态属性
        self.username = "玩家1"
        self.password = ""
        self.use_enhanced_version = False
        
        # 创建UI管理器（仅用于登录状态）
        self.ui_manager = arcade.gui.UIManager()
        self.setup_login_ui()
        
        # 创建动画元素
        self.stars = []
        for _ in range(50):
            self.stars.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT),
                'size': random.uniform(1, 3),
                'speed': random.uniform(0.5, 2)
            })
        
        # 卧室状态属性
        self.intro_text = [
            "亲爱的玩家，欢迎回到90后的童年",
            "这是一个充满回忆的地方",
            "在这里，你可以重温儿时的美好时光",
            "电视机、游戏机、收音机...",
            "这些都是我们童年的伙伴",
            "准备好开启这段怀旧之旅了吗？",
            "点击任意处进入童年房间..."
        ]
        self.current_line = 0
        self.text_alpha = 0
        self.fade_in = True
        self.welcome_phase = True
        
        # 时间系统
        current_time = datetime.datetime.now()
        self.game_time = datetime.datetime(1996, 1, 1, current_time.hour, current_time.minute)
        self.time_speed = 1  # 时间流逝速度倍数
        self.time_buttons = []  # 存储时间控制按钮
        self.setup_time_controls()
        
        # 卧室互动物品
        self.bedroom_items = []
        self.setup_bedroom_items()
        
        # 游戏状态属性
        self.game_objects = []
        self.special_interactions = {}
        self.setup_game_objects()
        
        # 共享属性
        self.total_time = 0.0
        self.current_message = ""
        self.message_timer = 0
        self.message_duration = 3.0
        
        # 防重复点击
        self.is_transitioning = False
        
        # 调试模式 - 坐标系统显示
        self.show_coordinates = False
        self.mouse_x = 0
        self.mouse_y = 0
        
        # 加载背景图片
        try:
            # 创建resources目录（如果不存在）
            os.makedirs("resources/bedroom", exist_ok=True)
            
            # 获取资源的绝对路径
            bedroom_sun_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources", "bedroom", "bedroom-sun.jpg")
            bedroom_night_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources", "bedroom", "beedroom-night.jpg")
            
            print(f"尝试加载白天背景图片: {bedroom_sun_path}")
            print(f"尝试加载夜晚背景图片: {bedroom_night_path}")
            
            # 检查文件是否存在
            if not os.path.exists(bedroom_sun_path):
                print(f"错误: 白天背景图片不存在: {bedroom_sun_path}")
            if not os.path.exists(bedroom_night_path):
                print(f"错误: 夜晚背景图片不存在: {bedroom_night_path}")
            
            # 加载卧室背景图片 - 使用绝对路径
            self.bedroom_bg_day = arcade.load_texture(bedroom_sun_path)
            self.bedroom_bg_night = arcade.load_texture(bedroom_night_path)
            
            # 当前使用的背景
            self.current_bg = self.bedroom_bg_night  # 默认夜晚
            
            self.has_bedroom_bg = True
            print("卧室背景图片加载成功")
        except Exception as e:
            self.has_bedroom_bg = False
            print(f"加载背景图片出错: {e}")
            import traceback
            traceback.print_exc()
        
        print("游戏管理器初始化完成")
    
    def setup_login_ui(self):
        """设置登录UI元素"""
        self.ui_manager.enable()
        
        # 创建一个垂直布局容器
        v_box = arcade.gui.UIBoxLayout()
        
        # 添加标题标签
        title_label = arcade.gui.UILabel(
            text="90后童年互动房间",
            font_size=40,
            width=500,
            align="center"
        )
        v_box.add(title_label.with_space_around(bottom=30))
        
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
        v_box.add(line_box.with_space_around(bottom=30))
        
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
        v_box.add(username_layout.with_space_around(bottom=20))
        
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
        v_box.add(password_layout.with_space_around(bottom=30))
        
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
        
        # 设置版本选择切换按钮 - 更漂亮的样式
        self.version_switch = arcade.gui.UIFlatButton(
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
        @self.version_switch.event("on_click")
        def on_version_switch(event):
            self.use_enhanced_version = not self.use_enhanced_version
            if self.use_enhanced_version:
                self.version_switch.text = "切换到基础版"
                self.version_switch.style["bg_color"] = arcade.color.DARK_RED
                self.version_switch.style["bg_color_pressed"] = arcade.color.DARK_PINK
            else:
                self.version_switch.text = "切换到增强版"
                self.version_switch.style["bg_color"] = arcade.color.DARK_GREEN
                self.version_switch.style["bg_color_pressed"] = arcade.color.DARK_PASTEL_GREEN
        
        # 登录按钮事件处理
        @login_button.event("on_click")
        def on_login_button_click(event):
            # 如果正在切换状态，则忽略重复点击
            if self.is_transitioning:
                return
            
            # 标记正在切换状态
            self.is_transitioning = True
            print("登录按钮点击")
            
            # 获取用户名
            self.username = self.username_input.text if self.username_input.text else "玩家"
            print(f"用户名: {self.username}")
            
            # 禁用UI管理器
            self.ui_manager.disable()
            
            # 更新intro_text中的用户名
            self.intro_text[0] = f"亲爱的{self.username}，欢迎回到90后的童年"
            
            # 切换到卧室状态
            print("切换到卧室状态")
            self.current_state = self.STATE_BEDROOM
            
            # 初始化时间并根据时间设置背景
            current_time = datetime.datetime.now()
            self.game_time = datetime.datetime(1996, 1, 1, current_time.hour, current_time.minute)
            self.update_background_by_time()
            
            # 重置标记
            self.is_transitioning = False
        
        # 添加一个按钮容器，使按钮并排显示
        button_row = arcade.gui.UIBoxLayout(vertical=False, space_between=20)
        button_row.add(login_button)
        button_row.add(self.version_switch)
        
        # 将按钮行添加到布局中
        v_box.add(button_row.with_space_around(bottom=30))
        
        # 将垂直框添加到管理器中
        self.ui_manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=v_box
            )
        )
    
    def setup_bedroom_items(self):
        """设置卧室中的互动物品"""
        self.bed = Bed(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
        self.desk = Desk(SCREEN_WIDTH * 0.25, SCREEN_HEIGHT * 0.5)
        self.computer = Computer(SCREEN_WIDTH * 0.25, SCREEN_HEIGHT * 0.6)
        self.homework = HomeworkBook(SCREEN_WIDTH * 0.6, SCREEN_HEIGHT * 0.55)
        self.window = Window(SCREEN_WIDTH * 0.75, SCREEN_HEIGHT * 0.6)
        
        # 将所有物品加入列表，方便统一管理
        self.bedroom_items = [
            self.bed, 
            self.desk, 
            self.computer,
            self.homework,
            self.window
        ]
    
    def setup_game_objects(self):
        """设置游戏中的交互对象"""
        # 基础对象
        self.tv = Television(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)
        self.remote = RemoteControl(SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT // 2 - 100)
        
        self.game_objects = [self.tv, self.remote]
        
        # 增强版对象
        if True:  # 先创建所有对象，使用时根据use_enhanced_version决定是否显示
            self.game_console = GameConsole(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 50)
            self.radio = Radio(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 200)
            self.bookshelf = Bookshelf(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2)
            
            self.game_objects.extend([
                self.game_console, self.radio, self.bookshelf
            ])
            
            # 特殊交互对象映射
            self.special_interactions = {
                self.remote: self._handle_remote,
                self.game_console: self._handle_game_console,
                self.radio: self._handle_radio,
                self.bookshelf: self._handle_bookshelf
            }
    
    def setup_time_controls(self):
        """设置时间控制按钮"""
        # 存储按钮位置信息 (x, y, width, height)
        self.time_button_pos = (SCREEN_WIDTH - 50, SCREEN_HEIGHT - 65, 80, 30)
    
    def advance_time(self, hours=0, minutes=0):
        """前进游戏时间"""
        delta = datetime.timedelta(hours=hours, minutes=minutes)
        self.game_time += delta
        
        # 更新背景（根据时间）
        self.update_background_by_time()
        
        # 显示时间变化消息
        self.current_message = f"时间已变为: {self.game_time.strftime('%Y年%m月%d日 %H:%M')}"
        self.message_timer = 0
    
    def update_background_by_time(self):
        """根据当前时间更新背景"""
        if hasattr(self, 'has_bedroom_bg') and self.has_bedroom_bg:
            hour = self.game_time.hour
            
            # 6:00-19:00 显示白天背景
            if 6 <= hour < 19:
                if self.current_bg != self.bedroom_bg_day:
                    self.current_bg = self.bedroom_bg_day
                    print("背景自动切换为白天")
            # 19:00-6:00 显示夜晚背景
            else:
                if self.current_bg != self.bedroom_bg_night:
                    self.current_bg = self.bedroom_bg_night
                    print("背景自动切换为夜晚")
    
    def on_update(self, delta_time):
        """更新游戏状态"""
        self.total_time += delta_time
        
        # 登录状态下的更新
        if self.current_state == self.STATE_LOGIN:
            # 更新星星位置
            for star in self.stars:
                star['y'] -= star['speed']
                if star['y'] < 0:
                    star['y'] = SCREEN_HEIGHT
                    star['x'] = random.randint(0, SCREEN_WIDTH)
        
        # 卧室状态下的更新
        elif self.current_state == self.STATE_BEDROOM:
            # 更新欢迎阶段的文字淡入淡出效果
            if self.welcome_phase:
                if self.fade_in:
                    self.text_alpha += 2  # 淡入速度
                    if self.text_alpha >= 255:
                        self.text_alpha = 255
                        self.fade_in = False
                else:
                    self.text_alpha -= 2  # 淡出速度
                    if self.text_alpha <= 0:
                        self.text_alpha = 0
                        self.fade_in = True
                        # 切换到下一行文字
                        self.current_line = (self.current_line + 1) % len(self.intro_text)
            
            # 更新物品状态
            for item in self.bedroom_items:
                # 如果是窗户，需要特殊处理来更新动画
                if isinstance(item, Window):
                    item.update(delta_time)
        
        # 游戏状态下的更新
        elif self.current_state == self.STATE_GAME:
            pass  # 游戏状态下的更新逻辑
        
        # 更新消息显示计时器
        if self.current_message:
            self.message_timer += delta_time
            if self.message_timer >= self.message_duration:
                self.message_timer = 0
                self.current_message = ""
    
    def on_draw(self):
        """渲染游戏画面"""
        arcade.start_render()
        
        # 登录状态下的绘制
        if self.current_state == self.STATE_LOGIN:
            self.draw_login_screen()
        
        # 卧室状态下的绘制
        elif self.current_state == self.STATE_BEDROOM:
            self.draw_bedroom_screen()
        
        # 游戏状态下的绘制
        elif self.current_state == self.STATE_GAME:
            self.draw_game_screen()
        
        # 如果启用坐标系统，绘制坐标轴
        if self.show_coordinates:
            draw_coordinate_system(SCREEN_WIDTH, SCREEN_HEIGHT, self.mouse_x, self.mouse_y)
    
    def draw_login_screen(self):
        """绘制登录页面"""
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
        self.ui_manager.draw()
        
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
    
    def draw_bedroom_screen(self):
        """绘制卧室场景"""
        # 如果有背景图片，使用背景图片
        if hasattr(self, 'has_bedroom_bg') and self.has_bedroom_bg:
            # 记录当前正在使用的背景
            if self.current_bg == self.bedroom_bg_day:
                bg_type = "白天背景"
            else:
                bg_type = "夜晚背景"
            print(f"正在绘制卧室背景: {bg_type}")
            
            # 绘制背景图片
            arcade.draw_texture_rectangle(
                center_x=SCREEN_WIDTH // 2,
                center_y=SCREEN_HEIGHT // 2,
                width=SCREEN_WIDTH,
                height=SCREEN_HEIGHT,
                texture=self.current_bg
            )
        else:
            print("警告: 没有背景图片可用，使用颜色背景")
            # 否则使用简单的颜色背景
            # 绘制墙壁
            arcade.draw_lrtb_rectangle_filled(
                0, SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_HEIGHT * 0.3,
                arcade.color.LIGHT_BLUE
            )
            
            # 绘制地板
            arcade.draw_lrtb_rectangle_filled(
                0, SCREEN_WIDTH, SCREEN_HEIGHT * 0.3, 0,
                arcade.color.LIGHT_BROWN
            )
        
        # 绘制所有可交互物品
        for item in self.bedroom_items:
            item.draw()
        
        # 在欢迎阶段显示开场白文字
        if self.welcome_phase and self.current_line < len(self.intro_text):
            arcade.draw_text(
                self.intro_text[self.current_line],
                start_x=SCREEN_WIDTH // 2,
                start_y=SCREEN_HEIGHT * 0.8,
                color=(0, 0, 0, self.text_alpha),
                font_size=24,
                anchor_x="center",
                bold=True
            )
        
        # 绘制时间显示
        if not self.welcome_phase:
            time_str = self.game_time.strftime("%Y年%m月%d日 %H:%M")
            
            # 绘制时间背景
            arcade.draw_rectangle_filled(
                SCREEN_WIDTH - 120, SCREEN_HEIGHT - 25,
                240, 40,
                (0, 0, 0, 150)
            )
            
            # 绘制时间文本
            arcade.draw_text(
                time_str,
                start_x=SCREEN_WIDTH - 120,
                start_y=SCREEN_HEIGHT - 25,
                color=arcade.color.WHITE,
                font_size=14,
                anchor_x="center",
                anchor_y="center"
            )
            
            # 绘制时间控制按钮
            if hasattr(self, 'time_button_pos'):
                btn_x, btn_y, btn_width, btn_height = self.time_button_pos
                arcade.draw_rectangle_filled(
                    btn_x, btn_y,
                    btn_width, btn_height,
                    arcade.color.DARK_BLUE
                )
                
                # 绘制按钮边框
                arcade.draw_rectangle_outline(
                    btn_x, btn_y,
                    btn_width, btn_height,
                    arcade.color.BLACK, 2
                )
                
                # 绘制按钮文本
                arcade.draw_text(
                    "+1小时",
                    start_x=btn_x,
                    start_y=btn_y,
                    color=arcade.color.WHITE,
                    font_size=14,
                    anchor_x="center",
                    anchor_y="center"
                )
        
        # 绘制交互消息
        if self.current_message:
            # 创建一个半透明的消息背景
            arcade.draw_rectangle_filled(
                SCREEN_WIDTH // 2, SCREEN_HEIGHT * 0.8,
                SCREEN_WIDTH * 0.8, 50,
                (0, 0, 0, 150)
            )
            
            arcade.draw_text(
                self.current_message,
                start_x=SCREEN_WIDTH // 2,
                start_y=SCREEN_HEIGHT * 0.8,
                color=arcade.color.WHITE,
                font_size=18,
                anchor_x="center",
                anchor_y="center",
                width=int(SCREEN_WIDTH * 0.75),
                align="center"
            )
            
        # 绘制提示文字
        if self.welcome_phase:
            instruction = "点击任意处跳过开场白..."
        else:
            instruction = "点击物品与它们互动，右键点击窗户切换日夜，右键点击电脑关机\n双击暑假作业可以写作业，点击屏幕空白处进入游戏"
        
        arcade.draw_text(
            instruction,
            start_x=SCREEN_WIDTH // 2,
            start_y=30,
            color=arcade.color.DARK_RED,
            font_size=14,
            anchor_x="center",
            anchor_y="center",
            width=int(SCREEN_WIDTH * 0.8),
            align="center"
        )
    
    def draw_game_screen(self):
        """绘制游戏画面"""
        # 绘制背景墙壁
        arcade.draw_rectangle_filled(
            SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT,
            color=arcade.color.LIGHT_BLUE
        )
        
        # 绘制地板
        arcade.draw_rectangle_filled(
            SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4, SCREEN_WIDTH, SCREEN_HEIGHT // 2,
            color=arcade.color.LIGHT_BROWN
        )
        
        # 绘制基础交互对象
        self.tv.draw()
        self.remote.draw()
        
        # 如果是增强版，绘制额外对象
        if self.use_enhanced_version:
            self.game_console.draw()
            self.radio.draw()
            self.bookshelf.draw()
        
        # 绘制使用说明
        instructions = [
            "点击电视右下角按钮开/关机",
            "点击遥控器切换频道"
        ]
        
        # 为增强版添加额外说明
        if self.use_enhanced_version:
            instructions.extend([
                "点击游戏机开/关机，再次点击切换游戏",
                "点击收音机开/关机，左旋钮调频道，右旋钮调音量",
                "点击书架上的书阅读"
            ])
        
        for i, instruction in enumerate(instructions):
            arcade.draw_text(
                text=instruction, 
                start_x=20, start_y=SCREEN_HEIGHT - 30 - i*20, 
                color=arcade.color.BLACK, font_size=12
            )
        
        # 显示用户名
        arcade.draw_text(
            text=f"玩家: {self.username}",
            start_x=SCREEN_WIDTH - 200,
            start_y=SCREEN_HEIGHT - 30,
            color=arcade.color.DARK_RED,
            font_size=16
        )
        
        # 绘制交互消息
        if self.current_message:
            # 创建一个半透明的消息背景
            arcade.draw_rectangle_filled(
                SCREEN_WIDTH // 2, SCREEN_HEIGHT * 0.8,
                SCREEN_WIDTH * 0.8, 50,
                (0, 0, 0, 150)
            )
            
            arcade.draw_text(
                self.current_message,
                start_x=SCREEN_WIDTH // 2,
                start_y=SCREEN_HEIGHT * 0.8,
                color=arcade.color.WHITE,
                font_size=18,
                anchor_x="center",
                anchor_y="center",
                width=int(SCREEN_WIDTH * 0.75),
                align="center"
            )
    
    def on_mouse_press(self, x, y, button, modifiers):
        """鼠标点击事件处理"""
        # 如果正在切换状态，忽略点击
        if self.is_transitioning:
            return
        
        # 登录状态下的点击处理
        if self.current_state == self.STATE_LOGIN:
            # 登录状态下点击由UI管理器处理
            pass
        
        # 卧室状态下的点击处理
        elif self.current_state == self.STATE_BEDROOM:
            # 检查是否点击了时间控制按钮
            if not self.welcome_phase and hasattr(self, 'time_button_pos'):
                btn_x, btn_y, btn_width, btn_height = self.time_button_pos
                if (abs(x - btn_x) <= btn_width/2 and
                    abs(y - btn_y) <= btn_height/2):
                    self.advance_time(hours=1)
                    return
            
            self.handle_bedroom_click(x, y, button)
        
        # 游戏状态下的点击处理
        elif self.current_state == self.STATE_GAME:
            self.handle_game_click(x, y, button)
    
    def handle_bedroom_click(self, x, y, button):
        """处理卧室场景的点击事件"""
        # 如果在欢迎阶段，点击任意处跳过
        if self.welcome_phase:
            self.welcome_phase = False
            return
        
        # 先检查是否点击了电脑桌面
        for item in self.bedroom_items:
            if isinstance(item, Computer) and item.show_desktop and item.is_active:
                desktop_result = item.handle_desktop_click(x, y)
                if desktop_result:
                    self.current_message = desktop_result
                    self.message_timer = 0
                    return
        
        # 检查是否点击了物品
        item_clicked = False
        for item in self.bedroom_items:
            if item.is_clicked(x, y):
                item_clicked = True
                
                # 根据点击的按钮类型处理
                if button == arcade.MOUSE_BUTTON_LEFT:
                    # 左键点击
                    message = item.on_click()
                    self.current_message = message
                    self.message_timer = 0
                elif button == arcade.MOUSE_BUTTON_RIGHT:
                    # 右键点击，特殊处理
                    if isinstance(item, Window):
                        # 将日夜变化回调传递给Window
                        message = item.change_time(self.on_day_night_change)
                        self.current_message = message
                        self.message_timer = 0
                    elif isinstance(item, Computer):
                        message = item.on_right_click()
                        self.current_message = message
                        self.message_timer = 0
                break
        
        # 如果没有点击任何物品且点击的是左键，进入游戏
        if not item_clicked and button == arcade.MOUSE_BUTTON_LEFT:
            self.is_transitioning = True
            print("从卧室进入游戏状态")
            self.current_state = self.STATE_GAME
            self.is_transitioning = False
    
    def handle_game_click(self, x, y, button):
        """处理游戏场景的点击事件"""
        # 基础版直接处理点击
        if not self.use_enhanced_version:
            # 检查点击的是否为遥控器
            if self.remote.is_clicked(x, y):
                self.tv.change_channel()
            
            # 检查其他交互对象
            for obj in [self.tv, self.remote]:
                if obj.is_clicked(x, y):
                    obj.on_click()
            return
        
        # 增强版处理特殊交互
        for obj, handler in self.special_interactions.items():
            if obj.is_clicked(x, y):
                handler(x, y)
                return
        
        # 处理普通交互对象
        for obj in self.game_objects:
            if obj.is_clicked(x, y):
                obj.on_click()
                break
    
    def _handle_remote(self, x, y):
        """处理遥控器交互"""
        # 点击遥控器切换电视频道
        self.tv.change_channel()
    
    def _handle_game_console(self, x, y):
        """处理游戏机交互"""
        if self.game_console.is_active:
            # 如果游戏机开着，点击切换游戏
            self.game_console.change_game()
        else:
            # 否则开机
            self.game_console.on_click()
    
    def _handle_radio(self, x, y):
        """处理收音机交互"""
        # 计算点击位置相对于收音机中心的坐标
        rel_x = x - self.radio.x
        rel_y = y - self.radio.y
        
        # 检查是否点击了左旋钮（调频道）
        if -40 < rel_x < -20 and -25 < rel_y < -5:
            if self.radio.is_active:
                self.radio.change_channel()
            return
        
        # 检查是否点击了右旋钮（调音量）
        if 20 < rel_x < 40 and -25 < rel_y < -5:
            if self.radio.is_active:
                # 上半部分增加音量，下半部分减小音量
                if rel_y > -15:
                    self.radio.increase_volume()
                else:
                    self.radio.decrease_volume()
            return
        
        # 其他部位点击开关机
        self.radio.on_click()
    
    def _handle_bookshelf(self, x, y):
        """处理书架交互"""
        # 检测点击的是哪本书
        for i in range(len(self.bookshelf.books)):
            book_x = self.bookshelf.x - 60 + (i % 2) * 80
            book_y = self.bookshelf.y + 60 - (i // 2) * 70
            
            # 判断点击位置是否在书本范围内
            if (book_x - 20 <= x <= book_x + 20 and 
                book_y - 30 <= y <= book_y + 30):
                self.bookshelf.select_book(i)
                return
        
        # 如果点击的不是书本，关闭当前阅读的书
        if self.bookshelf.selected_book is not None:
            self.bookshelf.selected_book = None
    
    def on_mouse_motion(self, x, y, dx, dy):
        """鼠标移动事件处理"""
        # 存储当前鼠标位置用于坐标显示
        self.mouse_x = x
        self.mouse_y = y
        
        # 只在卧室状态处理鼠标悬停
        if self.current_state == self.STATE_BEDROOM:
            self.hovered_item = None
            for item in self.bedroom_items:
                if hasattr(item, 'is_mouse_over') and item.is_mouse_over(x, y):
                    self.hovered_item = item
                    break
    
    def on_key_press(self, key, modifiers):
        """键盘按键事件处理"""
        # 按C键切换坐标系统显示
        if key == arcade.key.C:
            self.show_coordinates = not self.show_coordinates
            print(f"坐标系统显示: {'开启' if self.show_coordinates else '关闭'}")
        
        # 按空格键跳过欢迎阶段
        if key == arcade.key.SPACE and self.current_state == self.STATE_BEDROOM and self.welcome_phase:
            self.welcome_phase = False
    
    def on_mouse_double_click(self, x, y, button, modifiers):
        """鼠标双击事件处理"""
        # 只在卧室状态处理双击
        if self.current_state == self.STATE_BEDROOM:
            # 检查是否双击了作业本
            if hasattr(self, 'homework') and self.homework.is_clicked(x, y) and button == arcade.MOUSE_BUTTON_LEFT:
                message = self.homework.do_homework()
                self.current_message = message
                self.message_timer = 0 
    
    def on_day_night_change(self, time_state):
        """
        处理日夜切换的回调
        
        参数:
            time_state (str): 当前时间状态，"day"或"night"
        """
        if hasattr(self, 'has_bedroom_bg') and self.has_bedroom_bg:
            if time_state == "day":
                self.current_bg = self.bedroom_bg_day
                # 设置游戏时间为早上10点
                current_date = self.game_time.date()
                self.game_time = datetime.datetime.combine(current_date, datetime.time(10, 0))
                print(f"背景切换为白天，时间设为: {self.game_time.strftime('%H:%M')}")
            else:
                self.current_bg = self.bedroom_bg_night
                # 设置游戏时间为晚上21点
                current_date = self.game_time.date()
                self.game_time = datetime.datetime.combine(current_date, datetime.time(21, 0))
                print(f"背景切换为夜晚，时间设为: {self.game_time.strftime('%H:%M')}") 