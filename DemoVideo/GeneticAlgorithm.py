from manim import *

class GeneticAlgorithm(Scene):
    def construct(self):
        # 标题
        title = Text("遗传算法原理", font_size=48).to_edge(UP)
        self.play(Write(title))

        # 初始种群
        population_text = Text("1. 生成初始种群", font_size=36)
        self.play(Write(population_text))
        self.wait(1)

        population = VGroup(
            *[Rectangle(width=1, height=0.5).set_fill(BLUE, opacity=0.7) for _ in range(8)]
        ).arrange(RIGHT, buff=0.2).shift(DOWN)
        labels = VGroup(
            *[Text(f"个体{i+1}", font_size=24).next_to(population[i], DOWN) for i in range(8)]
        )
        self.play(FadeIn(population), Write(labels))
        self.wait(2)

        # 适应度计算
        fitness_text = Text("2. 计算适应度", font_size=36).to_edge(UP)
        self.play(ReplacementTransform(population_text, fitness_text))
        fitness_values = VGroup(
            *[Text(f"{0.1 + 0.1 * i:.1f}", font_size=24).next_to(population[i], UP) for i in range(8)]
        )
        self.play(Write(fitness_values))
        self.wait(2)

        # 选择
        selection_text = Text("3. 选择 (轮盘赌)", font_size=36).to_edge(UP)
        self.play(ReplacementTransform(fitness_text, selection_text))
        selected = population[:4].copy().set_fill(GREEN, opacity=0.7)
        self.play(ReplacementTransform(population[:4].copy(), selected))
        self.wait(2)

        # 交叉
        crossover_text = Text("4. 交叉", font_size=36).to_edge(UP)
        self.play(ReplacementTransform(selection_text, crossover_text))
        crossover = VGroup(
            *[
                Rectangle(width=1, height=0.5).set_fill(YELLOW, opacity=0.7)
                for _ in range(4)
            ]
        ).arrange(RIGHT, buff=0.2).next_to(selected, DOWN, buff=1)
        crossover_labels = VGroup(
            *[Text(f"新个体{i+1}", font_size=24).next_to(crossover[i], DOWN) for i in range(4)]
        )
        self.play(FadeIn(crossover), Write(crossover_labels))
        self.wait(2)

        # 变异
        mutation_text = Text("5. 变异", font_size=36).to_edge(UP)
        self.play(ReplacementTransform(crossover_text, mutation_text))
        mutated = crossover[2].copy().set_fill(RED, opacity=0.7)
        self.play(Transform(crossover[2], mutated))
        self.wait(2)

        # 总结
        summary_text = Text("遗传算法流程完成", font_size=36).to_edge(DOWN)
        self.play(Write(summary_text))
        self.wait(2)

        # 清场
        self.play(*[FadeOut(mob) for mob in self.mobjects])

        # 结束画面
        final_text = Text("遗传算法演示完成", font_size=48)
        self.play(Write(final_text))
        self.wait(3)


if __name__ == "__main__":
    import os

    os.system(r'cd G:\Order\MyPythonLib\Manim\PhdDissertation')
    os.system(r'manim -pql GeneticAlgorithm.py GeneticAlgorithm')
