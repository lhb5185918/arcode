import arcade
from login_view import LoginView
from interactive_room_game import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE

# 全局窗口实例
GAME_WINDOW = None

def main():
    """游戏的主入口函数"""
    global GAME_WINDOW
    
    # 如果已经有窗口实例，关闭它
    if GAME_WINDOW is not None:
        GAME_WINDOW.close()
    
    # 创建新窗口
    GAME_WINDOW = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    
    # 设置起始视图
    login_view = LoginView()
    GAME_WINDOW.show_view(login_view)
    
    # 运行游戏
    arcade.run()

if __name__ == "__main__":
    main() 