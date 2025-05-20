import arcade
import random
import math
# 删除这些导入，避免窗口创建
# from enhanced_game import EnhancedChildhoodRoom
# from interactive_room_game import ChildhoodRoom, SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE
# 只导入必要的常量
from interactive_room_game import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE
from bedroom_items import Bed, Desk, Computer, HomeworkBook, Window

class BedroomView(arcade.View):
    """90后童年卧室视图，展示开场白并作为游戏的中转页面"""
    
    def __init__(self, use_enhanced_version=False, username="玩家"):
        super().__init__()
        
        # 设置背景颜色
        arcade.set_background_color(arcade.color.BEIGE)
        
        # 是否使用增强版
        self.use_enhanced_version = use_enhanced_version
        
        # 玩家名称
        self.username = username
        
        # 开场白文字
        self.intro_text = [
            f"亲爱的{username}，欢迎回到90后的童年",
            "这是一个充满回忆的地方",
            "在这里，你可以重温儿时的美好时光",
            "电视机、游戏机、收音机...",
            "这些都是我们童年的伙伴",
            "准备好开启这段怀旧之旅了吗？",
            "点击任意处进入童年房间..."
        ]
        
        # 开场白文字的当前显示位置
        self.current_line = 0
        self.text_alpha = 0  # 文字透明度
        self.fade_in = True  # 是否正在淡入
        self.text_y = SCREEN_HEIGHT // 2  # 文字Y坐标
        
        # 创建可交互物品
        self.bed = Bed(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
        self.desk = Desk(SCREEN_WIDTH * 0.25, SCREEN_HEIGHT * 0.5)
        self.computer = Computer(SCREEN_WIDTH * 0.25, SCREEN_HEIGHT * 0.6)
        self.homework = HomeworkBook(SCREEN_WIDTH * 0.6, SCREEN_HEIGHT * 0.55)
        self.window = Window(SCREEN_WIDTH * 0.75, SCREEN_HEIGHT * 0.6)
        
        # 将所有物品加入列表，方便统一管理
        self.interactive_items = [
            self.bed, 
            self.desk, 
            self.computer,
            self.homework,
            self.window
        ]
        
        # 当前显示的消息
        self.current_message = ""
        self.message_timer = 0  # 消息显示计时器
        self.message_duration = 3.0  # 消息显示持续时间
        
        # 计时器
        self.total_time = 0
        self.text_timer = 0
        
        # 欢迎阶段标志
        self.welcome_phase = True
        
        # 当前悬停的物品
        self.hovered_item = None
        
        # 防止重复点击的标志
        self.is_transitioning = False
    
    def on_show_view(self):
        """显示视图时调用"""
        arcade.set_background_color(arcade.color.BEIGE)
        self.is_transitioning = False
    
    def on_update(self, delta_time):
        """更新动画"""
        self.total_time += delta_time
        self.text_timer += delta_time
        
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
        for item in self.interactive_items:
            # 如果是窗户，需要特殊处理来更新动画
            if isinstance(item, Window):
                item.update(delta_time)
        
        # 更新消息显示计时器
        if self.current_message:
            self.message_timer += delta_time
            if self.message_timer >= self.message_duration:
                self.message_timer = 0
                self.current_message = ""
    
    def on_draw(self):
        """渲染卧室场景"""
        arcade.start_render()
        
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
        for item in self.interactive_items:
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
                width=SCREEN_WIDTH * 0.75,
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
            width=SCREEN_WIDTH * 0.8,
            align="center"
        )
    
    def direct_to_game(self):
        """创建并切换到游戏视图"""
        try:
            print("正在准备切换到游戏视图...")
            
            # 使用延迟导入，避免循环导入问题
            import importlib
            
            # 导入room_view模块
            room_view_module = importlib.import_module('room_view')
            print("已动态导入RoomGameView模块")
            
            # 创建新的游戏视图实例
            if self.use_enhanced_version:
                print("创建增强版游戏视图")
                game_view = room_view_module.RoomGameView(enhanced=True, username=self.username)
            else:
                print("创建基础版游戏视图")
                game_view = room_view_module.RoomGameView(enhanced=False, username=self.username)
            
            print(f"游戏视图ID: {id(game_view)}")
            print("游戏视图已创建，准备切换...")
            
            # 获取当前窗口对象
            current_window = self.window
            print(f"当前窗口ID: {id(current_window)}")
            
            # 切换到游戏视图，关闭防重复点击标记
            self.is_transitioning = False
            current_window.show_view(game_view)
            print("已切换到游戏视图")
        except Exception as e:
            print(f"进入游戏时出错: {e}")
            import traceback
            traceback.print_exc()
            self.is_transitioning = False
    
    def on_mouse_press(self, x, y, button, modifiers):
        """鼠标点击事件处理"""
        # 如果正在切换视图，忽略点击
        if self.is_transitioning:
            return
            
        # 如果在欢迎阶段，点击任意处跳过
        if self.welcome_phase:
            self.welcome_phase = False
            return
        
        # 检查是否点击了物品
        item_clicked = False
        for item in self.interactive_items:
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
                        message = item.change_time()
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
            # 使用新的方法切换到游戏
            self.direct_to_game()
    
    def on_mouse_motion(self, x, y, dx, dy):
        """鼠标移动事件处理"""
        # 检查鼠标是否悬停在物品上
        self.hovered_item = None
        for item in self.interactive_items:
            if item.is_mouse_over(x, y):
                self.hovered_item = item
                break
    
    def on_mouse_release(self, x, y, button, modifiers):
        """鼠标释放事件处理"""
        pass
    
    def on_key_press(self, key, modifiers):
        """键盘按键事件处理"""
        # 按空格键跳过欢迎阶段
        if key == arcade.key.SPACE and self.welcome_phase:
            self.welcome_phase = False
    
    def on_mouse_double_click(self, x, y, button, modifiers):
        """鼠标双击事件处理"""
        # 检查是否双击了作业本
        if self.homework.is_clicked(x, y) and button == arcade.MOUSE_BUTTON_LEFT:
            message = self.homework.do_homework()
            self.current_message = message
            self.message_timer = 0 