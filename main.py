import arcade
import os
from interactive_room_game import ChildhoodRoom
from living_room_scene import LivingRoom

# 常量定义
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
SCREEN_TITLE = "90后童年互动房间 - 场景选择"

class Button:
    """按钮类"""
    def __init__(self, x, y, width, height, text, color=arcade.color.BLUE, text_color=arcade.color.WHITE):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = color
        self.text_color = text_color
        self.hover = False
        
    def draw(self):
        # 绘制按钮背景
        color = arcade.color.LIGHT_BLUE if self.hover else self.color
        arcade.draw_rectangle_filled(
            self.x, self.y, self.width, self.height, 
            color=color
        )
        
        # 绘制按钮边框
        arcade.draw_rectangle_outline(
            self.x, self.y, self.width, self.height, 
            color=arcade.color.BLACK, border_width=2
        )
        
        # 绘制按钮文字
        arcade.draw_text(
            self.text,
            self.x - self.width/2 + 20, self.y - 10,
            self.text_color, 20, width=int(self.width - 40),
            align="center"
        )
    
    def is_clicked(self, x, y):
        """检查是否被点击"""
        return (self.x - self.width/2 <= x <= self.x + self.width/2 and
                self.y - self.height/2 <= y <= self.y + self.height/2)
                
    def check_hover(self, x, y):
        """检查是否鼠标悬停"""
        self.hover = (self.x - self.width/2 <= x <= self.x + self.width/2 and
                     self.y - self.height/2 <= y <= self.y + self.height/2)

class SceneSelector(arcade.Window):
    """场景选择器类"""
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.SKY_BLUE)
        
        # 创建按钮
        self.buttons = []
        
        # 童年房间按钮
        self.childhood_room_button = Button(
            width // 2, height // 2 + 100, 300, 60, 
            "童年房间", arcade.color.ORANGE
        )
        
        # 客厅场景按钮
        self.living_room_button = Button(
            width // 2, height // 2, 300, 60, 
            "客厅场景", arcade.color.GREEN
        )
        
        # 退出按钮
        self.exit_button = Button(
            width // 2, height // 2 - 100, 300, 60, 
            "退出游戏", arcade.color.RED
        )
        
        self.buttons.extend([
            self.childhood_room_button,
            self.living_room_button,
            self.exit_button
        ])
    
    def on_draw(self):
        """渲染游戏画面"""
        arcade.start_render()
        
        # 绘制背景
        arcade.draw_rectangle_filled(
            SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT,
            color=arcade.color.SKY_BLUE
        )
        
        # 绘制标题
        arcade.draw_text(
            "90后童年互动房间",
            SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT - 150,
            arcade.color.DARK_BLUE, 50, width=600,
            align="center", bold=True
        )
        
        arcade.draw_text(
            "请选择场景:",
            SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT - 250,
            arcade.color.BLACK, 24, width=300,
            align="center"
        )
        
        # 绘制所有按钮
        for button in self.buttons:
            button.draw()
    
    def on_mouse_press(self, x, y, button, modifiers):
        """鼠标点击事件处理"""
        if self.childhood_room_button.is_clicked(x, y):
            # 打开童年房间场景
            self.close()
            room = ChildhoodRoom(SCREEN_WIDTH, SCREEN_HEIGHT, "90后童年互动房间")
            arcade.run()
        
        elif self.living_room_button.is_clicked(x, y):
            # 打开客厅场景
            self.close()
            room = LivingRoom(SCREEN_WIDTH, SCREEN_HEIGHT, "客厅场景")
            arcade.run()
        
        elif self.exit_button.is_clicked(x, y):
            # 退出游戏
            self.close()
    
    def on_mouse_motion(self, x, y, dx, dy):
        """鼠标移动事件处理"""
        for button in self.buttons:
            button.check_hover(x, y)

def main():
    """主函数 - 启动场景选择器"""
    selector = SceneSelector(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()

if __name__ == "__main__":
    main() 