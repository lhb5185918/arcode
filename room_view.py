import arcade
# 从interactive_room_game导入需要的类和常量，而不是整个模块
from interactive_room_game import Television, RemoteControl, SCREEN_WIDTH, SCREEN_HEIGHT
from extensions import GameConsole, Radio, Bookshelf

class RoomGameView(arcade.View):
    """90后童年房间游戏视图，继承自arcade.View而非arcade.Window"""
    
    def __init__(self, enhanced=False, username="玩家"):
        super().__init__()
        
        # 设置背景颜色
        arcade.set_background_color(arcade.color.BEIGE)
        
        # 是否使用增强版
        self.enhanced = enhanced
        
        # 玩家名称
        self.username = username
        
        # 交互对象列表
        self.interactive_objects = []
        
        # 初始化各个交互对象
        self.tv = Television(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)
        self.remote = RemoteControl(SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT // 2 - 100)
        
        # 添加基础对象到交互列表
        self.interactive_objects.extend([self.tv, self.remote])
        
        # 如果是增强版，添加额外对象
        if enhanced:
            self.game_console = GameConsole(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 50)
            self.radio = Radio(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 200)
            self.bookshelf = Bookshelf(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2)
            
            # 添加增强版对象到交互列表
            self.interactive_objects.extend([
                self.game_console, self.radio, self.bookshelf
            ])
            
            # 特殊交互对象映射 (用于特殊交互逻辑)
            self.special_interactions = {
                self.remote: self._handle_remote,
                self.game_console: self._handle_game_console,
                self.radio: self._handle_radio,
                self.bookshelf: self._handle_bookshelf
            }
    
    def on_draw(self):
        """渲染游戏画面"""
        arcade.start_render()
        
        # 绘制背景墙壁
        arcade.draw_rect_filled(
            arcade.rect.XYWH(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT),
            color=arcade.color.LIGHT_BLUE
        )
        
        # 绘制地板
        arcade.draw_rect_filled(
            arcade.rect.XYWH(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4, SCREEN_WIDTH, SCREEN_HEIGHT // 2),
            color=arcade.color.LIGHT_BROWN
        )
        
        # 绘制所有交互对象
        for obj in self.interactive_objects:
            obj.draw()
        
        # 绘制使用说明
        instructions = [
            "点击电视右下角按钮开/关机",
            "点击遥控器切换频道"
        ]
        
        # 为增强版添加额外说明
        if self.enhanced:
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
    
    def on_mouse_press(self, x, y, button, modifiers):
        """鼠标点击事件处理"""
        # 基础版直接处理点击
        if not self.enhanced:
            # 检查点击的是否为遥控器
            if self.remote.is_clicked(x, y):
                self.tv.change_channel()
            
            # 检查其他交互对象
            for obj in self.interactive_objects:
                if obj.is_clicked(x, y):
                    obj.on_click()
            return
        
        # 增强版处理特殊交互
        for obj, handler in self.special_interactions.items():
            if obj.is_clicked(x, y):
                handler(x, y)
                return
        
        # 处理普通交互对象
        for obj in self.interactive_objects:
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
    
    def on_show_view(self):
        """显示视图时调用"""
        arcade.set_background_color(arcade.color.BEIGE)
        print("RoomGameView已显示")
    
    def on_hide_view(self):
        """隐藏视图时调用"""
        print("RoomGameView已隐藏") 