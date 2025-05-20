import arcade
import random
import math

class BedroomItem:
    """卧室物品基类，定义所有可交互物品的基本属性和方法"""
    
    def __init__(self, x, y, width, height, name):
        """
        初始化卧室物品
        
        参数:
            x (float): 物品中心的X坐标
            y (float): 物品中心的Y坐标
            width (float): 物品宽度
            height (float): 物品高度
            name (str): 物品名称
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.name = name
        self.is_hovered = False  # 鼠标是否悬停在物品上
        self.is_active = False   # 物品是否被激活(例如被点击)
        self.message = ""        # 物品的交互消息
    
    def draw(self):
        """绘制物品，需要在子类中实现"""
        pass
    
    def draw_hover_effect(self):
        """绘制鼠标悬停效果"""
        if self.is_hovered:
            # 绘制轮廓
            arcade.draw_rectangle_outline(
                self.x, self.y, self.width + 10, self.height + 10,
                arcade.color.YELLOW, 2
            )
            
            # 在物品上方绘制名称标签
            arcade.draw_text(
                self.name,
                start_x=self.x,
                start_y=self.y + self.height/2 + 15,
                color=arcade.color.BLACK,
                font_size=12,
                anchor_x="center"
            )
    
    def is_clicked(self, x, y):
        """
        检测物品是否被点击
        
        参数:
            x (float): 点击位置的X坐标
            y (float): 点击位置的Y坐标
            
        返回:
            bool: 如果点击位置在物品范围内，返回True，否则返回False
        """
        return (self.x - self.width/2 <= x <= self.x + self.width/2 and
                self.y - self.height/2 <= y <= self.y + self.height/2)
    
    def is_mouse_over(self, x, y):
        """
        检测鼠标是否悬停在物品上
        
        参数:
            x (float): 鼠标位置的X坐标
            y (float): 鼠标位置的Y坐标
            
        返回:
            bool: 如果鼠标位置在物品范围内，返回True，否则返回False
        """
        result = self.is_clicked(x, y)
        self.is_hovered = result
        return result
    
    def on_click(self):
        """
        点击物品时的处理，在子类中实现具体逻辑
        
        返回:
            str: 返回交互消息
        """
        self.is_active = not self.is_active
        self.message = f"你点击了{self.name}"
        return self.message


class Bed(BedroomItem):
    """床，可以用来休息"""
    
    def __init__(self, x, y, width=300, height=150):
        """
        初始化床
        
        参数:
            x (float): 床中心的X坐标
            y (float): 床中心的Y坐标
            width (float): 床宽度，默认300
            height (float): 床高度，默认150
        """
        super().__init__(x, y, width, height, "床")
        self.messages = [
            "睡觉是孩子的天性，但是暑假作业还没写完...",
            "小憩一下，回忆起小时候午睡的时光",
            "还记得小时候玩累了就能睡个午觉吗？",
            "床上放着几个毛绒玩具，都是儿时的好伙伴"
        ]
    
    def draw(self):
        """绘制床"""
        # 床架
        arcade.draw_rectangle_filled(
            self.x, self.y, self.width, self.height,
            arcade.color.BROWN
        )
        
        # 床垫
        arcade.draw_rectangle_filled(
            self.x, self.y + self.height * 0.1,
            self.width * 0.9, self.height * 0.6,
            arcade.color.WHITE
        )
        
        # 枕头
        arcade.draw_rectangle_filled(
            self.x - self.width * 0.25, self.y + self.height * 0.2,
            self.width * 0.3, self.height * 0.3,
            arcade.color.LIGHT_BLUE
        )
        
        # 被子
        arcade.draw_rectangle_filled(
            self.x + self.width * 0.05, self.y + self.height * 0.1,
            self.width * 0.6, self.height * 0.5,
            arcade.color.PINK
        )
        
        # 绘制毛绒玩具
        if not self.is_active:  # 只在床没被激活时显示玩具
            # 小熊
            arcade.draw_circle_filled(
                self.x - self.width * 0.1, 
                self.y + self.height * 0.25,
                15, arcade.color.BROWN
            )
            # 熊耳朵
            arcade.draw_circle_filled(
                self.x - self.width * 0.1 - 8, 
                self.y + self.height * 0.25 + 10,
                5, arcade.color.BROWN
            )
            arcade.draw_circle_filled(
                self.x - self.width * 0.1 + 8, 
                self.y + self.height * 0.25 + 10,
                5, arcade.color.BROWN
            )
        
        # 绘制悬停效果
        self.draw_hover_effect()
    
    def on_click(self):
        """点击床时的处理"""
        self.is_active = not self.is_active
        self.message = random.choice(self.messages)
        return self.message


class Desk(BedroomItem):
    """书桌，可以用来学习或玩电脑"""
    
    def __init__(self, x, y, width=200, height=100):
        """
        初始化书桌
        
        参数:
            x (float): 书桌中心的X坐标
            y (float): 书桌中心的Y坐标
            width (float): 书桌宽度，默认200
            height (float): 书桌高度，默认100
        """
        super().__init__(x, y, width, height, "书桌")
        self.messages = [
            "这张书桌见证了无数做作业到深夜的时光",
            "书桌上还放着一些学习用品，勾起了上学时的回忆",
            "书桌旁边有一盏台灯，陪伴我度过了许多学习的夜晚",
            "书桌抽屉里好像塞着一些小秘密"
        ]
    
    def draw(self):
        """绘制书桌"""
        # 桌面
        arcade.draw_rectangle_filled(
            self.x, self.y, self.width, self.height * 0.1,
            arcade.color.BROWN
        )
        
        # 桌腿
        arcade.draw_rectangle_filled(
            self.x - self.width * 0.4, self.y - self.height * 0.4,
            self.width * 0.1, self.height * 0.8,
            arcade.color.BROWN
        )
        arcade.draw_rectangle_filled(
            self.x + self.width * 0.4, self.y - self.height * 0.4,
            self.width * 0.1, self.height * 0.8,
            arcade.color.BROWN
        )
        
        # 桌上物品
        # 台灯
        arcade.draw_rectangle_filled(
            self.x - self.width * 0.3, self.y + self.height * 0.2,
            self.width * 0.1, self.height * 0.3,
            arcade.color.DARK_GRAY
        )
        arcade.draw_circle_filled(
            self.x - self.width * 0.3, self.y + self.height * 0.4,
            self.width * 0.08,
            arcade.color.YELLOW if self.is_active else arcade.color.LIGHT_GRAY
        )
        
        # 书本
        book_colors = [arcade.color.RED, arcade.color.GREEN, arcade.color.BLUE]
        for i in range(3):
            arcade.draw_rectangle_filled(
                self.x + self.width * 0.2 - i * 10, 
                self.y + self.height * 0.1 + i * 10,
                self.width * 0.2, self.height * 0.05,
                book_colors[i]
            )
        
        # 铅笔
        arcade.draw_line(
            self.x + self.width * 0.1, self.y + self.height * 0.05,
            self.x + self.width * 0.3, self.y + self.height * 0.05,
            arcade.color.YELLOW, 3
        )
        
        # 绘制悬停效果
        self.draw_hover_effect()
    
    def on_click(self):
        """点击书桌时的处理"""
        self.is_active = not self.is_active
        self.message = random.choice(self.messages)
        return self.message


class Computer(BedroomItem):
    """电脑，可以用来玩游戏或者上网"""
    
    def __init__(self, x, y, width=100, height=80):
        """
        初始化电脑
        
        参数:
            x (float): 电脑中心的X坐标
            y (float): 电脑中心的Y坐标
            width (float): 电脑宽度，默认100
            height (float): 电脑高度，默认80
        """
        super().__init__(x, y, width, height, "电脑")
        self.messages = [
            "这台电脑承载了多少网络游戏的回忆啊",
            "还记得小时候偷偷玩电脑被发现的紧张感吗？",
            "电脑里有QQ、红警、仙剑奇侠传...",
            "曾经的大哥大，如今成了古董",
            "没网的时候，还能玩扫雷和纸牌"
        ]
        self.screen_colors = [
            arcade.color.BLUE,
            arcade.color.GREEN,
            arcade.color.RED,
            arcade.color.PURPLE
        ]
        self.current_screen = 0
    
    def draw(self):
        """绘制电脑"""
        # 绘制显示器
        arcade.draw_rectangle_filled(
            self.x, self.y + self.height * 0.1,
            self.width, self.height * 0.6,
            arcade.color.DARK_GRAY
        )
        
        # 绘制屏幕
        if self.is_active:
            screen_color = self.screen_colors[self.current_screen]
        else:
            screen_color = arcade.color.BLACK
        
        arcade.draw_rectangle_filled(
            self.x, self.y + self.height * 0.1,
            self.width * 0.8, self.height * 0.5,
            screen_color
        )
        
        # 绘制显示器底座
        arcade.draw_rectangle_filled(
            self.x, self.y - self.height * 0.2,
            self.width * 0.5, self.height * 0.1,
            arcade.color.DARK_GRAY
        )
        
        # 绘制键盘
        arcade.draw_rectangle_filled(
            self.x, self.y - self.height * 0.4,
            self.width * 1.2, self.height * 0.15,
            arcade.color.LIGHT_GRAY
        )
        
        # 绘制鼠标
        arcade.draw_circle_filled(
            self.x + self.width * 0.4, self.y - self.height * 0.4,
            self.width * 0.1,
            arcade.color.LIGHT_GRAY
        )
        
        # 如果电脑开着，画一些屏幕元素
        if self.is_active:
            if self.current_screen == 0:  # QQ界面
                # 绘制QQ图标
                arcade.draw_circle_filled(
                    self.x, self.y + self.height * 0.1,
                    10, arcade.color.WHITE
                )
                # 绘制企鹅身体
                arcade.draw_circle_filled(
                    self.x, self.y + self.height * 0.05,
                    15, arcade.color.BLACK
                )
            elif self.current_screen == 1:  # 游戏界面
                # 绘制游戏场景（简单的格子）
                for i in range(3):
                    for j in range(3):
                        arcade.draw_rectangle_outline(
                            self.x - 20 + i * 20, self.y + self.height * 0.1 - 20 + j * 20,
                            15, 15, arcade.color.WHITE, 1
                        )
            elif self.current_screen == 2:  # 网页浏览
                # 绘制网页结构
                arcade.draw_rectangle_filled(
                    self.x, self.y + self.height * 0.3,
                    self.width * 0.7, self.height * 0.1,
                    arcade.color.WHITE
                )
                # 几行文本
                for i in range(3):
                    arcade.draw_rectangle_filled(
                        self.x, self.y + self.height * 0.1 - i * 15,
                        self.width * 0.7, 5,
                        arcade.color.WHITE
                    )
            elif self.current_screen == 3:  # 聊天窗口
                # 聊天消息框
                arcade.draw_rectangle_filled(
                    self.x, self.y + self.height * 0.2,
                    self.width * 0.7, self.height * 0.3,
                    arcade.color.WHITE
                )
                # 输入框
                arcade.draw_rectangle_filled(
                    self.x, self.y,
                    self.width * 0.7, self.height * 0.1,
                    arcade.color.WHITE
                )
        
        # 绘制悬停效果
        self.draw_hover_effect()
    
    def on_click(self):
        """点击电脑时的处理"""
        if self.is_active:
            # 如果电脑已经开着，切换屏幕
            self.current_screen = (self.current_screen + 1) % len(self.screen_colors)
            self.message = f"你切换到了{'QQ|游戏|网页|聊天'.split('|')[self.current_screen]}界面"
        else:
            # 开机
            self.is_active = True
            self.message = "电脑开机了，满满的都是回忆..."
        
        return self.message
    
    def on_right_click(self):
        """右键点击电脑时的处理，关机"""
        if self.is_active:
            self.is_active = False
            self.message = "你关闭了电脑"
        else:
            self.message = "电脑已经关机了"
        
        return self.message


class HomeworkBook(BedroomItem):
    """暑假作业本，可以用来做作业"""
    
    def __init__(self, x, y, width=70, height=100):
        """
        初始化暑假作业本
        
        参数:
            x (float): 作业本中心的X坐标
            y (float): 作业本中心的Y坐标
            width (float): 作业本宽度，默认70
            height (float): 作业本高度，默认100
        """
        super().__init__(x, y, width, height, "暑假作业")
        self.progress = 0  # 作业完成进度，0-100
        self.messages = [
            "暑假作业，永远写不完的噩梦...",
            "每次开学前的最后一天都在疯狂赶作业",
            "还记得那些被各种饮料泡过的作业本吗？",
            "老师：开学检查暑假作业！学生：瑟瑟发抖",
            "有道数学题一直不会做，只能空着了"
        ]
    
    def draw(self):
        """绘制暑假作业本"""
        # 绘制作业本
        arcade.draw_rectangle_filled(
            self.x, self.y, self.width, self.height,
            arcade.color.ORANGE_RED
        )
        
        # 绘制作业本封面标题
        arcade.draw_text(
            "暑假\n作业",
            start_x=self.x,
            start_y=self.y + 15,
            color=arcade.color.BLACK,
            font_size=12,
            anchor_x="center",
            anchor_y="center",
            align="center"
        )
        
        # 如果作业本被激活，显示内页
        if self.is_active:
            # 打开的作业本
            arcade.draw_rectangle_filled(
                self.x - self.width * 0.6, self.y, self.width, self.height,
                arcade.color.WHITE
            )
            arcade.draw_rectangle_filled(
                self.x + self.width * 0.6, self.y, self.width, self.height,
                arcade.color.WHITE
            )
            
            # 绘制作业进度条
            progress_width = self.width * 0.8 * (self.progress / 100)
            arcade.draw_rectangle_filled(
                self.x - self.width * 0.6 - (self.width * 0.8 - progress_width)/2, 
                self.y - self.height * 0.3,
                progress_width, 10,
                arcade.color.GREEN
            )
            arcade.draw_rectangle_outline(
                self.x - self.width * 0.6, self.y - self.height * 0.3,
                self.width * 0.8, 10,
                arcade.color.BLACK, 1
            )
            
            # 绘制进度文字
            arcade.draw_text(
                f"完成: {self.progress}%",
                start_x=self.x - self.width * 0.6,
                start_y=self.y - self.height * 0.3 - 15,
                color=arcade.color.BLACK,
                font_size=10,
                anchor_x="center"
            )
            
            # 右侧页面绘制一些文字和练习题
            arcade.draw_text(
                "练习题:\n1. 1+1=?\n2. 2+2=?\n3. ...",
                start_x=self.x + self.width * 0.3,
                start_y=self.y + self.height * 0.3,
                color=arcade.color.BLACK,
                font_size=8,
                width=self.width * 0.9
            )
        
        # 绘制悬停效果
        self.draw_hover_effect()
    
    def on_click(self):
        """点击作业本时的处理"""
        self.is_active = not self.is_active
        
        if self.is_active:
            self.message = random.choice(self.messages)
        else:
            self.message = "你合上了暑假作业本，还有这么多没写完..."
        
        return self.message
    
    def do_homework(self):
        """做作业，增加进度"""
        if self.is_active:
            if self.progress < 100:
                # 随机增加1-5的进度
                increase = random.randint(1, 5)
                self.progress = min(100, self.progress + increase)
                self.message = f"你写了一会儿作业，进度增加了{increase}%，当前完成{self.progress}%"
            else:
                self.message = "作业已经全部完成了！可以出去玩了！"
        else:
            self.message = "要先打开作业本才能写作业"
        
        return self.message


class Window(BedroomItem):
    """窗户，可以看到窗外的风景"""
    
    def __init__(self, x, y, width=180, height=200):
        """
        初始化窗户
        
        参数:
            x (float): 窗户中心的X坐标
            y (float): 窗户中心的Y坐标
            width (float): 窗户宽度，默认180
            height (float): 窗户高度，默认200
        """
        super().__init__(x, y, width, height, "窗户")
        self.is_open = False  # 窗户是否打开
        self.day_time = "night"  # 白天或夜晚
        self.messages = {
            "night": [
                "窗外的夜空繁星点点，让人想起小时候数星星的夜晚",
                "夏夜的风轻轻吹进来，带着一丝凉意",
                "远处传来蛙鸣和蝉鸣声，夏夜的声音",
                "看着窗外的月亮，想起了小时候听过的嫦娥奔月的故事"
            ],
            "day": [
                "阳光透过窗户洒进来，照在地板上",
                "窗外的树上有知了在叫，是夏天的声音",
                "看到窗外的小朋友在玩耍，真想出去和他们一起玩",
                "蓝天白云，是记忆中暑假午后的标配"
            ]
        }
        
        # 窗外的星星
        self.stars = []
        for _ in range(20):
            self.stars.append({
                'x': random.randint(int(self.x - self.width/2), int(self.x + self.width/2)),
                'y': random.randint(int(self.y - self.height/2), int(self.y + self.height/2)),
                'size': random.uniform(1, 3),
                'twinkle_speed': random.uniform(1, 3),
                'alpha': random.randint(100, 255)
            })
        
        # 窗外的云朵
        self.clouds = []
        for _ in range(3):
            self.clouds.append({
                'x': random.randint(int(self.x - self.width/2), int(self.x + self.width/2)),
                'y': random.randint(int(self.y - self.height/4), int(self.y + self.height/4)),
                'size': random.uniform(20, 40),
                'speed': random.uniform(0.2, 0.5) * random.choice([-1, 1]),
            })
        
        # 计时器
        self.total_time = 0
    
    def update(self, delta_time):
        """
        更新窗外的动画
        
        参数:
            delta_time (float): 自上次更新以来的时间，以秒为单位
        """
        self.total_time += delta_time
        
        # 更新星星闪烁
        for star in self.stars:
            # 根据时间和各自速度调整星星的alpha值
            star['alpha'] = 128 + int(127 * math.sin(self.total_time * star['twinkle_speed']))
        
        # 更新云朵位置
        for cloud in self.clouds:
            cloud['x'] += cloud['speed']
            # 如果云朵移出窗口，重新放到另一边
            if cloud['x'] > self.x + self.width/2 + cloud['size']:
                cloud['x'] = self.x - self.width/2 - cloud['size']
            elif cloud['x'] < self.x - self.width/2 - cloud['size']:
                cloud['x'] = self.x + self.width/2 + cloud['size']
    
    def draw(self):
        """绘制窗户"""
        # 绘制窗框
        arcade.draw_rectangle_outline(
            self.x, self.y, self.width, self.height,
            arcade.color.BROWN, 8
        )
        
        # 绘制窗户的十字框
        arcade.draw_line(
            self.x - self.width/2, self.y,
            self.x + self.width/2, self.y,
            arcade.color.BROWN, 5
        )
        arcade.draw_line(
            self.x, self.y - self.height/2,
            self.x, self.y + self.height/2,
            arcade.color.BROWN, 5
        )
        
        # 窗外的景色取决于时间
        if self.day_time == "night":
            # 夜晚
            # 绘制窗外的夜空
            arcade.draw_rectangle_filled(
                self.x, self.y, self.width - 10, self.height - 10,
                arcade.color.DARK_BLUE
            )
            
            # 绘制月亮
            arcade.draw_circle_filled(
                self.x - 40, self.y + 40, 25,
                arcade.color.YELLOW
            )
            
            # 绘制星星
            for star in self.stars:
                arcade.draw_circle_filled(
                    star['x'], star['y'], star['size'],
                    (255, 255, 255, star['alpha'])
                )
        else:
            # 白天
            # 绘制窗外的蓝天
            arcade.draw_rectangle_filled(
                self.x, self.y, self.width - 10, self.height - 10,
                arcade.color.SKY_BLUE
            )
            
            # 绘制太阳
            arcade.draw_circle_filled(
                self.x + 40, self.y + 40, 25,
                arcade.color.YELLOW
            )
            
            # 绘制云朵
            for cloud in self.clouds:
                self.draw_cloud(cloud['x'], cloud['y'], cloud['size'])
        
        # 如果窗户打开，绘制打开的窗户
        if self.is_open:
            # 打开的窗户（一半透明）
            arcade.draw_rectangle_filled(
                self.x - self.width/4, self.y, self.width/2 - 10, self.height - 20,
                (200, 200, 200, 150)  # 半透明
            )
        
        # 绘制悬停效果
        self.draw_hover_effect()
    
    def draw_cloud(self, x, y, size):
        """
        绘制云朵
        
        参数:
            x (float): 云朵中心的X坐标
            y (float): 云朵中心的Y坐标
            size (float): 云朵大小
        """
        arcade.draw_circle_filled(x, y, size, arcade.color.WHITE)
        arcade.draw_circle_filled(x + size*0.6, y, size*0.7, arcade.color.WHITE)
        arcade.draw_circle_filled(x - size*0.6, y, size*0.7, arcade.color.WHITE)
        arcade.draw_circle_filled(x + size*0.3, y + size*0.3, size*0.7, arcade.color.WHITE)
        arcade.draw_circle_filled(x - size*0.3, y + size*0.3, size*0.7, arcade.color.WHITE)
    
    def on_click(self):
        """点击窗户时的处理"""
        self.is_open = not self.is_open
        
        if self.is_open:
            self.message = "你打开了窗户，" + random.choice(self.messages[self.day_time])
        else:
            self.message = "你关上了窗户"
        
        return self.message
    
    def change_time(self):
        """切换白天和黑夜"""
        if self.day_time == "night":
            self.day_time = "day"
            self.message = "天亮了，又是美好的一天"
        else:
            self.day_time = "night"
            self.message = "夜幕降临，繁星点点"
        
        return self.message 