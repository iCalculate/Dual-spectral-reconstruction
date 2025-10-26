from manim import *
import random

class IsingModelAnnealing(Scene):
    def construct(self):
        # 标题
        title = Text("Ising模型退火收敛过程", font_size=48).to_edge(UP)
        self.play(Write(title))
        
        # 参数设置
        grid_size = 6  # 网格大小
        temp_steps = [10, 5, 3, 1]  # 退火温度步进
        final_temp = 0.1  # 最终低温

        # 初始状态生成
        grid = self.create_grid(grid_size)
        self.play(Create(grid))
        self.wait(2)

        # 初始随机状态
        spins = self.create_random_spins(grid_size)
        self.update_grid(grid, spins)
        self.play(*[FadeIn(mob) for mob in grid], run_time=2)
        self.wait(1)

        # 退火过程
        for i, temp in enumerate(temp_steps):
            annealing_text = Text(f"退火温度: T = {temp}", font_size=36).to_edge(DOWN)
            self.play(Write(annealing_text))
            spins = self.annealing_step(spins, grid_size, temp)
            self.update_grid(grid, spins)
            self.wait(2)
            self.play(FadeOut(annealing_text))

        # 最终低温收敛状态
        final_text = Text(f"最终温度: T = {final_temp}", font_size=36).to_edge(DOWN)
        self.play(Write(final_text))
        spins = self.annealing_step(spins, grid_size, final_temp)
        self.update_grid(grid, spins)
        self.wait(2)
        self.play(FadeOut(final_text))

        # 收敛完成
        summary_text = Text("Ising模型退火收敛完成", font_size=36).to_edge(DOWN)
        self.play(Write(summary_text))
        self.wait(3)

    def create_grid(self, grid_size):
        """创建网格节点"""
        grid = VGroup()
        for i in range(grid_size):
            for j in range(grid_size):
                square = Square(side_length=0.8)
                square.move_to(np.array([i - grid_size // 2, j - grid_size // 2, 0]))
                grid.add(square)
        return grid

    def create_random_spins(self, grid_size):
        """初始化随机自旋状态"""
        return [[random.choice([-1, 1]) for _ in range(grid_size)] for _ in range(grid_size)]

    def update_grid(self, grid, spins):
        """根据自旋状态更新网格颜色"""
        for i in range(len(spins)):
            for j in range(len(spins[i])):
                index = i * len(spins) + j
                color = WHITE if spins[i][j] == 1 else BLACK
                grid[index].set_fill(color, opacity=1)

    def annealing_step(self, spins, grid_size, temperature):
        """模拟退火过程中的一次步进"""
        for _ in range(50):  # 每步尝试改变多个节点
            i, j = random.randint(0, grid_size - 1), random.randint(0, grid_size - 1)
            delta_energy = 2 * spins[i][j] * self.neighbor_sum(spins, i, j, grid_size)
            if delta_energy < 0 or random.random() < np.exp(-delta_energy / temperature):
                spins[i][j] *= -1
        return spins

    def neighbor_sum(self, spins, i, j, grid_size):
        """计算邻居自旋的和"""
        neighbors = [
            spins[(i - 1) % grid_size][j],
            spins[(i + 1) % grid_size][j],
            spins[i][(j - 1) % grid_size],
            spins[i][(j + 1) % grid_size],
        ]
        return sum(neighbors)


if __name__ == "__main__":
    import os

    os.system(r'cd G:\Order\MyPythonLib\Manim\PhdDissertation')
    os.system(r'manim -pql IsingModelAnnealing.py IsingModelAnnealing')
