import arcade
from game_manager import GameManager  # 我们将创建这个类来管理游戏状态
from interactive_room_game import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE

def main():
    """游戏的主入口函数"""
    try:
        # 创建游戏管理器实例
        print("创建游戏管理器")
        game_manager = GameManager(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        
        # 运行游戏
        print("开始游戏循环")
        arcade.run()
    except Exception as e:
        print(f"游戏初始化出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 