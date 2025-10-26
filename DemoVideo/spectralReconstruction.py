from manim import *
import itertools as it

class ManimiCLogo(Scene):
    def construct(self):
        self.camera.background_color = "#333333"#"#ece6e2"
        logo_green = "#87c2a5"
        logo_blue = "#525893"
        logo_red = "#e07a5f"
        logo_black = "#343434"
        logo_white = "#ece6e2"
        ds_m = MathTex(r"i\mathbb{C}", fill_color=logo_white).scale(7)
        ds_m.shift(2.25 * LEFT + 1.5 * UP)
        ds_l = MathTex(r"al", fill_color=logo_white).scale(6).shift(UP*0.45).shift(RIGHT*0.4)
        circle = Circle(color=logo_green, fill_opacity=1).shift(LEFT)
        square = Square(color=logo_blue, fill_opacity=1).shift(UP)
        triangle = Triangle(color=logo_red, fill_opacity=1).shift(RIGHT)
        item = VGroup(triangle, square, circle)
        logo = VGroup(triangle, square, circle, ds_m)  # order matters
        logo.move_to(ORIGIN)
        totlogo = VGroup(triangle, square, circle, ds_m, ds_l)
        #self.add(logo)
        self.play(DrawBorderThenFill(logo))
        self.play(Write(ds_l), item.animate.shift(RIGHT*1.5), ds_m.animate.shift(LEFT*1.5))
        self.wait(1.0)
        self.play(FadeOut(totlogo, shift=DOWN * 1, scale=0.6))
       
class TraditionalApproach(Scene):
    def construct(self):
        self.camera.background_color = "#333333"#"
        # title = Title(f"Traditional Spectral Detection")

        self.showSpectrum1()

    def showSpectrum1(self):
        axS1 = Axes(
            x_range=[0, 10], y_range=[0, 100, 10], axis_config={"include_tip": False}
        ).shift(UP * 2 + LEFT *3.15)
        axS1.height = 6.0
        axS1.width = 6.0
        x_label = axS1.get_x_axis_label(
            Tex(r"Wavelength $\lambda$").scale(0.65), edge=DOWN, direction=DOWN, buff=0.15
        )
        y_label = axS1.get_y_axis_label(
            Tex(r"Spectrum $S(\lambda)$").scale(0.65).rotate(90 * DEGREES),
            edge=LEFT,
            direction=LEFT,
            buff=0.15,
        )

        axR1 = Axes(
            x_range=[0, 10], y_range=[0, 100, 10], axis_config={"include_tip": False}
        ).shift(UP * 2 + RIGHT *3.7)
        axR1.height = 6.0
        axR1.width = 6.0
        s_label = axR1.get_x_axis_label(
            Tex("States").scale(0.65), edge=DOWN, direction=DOWN, buff=0.15
        )
        r_label = axR1.get_y_axis_label(
            Tex("Response $R$").scale(0.65).rotate(90 * DEGREES),
            edge=LEFT,
            direction=LEFT,
            buff=0.15,
        )

        def func(x):
            return 20*np.exp(-(x-1)*(x-1))+\
                    80*np.exp(-(x-3)*(x-3))+\
                    40*np.exp(-(x-5)*(x-5))+\
                    50*np.exp(-(x-7)*(x-7))+\
                    30*np.exp(-(x-9)*(x-9))
        spec = axS1.plot(func, color=YELLOW_D)

        area0 = axS1.get_area(spec, [0, 1], color=GREY, opacity=0.5)
        dot0 = Dot(axR1.coords_to_point(0.5, func(0.5)), color=GREEN)

        self.add()
        self.play(DrawBorderThenFill(axS1))
        self.play(FadeIn(x_label, y_label))
        self.play(DrawBorderThenFill(spec))
        self.play(FadeIn(area0))
        self.play(DrawBorderThenFill(axR1))
        self.play(FadeIn(s_label, r_label))
        self.play(ReplacementTransform(area0, dot0))

        for i in range(9):
            area0 = axS1.get_area(spec, [i+1, i+2], color=GREY, opacity=0.5)
            dot0 = Dot(axR1.coords_to_point(1.5+i, func(1.5+i)), color=GREEN)
            self.play(FadeIn(area0))
            self.play(ReplacementTransform(area0, dot0))

        line_graph = axR1.plot_line_graph(
            x_values = [i+0.5 for i in range(0, 10)],
            y_values = [func(i+0.5) for i in range(0, 10)],
            line_color=GREEN_D,
            vertex_dot_style=dict(stroke_width=3,  fill_color=GREEN_D),
            stroke_width = 4,
        )
        self.play(DrawBorderThenFill(line_graph))

        area0 = axS1.get_area(spec, [3, 4], color=GREY, opacity=0.5)
        dot0 = Dot(axR1.coords_to_point(3.5, func(3.5)), color=GREEN)
        line = axR1.get_vertical_line(axR1.coords_to_point(3.5, func(3.5)), line_config={"dashed_ratio": 0.85}, color=GREEN_D)
        label = MathTex(r"R_i").shift(UP*2.9+RIGHT*3).scale(0.8)
        self.play(FadeIn(area0))
        self.add(line)
        self.play(Flash(dot0))
        self.play(Write(label))

        formu1 = MathTex(r"R_i=\int_{\lambda_i-\Delta\lambda}^{\lambda_i+\Delta\lambda}",r"S(\lambda )d\lambda").shift(UP*2.9+RIGHT*4.5).scale(0.8) 
        formu2 = MathTex(r"R_i=\int_{\lambda_i-\Delta\lambda}^{\lambda_i+\Delta\lambda}",r"\eta_n",r"S(\lambda )d\lambda").shift(UP*2.9+RIGHT*4.5).scale(0.8) 

        self.play(ReplacementTransform(label, formu1))
        self.play(ReplacementTransform(formu1, formu2))
        self.play(Circumscribe(formu2[1]))

        eta = 0.5+0.5*(np.random.rand(10))
        line_graph_eta = axR1.plot_line_graph(
            x_values = [i+0.5 for i in range(0, 10)],
            y_values = [func(i+0.5)*eta[i] for i in range(0, 10)],
            line_color=GREEN_B,
            vertex_dot_style=dict(stroke_width=3,  fill_color=GREEN_B),
            stroke_width = 4,
        )
        self.play(ReplacementTransform(line_graph, line_graph_eta))


        mat1 = MathTex(r"S(\lambda )=[ S_1\quad S_2\quad \cdots \quad S_{n-1}\quad S_n ]^{T} ")\
                .shift(DOWN*0.5+LEFT*3).scale(0.6) 
        mat2 = MathTex(r"R(state)=[ R_1\quad R_2\quad \cdots \quad R_{n-1}\quad R_n ]^{T} ")\
                .shift(DOWN*0.5+RIGHT*3).scale(0.6)         

        self.play(TransformFromCopy(spec, mat1))
        self.play(TransformFromCopy(line_graph_eta, mat2))

        m_eta = Matrix([[r"\eta_1", 0, 0, 0, 0],\
                        [0, r"\eta_2", 0, 0, 0],\
                        [0, 0, r"\ddots", 0, 0],\
                        [0, 0, 0, r"\eta_{n-1}", 0],\
                        [0, 0, 0, 0, r"\eta_n"]]).shift(DOWN*2.3+LEFT*4.5).scale(0.6)   
        m_S = Matrix([["S_1"],\
                        ["S_2"],\
                        ["\\vdots"],\
                        ["S_{n-1}"],\
                        ["S_n"]]).shift(DOWN*2.3+LEFT*1.7).scale(0.59).set_colors(YELLOW)

        m_R = Matrix([["R_1"],\
                        ["R_2"],\
                        [r"\vdots"],\
                        ["R_{n-1}"],\
                        ["R_n"]]).shift(DOWN*2.3+LEFT*0.1).scale(0.59).set_colors(GREEN)
        
        m_R.generate_target()
        m_R.target.shift(4.3*RIGHT)


        self.play(TransformFromCopy(formu2[1], m_eta))
        self.play(TransformFromCopy(mat1, m_S))

        arrow_1 = Arrow(start=LEFT*0.18, end=RIGHT*0.18).shift(DOWN*2.3+LEFT*0.85)
        self.play(GrowArrow(arrow_1))

        self.play(TransformFromCopy(mat2, m_R))
        self.play(MoveToTarget(m_R))


        m_eta_inv = Matrix([[r"\eta_1^{-1}", 0, 0, 0, 0],\
                        [0, r"\eta_2^{-1}", 0, 0, 0],\
                        [0, 0, r"\ddots", 0, 0],\
                        [0, 0, 0, r"\eta_{n-1}^{-1}", 0],\
                        [0, 0, 0, 0, r"\eta_n^{-1}"]]).shift(DOWN*2.3+RIGHT*1.4).scale(0.57) 

        self.play(TransformFromCopy(m_eta, m_eta_inv))
        arrow_2 = Arrow(start=LEFT*0.18, end=RIGHT*0.18).shift(DOWN*2.3+RIGHT*5.1)
        self.play(GrowArrow(arrow_2))

        m_S_hat = Matrix([[r"\hat{S_1}"],\
                        [r"\hat{S_2}"],\
                        [r"\vdots"],\
                        [r"\hat{S_{n-1}}"],\
                        [r"\hat{S_n}"]]).shift(DOWN*2.3+RIGHT*6.0).scale(0.58).set_colors(YELLOW)

        self.play(DrawBorderThenFill(m_S_hat))
        self.play(Indicate(m_S_hat))


        self.wait()

class IdealReconstruction(Scene):
    def construct(self):
        self.camera.background_color = "#333333"#"
        # title = Title(f"Traditional Spectral Detection")

        self.showSpectrum()

    def showSpectrum(self):
        axS1 = Axes(
            x_range=[0, 10], y_range=[0, 100, 10], axis_config={"include_tip": False}
        ).shift(UP * 2 + LEFT *3.15)
        axS1.height = 6.0
        axS1.width = 6.0
        x_label = axS1.get_x_axis_label(
            Tex(r"Wavelength $\lambda$").scale(0.65), edge=DOWN, direction=DOWN, buff=0.15
        )
        y_label = axS1.get_y_axis_label(
            Tex(r"Spectrum $S(\lambda)$").scale(0.65).rotate(90 * DEGREES),
            edge=LEFT,
            direction=LEFT,
            buff=0.15,
        )

        axR1 = Axes(
            x_range=[0, 10], y_range=[0, 100, 10], axis_config={"include_tip": False}
        ).shift(UP * 2 + RIGHT *3.7)
        axR1.height = 6.0
        axR1.width = 6.0
        s_label = axR1.get_x_axis_label(
            Tex("States").scale(0.65), edge=DOWN, direction=DOWN, buff=0.15
        )
        r_label = axR1.get_y_axis_label(
            Tex("Response $R$").scale(0.65).rotate(90 * DEGREES),
            edge=LEFT,
            direction=LEFT,
            buff=0.15,
        )

        def func(x):
            return 20*np.exp(-(x-1)*(x-1))+\
                    80*np.exp(-(x-3)*(x-3))+\
                    40*np.exp(-(x-5)*(x-5))+\
                    50*np.exp(-(x-7)*(x-7))+\
                    30*np.exp(-(x-9)*(x-9))
        spec = axS1.plot(func, color=YELLOW_D)

        area0 = axS1.get_area(spec, [0, 1], color=GREY, opacity=0.5)
        dot0 = Dot(axR1.coords_to_point(0.5, func(0.5)*0.2), color=GREEN)
        resList = []
        resList.append(func(0.5)*0.2)

        self.add()
        self.play(DrawBorderThenFill(axS1))
        self.play(FadeIn(x_label, y_label))
        self.play(DrawBorderThenFill(spec))
        self.play(FadeIn(area0))
        self.play(DrawBorderThenFill(axR1))
        self.play(FadeIn(s_label, r_label))
        self.play(ReplacementTransform(area0, dot0))

        for i in range(9):
            area0 = axS1.get_area(spec, [0, i+2], color=GREY, opacity=0.5)
            resSum = 0
            for j in range(i+2):
                resSum += 0.2*func(0.5+j)
            resList.append(resSum)
            dot0 = Dot(axR1.coords_to_point(1.5+i, resSum), color=GREEN)
            self.play(FadeIn(area0))
            self.play(ReplacementTransform(area0, dot0))

        line_graph = axR1.plot_line_graph(
            x_values = [i+0.5 for i in range(0, 10)],
            y_values = resList,
            line_color=GREEN_D,
            vertex_dot_style=dict(stroke_width=3,  fill_color=GREEN_D),
            stroke_width = 4,
        )
        self.play(DrawBorderThenFill(line_graph))

        area0 = axS1.get_area(spec, [0, 8], color=GREY, opacity=0.5)
        dot0 = Dot(axR1.coords_to_point(8.5, resList[8]), color=GREEN)
        line = axR1.get_vertical_line(axR1.coords_to_point(8.5, resList[8]), line_config={"dashed_ratio": 0.85}, color=GREEN_D)
        label = MathTex(r"R_i").shift(UP*3.1+RIGHT*5.3).scale(0.8)
        self.play(FadeIn(area0))
        self.add(line)
        self.play(Flash(dot0))
        self.play(Write(label))

        formu1 = MathTex(r"R_i=\int_{\lambda _{0}}^{\lambda _{i}}","S(\lambda )d\lambda")\
                    .shift(UP*2.6+RIGHT*2.8).scale(0.8) 
        formu2 = MathTex(r"R_i=\int_{\lambda _{0}}^{\lambda _{i}}","\eta_{n}","S(\lambda )d\lambda")\
                    .shift(UP*2.6+RIGHT*2.8).scale(0.8) 

        self.play(ReplacementTransform(label, formu1))
        self.play(ReplacementTransform(formu1, formu2))
        self.play(Circumscribe(formu2[1]))

        eta = 0.7+0.3*(np.random.rand(10))
        line_graph_eta = axR1.plot_line_graph(
            x_values = [i+0.5 for i in range(0, 10)],
            y_values = [resList[i]*eta[i] for i in range(0, 10)],
            line_color=GREEN_B,
            vertex_dot_style=dict(stroke_width=3,  fill_color=GREEN_B),
            stroke_width = 4,
        )
        self.play(ReplacementTransform(line_graph, line_graph_eta))


        mat1 = MathTex(r"S(\lambda )=[ S_1\quad S_2\quad \cdots \quad S_{n-1}\quad S_n ]^{T} ")\
                .shift(DOWN*0.5+LEFT*3).scale(0.6) 
        mat2 = MathTex(r"R(state)=[ R_1\quad R_2\quad \cdots \quad R_{n-1}\quad R_n ]^{T} ")\
                .shift(DOWN*0.5+RIGHT*3).scale(0.6)         

        self.play(TransformFromCopy(spec, mat1))
        self.play(TransformFromCopy(line_graph_eta, mat2))

        m_eta = Matrix([[r"\eta_1", 0, 0, 0, 0],\
                        [r"\eta_2", r"\eta_2", 0, 0, 0],\
                        [r"\vdots", r"\ddots", r"\ddots", 0, 0],\
                        [r"\eta_{n-1}", r"\cdots", r"\ddots", r"\eta_{n-1}", 0],\
                        [r"\eta_{n}", r"\cdots", r"\cdots", r"\cdots", r"\eta_{n}"]]).shift(DOWN*2.3+LEFT*4).scale(0.6)   

        m_eta_norm = Matrix([[r"1", 0, 0, 0, 0],\
                        [r"1", r"1", 0, 0, 0],\
                        [r"\vdots", r"\ddots", r"\ddots", 0, 0],\
                        [r"1", r"\cdots", r"\ddots", r"1", 0],\
                        [r"1", r"\cdots", r"\cdots", r"\cdots", r"1"]]).shift(DOWN*2.3+LEFT*3.7).scale(0.6)   

        eta_vector = Matrix([[r"\eta_1"],\
                        [r"\eta_2"],\
                        [r"\vdots"],\
                        [r"\eta_{n-1}"],\
                        [r"\eta_n"]]).shift(DOWN*2.3+LEFT*6.2).scale(0.61).set_colors(YELLOW)

        m_S = Matrix([["S_1"],\
                        ["S_2"],\
                        ["\\vdots"],\
                        ["S_{n-1}"],\
                        ["S_n"]]).shift(DOWN*2.3+LEFT*1.2).scale(0.59).set_colors(YELLOW)

        m_R = Matrix([["R_1"],\
                        ["R_2"],\
                        [r"\vdots"],\
                        ["R_{n-1}"],\
                        ["R_n"]]).shift(DOWN*2.3+RIGHT*0.4).scale(0.59).set_colors(GREEN)

        m_R_over_eta = Matrix([[r"R_1/\eta_1"],\
                        [r"R_2/\eta_2"],\
                        [r"\vdots"],\
                        [r"\vdots"],\
                        [r"R_n/\eta_n"]]).shift(DOWN*2.3+RIGHT*4.5).scale(0.58).set_colors(GREEN)

        self.play(TransformFromCopy(formu2[1], m_eta))
        self.play(TransformFromCopy(mat1, m_S))

        arrow_1 = Arrow(start=LEFT*0.18, end=RIGHT*0.68).shift(DOWN*2.3+LEFT*0.65)
        self.play(GrowArrow(arrow_1))

        self.play(TransformFromCopy(mat2, m_R))

        self.play(Transform(m_eta, m_eta_norm),FadeIn(eta_vector))

        self.play(Transform(m_R, m_R_over_eta))


        m_eta_inv = Matrix([[1, 0, 0, 0, 0],\
                            [-1, 1, 0, 0, 0],\
                            [0, 0, r"\ddots", 0, 0],\
                            [0, 0, -1, 1, 0],\
                            [0, 0, 0, -1, 1]]).shift(DOWN*2.3+RIGHT*1.8).scale(0.6) 

        self.play(TransformFromCopy(m_eta, m_eta_inv))
        arrow_2 = Arrow(start=LEFT*0.18, end=RIGHT*0.18).shift(DOWN*2.3+RIGHT*5.4)
        self.play(GrowArrow(arrow_2))

        m_S_hat = Matrix([[r"\hat{S_1}"],\
                        [r"\hat{S_2}"],\
                        [r"\vdots"],\
                        [r"\hat{S_{n-1}}"],\
                        [r"\hat{S_n}"]]).shift(DOWN*2.3+RIGHT*6.2).scale(0.58).set_colors(YELLOW)

        self.play(DrawBorderThenFill(m_S_hat))
        self.play(Indicate(m_S_hat))


        self.wait()

class GeneralReconstruction(Scene):
    def construct(self):
        self.camera.background_color = "#333333"#"
        # title = Title(f"Traditional Spectral Detection")

        self.showTraditionalApproach(loop = 5)
        self.showIdealApproach(loop = 5)
        self.showGeneralApproach(loop = 5)

    def showTraditionalApproach(self, loop):
        title_1 = Text('Traditional Approach',  font="Harding Text Web")\
                    .scale(0.5).shift(UP*3.3+LEFT*4.5)
        ax_1 = Axes(
            x_range=[0, 10],
            y_range=[0, 1, 0.2],
            x_length=4,
            y_length=2,
            tips=False,
        ).shift(UP*1.6+LEFT*4.5)

        graphs = VGroup()
        area = VGroup()
        colorList = ["#fde099", "#fcd166", "#fbc233", "#fbb301"]
        eta = 0.5+0.5*(np.random.rand(4))
        for n in range(4):
            resCurve = ax_1.plot(
                lambda x: eta[n]*(np.heaviside(x-1-n*2,1)-np.heaviside(x-3-n*2,1)), color=colorList[n]\
                , use_smoothing=False)
            area0 = ax_1.get_area(resCurve, [0, 10], color=colorList[n], opacity=0.5*n/10)
            area += area0
            graphs += resCurve

        formu_1 = MathTex(r"R_i=\int_{\lambda_i-\Delta\lambda}^{\lambda_i+\Delta\lambda}",r"\eta_n",r"S(\lambda )d\lambda")\
                    .shift(DOWN*0.5+LEFT*4.5).scale(0.7) 

        mat_1 = DecimalMatrix([[eta[0],0,0,0],\
                                [0,eta[1],0,0],\
                                [0,0,eta[2],0],\
                                [0,0,0,eta[3]]],element_to_mobject_config={"num_decimal_places": 2})\
                    .shift(DOWN*2.5+LEFT*4.5).scale(0.6)
        ent_1 = mat_1.get_entries()
        for n in range(4):
            ent_1[n*4+n].set_color(colorList[n])
        
        #self.add(ax_1,title_1,formu_1,graphs,area,mat_1)
        self.play(Write(title_1))
        self.play(DrawBorderThenFill(ax_1))
        self.play(DrawBorderThenFill(graphs),FadeIn(area))
        self.play(DrawBorderThenFill(formu_1))
        self.play(DrawBorderThenFill(mat_1))


        for n in range(loop):
            eta = 0.5+0.5*(np.random.rand(4))
            graphs_new = VGroup()
            area_new = VGroup()
            for n in range(4):
                resCurve = ax_1.plot(
                    lambda x: eta[n]*(np.heaviside(x-1-n*2,1)-np.heaviside(x-3-n*2,1)), color=colorList[n]\
                    , use_smoothing=False)
                area0 = ax_1.get_area(resCurve, [0, 10], color=colorList[n], opacity=0.5*n/10)
                area_new += area0
                graphs_new += resCurve

            mat_1_new = DecimalMatrix([[eta[0],0,0,0],\
                                    [0,eta[1],0,0],\
                                    [0,0,eta[2],0],\
                                    [0,0,0,eta[3]]],element_to_mobject_config={"num_decimal_places": 2})\
                        .shift(DOWN*2.5+LEFT*4.5).scale(0.6)
            ent_1_new = mat_1_new.get_entries()
            for n in range(4):
                ent_1_new[n*4+n].set_color(colorList[n])

            self.play(ReplacementTransform(graphs, graphs_new),\
                    ReplacementTransform(area, area_new),\
                    ReplacementTransform(mat_1, mat_1_new))
            self.wait(1.0)

            graphs = graphs_new
            area = area_new
            mat_1 = mat_1_new

    def showIdealApproach(self,loop):
        title_2 = Text('Ideal Reconstruction',  font="Harding Text Web")\
                    .scale(0.5).shift(UP*3.3)
        ax_2 = Axes(
            x_range=[0, 10],
            y_range=[0, 1, 0.2],
            x_length=4,
            y_length=2,
            tips=False,
        ).shift(UP*1.6)

        graphs = VGroup()
        area = VGroup()
        colorList = ["#c9d5c2", "#aec1a4", "#93ac86", "#789868"]
        eta = [0.9+0.05*(np.random.rand()),\
                0.7+0.1*(np.random.rand()),\
                0.5+0.15*(np.random.rand()),\
                0.3+0.2*(np.random.rand())]
        for n in range(4):
            resCurve = ax_2.plot(
                lambda x: eta[n]*(1-np.heaviside(x-3-n*2,1)), color=colorList[n]\
                , use_smoothing=False)
            area0 = ax_2.get_area(resCurve, [0, 10], color=colorList[n], opacity=0.5*n/10)
            area += area0
            graphs += resCurve

        formu_2 = MathTex(r"R_i=\int_{0}^{\lambda _{i}}",r"\eta_{n}",r"S(\lambda )d\lambda")\
            .scale(0.7).shift(DOWN*0.5)

        mat_2 = DecimalMatrix([[eta[0],0,0,0],\
                                [eta[1],eta[1],0,0],\
                                [eta[2],eta[2],eta[2],0],\
                                [eta[3],eta[3],eta[3],eta[3]]],element_to_mobject_config={"num_decimal_places": 2})\
                    .shift(DOWN*2.5).scale(0.6)
        ent_2 = mat_2.get_entries()
        for n in range(4):
            for m in range(4):
                if m<=n: ent_2[n*4+m].set_color(colorList[n])
            
        
        #self.add(ax_2,title_2,formu_2,graphs,area,mat_2)

        self.play(Write(title_2))
        self.play(DrawBorderThenFill(ax_2))
        self.play(DrawBorderThenFill(graphs),FadeIn(area))
        self.play(DrawBorderThenFill(formu_2))
        self.play(DrawBorderThenFill(mat_2))

        for i in range(loop):
            eta = [0.9+0.05*(np.random.rand()),\
                0.7+0.1*(np.random.rand()),\
                0.5+0.15*(np.random.rand()),\
                0.3+0.2*(np.random.rand())]
            graphs_new = VGroup()
            area_new = VGroup()
            for n in range(4):
                resCurve = ax_2.plot(
                    lambda x: eta[n]*(1-np.heaviside(x-3-n*2,1)), color=colorList[n]\
                    , use_smoothing=False)
                area0 = ax_2.get_area(resCurve, [0, 10], color=colorList[n], opacity=0.5*n/10)
                area_new += area0
                graphs_new += resCurve

            mat_2_new = DecimalMatrix([[eta[0],0,0,0],\
                                [eta[1],eta[1],0,0],\
                                [eta[2],eta[2],eta[2],0],\
                                [eta[3],eta[3],eta[3],eta[3]]],element_to_mobject_config={"num_decimal_places": 2})\
                        .shift(DOWN*2.5).scale(0.6)
            ent_2 = mat_2_new.get_entries()
            for n in range(4):
                for m in range(4):
                    if m<=n: ent_2[n*4+m].set_color(colorList[n])

            self.play(ReplacementTransform(graphs, graphs_new),\
                    ReplacementTransform(area, area_new),\
                    ReplacementTransform(mat_2, mat_2_new))
            self.wait(1.0)
        
            graphs = graphs_new
            area = area_new
            mat_2 = mat_2_new

    def showGeneralApproach(self,loop):
        title_3 = Text('Genearal Reconstruction',  font="Harding Text Web")\
                    .scale(0.5).shift(UP*3.3+RIGHT*4.5)
        ax_3 = Axes(
            x_range=[0, 10],
            y_range=[0, 1, 0.2],
            x_length=4,
            y_length=2,
            tips=False,
        ).shift(UP*1.6+RIGHT*4.5)

        formu_3 = MathTex(r"R_i=\int_{\lambda _0}^{\lambda _n} \eta (\lambda )S(\lambda )d\lambda ")\
                    .shift(DOWN*0.5+RIGHT*4.5).scale(0.7) 

        graphs = VGroup()
        area = VGroup()
        colorList = ["#abbee4", "#829ed7", "#587eca", "#2f5ebd"]
        eta = 0.3+0.7*np.random.rand(4,4)
        for n in range(4):
            resCurve = ax_3.plot(
                lambda x: eta[n][0]*(0.8*np.exp(-pow(x-1.25+eta[n][3]-0.75,2)/2))+\
                          eta[n][1]*(0.8*np.exp(-pow(x-3.75+eta[n][2]-0.75,2)/2))+\
                          eta[n][2]*(0.8*np.exp(-pow(x-6.25+eta[n][1]-0.75,2)/2))+\
                          eta[n][3]*(0.8*np.exp(-pow(x-8.75+eta[n][0]-0.75,2)/2)), color=colorList[n]\
                , use_smoothing=True)
            area0 = ax_3.get_area(resCurve, [0, 10], color=colorList[n], opacity=0.5*n/10)
            area += area0
            graphs += resCurve

        mat_3 = DecimalMatrix([[eta[0][0],eta[0][1],eta[0][2],eta[0][3]],\
                               [eta[1][0],eta[1][1],eta[1][2],eta[1][3]],\
                               [eta[2][0],eta[2][1],eta[2][2],eta[2][3]],\
                               [eta[3][0],eta[3][1],eta[3][2],eta[3][3]]],\
                            element_to_mobject_config={"num_decimal_places": 2}).shift(DOWN*2.5+RIGHT*4.5).scale(0.6)
        ent_3 = mat_3.get_entries()
        for n in range(4):
            for m in range(4):
                ent_3[n*4+m].set_color(colorList[n])
            
        
        #self.add(ax_3,title_3,formu_3,graphs,area,mat_3)

        self.play(Write(title_3))
        self.play(DrawBorderThenFill(ax_3))
        self.play(DrawBorderThenFill(graphs),FadeIn(area))
        self.play(DrawBorderThenFill(formu_3))
        self.play(DrawBorderThenFill(mat_3))

        for i in range(loop):
            eta = 0.3+0.7*np.random.rand(4,4)
            graphs_new = VGroup()
            area_new = VGroup()
            for n in range(4):
                resCurve = ax_3.plot(
                lambda x: eta[n][0]*(0.8*np.exp(-pow(x-1.25+eta[n][3]-0.75,2)/2))+\
                          eta[n][1]*(0.8*np.exp(-pow(x-3.75+eta[n][2]-0.75,2)/2))+\
                          eta[n][2]*(0.8*np.exp(-pow(x-6.25+eta[n][1]-0.75,2)/2))+\
                          eta[n][3]*(0.8*np.exp(-pow(x-8.75+eta[n][0]-0.75,2)/2)), color=colorList[n]\
                , use_smoothing=True)
                area0 = ax_3.get_area(resCurve, [0, 10], color=colorList[n], opacity=0.5*n/10)
                area_new += area0
                graphs_new += resCurve

            mat_3_new = DecimalMatrix([[eta[0][0],eta[0][1],eta[0][2],eta[0][3]],\
                               [eta[1][0],eta[1][1],eta[1][2],eta[1][3]],\
                               [eta[2][0],eta[2][1],eta[2][2],eta[2][3]],\
                               [eta[3][0],eta[3][1],eta[3][2],eta[3][3]],],\
                            element_to_mobject_config={"num_decimal_places": 2})\
                    .shift(DOWN*2.5+RIGHT*4.5).scale(0.6)
            ent_3 = mat_3_new.get_entries()
            for n in range(4):
                for m in range(4):
                    ent_3[n*4+m].set_color(colorList[n])

            self.play(ReplacementTransform(graphs, graphs_new),\
                    ReplacementTransform(area, area_new),\
                    ReplacementTransform(mat_3, mat_3_new))
            self.wait(1.0)
        
            graphs = graphs_new
            area = area_new
            mat_3 = mat_3_new


if __name__ == "__main__":
    import os

    os.system(r'cd G:\Order\MyPythonLib\Manim\PhdDissertation')
    os.system(r'manim -pql SpectralReconstruction.py ManimiCLogo')