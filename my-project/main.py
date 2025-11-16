from manim import *
import numpy as np

class SemicircleProblem(Scene):
    def __init__(self):
        super().__init__()
        self.camera.frame_width = 14
        self.camera.frame_height = 8
    
    def construct(self):
        self.camera.background_color = BLACK
        
        # === ПРАВИЛЬНАЯ ГЕОМЕТРИЯ ===
        R_big = 3.0  # Радиус большой полуокружности
        
        # Большая полуокружность (вверх) - ТОЛЩЕ
        semicircle = Arc(
            radius=R_big,
            start_angle=0,
            angle=PI,
            color=RED,
            stroke_width=6
        )
        
        # Диаметр AB - ТОЛЩЕ
        A = LEFT * R_big
        B = RIGHT * R_big
        diameter = Line(A, B, color=WHITE, stroke_width=4)
        
        self.play(Create(semicircle), run_time=2)
        self.play(Create(diameter), run_time=1)
        
        # Точки A и B
        dot_A = Dot(A, color=WHITE, radius=0.1)
        dot_B = Dot(B, color=WHITE, radius=0.1)
        label_A = Text("A", font_size=32, color=WHITE).next_to(A, DOWN, buff=0.2)
        label_B = Text("B", font_size=32, color=WHITE).next_to(B, DOWN, buff=0.2)
        
        self.play(
            Create(dot_A), Write(label_A),
            Create(dot_B), Write(label_B),
            run_time=1
        )
        
        # === МАЛАЯ ОКРУЖНОСТЬ - ТОЧНО КАСАЕТСЯ ДУГИ AB И ДИАМЕТРА ===
        r = 1.3  # УВЕЛИЧЕННЫЙ радиус
        
        # Центр малой окружности должен быть на расстоянии R_big - r от центра большой
        # И на высоте r от диаметра (чтобы касаться диаметра)
        # Решаем: x^2 + r^2 = (R_big - r)^2
        x_small = np.sqrt((R_big - r)**2 - r**2)
        O_small = np.array([x_small, r, 0])  # Точно касается и диаметра и дуги
        
        small_circle = Circle(radius=r, color=BLUE, stroke_width=4)
        small_circle.move_to(O_small)
        
        self.play(Create(small_circle), run_time=1.5)
        
        # Центр малой окружности
        dot_O_small = Dot(O_small, color=WHITE, radius=0.08)
        self.play(Create(dot_O_small), run_time=0.5)
        
        # Радиус r - ТОЛЩЕ
        r_line = Line(O_small, O_small + RIGHT * r, color=GREEN, stroke_width=4)
        r_label = Text("r", font_size=28, color=GREEN).next_to(r_line, UP, buff=0.15)
        
        self.play(Create(r_line), Write(r_label), run_time=1)
        
        # Точка T - касание малой окружности с диаметром
        T = np.array([O_small[0], 0, 0])
        dot_T = Dot(T, color=WHITE, radius=0.1)
        label_T = Text("T", font_size=32, color=WHITE).next_to(T, DOWN, buff=0.2)
        
        self.play(
            Create(dot_T), Write(label_T),
            run_time=1
        )
        
        # Точка E - касание малой и большой окружности
        # Лежит на линии, соединяющей центры
        vec_centers = O_small - ORIGIN
        vec_centers_norm = vec_centers / np.linalg.norm(vec_centers)
        E = ORIGIN + vec_centers_norm * R_big
        
        dot_E = Dot(E, color=WHITE, radius=0.08)
        label_E = Text("E", font_size=28, color=WHITE).next_to(E, UP, buff=0.15)
        
        self.play(Create(dot_E), Write(label_E), run_time=1)
        
        # === КАСАТЕЛЬНАЯ ИЗ A К МАЛОЙ ОКРУЖНОСТИ ===
        
        def find_tangent_point_from_A(A, O, r):
            """Находит точку касания C из точки A к окружности с центром O и радиусом r"""
            # Вектор от A к O
            AO = O - A
            dist_AO = np.linalg.norm(AO)
            
            # Угол между AO и касательной
            angle = np.arcsin(r / dist_AO)
            
            # Нормализованный вектор AO
            AO_norm = AO / dist_AO
            
            # Перпендикулярный вектор
            perp = np.array([-AO_norm[1], AO_norm[0], 0])
            
            # Выбираем касательную, которая идет вверх и вправо
            C_dir = np.cos(angle) * AO_norm + np.sin(angle) * perp
            
            # Точка касания C
            C = O - r * (np.sin(angle) * AO_norm - np.cos(angle) * perp)
            
            return C
        
        # Находим точку касания C
        C = find_tangent_point_from_A(A, O_small, r)
        
        # Линия AC продолжаем до пересечения с большой полуокружностью в D
        line_dir = (C - A)
        line_dir = line_dir / np.linalg.norm(line_dir)
        
        # Находим пересечение линии A->C с большой окружностью
        O_big = ORIGIN
        OA = A - O_big
        a = np.dot(line_dir, line_dir)
        b = 2 * np.dot(OA, line_dir)
        c = np.dot(OA, OA) - R_big**2
        
        discriminant = b**2 - 4*a*c
        t1 = (-b + np.sqrt(discriminant)) / (2*a)
        t2 = (-b - np.sqrt(discriminant)) / (2*a)
        
        # Выбираем t > 0 (точка D дальше от A чем C)
        t_D = max(t1, t2)
        D = A + t_D * line_dir
        
        # Касательная AD - ТОЛЩЕ
        tangent_line = Line(A, D, color=WHITE, stroke_width=4)
        
        # Точки C и D
        dot_C = Dot(C, color=WHITE, radius=0.08)
        dot_D = Dot(D, color=WHITE, radius=0.08)
        label_C = Text("C", font_size=28, color=WHITE).next_to(C, LEFT + UP, buff=0.15)
        label_D = Text("D", font_size=28, color=WHITE).next_to(D, UP, buff=0.15)
        
        self.play(Create(tangent_line), run_time=1.5)
        self.play(
            Create(dot_C), Write(label_C),
            Create(dot_D), Write(label_D),
            run_time=1
        )
        
        # Отрезок CD (изначально белый)
        CD_line_white = Line(C, D, color=WHITE, stroke_width=4)
        CD_line_yellow = Line(C, D, color=YELLOW, stroke_width=5)
        
        # Отрезок TB (изначально белый)
        TB_line_white = Line(T, B, color=WHITE, stroke_width=4)
        TB_line_yellow = Line(T, B, color=YELLOW, stroke_width=5)
        
        # Создаем отрезки белыми
        self.play(Create(CD_line_white), Create(TB_line_white), run_time=1)
        
        # Подписи 6 и 15 - РОВНО ПО ЦЕНТРУ ОТРЕЗКОВ
        label_6 = Text("6", font_size=28, color=YELLOW)
        label_6.move_to((C + D) / 2)  # Точный центр отрезка CD
        label_6.shift(UP * 0.3)  # Немного выше отрезка
        
        label_15 = Text("15", font_size=28, color=YELLOW)
        label_15.move_to((T + B) / 2)  # Точный центр отрезка TB
        label_15.shift(DOWN * 0.3)  # Немного ниже отрезка
        
        # ПЛАВНОЕ ИЗМЕНЕНИЕ ЦВЕТА на желтый
        self.play(
            Transform(CD_line_white, CD_line_yellow),
            Transform(TB_line_white, TB_line_yellow),
            Write(label_6),
            Write(label_15),
            run_time=2
        )
        
        self.wait(1)
        
        # === ДОПОЛНИТЕЛЬНЫЕ ПОСТРОЕНИЯ ===
        
        # 1. Отрезок OE сразу красным цветом
        line_OE = Line(O_small, E, color=PURPLE, stroke_width=5)
        
        # Прямая через O_small и E до пересечения с AB
        line_dir = (E - O_small) / np.linalg.norm(E - O_small)
        
        # Находим пересечение с AB (y = 0)
        if abs(line_dir[1]) > 1e-6:
            t_intersect = -O_small[1] / line_dir[1]
            O_point = O_small + t_intersect * line_dir
        else:
            O_point = O_small + line_dir * 5
        
        # Проверяем что точка O лежит на отрезке AB
        if O_point[0] < A[0]:
            O_point = A
        elif O_point[0] > B[0]:
            O_point = B
        
        # Прямая O_small -> O (через E)
        line_O_small_O = Line(O_small, O_point, color=PURPLE, stroke_width=3)
        
        # Точка O на AB
        dot_O = Dot(O_point, color=WHITE, radius=0.08)
        label_O = Text("O", font_size=28, color=WHITE).next_to(O_point, DOWN, buff=0.15)
        
        self.play(
            Create(line_OE),
            Create(line_O_small_O),
            Create(dot_O), Write(label_O),
            run_time=1.5
        )
        
        # 2. Касательная к полуокружности в точке E (пунктиром)
        # Касательная перпендикулярна радиусу O_big->E
        radius_dir = (E - ORIGIN) / np.linalg.norm(E - ORIGIN)
        tangent_dir = np.array([-radius_dir[1], radius_dir[0], 0])
        
        tangent_length = 2.0
        tangent_start = E - tangent_dir * tangent_length
        tangent_end = E + tangent_dir * tangent_length
        tangent_dashed = DashedLine(tangent_start, tangent_end, color=WHITE, stroke_width=2, dash_length=0.1)
        
        self.play(Create(tangent_dashed), run_time=1.5)
        
        # 3. ПРАВИЛЬНЫЙ уголок - классическое обозначение прямого угла
        # Вектор направления OE
        OE_dir = (E - O_small) / np.linalg.norm(E - O_small)
        
        # Уголок в точке E - КЛАССИЧЕСКОЕ ОБОЗНАЧЕНИЕ (отзеркаленный квадратик)
        angle_length = 0.25
        
        # Создаем квадратик в угле
        # Первая линия - вдоль OE (от E в сторону O_small)
        angle_line1_start = E - OE_dir * angle_length
        angle_line1_end = angle_line1_start + tangent_dir * angle_length
        angle_line1 = Line(angle_line1_start, angle_line1_end, color=YELLOW, stroke_width=3)
        
        # Вторая линия - вдоль касательной (от E в нужную сторону)  
        angle_line2_start = E + tangent_dir * angle_length
        angle_line2_end = angle_line2_start - OE_dir * angle_length
        angle_line2 = Line(angle_line2_start, angle_line2_end, color=YELLOW, stroke_width=3)
        
        # Прямоугольный угол (квадратик в угле)
        angle_square = VGroup(angle_line1, angle_line2)
        
        self.play(Create(angle_square), run_time=1)
        
        self.wait(1)
        
        # 4. Убираем вспомогательные элементы (кроме OE)
        self.play(
            FadeOut(tangent_dashed),
            FadeOut(angle_square),
            run_time=1.5
        )
        
        # 5. Подпись R появляется ПОСЛЕ исчезновения касательной
        R_label = Text("R", font_size=28, color=PURPLE)
        R_position = O_small + (E - O_small) * 0.5
        R_label.move_to(R_position)
        R_label.shift(LEFT * 0.2 + UP * 0.1)
        
        self.play(Write(R_label), run_time=1)
        
        # Финальная пауза
        self.wait(3)

if __name__ == "__main__":
    scene = SemicircleProblem()
    scene.render()

#manim main.py SemiCircleScene -pql