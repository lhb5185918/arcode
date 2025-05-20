import arcade
from arcade.text import draw_text
from interactive_room_game import InteractiveObject

def color_from_hex_string(hex_string):
    """将16进制颜色字符串转换为RGB颜色元组"""
    # 移除可能存在的#前缀
    if hex_string.startswith('#'):
        hex_string = hex_string[1:]
    
    # 将16进制字符串转换为RGB值
    r = int(hex_string[0:2], 16)
    g = int(hex_string[2:4], 16)
    b = int(hex_string[4:6], 16)
    
    return (r, g, b)

class GameConsole(InteractiveObject):
    """游戏机类"""
    def __init__(self, x, y):
        super().__init__(x, y, 150, 80, color=arcade.color.GRAY)
        self.game_running = False
        self.games = ["超级玛丽", "魂斗罗", "冒险岛", "坦克大战"]
        self.current_game = 0
    
    def draw(self):
        # 绘制游戏机主体
        arcade.draw_rect_filled(
            arcade.rect.XYWH(self.x, self.y, self.width, self.height),
            color=self.color
        )
        
        # 绘制游戏机按钮
        button_colors = [arcade.color.RED, arcade.color.BLACK]
        for i in range(2):
            arcade.draw_circle_filled(
                center_x=self.x - 50 + i*30, 
                center_y=self.y - 20, 
                radius=5, color=button_colors[i]
            )
        
        # 绘制卡带插槽
        arcade.draw_rect_filled(
            arcade.rect.XYWH(self.x, self.y + 10, self.width - 40, 20),
            color=arcade.color.BLACK
        )
        
        # 如果游戏机开启，显示游戏信息
        if self.is_active:
            arcade.draw_text(
                text=f"游戏: {self.games[self.current_game]}",
                start_x=self.x - 60, start_y=self.y - 5, 
                color=arcade.color.WHITE, font_size=12, 
                width=120, align="center"
            )
    
    def change_game(self):
        """切换游戏"""
        if self.is_active:
            self.current_game = (self.current_game + 1) % len(self.games)

class Radio(InteractiveObject):
    """收音机类"""
    def __init__(self, x, y):
        super().__init__(x, y, 120, 70, color=arcade.color.DARK_BROWN)
        self.channels = ["音乐频道", "新闻频道", "故事频道"]
        self.current_channel = 0
        self.volume = 5  # 音量，范围1-10
    
    def draw(self):
        # 绘制收音机主体
        arcade.draw_rect_filled(
            arcade.rect.XYWH(self.x, self.y, self.width, self.height),
            color=self.color
        )
        
        # 绘制收音机显示屏
        display_color = arcade.color.LIGHT_GRAY
        if self.is_active:
            display_color = arcade.color.YELLOW
        
        arcade.draw_rect_filled(
            arcade.rect.XYWH(self.x, self.y + 15, self.width - 30, 25),
            color=display_color
        )
        
        # 绘制控制旋钮
        arcade.draw_circle_filled(
            center_x=self.x - 30, center_y=self.y - 15, 
            radius=10, color=arcade.color.SILVER
        )
        arcade.draw_circle_filled(
            center_x=self.x + 30, center_y=self.y - 15, 
            radius=10, color=arcade.color.SILVER
        )
        
        # 如果收音机开启，显示频道信息
        if self.is_active:
            arcade.draw_text(
                text=f"{self.channels[self.current_channel]} 音量:{self.volume}",
                start_x=self.x - 50, start_y=self.y + 12, 
                color=arcade.color.BLACK, font_size=10, 
                width=100, align="center"
            )
    
    def change_channel(self):
        """切换频道"""
        if self.is_active:
            self.current_channel = (self.current_channel + 1) % len(self.channels)
    
    def increase_volume(self):
        """增加音量"""
        if self.is_active and self.volume < 10:
            self.volume += 1
    
    def decrease_volume(self):
        """减小音量"""
        if self.is_active and self.volume > 0:
            self.volume -= 1

class Bookshelf(InteractiveObject):
    """书架类"""
    def __init__(self, x, y):
        super().__init__(x, y, 180, 220, color=arcade.color.BROWN)
        self.books = ["童话故事", "科普百科", "漫画集", "课本"]
        self.selected_book = None
    
    def draw(self):
        # 绘制书架主体
        arcade.draw_rect_filled(
            arcade.rect.XYWH(self.x, self.y, self.width, self.height),
            color=self.color
        )
        
        # 绘制书架层板
        for i in range(3):
            arcade.draw_rect_filled(
                arcade.rect.XYWH(self.x, self.y - 50 + i*70, self.width, 5),
                color=arcade.color.DARK_BROWN
            )
        
        # 绘制书本
        for i, book in enumerate(self.books):
            book_x = self.x - 60 + (i % 2) * 80
            book_y = self.y + 60 - (i // 2) * 70
            book_color = color_from_hex_string(
                ["#FF9999", "#99FF99", "#9999FF", "#FFFF99"][i]
            )
            
            arcade.draw_rect_filled(
                arcade.rect.XYWH(book_x, book_y, 40, 60),
                color=book_color
            )
            
            # 书脊上的文字
            arcade.draw_text(
                text=book, start_x=book_x - 15, start_y=book_y - 5, 
                color=arcade.color.BLACK, font_size=8, 
                width=30, align="center", rotation=90
            )
        
        # 如果有选中的书，显示内容
        if self.selected_book is not None:
            arcade.draw_rect_filled(
                arcade.rect.XYWH(self.x + 200, self.y, 150, 200),
                color=arcade.color.WHITE
            )
            arcade.draw_text(
                text=f"{self.books[self.selected_book]}内容...",
                start_x=self.x + 130, start_y=self.y + 80, 
                color=arcade.color.BLACK, font_size=12, 
                width=140, align="center"
            )
    
    def select_book(self, index):
        """选择一本书"""
        if 0 <= index < len(self.books):
            if self.selected_book == index:
                self.selected_book = None  # 再次点击同一本书会放回去
            else:
                self.selected_book = index 