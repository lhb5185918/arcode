import arcade
import arcade.gui
from enhanced_game import EnhancedChildhoodRoom
from interactive_room_game import ChildhoodRoom, SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE

class LoginView(arcade.View):
    """游戏登录页视图"""
    
    def __init__(self):
        super().__init__()
        
        # 设置背景颜色
        arcade.set_background_color(arcade.color.LIGHT_STEEL_BLUE)
        
        # 创建UI管理器
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        
        # 创建一个垂直布局容器
        self.v_box = arcade.gui.UIBoxLayout()
        
        # 添加标题标签
        title_label = arcade.gui.UILabel(
            text="90后童年互动房间",
            font_size=30,
            width=400,
            align="center"
        )
        self.v_box.add(title_label.with_space_around(bottom=20))
        
        # 创建用户名输入框
        self.username_input = arcade.gui.UIInputText(
            text="玩家1",
            width=300,
            text_color=arcade.color.BLACK
        )
        username_field = arcade.gui.UILabel(text="用户名:", width=100, text_color=arcade.color.BLACK)
        username_layout = arcade.gui.UIBoxLayout(vertical=False)
        username_layout.add(username_field)
        username_layout.add(self.username_input)
        self.v_box.add(username_layout.with_space_around(bottom=15))
        
        # 创建密码输入框
        self.password_input = arcade.gui.UIInputText(
            text="",
            width=300,
            text_color=arcade.color.BLACK,
            password=True
        )
        password_field = arcade.gui.UILabel(text="密码:", width=100, text_color=arcade.color.BLACK)
        password_layout = arcade.gui.UIBoxLayout(vertical=False)
        password_layout.add(password_field)
        password_layout.add(self.password_input)
        self.v_box.add(password_layout.with_space_around(bottom=15))
        
        # 登录按钮
        login_button = arcade.gui.UIFlatButton(
            text="登录",
            width=200,
            style={
                "font_color": arcade.color.WHITE,
                "bg_color": arcade.color.DARK_BLUE_GRAY,
                "border_color": arcade.color.BLACK,
                "border_width": 2,
                "bg_color_pressed": arcade.color.GRAY_BLUE,
            }
        )
        
        # 将使用原始版本还是增强版的标志
        self.use_enhanced_version = False
        
        # 设置版本选择切换按钮
        version_switch = arcade.gui.UIFlatButton(
            text="切换到增强版",
            width=200,
            style={
                "font_color": arcade.color.WHITE,
                "bg_color": arcade.color.DARK_GREEN,
                "border_color": arcade.color.BLACK,
                "border_width": 2,
                "bg_color_pressed": arcade.color.GRAY_GREEN,
            }
        )
        
        # 版本切换按钮事件处理
        @version_switch.event("on_click")
        def on_version_switch(event):
            self.use_enhanced_version = not self.use_enhanced_version
            if self.use_enhanced_version:
                version_switch.text = "切换到基础版"
                version_switch.style["bg_color"] = arcade.color.DARK_RED
                version_switch.style["bg_color_pressed"] = arcade.color.GRAY_BROWN
            else:
                version_switch.text = "切换到增强版"
                version_switch.style["bg_color"] = arcade.color.DARK_GREEN
                version_switch.style["bg_color_pressed"] = arcade.color.GRAY_GREEN
        
        # 登录按钮事件处理
        @login_button.event("on_click")
        def on_login_button_click(event):
            # 这里可以添加真实的用户名密码验证逻辑
            # 为了演示，这里简单地允许任何登录
            # 根据版本选择启动不同的游戏
            if self.use_enhanced_version:
                game_view = EnhancedChildhoodRoom(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
            else:
                game_view = ChildhoodRoom(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
            
            # 设置游戏视图
            self.window.show_view(game_view)
        
        # 将按钮添加到布局中
        self.v_box.add(login_button.with_space_around(bottom=15))
        self.v_box.add(version_switch.with_space_around(bottom=15))
        
        # 创建一个UI框架并添加垂直布局
        frame = arcade.gui.UILayout()
        frame.add(self.v_box, align_x=SCREEN_WIDTH/2, align_y=SCREEN_HEIGHT/2, anchor_x="center", anchor_y="center")
        
        # 添加UI元素到管理器
        self.manager.add(frame)
    
    def on_draw(self):
        """渲染登录页面"""
        self.clear()
        self.manager.draw()
        
        # 绘制一些装饰元素，增加90后童年氛围
        # 绘制彩色气球
        for i in range(10):
            x = 50 + i * 100
            y = SCREEN_HEIGHT - 50
            arcade.draw_circle_filled(x, y, 20, arcade.color.random_color())
            arcade.draw_line(x, y - 20, x, y - 70, arcade.color.BLACK, 2)
        
        # 绘制底部提示文字
        arcade.draw_text(
            "登录以体验90后童年的回忆",
            x=SCREEN_WIDTH / 2,
            y=100,
            color=arcade.color.DARK_SLATE_GRAY,
            font_size=14,
            anchor_x="center"
        )
    
    def on_show_view(self):
        """显示视图时的处理"""
        arcade.set_background_color(arcade.color.LIGHT_STEEL_BLUE)
    
    def on_hide_view(self):
        """隐藏视图时的处理"""
        self.manager.disable()

def main():
    """主函数"""
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    login_view = LoginView()
    window.show_view(login_view)
    arcade.run()

if __name__ == "__main__":
    main() 