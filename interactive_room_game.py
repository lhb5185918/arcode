import arcade
import os
from arcade.text import draw_text
from arcade.texture import load_texture

# 常量定义
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
SCREEN_TITLE = "90后童年互动房间"

# 资源路径
RESOURCES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources")

class InteractiveObject:
    """交互对象基类"""
    def __init__(self, x, y, width, height, texture_path=None, color=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.texture = None
        self.color = color or arcade.color.BLUE
        self.is_active = False
        
        if texture_path and os.path.exists(texture_path):
            self.texture = arcade.load_texture(texture_path)
    
    def draw(self):
        """绘制对象"""
        if self.texture:
            arcade.draw_texture_rect(
                texture=self.texture,
                rect=arcade.rect.XYWH(self.x, self.y, self.width, self.height)
            )
        else:
            # 如果没有纹理，使用颜色绘制
            arcade.draw_rect_filled(
                arcade.rect.XYWH(self.x, self.y, self.width, self.height),
                color=self.color
            )
    
    def is_clicked(self, x, y):
        """检查是否被点击"""
        return (self.x - self.width/2 <= x <= self.x + self.width/2 and
                self.y - self.height/2 <= y <= self.y + self.height/2)
    
    def on_click(self):
        """点击事件处理"""
        self.is_active = not self.is_active
        return self.is_active

class Television(InteractiveObject):
    """电视机类"""
    def __init__(self, x, y):
        super().__init__(x, y, 200, 150, color=arcade.color.BLACK)
        self.channel = 0
        self.channels = ["新闻", "电影", "动画", "游戏"]
        self.screen_color = arcade.color.BLACK
    
    def draw(self):
        # 绘制电视外壳
        arcade.draw_rect_filled(arcade.rect.XYWH(self.x, self.y, self.width, self.height), color=self.color)
        
        # 绘制电视屏幕
        screen_color = self.screen_color if not self.is_active else arcade.color.BLUE
        arcade.draw_rect_filled(
            arcade.rect.XYWH(self.x, self.y + 10, self.width - 20, self.height - 40),
            color=screen_color
        )
        
        # 绘制开关按钮
        button_color = arcade.color.RED if self.is_active else arcade.color.GRAY
        arcade.draw_circle_filled(
            center_x=self.x + self.width/2 - 15, 
            center_y=self.y - self.height/2 + 15, 
            radius=10, color=button_color
        )
        
        # 如果电视开着，显示频道信息
        if self.is_active:
            arcade.draw_text(
                text=f"频道: {self.channels[self.channel]}",
                x=self.x - 70, y=self.y, 
                color=arcade.color.WHITE, font_size=16, 
                width=140, align="center"
            )
    
    def change_channel(self):
        """切换频道"""
        if self.is_active:
            self.channel = (self.channel + 1) % len(self.channels)

class RemoteControl(InteractiveObject):
    """遥控器类"""
    def __init__(self, x, y):
        super().__init__(x, y, 50, 100, color=arcade.color.GRAY)
    
    def draw(self):
        # 绘制遥控器主体
        arcade.draw_rect_filled(arcade.rect.XYWH(self.x, self.y, self.width, self.height), color=self.color)
        
        # 绘制遥控器按钮
        button_colors = [arcade.color.RED, arcade.color.GREEN, arcade.color.BLUE]
        for i in range(3):
            arcade.draw_circle_filled(
                center_x=self.x, 
                center_y=self.y + 30 - i*25, 
                radius=10, color=button_colors[i]
            )

class ChildhoodRoom(arcade.Window):
    """主游戏窗口"""
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.BEIGE)
        
        # 创建资源目录
        os.makedirs(RESOURCES_DIR, exist_ok=True)
        
        # 交互对象列表
        self.interactive_objects = []
        
        # 初始化各个交互对象
        self.tv = Television(width // 2, height // 2 + 100)
        self.remote = RemoteControl(width // 2 + 200, height // 2 - 100)
        
        self.interactive_objects.append(self.tv)
        self.interactive_objects.append(self.remote)
    
    def on_draw(self):
        """渲染游戏画面"""
        self.clear()
        
        # 绘制背景和墙壁
        arcade.draw_rect_filled(
            arcade.rect.XYWH(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT),
            color=arcade.color.LIGHT_BLUE
        )
        
        arcade.draw_rect_filled(
            arcade.rect.XYWH(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4, SCREEN_WIDTH, SCREEN_HEIGHT // 2),
            color=arcade.color.LIGHT_BROWN
        )
        
        # 绘制所有交互对象
        for obj in self.interactive_objects:
            obj.draw()
        
        # 绘制使用说明
        arcade.draw_text(
            text="点击电视右下角按钮开/关机\n点击遥控器切换频道",
            x=20, y=SCREEN_HEIGHT - 60, 
            color=arcade.color.BLACK, font_size=16
        )
    
    def on_mouse_press(self, x, y, button, modifiers):
        """鼠标点击事件处理"""
        # 检查点击的是否为遥控器
        if self.remote.is_clicked(x, y):
            self.tv.change_channel()
        
        # 检查其他交互对象
        for obj in self.interactive_objects:
            if obj.is_clicked(x, y):
                obj.on_click()

def main():
    """主函数"""
    game = ChildhoodRoom(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()

if __name__ == "__main__":
    main() 