import arcade
import os
import math
import random
from interactive_room_game import InteractiveObject, Television, RemoteControl

# 常量定义
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
SCREEN_TITLE = "客厅场景"

# 资源路径
RESOURCES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources")

class LightEffect:
    """光照效果类"""
    def __init__(self, x, y, radius=200, intensity=0.8, color=arcade.color.YELLOW):
        self.x = x
        self.y = y
        self.radius = radius
        self.intensity = intensity
        self.color = color
        self.flicker_count = 0
        
    def draw(self, alpha=1.0, flicker=False):
        """绘制光照效果"""
        if flicker and random.random() > 0.95:
            # 随机闪烁效果
            alpha *= random.uniform(0.85, 1.0)
            
        # 绘制多层渐变光晕，使用更低的透明度和更少的图层
        for i in range(5):  # 减少图层数量
            radius = self.radius * (1 - i/5)
            alpha_i = alpha * (1 - i/5) * self.intensity * 0.5  # 降低整体透明度
            
            # 将alpha值裁剪到合理范围内
            alpha_i = min(max(alpha_i, 0), 1)
            
            light_color = list(self.color)
            light_color[3] = int(255 * alpha_i)
            
            arcade.draw_circle_filled(
                self.x, self.y, radius, light_color
            )

class Shadow:
    """阴影类"""
    def __init__(self, obj, light_source):
        self.obj = obj
        self.light_source = light_source
        self.shadow_color = (0, 0, 0, 80)  # 半透明黑色
    
    def draw(self):
        """绘制阴影"""
        # 计算物体到光源的方向
        dx = self.obj.x - self.light_source.x
        dy = self.obj.y - self.light_source.y
        
        # 阴影长度取决于物体到光源的距离
        distance = math.sqrt(dx*dx + dy*dy)
        if distance < 10:  # 防止除以零
            return
            
        # 标准化方向向量
        dx /= distance
        dy /= distance
        
        # 阴影长度和强度
        shadow_length = min(self.obj.height * 1.5, 150)
        shadow_intensity = min(1.0, 200 / distance) * 0.5  # 降低阴影强度
        
        # 计算阴影点
        shadow_points = []
        
        # 物体底部中心点
        bottom_x = self.obj.x
        bottom_y = self.obj.y - self.obj.height/2
        
        # 物体底部左右边缘点
        left_x = bottom_x - self.obj.width/2
        right_x = bottom_x + self.obj.width/2
        
        # 添加物体底部边缘点
        shadow_points.append((left_x, bottom_y))
        shadow_points.append((right_x, bottom_y))
        
        # 添加阴影投射点
        offset_x = dx * shadow_length
        offset_y = dy * shadow_length
        
        shadow_points.append((right_x + offset_x, bottom_y + offset_y))
        shadow_points.append((left_x + offset_x, bottom_y + offset_y))
        
        # 绘制阴影多边形
        shadow_color = (0, 0, 0, int(80 * shadow_intensity))  # 降低阴影透明度
        arcade.draw_polygon_filled(shadow_points, shadow_color)

class CeilingLamp(InteractiveObject):
    """吊灯类"""
    def __init__(self, x, y, light_color=arcade.color.YELLOW_ORANGE, size=80):
        color_with_alpha = light_color + (255,) if len(light_color) == 3 else light_color
        super().__init__(x, y, size, size, color=color_with_alpha)
        self.light_color = light_color
        self.size = size
        # 减小灯光半径
        self.light_effect = LightEffect(x, y, radius=size*2, color=self.light_color+(50,))
        self.brightness = 0.0
        self.target_brightness = 0.0
        self.transition_speed = 0.05
        
    def update(self):
        """更新灯光状态"""
        if self.is_active:
            self.target_brightness = 1.0
        else:
            self.target_brightness = 0.0
            
        # 平滑过渡灯光亮度
        if abs(self.brightness - self.target_brightness) > 0.01:
            self.brightness += (self.target_brightness - self.brightness) * self.transition_speed
        
    def draw(self, render_light=True):
        """绘制吊灯"""
        # 绘制灯具
        # 灯罩
        arcade.draw_circle_filled(
            self.x, self.y, self.size/2, 
            arcade.color.LIGHT_GRAY
        )
        
        # 灯绳
        arcade.draw_line(
            self.x, self.y + self.size/2,
            self.x, SCREEN_HEIGHT,
            arcade.color.BLACK, 3
        )
        
        # 灯光开启时绘制发光部分
        if self.brightness > 0:
            # 灯泡发光部分
            bulb_color = list(self.light_color) + [int(255 * self.brightness)]
            arcade.draw_circle_filled(
                self.x, self.y, self.size/3, 
                bulb_color
            )
            
            # 绘制光照效果（可选）
            if render_light:
                self.light_effect.draw(alpha=self.brightness * 0.7, flicker=True)  # 降低亮度

class FloorLamp(InteractiveObject):
    """落地灯类"""
    def __init__(self, x, y, light_color=arcade.color.YELLOW, height=200):
        super().__init__(x, y, 40, height, color=arcade.color.DARK_BROWN)
        self.light_color = light_color
        self.height = height
        # 减小灯光半径
        self.light_effect = LightEffect(x, y + height/2, radius=height*0.7, color=self.light_color+(50,))
        self.brightness = 0.0
        self.target_brightness = 0.0
        self.transition_speed = 0.05
        
    def update(self):
        """更新灯光状态"""
        if self.is_active:
            self.target_brightness = 1.0
        else:
            self.target_brightness = 0.0
            
        # 平滑过渡灯光亮度
        if abs(self.brightness - self.target_brightness) > 0.01:
            self.brightness += (self.target_brightness - self.brightness) * self.transition_speed
        
    def draw(self, render_light=True):
        """绘制落地灯"""
        # 绘制灯座
        arcade.draw_rectangle_filled(
            self.x, self.y - self.height/2 + 15, 60, 30, 
            color=arcade.color.DARK_BROWN
        )
        
        # 绘制灯杆
        arcade.draw_rectangle_filled(
            self.x, self.y - self.height/4, 10, self.height/2, 
            color=arcade.color.DARK_BROWN
        )
        
        # 绘制灯罩
        arcade.draw_ellipse_filled(
            self.x, self.y + self.height/4, 60, 80, 
            color=arcade.color.BEIGE
        )
        
        # 灯光开启时绘制发光部分
        if self.brightness > 0:
            # 灯泡发光部分
            bulb_color = list(self.light_color) + [int(255 * self.brightness)]
            arcade.draw_ellipse_filled(
                self.x, self.y + self.height/4, 40, 60, 
                bulb_color
            )
            
            # 绘制光照效果（可选）
            if render_light:
                self.light_effect.draw(alpha=self.brightness * 0.7, flicker=False)  # 降低亮度

class TVBacklight(InteractiveObject):
    """电视背光类"""
    def __init__(self, tv):
        super().__init__(tv.x, tv.y, tv.width + 40, tv.height + 40, color=arcade.color.BLUE_VIOLET)
        self.tv = tv
        self.colors = [
            arcade.color.BLUE,
            arcade.color.PURPLE,
            arcade.color.FUCHSIA,
            arcade.color.RED,
            arcade.color.ORANGE,
            arcade.color.YELLOW,
            arcade.color.GREEN,
            arcade.color.AQUA
        ]
        self.current_color_idx = 0
        self.color_transition = 0.0
        # 减小电视背光范围
        self.light_effect = LightEffect(tv.x, tv.y, radius=tv.width*0.7, color=self.colors[0]+(30,))
        self.brightness = 0.0
        self.is_active = False
        
    def update(self):
        """更新电视背光效果"""
        # 只有电视开启时才显示背光
        if self.tv.is_active and self.is_active:
            # 颜色渐变过渡
            self.color_transition += 0.01
            if self.color_transition >= 1.0:
                self.color_transition = 0.0
                self.current_color_idx = (self.current_color_idx + 1) % len(self.colors)
                
            self.brightness = 1.0
        else:
            self.brightness = 0.0
            
        # 更新光照效果颜色
        current_color = self.colors[self.current_color_idx]
        next_color = self.colors[(self.current_color_idx + 1) % len(self.colors)]
        
        # 颜色插值
        r = int(current_color[0] * (1 - self.color_transition) + next_color[0] * self.color_transition)
        g = int(current_color[1] * (1 - self.color_transition) + next_color[1] * self.color_transition)
        b = int(current_color[2] * (1 - self.color_transition) + next_color[2] * self.color_transition)
        
        self.light_effect.color = (r, g, b, 30)
        
    def draw(self, render_light=True):
        """绘制电视背光"""
        if self.brightness <= 0:
            return
            
        # 绘制电视背光效果
        if render_light:
            self.light_effect.draw(alpha=self.brightness * 0.6)  # 降低亮度
    
    def on_click(self):
        """点击事件处理"""
        self.is_active = not self.is_active
        return self.is_active

class LightSwitch(InteractiveObject):
    """灯光开关类"""
    def __init__(self, x, y, lights=None):
        super().__init__(x, y, 40, 60, color=arcade.color.WHITE)
        self.lights = lights or []
        
    def draw(self):
        """绘制灯光开关"""
        # 绘制开关面板
        arcade.draw_rectangle_filled(
            self.x, self.y, self.width, self.height, 
            color=self.color
        )
        
        # 绘制开关按钮
        button_color = arcade.color.YELLOW if self.is_active else arcade.color.GRAY
        button_y = self.y + 10 if self.is_active else self.y - 10
        
        arcade.draw_rectangle_filled(
            self.x, button_y, self.width - 10, self.height/3,
            color=button_color
        )
        
    def on_click(self):
        """点击事件处理"""
        self.is_active = not self.is_active
        
        # 控制关联的灯光
        for light in self.lights:
            light.is_active = self.is_active
            
        return self.is_active

class LightingRenderer:
    """光照渲染器类 - 用于分层渲染光照和阴影效果"""
    def __init__(self):
        self.light_sources = []
        self.objects = []
        self.shadows = []
        
    def add_light(self, light):
        """添加光源"""
        self.light_sources.append(light)
        
    def add_object(self, obj):
        """添加物体"""
        self.objects.append(obj)
        
        # 为每个物体创建阴影
        for light in self.light_sources:
            # 只为较大的物体创建阴影
            if isinstance(obj, (Sofa, CoffeeTable)) and not isinstance(obj, (LightSwitch, RemoteControl)):
                shadow = Shadow(obj, light)
                self.shadows.append(shadow)
    
    def render_scene_base(self, env_brightness):
        """渲染场景基础部分"""
        # 计算房间基础颜色
        bg_color = (
            int(40 + 200 * env_brightness),
            int(40 + 200 * env_brightness),
            int(50 + 180 * env_brightness)
        )
        
        # 绘制背景墙壁
        arcade.draw_rectangle_filled(
            SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT,
            color=bg_color
        )
        
        # 绘制地板
        floor_color = (
            int(40 + 100 * env_brightness),
            int(20 + 60 * env_brightness),
            int(0 + 40 * env_brightness)
        )
        arcade.draw_rectangle_filled(
            SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4, SCREEN_WIDTH, SCREEN_HEIGHT // 2,
            color=floor_color
        )
        
        # 绘制窗户
        window_color = (
            int(100 + 100 * env_brightness),
            int(150 + 80 * env_brightness),
            int(200 + 50 * env_brightness)
        )
        arcade.draw_rectangle_filled(
            SCREEN_WIDTH - 200, SCREEN_HEIGHT - 150, 200, 150,
            color=window_color
        )
        arcade.draw_rectangle_outline(
            SCREEN_WIDTH - 200, SCREEN_HEIGHT - 150, 200, 150,
            color=arcade.color.BLACK, border_width=5
        )
    
    def render_shadows(self):
        """渲染阴影"""
        for shadow in self.shadows:
            light = shadow.light_source
            # 只渲染亮着的灯的阴影
            if getattr(light, "brightness", 0) > 0.3:
                shadow.draw()
    
    def render_objects(self):
        """渲染场景物体"""
        # 先渲染非光源物体
        non_lights = [obj for obj in self.objects if obj not in self.light_sources]
        for obj in non_lights:
            obj.draw()
    
    def render_lights(self, render_effects=True):
        """渲染光源"""
        # 渲染光源物体，但不渲染光效
        for light in self.light_sources:
            light.draw(render_light=False)  # 先只渲染灯具，不渲染光效
    
    def render_light_effects(self):
        """渲染光效"""
        # 使用混合模式单独渲染所有光效
        for light in self.light_sources:
            if isinstance(light, (CeilingLamp, FloorLamp, TVBacklight)) and getattr(light, "brightness", 0) > 0:
                light.draw(render_light=True)  # 只渲染光效
                
    def calculate_environment_brightness(self):
        """计算环境亮度"""
        env_brightness = 0.1  # 基础亮度
        for light in self.light_sources:
            env_brightness += getattr(light, "brightness", 0) * 0.15  # 降低灯光对整体亮度的影响
        
        return min(env_brightness, 1.0)

class Sofa(InteractiveObject):
    """沙发类"""
    def __init__(self, x, y):
        super().__init__(x, y, 300, 120, color=arcade.color.BROWN)
        self.is_occupied = False
        
    def draw(self):
        """绘制沙发"""
        # 绘制沙发主体
        arcade.draw_rectangle_filled(
            self.x, self.y, self.width, self.height, 
            color=self.color
        )
        
        # 绘制沙发靠背
        arcade.draw_rectangle_filled(
            self.x, self.y + self.height/2 - 20, self.width, 40,
            color=arcade.color.DARK_BROWN
        )
        
        # 绘制沙发垫子
        for i in range(3):
            offset = (i - 1) * 90
            arcade.draw_rectangle_filled(
                self.x + offset, self.y - 20, 80, self.height - 40,
                color=arcade.color.BEIGE
            )
            
        # 如果有人坐在沙发上
        if self.is_occupied:
            arcade.draw_text(
                "有人坐在这里",
                self.x - 70, self.y - 10,
                arcade.color.BLACK, 14
            )
    
    def on_click(self):
        """点击事件处理"""
        self.is_occupied = not self.is_occupied
        return self.is_occupied

class CoffeeTable(InteractiveObject):
    """茶几类"""
    def __init__(self, x, y):
        super().__init__(x, y, 180, 100, color=arcade.color.LIGHT_BROWN)
        self.items = []
        
    def draw(self):
        """绘制茶几"""
        # 绘制茶几桌面
        arcade.draw_rectangle_filled(
            self.x, self.y, self.width, self.height/3, 
            color=self.color
        )
        
        # 绘制茶几腿
        for i in range(4):
            x_offset = self.width/2 - 20 if i in [0, 2] else -self.width/2 + 20
            y_offset = self.height/3 - 10 if i in [0, 1] else -self.height/3 + 10
            
            arcade.draw_rectangle_filled(
                self.x + x_offset, self.y + y_offset, 10, self.height*2/3,
                color=arcade.color.DARK_BROWN
            )
            
        # 绘制茶几上的物品
        if self.is_active:
            arcade.draw_circle_filled(
                self.x, self.y + 30, 20, arcade.color.ORANGE
            )
            arcade.draw_text(
                "茶杯",
                self.x - 20, self.y + 40,
                arcade.color.BLACK, 12
            )

class LivingRoom(arcade.Window):
    """客厅场景类"""
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.WHITE)
        
        # 创建资源目录
        os.makedirs(RESOURCES_DIR, exist_ok=True)
        
        # 初始化渲染器
        self.renderer = LightingRenderer()
        
        # 交互对象列表
        self.interactive_objects = []
        self.lights = []
        
        # 初始化各个交互对象
        self.tv = Television(width // 2, height // 2 + 150)
        self.remote = RemoteControl(width // 2 + 200, height // 2 - 150)
        self.sofa = Sofa(width // 2, height // 2 - 100)
        self.coffee_table = CoffeeTable(width // 2, height // 2)
        
        # 初始化灯光
        self.ceiling_lamp = CeilingLamp(width // 2, height - 150)
        self.floor_lamp_left = FloorLamp(width // 4, height // 2 - 50)
        self.floor_lamp_right = FloorLamp(width * 3 // 4, height // 2 - 50)
        self.tv_backlight = TVBacklight(self.tv)
        
        # 添加灯光到列表
        self.lights.extend([
            self.ceiling_lamp,
            self.floor_lamp_left,
            self.floor_lamp_right,
            self.tv_backlight
        ])
        
        # 添加灯光到渲染器
        for light in self.lights:
            self.renderer.add_light(light)
        
        # 创建灯光开关
        self.main_light_switch = LightSwitch(
            width - 50, height // 2 + 200,
            lights=[self.ceiling_lamp]
        )
        
        self.floor_lamp_switch = LightSwitch(
            width - 50, height // 2 + 120,
            lights=[self.floor_lamp_left, self.floor_lamp_right]
        )
        
        self.tv_backlight_switch = LightSwitch(
            width - 50, height // 2 + 40,
            lights=[self.tv_backlight]
        )
        
        # 添加所有对象到交互列表
        self.interactive_objects.extend([
            self.tv, self.remote, self.sofa, 
            self.coffee_table,
            self.ceiling_lamp, self.floor_lamp_left, self.floor_lamp_right,
            self.tv_backlight,
            self.main_light_switch, self.floor_lamp_switch, self.tv_backlight_switch
        ])
        
        # 添加物体到渲染器
        for obj in self.interactive_objects:
            self.renderer.add_object(obj)
        
        # 设置更新间隔
        self.set_update_rate(1/60)
        
        # 默认开启主灯
        self.main_light_switch.is_active = True
        self.ceiling_lamp.is_active = True
        
        # 渲染模式
        self.use_deferred_lighting = True
    
    def on_update(self, delta_time):
        """更新场景状态"""
        # 更新所有灯光
        for light in self.lights:
            light.update()
    
    def on_draw(self):
        """渲染游戏画面"""
        arcade.start_render()
        
        # 计算环境亮度
        env_brightness = self.renderer.calculate_environment_brightness()
        
        if self.use_deferred_lighting:
            # 分层渲染 - 更真实的光照效果
            # 1. 渲染场景基础
            self.renderer.render_scene_base(env_brightness)
            
            # 2. 先渲染阴影
            self.renderer.render_shadows()
            
            # 3. 渲染物体
            self.renderer.render_objects()
            
            # 4. 渲染光源（不含光效）
            self.renderer.render_lights(render_effects=False)
            
            # 5. 单独渲染光效
            self.renderer.render_light_effects()
        else:
            # 简单渲染 - 旧的渲染方式
            # 房间基础颜色
            bg_color = (
                int(40 + 200 * env_brightness),
                int(40 + 200 * env_brightness),
                int(50 + 180 * env_brightness)
            )
            
            # 绘制背景墙壁
            arcade.draw_rectangle_filled(
                SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT,
                color=bg_color
            )
            
            # 绘制地板
            floor_color = (
                int(40 + 100 * env_brightness),
                int(20 + 60 * env_brightness),
                int(0 + 40 * env_brightness)
            )
            arcade.draw_rectangle_filled(
                SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4, SCREEN_WIDTH, SCREEN_HEIGHT // 2,
                color=floor_color
            )
            
            # 绘制窗户
            window_color = (
                int(100 + 100 * env_brightness),
                int(150 + 80 * env_brightness),
                int(200 + 50 * env_brightness)
            )
            arcade.draw_rectangle_filled(
                SCREEN_WIDTH - 200, SCREEN_HEIGHT - 150, 200, 150,
                color=window_color
            )
            arcade.draw_rectangle_outline(
                SCREEN_WIDTH - 200, SCREEN_HEIGHT - 150, 200, 150,
                color=arcade.color.BLACK, border_width=5
            )
            
            # 绘制电视背光
            self.tv_backlight.draw()
            
            # 绘制不发光的对象
            non_lights = [obj for obj in self.interactive_objects if obj not in self.lights]
            for obj in non_lights:
                obj.draw()
                
            # 绘制灯光效果
            for light in self.lights:
                if isinstance(light, (CeilingLamp, FloorLamp)):
                    light.draw()
        
        # 绘制使用说明
        text_color = arcade.color.WHITE if env_brightness < 0.5 else arcade.color.BLACK
        arcade.draw_text(
            text="点击物体与之交互:\n- 电视右下角按钮开/关机\n- 点击遥控器切换频道\n- 点击沙发坐下/起身\n- 点击茶几放置/移除物品\n- 墙上三个开关控制不同灯光 (R键切换渲染模式)",
            start_x=20, start_y=SCREEN_HEIGHT - 120, 
            color=text_color, font_size=14
        )
    
    def on_key_press(self, key, modifiers):
        """键盘按键事件处理"""
        if key == arcade.key.R:
            # 按R键切换渲染模式
            self.use_deferred_lighting = not self.use_deferred_lighting
    
    def on_mouse_press(self, x, y, button, modifiers):
        """鼠标点击事件处理"""
        # 检查点击的是否为遥控器
        if self.remote.is_clicked(x, y):
            self.tv.change_channel()
            return
        
        # 检查点击的是否为灯光开关
        if self.main_light_switch.is_clicked(x, y):
            self.main_light_switch.on_click()
            return
            
        if self.floor_lamp_switch.is_clicked(x, y):
            self.floor_lamp_switch.on_click()
            return
            
        if self.tv_backlight_switch.is_clicked(x, y):
            self.tv_backlight_switch.on_click()
            return
        
        # 检查其他交互对象
        for obj in self.interactive_objects:
            if obj.is_clicked(x, y):
                obj.on_click()
                break

def main():
    """主函数 - 创建客厅窗口并运行游戏"""
    game = LivingRoom(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()

if __name__ == "__main__":
    main() 