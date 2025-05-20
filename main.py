import arcade
from login_view import LoginView
from interactive_room_game import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE

def main():
    """游戏的主入口函数"""
    # 创建窗口
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    
    # 设置起始视图
    login_view = LoginView()
    window.show_view(login_view)
    
    # 运行游戏
    arcade.run()

if __name__ == "__main__":
    main() 