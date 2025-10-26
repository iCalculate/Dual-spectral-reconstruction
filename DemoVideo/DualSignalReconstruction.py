from manim import *
import itertools as it
import math

def updateNetwork(NeuralNetworkMobject):
    pass
    return NeuralNetworkMobject.weight_color().weight_width().nodes_color()

class NeuralNetworkMobject(VGroup):
    CONFIG = {
        "neuron_radius": 0.3,
        "neuron_to_neuron_buff": MED_SMALL_BUFF,
        "layer_to_layer_buff": LARGE_BUFF,
        "output_neuron_color": YELLOW,
        "input_neuron_color": BLUE,
        "hidden_layer_neuron_color": WHITE,
        "neuron_stroke_width": 2,
        "neuron_fill_color": GREEN,
        "edge_color": LIGHT_GREY,
        "edge_stroke_width": 2,
        "edge_propogation_color": YELLOW,
        "edge_propogation_time": 1,
        "max_shown_neurons": 11,
        "brace_for_large_layers": True,
        "average_shown_activation_of_large_layer": True,
        "include_output_labels": False,
        "arrow": False,
        "arrow_tip_size": 0.1,
        "left_size": 1,
        "neuron_fill_opacity": 1
    }
    # Constructor with parameters of the neurons in a list
    def __init__(self, neural_network, *args, **kwargs):
        VGroup.__init__(self, *args, **kwargs)
        self.__dict__.update(self.CONFIG)
        self.layer_sizes = neural_network
        self.add_neurons()
        self.add_edges()
        self.add_to_back(self.layers)
        self.add_to_back(self.edge_groups)
    # Helper method for constructor
    def add_neurons(self):
        layers = VGroup(*[
            self.get_layer(size, index)
            for index, size in enumerate(self.layer_sizes)
        ])
        layers.arrange_submobjects(RIGHT, buff=self.layer_to_layer_buff)
        self.layers = layers
        if self.include_output_labels:
            self.label_outputs_text()
    # Helper method for constructor
    def get_nn_fill_color(self, index):
        if index == -1 or index == len(self.layer_sizes) - 1:
            return self.output_neuron_color
        if index == 0:
            return self.input_neuron_color
        else:
            return self.hidden_layer_neuron_color
    # Helper method for constructor
    def get_layer(self, size, index=-1):
        layer = VGroup()
        n_neurons = size
        if n_neurons > self.max_shown_neurons:
            n_neurons = self.max_shown_neurons
        neurons = VGroup(*[
            Circle(
                radius=self.neuron_radius,
                stroke_color=self.get_nn_fill_color(index),
                stroke_width=self.neuron_stroke_width,
                fill_color=BLACK,
                fill_opacity=self.neuron_fill_opacity,
            )
            for x in range(n_neurons)
        ])
        neurons.arrange_submobjects(
            DOWN, buff=self.neuron_to_neuron_buff
        )
        for neuron in neurons:
            neuron.edges_in = VGroup()
            neuron.edges_out = VGroup()
        layer.neurons = neurons
        layer.add(neurons)

        if size > n_neurons:
            dots = Tex(r"\vdots")
            dots.move_to(neurons)
            VGroup(*neurons[:len(neurons) // 2]).next_to(
                dots, UP, MED_SMALL_BUFF
            )
            VGroup(*neurons[len(neurons) // 2:]).next_to(
                dots, DOWN, MED_SMALL_BUFF
            )
            layer.dots = dots
            layer.add(dots)
            if self.brace_for_large_layers:
                brace = Brace(layer, LEFT)
                brace_label = brace.get_tex(str(size))
                layer.brace = brace
                layer.brace_label = brace_label
                layer.add(brace, brace_label)

        return layer
    # Helper method for constructor
    def add_edges(self):
        self.edge_groups = VGroup()
        for l1, l2 in zip(self.layers[:-1], self.layers[1:]):
            edge_group = VGroup()
            for n1, n2 in it.product(l1.neurons, l2.neurons):
                edge = self.get_edge(n1, n2)
                edge_group.add(edge)
                n1.edges_out.add(edge)
                n2.edges_in.add(edge)
            self.edge_groups.add(edge_group)
        self.add_to_back(self.edge_groups)
    # Helper method for constructor
    def get_edge(self, neuron1, neuron2):
        if self.arrow:
            return Arrow(
                neuron1.get_center(),
                neuron2.get_center(),
                buff=self.neuron_radius,
                stroke_color=self.edge_color,
                stroke_width=self.edge_stroke_width,
                tip_length=self.arrow_tip_size
            )
        return Line(
            neuron1.get_center(),
            neuron2.get_center(),
            buff=self.neuron_radius,
            stroke_color=self.edge_color,
            stroke_width=self.edge_stroke_width,
        )
    
    # Labels each input neuron with a char l or a LaTeX character
    def label_inputs(self, l):
        self.output_labels = VGroup()
        for n, neuron in enumerate(self.layers[0].neurons):
            label = MathTex(f"{l}_"+"{"+f"{n + 1}"+"}")
            label.set_height(0.3 * neuron.get_height())
            label.move_to(neuron)
            self.output_labels.add(label)
        self.add(self.output_labels)

    # Labels each output neuron with a char l or a LaTeX character
    def label_outputs(self, l):
        self.output_labels = VGroup()
        for n, neuron in enumerate(self.layers[-1].neurons):
            label = MathTex(f"{l}_"+"{"+f"{n + 1}"+"}")
            label.set_height(0.4 * neuron.get_height())
            label.move_to(neuron)
            self.output_labels.add(label)
        self.add(self.output_labels)

    # Labels each neuron in the output layer with text according to an output list
    def label_outputs_text(self, outputs):
        self.output_labels = VGroup()
        for n, neuron in enumerate(self.layers[-1].neurons):
            label = MathTex(outputs[n])
            label.set_height(0.75*neuron.get_height())
            label.move_to(neuron)
            label.shift((neuron.get_width() + label.get_width()/2)*RIGHT)
            self.output_labels.add(label)
        self.add(self.output_labels)

    # Labels the hidden layers with a char l or a LaTeX character
    def label_hidden_layers(self, l):
        self.output_labels = VGroup()
        for layer in self.layers[1:-1]:
            for n, neuron in enumerate(layer.neurons):
                label = MathTex(f"{l}_{n + 1}")
                label.set_height(0.4 * neuron.get_height())
                label.move_to(neuron)
                self.output_labels.add(label)
        self.add(self.output_labels)

    def weight_color(self, pos_color = RED, neg_color = BLUE):
        for i in range(len(self.layer_sizes)-1):
            edge = self.edge_groups[i]
            for j in range(self.layer_sizes[i]*self.layer_sizes[i+1]):
                weight = np.random.rand()
                # edge[j].stroke_width = abs(self.edge_stroke_width*4*(weight-0.5))
                if weight>0.5: edge[j].set_color(pos_color)
                else: edge[j].set_color(neg_color)
        return self

    def weight_width(self, width = 2.0):
        for i in range(len(self.layer_sizes)-1):
            edge = self.edge_groups[i]
            for j in range(self.layer_sizes[i]*self.layer_sizes[i+1]):
                weight = np.random.rand()
                edge[j].stroke_width = abs(width*4*(weight-0.5))
        return self

    def nodes_color(self, color_bottom = BLACK, color_top = GREY):
        colormap = color_gradient([color_bottom,color_top],32)
        for i in self.layers:
            for j in i:
                for k in j:
                    color = colormap[int(np.random.rand()*len(colormap))]
                    k.fill_color = color
        return self

class SquareWithContent(VGroup):
    def __init__(self, content, color=BLUE, fill = 0.5):
        super().__init__()
        self.square = Square(side_length=0.6 ,color=color, fill_opacity=fill)
        self.content = content
        self.add(self.square, content)
        content.move_to(self.square.get_center())

    def clear_content(self):
        self.remove(self.content)
        self.content = None

    @override_animate(clear_content)
    def _clear_content_animation(self, anim_args=None):
        if anim_args is None:
            anim_args = {}
        anim = Uncreate(self.content, **anim_args)
        self.clear_content()
        return anim

class DeviceResponse(Scene):
    def construct(self):
        self.camera.background_color = "#333333"
        title = Title("Dual-signal Sampling Reconstruction")


        devImgIllus = Text('Device Schematic', font="Harding Text Web")\
                        .scale(0.5).to_edge(LEFT, buff=0.8).shift(UP*2.2)
        devImg= ImageMobject("assets/img/devImg.png")\
                    .scale(1.4).to_edge(LEFT, buff=0.6).shift(DOWN*1.2)

        ax_1 = Axes(x_range=[0, 10, 2.0], y_range=[0, 1, 0.2], x_length=5.5, y_length=4, tips=False)\
                .to_edge(RIGHT, buff=0.8).shift(DOWN*1.2)

        x_label = ax_1.get_x_axis_label(Tex(r"$time$").scale(0.8), edge=RIGHT, direction=DOWN, buff=0.25)
        y_label = ax_1.get_y_axis_label(Tex(r"$I_{ds}$").scale(0.8), edge=UP, direction=RIGHT, buff=0.25)

        sigIllus = Text('Photocurrent Signal', font="Harding Text Web")\
                        .scale(0.5).to_edge(LEFT, buff=0.8).shift(UP*2.2+RIGHT*7)

        formu1 = MathTex(r"Signal(",r"R",r",\tau_{rise},",r"\tau_{fall}",r")\Longleftrightarrow E_{in-plane}")\
                    .shift(UP*1.6+RIGHT*4.0).scale(0.7) 
        

        light = Polygon([1, 1.2, 0], [0.8, -1.2, 0], [-0.8, -1.2, 0], [-1, 1.2, 0])\
                    .set_fill(BLUE, opacity=0.5).set_stroke(opacity=0).shift(LEFT*3.8+UP*0.5)

        light_arrows = VGroup()
        for i in range(4):light_arrows += Arrow(start=ORIGIN, end=DOWN*1.2, color=BLUE)
        light_arrows.arrange(LEFT).shift(LEFT*3.8+UP*1.2)

        light_wl = MathTex(r"435 nm")\
                    .shift(UP*1.3+LEFT*2.0).scale(0.7) 


        sig_para = [0.1, 0.8, 3, 5]  # [bottom, height, tau_rise, tau_fall]
        def sig_func(t):
            sig = sig_para[0]
            if t>1 and t<5:
                sig = sig_para[0]+sig_para[1]*(np.tanh(sig_para[2]*(t-1)))
            if t>=5:   
                sig = sig_para[0]+sig_para[1]*np.exp(-sig_para[3]*(t-5))
            return sig
        sig = ax_1.plot(sig_func, x_range=(0, 10, 0.001), color=BLUE, use_smoothing=False)
        area = ax_1.get_area(sig, [1, 5], color=BLUE_E, opacity=0.2)
        line_on = ax_1.get_vertical_line(ax_1.coords_to_point(1, sig_para[0]), line_config={"dashed_ratio": 0.85}, color=GREEN_D)
        line_off = ax_1.get_vertical_line(ax_1.coords_to_point(5, sig_para[0]+sig_para[1]), line_config={"dashed_ratio": 0.85}, color=GREEN_D)


        '''
        # Add Coordinates dots array
        for x in range(-7, 8):
            for y in range(-4, 5):
                if x==0 and y==0:self.add(Dot(np.array([x, y, 0]),radius=0.1, color=GREEN, fill_opacity=0.8))
                self.add(Dot(np.array([x, y, 0]),radius=0.1, color=GOLD_E, fill_opacity=0.3))
        '''

        #self.add(title, devImg, devImgIllus, ax_1, sigIllus,light,x_label,y_label,line_on,line_off,area,formu1,sig,light_arrows,light_wl)
        self.play(Write(title))
        self.play(Write(devImgIllus))
        self.play(FadeIn(devImg))
        self.play(Write(sigIllus))
        self.play(DrawBorderThenFill(ax_1),FadeIn(x_label, y_label))
        self.play(FadeIn(light, shift=DOWN, scale=0.66),\
                    FadeIn(light_arrows, shift=DOWN, scale=0.66),\
                    DrawBorderThenFill(light_wl))
        self.play(Create(sig))
        self.play(FadeIn(line_on,line_off),FadeIn(area))
        self.play(FadeOut(light),FadeOut(light_arrows),FadeOut(light_wl))

        # GREEN
        sig_para = [0.1, 0.6, 1, 1]
        sig = ax_1.plot(sig_func, x_range=(0, 10, 0.001), color=GREEN, use_smoothing=False)
        area = ax_1.get_area(sig, [1, 5], color=GREEN_E, opacity=0.2)

        light = Polygon([1, 1.2, 0], [0.8, -1.2, 0], [-0.8, -1.2, 0], [-1, 1.2, 0])\
                    .set_fill(GREEN, opacity=0.5).set_stroke(opacity=0).shift(LEFT*3.8+UP*0.5)
        light_arrows = VGroup()
        for i in range(4):light_arrows += Arrow(start=ORIGIN, end=DOWN*1.2, color=GREEN)
        light_arrows.arrange(LEFT).shift(LEFT*3.8+UP*1.2)
        light_wl = MathTex(r"532 nm")\
                    .shift(UP*1.3+LEFT*2.0).scale(0.7) 

  
        self.play(FadeIn(light, shift=DOWN, scale=0.66),\
                    FadeIn(light_arrows, shift=DOWN, scale=0.66),\
                    DrawBorderThenFill(light_wl))
        self.play(Create(sig))
        self.play(FadeIn(line_on,line_off),FadeIn(area))

        self.play(FadeOut(light),FadeOut(light_arrows),FadeOut(light_wl))

        # Orange
        sig_para = [0.1, 0.4, 0.7, 0.5]

        sig = ax_1.plot(sig_func, x_range=(0, 10, 0.001), color=ORANGE, use_smoothing=False)
        area = ax_1.get_area(sig, [1, 5], color=ORANGE, opacity=0.2)

        light = Polygon([1, 1.2, 0], [0.8, -1.2, 0], [-0.8, -1.2, 0], [-1, 1.2, 0])\
                    .set_fill(ORANGE, opacity=0.5).set_stroke(opacity=0).shift(LEFT*3.8+UP*0.5)
        light_arrows = VGroup()
        for i in range(4):light_arrows += Arrow(start=ORIGIN, end=DOWN*1.2, color=ORANGE)
        light_arrows.arrange(LEFT).shift(LEFT*3.8+UP*1.2)
        light_wl = MathTex(r"620 nm")\
                    .shift(UP*1.3+LEFT*2.0).scale(0.7) 
  
        self.play(FadeIn(light, shift=DOWN, scale=0.66),\
                    FadeIn(light_arrows, shift=DOWN, scale=0.66),\
                    DrawBorderThenFill(light_wl))
        self.play(Create(sig))
        self.play(FadeIn(line_on,line_off),FadeIn(area))

        self.play(DrawBorderThenFill(formu1))
        self.play(Indicate(formu1[1]), Indicate(formu1[3]))
        self.play(formu1[1].animate.set_color(RED), formu1[3].animate.set_color(PURPLE))
        #self.wait()

        arrow_R = Arrow(start=ORIGIN, end=DOWN*2.8, color=RED,max_tip_length_to_length_ratio=0.1).shift(RIGHT*3+UP*0.8)
        formu_R = MathTex(r"\lambda \uparrow \space\Longrightarrow \thinspace R\downarrow")\
                    .shift(RIGHT*4.7).scale(0.7).set_color(RED_A)

        arrow_tau = Arrow(start=ORIGIN, end=RIGHT*2.5, color=PURPLE,max_tip_length_to_length_ratio=0.1).shift(RIGHT*3.0+DOWN*2)
        formu_tau = MathTex(r"\lambda \uparrow \space\Longrightarrow \thinspace \tau \uparrow")\
                    .shift(DOWN*1.5+RIGHT*5).scale(0.7).set_color(PURPLE_A)

        self.play(DrawBorderThenFill(arrow_R),DrawBorderThenFill(formu_R))
        self.play(DrawBorderThenFill(arrow_tau),DrawBorderThenFill(formu_tau))

class RelaxationSampling(Scene):
    def construct(self):
        self.camera.background_color = "#333333"
        title = Title("Relaxation Time Sampling")

        devImgIllus = Text('Chopping Schematic', font="Harding Text Web")\
                        .scale(0.5).to_edge(LEFT, buff=0.8).shift(UP*2.2)
        devImg= ImageMobject("assets/img/devChopping.png")\
                    .scale(1.0).to_edge(LEFT, buff=-0.3).shift(DOWN*1.2)

        # Add Coordinates dots array
        for x in range(-7, 8):
            for y in range(-4, 5):
                pass


        ax_1 = Axes(x_range=[0, 30, 3.0], y_range=[0, 1, 0.5], x_length=8, y_length=1.7, tips=False)\
                .to_edge(RIGHT, buff=0.8).shift(UP*1.5)
        x_1_label = ax_1.get_x_axis_label(Tex(r"$t$").scale(0.7), edge=RIGHT, direction=RIGHT, buff=0.25)
        y_1_label = ax_1.get_y_axis_label(Tex(r"Chop").scale(0.7).rotate(90 * DEGREES), edge=LEFT, direction=LEFT, buff=0.15)
        ax_chop = VGroup(ax_1,x_1_label,y_1_label)

        ax_2 = Axes(x_range=[0, 30, 3.0], y_range=[0, 1, 0.5], x_length=8, y_length=1.7, tips=False)\
                .to_edge(RIGHT, buff=0.8).shift(DOWN*0.5)
        x_2_label = ax_2.get_x_axis_label(Tex(r"$t$").scale(0.7), edge=RIGHT, direction=RIGHT, buff=0.25)
        y_2_label = ax_2.get_y_axis_label(Tex(r"$I_{ds}$").scale(0.7).rotate(90 * DEGREES), edge=LEFT, direction=LEFT, buff=0.15)
        ax_sig = VGroup(ax_2,x_2_label,y_2_label)

        ax_3 = Axes(x_range=[0, 30, 3.0], y_range=[0, 1, 0.5], x_length=8, y_length=1.7, tips=False)\
                .to_edge(RIGHT, buff=0.8).shift(DOWN*2.5)
        x_3_label = ax_3.get_x_axis_label(Tex(r"$t$").scale(0.7), edge=RIGHT, direction=RIGHT, buff=0.25)
        y_3_label = ax_3.get_y_axis_label(Tex(r"LP($I_{ds}$)").scale(0.7).rotate(90 * DEGREES), edge=LEFT, direction=LEFT, buff=0.15)
        ax_sin = VGroup(ax_3,x_3_label,y_3_label)

        sig_para = [0.1, 0.8, 3, 5, 2, 0.6]  # [bottom, height, tau_rise, tau_fall, phi, amp]
        def chop_func(t):
            t = t % 10
            sig = 0.1
            if t>1 and t<5:
                sig = 0.9
            return sig
        def sig_func(t):
            t = t % 10
            sig = sig_para[0]
            if t>1 and t<5:
                sig = sig_para[0]+sig_para[1]*(np.tanh(sig_para[2]*(t-1)))
            if t>=5:   
                sig = sig_para[0]+sig_para[1]*np.exp(-sig_para[3]*(t-5))
            return sig
        def sin_func(t):
            return sig_para[5]/2*np.sin(math.pi/5*(t-sig_para[4]))+0.5

        sig_chop = ax_1.plot(chop_func, x_range=(0, 30, 0.01), color=WHITE, use_smoothing=False)
        sig_ids = ax_2.plot(sig_func, x_range=(0, 30, 0.01), color=BLUE, use_smoothing=False)
        sig_sin = ax_3.plot(sin_func, x_range=(0, 30, 0.01), color=BLUE, use_smoothing=False)

        line_off = ax_3.get_vertical_line(ax_3.coords_to_point(5, 3.3), color=MAROON)
        line_off_point = ax_3.get_lines_to_point(ax_3.c2p(5+sig_para[4], 0.5), color=MAROON)
        double_arrow_off = DoubleArrow(start=0.6*LEFT, end=0.45*RIGHT, tip_length=0.2, color=MAROON).shift(DOWN*2.5)
        off_tau_text = MathTex(r"\phi_{fall}").scale(0.7).set_color(MAROON_A).shift(DOWN*2.8+LEFT*0.1)
        off_tau=VGroup(line_off,line_off_point,double_arrow_off,off_tau_text)

        line_on = ax_3.get_vertical_line(ax_3.coords_to_point(11, 3.3), color=PURPLE)
        line_on_point = ax_3.get_lines_to_point(ax_3.c2p(10+sig_para[4], 0.5), color=PURPLE)
        double_arrow_on = DoubleArrow(start=1.0*RIGHT, end=1.8*RIGHT, tip_length=0.2, color=PURPLE).shift(DOWN*2.5)
        on_tau_text = MathTex(r"\phi_{rise}").scale(0.7).set_color(PURPLE_A).shift(DOWN*2.2+RIGHT*0.85)
        on_tau=VGroup(line_on,line_on_point,double_arrow_on,on_tau_text)

        R_square = SquareWithContent(Tex(r"$R_{ij}$").scale(0.6),color=BLUE, fill=0.5)\
                        .shift(DOWN*2+RIGHT*3.87)
        T_square = SquareWithContent(Tex(r"$\tau_{ij}$").scale(0.6),color=RED, fill=0.5)\
                        .shift(DOWN*2+RIGHT*3.12)

        amp_line = ax_3.get_lines_to_point(ax_3.c2p(29.5, 0.2), color=BLUE)
        amp_arrow = DoubleArrow(start=0.75*DOWN, end=0.75*UP, tip_length=0.2, color=BLUE).shift(RIGHT*4.85+DOWN*2.5)

        boxMatrix = VGroup()
        for i in range(5):
            boxVector = VGroup()
            for j in range(4):
                t = Tex("$R_{"+str(j)+str(i)+"}$").scale(0.6)
                boxVector += SquareWithContent(t,color=BLUE, fill=0.6*np.tanh(np.random.rand()*(i+1)*(j+1)))
            boxVector.arrange(DOWN,buff=0.2)
            boxMatrix+=boxVector
        boxMatrix.arrange(RIGHT,buff=0.2).to_edge(LEFT, buff=0.8).shift(DOWN*0.5)


        boxMatrix_ext = VGroup()
        for i in range(5):
            boxVector_ext = VGroup()
            for j in range(4):
                r = Tex("$R_{"+str(j)+str(i)+"}$").scale(0.6)
                t = Tex(r"$\tau_{"+str(j)+str(i)+"}$").scale(0.6)
                R = SquareWithContent(r,color=BLUE, fill=0.6*np.tanh(np.random.rand()*(i+1)*(j+1)))
                T = SquareWithContent(t,color=RED, fill=0.6*np.tanh(np.random.rand()*(4-i)*(j+1)))
                boxVector_ext += VGroup(R,T).arrange(DOWN,buff=0.2)
            boxVector_ext.arrange(DOWN,buff=0.2)
            boxMatrix_ext+=boxVector_ext
        boxMatrix_ext.arrange(RIGHT,buff=0.2).to_edge(LEFT, buff=0.8).shift(DOWN*0.65)

        #self.add(title,ax_chop,ax_sig,ax_sin,sig_chop,sig_ids,sig_sin,\
        #   off_tau,on_tau,boxMatrix,boxMatrix_ext,R_square,T_square,amp_arrow,amp_line)

        sig_para = [0.1, 0.6, 2, 2, 3, 0.5]
        sig_ids_1 = ax_2.plot(sig_func, x_range=(0, 30, 0.01), color=GREEN, use_smoothing=False)
        sig_sin_1 = ax_3.plot(sin_func, x_range=(0, 30, 0.01), color=GREEN, use_smoothing=False)

        sig_para = [0.1, 0.4, 1, 1, 4, 0.4]
        sig_ids_2 = ax_2.plot(sig_func, x_range=(0, 30, 0.01), color=ORANGE, use_smoothing=False)
        sig_sin_2 = ax_3.plot(sin_func, x_range=(0, 30, 0.01), color=ORANGE, use_smoothing=False)

        # animation
        self.play(Write(title))
        self.play(Write(devImgIllus))
        self.play(FadeIn(devImg),DrawBorderThenFill(ax_chop))
        self.play(Create(sig_chop))
        self.play(DrawBorderThenFill(ax_sig))
        self.play(Create(sig_ids))
        self.play(Create(sig_ids_1))
        self.play(Create(sig_ids_2))

        self.play(FadeOut(sig_ids_1,sig_ids_2,devImg,devImgIllus))
        self.play(TransformFromCopy(sig_ids,boxMatrix[0][0]))
        self.play(ReplacementTransform(sig_ids,sig_ids_1))
        self.play(TransformFromCopy(sig_ids_1,boxMatrix[0][1]))
        self.play(ReplacementTransform(sig_ids_1,sig_ids_2))
        self.play(ReplacementTransform(sig_ids_2,boxMatrix[0][2]))
        self.play(FadeIn(boxMatrix))


        sig_para = [0.1, 0.8, 3, 5, 2, 0.6]
        sig_ids = ax_2.plot(sig_func, x_range=(0, 30, 0.01), color=BLUE, use_smoothing=False)
        sig_sin = ax_3.plot(sin_func, x_range=(0, 30, 0.01), color=BLUE, use_smoothing=False)

        sig_para = [0.1, 0.6, 2, 2, 3, 0.5]
        sig_ids_1 = ax_2.plot(sig_func, x_range=(0, 30, 0.01), color=GREEN, use_smoothing=False)
        sig_sin_1 = ax_3.plot(sin_func, x_range=(0, 30, 0.01), color=GREEN, use_smoothing=False)

        sig_para = [0.1, 0.4, 1, 1, 4, 0.4]
        sig_ids_2 = ax_2.plot(sig_func, x_range=(0, 30, 0.01), color=ORANGE, use_smoothing=False)
        sig_sin_2 = ax_3.plot(sin_func, x_range=(0, 30, 0.01), color=ORANGE, use_smoothing=False)

        self.play(DrawBorderThenFill(ax_sin))
        self.play(Create(sig_sin_2),Create(sig_ids_2))
        self.wait(0.5)
        self.play(ReplacementTransform(sig_sin_2,sig_sin_1),\
                    ReplacementTransform(sig_ids_2,sig_ids_1))
        self.wait(0.5)
        self.play(ReplacementTransform(sig_sin_1,sig_sin),\
                    ReplacementTransform(sig_ids_1,sig_ids))
        self.play(DrawBorderThenFill(off_tau))
        self.play(DrawBorderThenFill(on_tau))

        self.play(Indicate(off_tau_text),Indicate(on_tau_text))
        self.play(DrawBorderThenFill(amp_line),DrawBorderThenFill(amp_arrow))

        self.play(ReplacementTransform(amp_arrow,R_square))
        self.play(ReplacementTransform(double_arrow_off,T_square))

        self.play(Transform(boxMatrix,boxMatrix_ext))

        self.wait()

class NeuralNetworkReconstruction(Scene):
    def construct(self):
        self.camera.background_color = "#333333"
        title = Title("Neural Network Reconstruction")
        '''
        # Add Coordinates dots array
        for x in range(-7, 8):
            for y in range(-4, 5):
                if x==0 and y==0:self.add(Dot(np.array([x, y, 0]),radius=0.1, color=GREEN, fill_opacity=0.8))
                self.add(Dot(np.array([x, y, 0]),radius=0.1, color=GOLD_E, fill_opacity=0.3))
        '''

        ax_1 = Axes(x_range=[0, 30, 3.0], y_range=[0, 1, 0.5], x_length=8, y_length=1.7, tips=False)\
                .to_edge(LEFT, buff=0.8).shift(UP*1.5)
        x_1_label = ax_1.get_x_axis_label(Tex(r"$t$").scale(0.7), edge=RIGHT, direction=RIGHT, buff=0.25)
        y_1_label = ax_1.get_y_axis_label(Tex(r"Chop").scale(0.7).rotate(90 * DEGREES), edge=LEFT, direction=LEFT, buff=0.15)
        ax_chop = VGroup(ax_1,x_1_label,y_1_label)

        ax_2 = Axes(x_range=[0, 30, 3.0], y_range=[0, 1, 0.5], x_length=8, y_length=1.7, tips=False)\
                .to_edge(LEFT, buff=0.8).shift(DOWN*0.5)
        x_2_label = ax_2.get_x_axis_label(Tex(r"$t$").scale(0.7), edge=RIGHT, direction=RIGHT, buff=0.25)
        y_2_label = ax_2.get_y_axis_label(Tex(r"$I_{ds}$").scale(0.7).rotate(90 * DEGREES), edge=LEFT, direction=LEFT, buff=0.15)
        ax_sig = VGroup(ax_2,x_2_label,y_2_label)

        ax_3 = Axes(x_range=[0, 30, 3.0], y_range=[0, 1, 0.5], x_length=8, y_length=1.7, tips=False)\
                .to_edge(LEFT, buff=0.8).shift(DOWN*2.5)
        x_3_label = ax_3.get_x_axis_label(Tex(r"$t$").scale(0.7), edge=RIGHT, direction=RIGHT, buff=0.25)
        y_3_label = ax_3.get_y_axis_label(Tex(r"LP($I_{ds}$)").scale(0.7).rotate(90 * DEGREES), edge=LEFT, direction=LEFT, buff=0.15)
        ax_sin = VGroup(ax_3,x_3_label,y_3_label)

        sig_para = [0.1, 0.8, 3, 5, 2, 0.6]  # [bottom, height, tau_rise, tau_fall, phi, amp]
        def chop_func(t):
            t = t % 10
            sig = 0.1
            if t>1 and t<5:
                sig = 0.9
            return sig
        def sig_func(t):
            t = t % 10
            sig = sig_para[0]
            if t>1 and t<5:
                sig = sig_para[0]+sig_para[1]*(np.tanh(sig_para[2]*(t-1)))
            if t>=5:   
                sig = sig_para[0]+sig_para[1]*np.exp(-sig_para[3]*(t-5))
            return sig
        def sin_func(t):
            return sig_para[5]/2*np.sin(math.pi/5*(t-sig_para[4]))+0.5

        sig_para = [0.1, 0.8, 3, 5, 2, 0.6]

        sig_chop = ax_1.plot(chop_func, x_range=(0, 30, 0.01), color=WHITE, use_smoothing=False)
        sig_ids = ax_2.plot(sig_func, x_range=(0, 30, 0.01), color=BLUE, use_smoothing=False)
        sig_sin = ax_3.plot(sin_func, x_range=(0, 30, 0.01), color=BLUE, use_smoothing=False)

        line_off = ax_3.get_vertical_line(ax_3.coords_to_point(5, 3.3), color=RED)
        line_off_point = ax_3.get_lines_to_point(ax_3.c2p(5+sig_para[4], 0.5), color=RED)
        off_tau_text = MathTex(r"\phi_{fall}").scale(0.7).set_color(RED_A).shift(DOWN*3.6+LEFT*4.6)
        off_tau=VGroup(line_off,line_off_point,off_tau_text)

        line_on = ax_3.get_vertical_line(ax_3.coords_to_point(11, 3.3), color=PURPLE)
        line_on_point = ax_3.get_lines_to_point(ax_3.c2p(10+sig_para[4], 0.5), color=PURPLE)
        on_tau_text = MathTex(r"\phi_{rise}").scale(0.7).set_color(PURPLE_A).shift(DOWN*3.6+LEFT*3.0)
        on_tau=VGroup(line_on,line_on_point,on_tau_text)

        R_square = SquareWithContent(Tex(r"$R_{ij}$").scale(0.6),color=BLUE, fill=0.5)\
                        .shift(DOWN*2+RIGHT*3.87)
        T_square = SquareWithContent(Tex(r"$\tau_{ij}$").scale(0.6),color=RED, fill=0.5)\
                        .shift(DOWN*2+RIGHT*3.12)

        amp_line = ax_3.get_lines_to_point(ax_3.c2p(30, 0.5-sig_para[5]/2), color=BLUE)
        amp_arrow = DoubleArrow(start=(0.5*sig_para[5]/0.6+0.25)*DOWN, end=(0.5*sig_para[5]/0.6+0.25)*UP, tip_length=0.2, color=BLUE).shift(RIGHT*(0.32+8/30*(sig_para[4]-2))+DOWN*2.5)

        amp_group=VGroup(amp_line,amp_arrow)
        tau_group = VGroup(off_tau, on_tau)

        t0 = Table(
            [[" ", "   "],
            [" ","   "],
            [" ","   "],
            [" ","   "]],
            row_labels=[Tex("$G_1$").scale(1.5), Tex("$G_2$").scale(1.5), Tex("$G_i$").scale(1.5), Tex("$G_m$").scale(1.5)],
            col_labels=[Tex("$R_i$").scale(1.5), Tex(r"$\tau_i$").scale(1.5)],
            top_left_entry=Text(" "),
            v_buff = 1.2,
            h_buff = 1.2).scale(0.6).to_edge(RIGHT, buff=0.8).to_edge(DOWN, buff=0.6)

        R_1 = SquareWithContent(Tex(r"$R_{1}$").scale(0.85),color=BLUE, fill=0.5)\
                        .shift(UP*0.45+RIGHT*4.75)
        T_1 = SquareWithContent(Tex(r"$\tau_{1}$").scale(0.85),color=RED, fill=0.5)\
                        .shift(UP*0.45+RIGHT*5.85)

        R_2 = SquareWithContent(Tex(r"$R_{2}$").scale(0.85),color=BLUE, fill=0.5)\
                        .shift(UP*(0.45-1.1)+RIGHT*4.75)
        T_2 = SquareWithContent(Tex(r"$\tau_{2}$").scale(0.85),color=RED, fill=0.5)\
                        .shift(UP*(0.45-1.1)+RIGHT*5.85)

        R_i = SquareWithContent(Tex(r"$R_{i}$").scale(0.85),color=BLUE, fill=0.5)\
                        .shift(UP*(0.45-2.2)+RIGHT*4.75)
        T_i = SquareWithContent(Tex(r"$\tau_{i}$").scale(0.85),color=RED, fill=0.5)\
                        .shift(UP*(0.45-2.2)+RIGHT*5.85)

        R_m = SquareWithContent(Tex(r"$R_{m}$").scale(0.85),color=BLUE, fill=0.5)\
                        .shift(UP*(0.45-3.3)+RIGHT*4.75)
        T_m = SquareWithContent(Tex(r"$\tau_{m}$").scale(0.85),color=RED, fill=0.5)\
                        .shift(UP*(0.45-3.3)+RIGHT*5.85)


        self.play(Write(title))
        self.play(DrawBorderThenFill(ax_chop),\
                    DrawBorderThenFill(ax_sig),\
                    DrawBorderThenFill(ax_sin))
        self.play(Create(sig_chop),\
                    Create(sig_ids),\
                    Create(sig_sin))
        self.play(DrawBorderThenFill(tau_group),\
                    DrawBorderThenFill(amp_group))
        self.play(DrawBorderThenFill(t0))
        self.play(TransformFromCopy(amp_arrow,R_1))
        self.play(TransformFromCopy(off_tau_text,T_1))


        sig_para = [0.1, 0.6, 2, 4, 3, 0.5, BLUE]
        sig_ids_1 = ax_2.plot(sig_func, x_range=(0, 30, 0.01), color=sig_para[6], use_smoothing=False)
        sig_sin_1 = ax_3.plot(sin_func, x_range=(0, 30, 0.01), color=sig_para[6], use_smoothing=False)

        line_off_1 = ax_3.get_vertical_line(ax_3.coords_to_point(5, 3.3), color=RED)
        line_off_point_1 = ax_3.get_lines_to_point(ax_3.c2p(5+sig_para[4], 0.5), color=RED)
        off_tau_text_1 = MathTex(r"\phi_{fall}").scale(0.7).set_color(RED_A).shift(DOWN*3.6+LEFT*4.6)
        off_tau_1=VGroup(line_off_1,line_off_point_1,off_tau_text_1)

        line_on_1 = ax_3.get_vertical_line(ax_3.coords_to_point(11, 3.3), color=PURPLE)
        line_on_point_1 = ax_3.get_lines_to_point(ax_3.c2p(10+sig_para[4], 0.5), color=PURPLE)
        on_tau_text_1 = MathTex(r"\phi_{rise}").scale(0.7).set_color(PURPLE_A).shift(DOWN*3.6+LEFT*3.0)
        on_tau_1=VGroup(line_on_1,line_on_point_1,on_tau_text_1)

        amp_line_1 = ax_3.get_lines_to_point(ax_3.c2p(30, 0.5-sig_para[5]/2), color=BLUE)
        amp_arrow_1 = DoubleArrow(start=(0.5*sig_para[5]/0.6+0.25)*DOWN, end=(0.5*sig_para[5]/0.6+0.25)*UP, tip_length=0.2, color=sig_para[6]).shift(RIGHT*(0.32+8/30*(sig_para[4]-2))+DOWN*2.5)

        amp_group_1=VGroup(amp_line_1,amp_arrow_1)
        tau_group_1 = VGroup(off_tau_1, on_tau_1)

        self.play(ReplacementTransform(sig_ids,sig_ids_1),\
                    ReplacementTransform(sig_sin,sig_sin_1),\
                    ReplacementTransform(amp_group,amp_group_1),\
                    ReplacementTransform(tau_group,tau_group_1))

        self.play(TransformFromCopy(amp_arrow_1,R_2))
        self.play(TransformFromCopy(off_tau_text_1,T_2))

        sig_para = [0.1, 0.6, 1, 3, 4, 0.4, BLUE]
        sig_ids = ax_2.plot(sig_func, x_range=(0, 30, 0.01), color=sig_para[6], use_smoothing=False)
        sig_sin = ax_3.plot(sin_func, x_range=(0, 30, 0.01), color=sig_para[6], use_smoothing=False)

        line_off = ax_3.get_vertical_line(ax_3.coords_to_point(5, 3.3), color=RED)
        line_off_point = ax_3.get_lines_to_point(ax_3.c2p(5+sig_para[4], 0.5), color=RED)
        off_tau_text = MathTex(r"\phi_{fall}").scale(0.7).set_color(RED_A).shift(DOWN*3.6+LEFT*4.6)
        off_tau=VGroup(line_off,line_off_point,off_tau_text)

        line_on = ax_3.get_vertical_line(ax_3.coords_to_point(11, 3.3), color=PURPLE)
        line_on_point = ax_3.get_lines_to_point(ax_3.c2p(10+sig_para[4], 0.5), color=PURPLE)
        on_tau_text = MathTex(r"\phi_{rise}").scale(0.7).set_color(PURPLE_A).shift(DOWN*3.6+LEFT*3.0)
        on_tau=VGroup(line_on,line_on_point,on_tau_text)

        amp_line = ax_3.get_lines_to_point(ax_3.c2p(30, 0.5-sig_para[5]/2), color=BLUE)
        amp_arrow = DoubleArrow(start=(0.5*sig_para[5]/0.6+0.25)*DOWN, end=(0.5*sig_para[5]/0.6+0.25)*UP, tip_length=0.2, color=sig_para[6]).shift(RIGHT*(0.32+8/30*(sig_para[4]-2))+DOWN*2.5)

        amp_group=VGroup(amp_line,amp_arrow)
        tau_group = VGroup(off_tau, on_tau)

        self.play(ReplacementTransform(sig_ids_1,sig_ids),\
                    ReplacementTransform(sig_sin_1,sig_sin),\
                    ReplacementTransform(amp_group_1,amp_group),\
                    ReplacementTransform(tau_group_1,tau_group))

        self.play(TransformFromCopy(amp_arrow,R_i))
        self.play(TransformFromCopy(off_tau_text,T_i))



        sig_para = [0.1, 0.32, 1, 1.5, 3, 0.32, BLUE]
        sig_ids_1 = ax_2.plot(sig_func, x_range=(0, 30, 0.01), color=sig_para[6], use_smoothing=False)
        sig_sin_1 = ax_3.plot(sin_func, x_range=(0, 30, 0.01), color=sig_para[6], use_smoothing=False)

        line_off_1 = ax_3.get_vertical_line(ax_3.coords_to_point(5, 3.3), color=RED)
        line_off_point_1 = ax_3.get_lines_to_point(ax_3.c2p(5+sig_para[4], 0.5), color=RED)
        off_tau_text_1 = MathTex(r"\phi_{fall}").scale(0.7).set_color(RED_A).shift(DOWN*3.6+LEFT*4.6)
        off_tau_1=VGroup(line_off_1,line_off_point_1,off_tau_text_1)

        line_on_1 = ax_3.get_vertical_line(ax_3.coords_to_point(11, 3.3), color=PURPLE)
        line_on_point_1 = ax_3.get_lines_to_point(ax_3.c2p(10+sig_para[4], 0.5), color=PURPLE)
        on_tau_text_1 = MathTex(r"\phi_{rise}").scale(0.7).set_color(PURPLE_A).shift(DOWN*3.6+LEFT*3.0)
        on_tau_1=VGroup(line_on_1,line_on_point_1,on_tau_text_1)

        amp_line_1 = ax_3.get_lines_to_point(ax_3.c2p(30, 0.5-sig_para[5]/2), color=BLUE)
        amp_arrow_1 = DoubleArrow(start=(0.5*sig_para[5]/0.6+0.25)*DOWN, end=(0.5*sig_para[5]/0.6+0.25)*UP, tip_length=0.2, color=sig_para[6]).shift(RIGHT*(0.32+8/30*(sig_para[4]-2))+DOWN*2.5)

        amp_group_1=VGroup(amp_line_1,amp_arrow_1)
        tau_group_1 = VGroup(off_tau_1, on_tau_1)

        self.play(ReplacementTransform(sig_ids,sig_ids_1),\
                    ReplacementTransform(sig_sin,sig_sin_1),\
                    ReplacementTransform(amp_group,amp_group_1),\
                    ReplacementTransform(tau_group,tau_group_1))

        self.play(TransformFromCopy(amp_arrow_1,R_m))
        self.play(TransformFromCopy(off_tau_text_1,T_m))


        rt_group = VGroup(R_1,R_2,R_i,R_m,T_1,T_2,T_i,T_m)

        R_1_0 = SquareWithContent(Tex(r"$R_{1}$").scale(0.85),color=BLUE, fill=0.5)\
                        .shift(UP*0.45+RIGHT*4.75)
        T_1_0 = SquareWithContent(Tex(r"$\tau_{1}$").scale(0.85),color=RED, fill=0.5)\
                        .shift(UP*0.45+RIGHT*5.85)

        R_2_0 = SquareWithContent(Tex(r"$R_{2}$").scale(0.85),color=BLUE, fill=0.5)\
                        .shift(UP*(0.45-1.1)+RIGHT*4.75)
        T_2_0 = SquareWithContent(Tex(r"$\tau_{2}$").scale(0.85),color=RED, fill=0.5)\
                        .shift(UP*(0.45-1.1)+RIGHT*5.85)

        R_i_0 = SquareWithContent(Tex(r"$R_{i}$").scale(0.85),color=BLUE, fill=0.5)\
                        .shift(UP*(0.45-2.2)+RIGHT*4.75)
        T_i_0 = SquareWithContent(Tex(r"$\tau_{i}$").scale(0.85),color=RED, fill=0.5)\
                        .shift(UP*(0.45-2.2)+RIGHT*5.85)

        R_m_0 = SquareWithContent(Tex(r"$R_{m}$").scale(0.85),color=BLUE, fill=0.5)\
                        .shift(UP*(0.45-3.3)+RIGHT*4.75)
        T_m_0 = SquareWithContent(Tex(r"$\tau_{m}$").scale(0.85),color=RED, fill=0.5)\
                        .shift(UP*(0.45-3.3)+RIGHT*5.85)


        R_group_0 = VGroup(R_1_0,R_2_0,R_i_0,R_m_0).arrange(DOWN,buff=0.2)

        T_group_0 = VGroup(T_1_0,T_2_0,T_i_0,T_m_0).arrange(DOWN,buff=0.2)

        RT_group_0 = VGroup(R_group_0,T_group_0)\
                    .arrange(DOWN,buff=0.2).to_edge(LEFT,buff=1.0).to_edge(DOWN,buff=0.4).scale(0.9).shift(DOWN*0.2)

        self.play(FadeOut(VGroup(ax_chop,ax_sig,ax_sin,sig_chop,sig_ids,sig_sin,t0,sig_ids_1,sig_sin_1,amp_group_1,tau_group_1)))
        self.play(ReplacementTransform(rt_group,RT_group_0))

        norm_text = MathTex(r"\xrightarrow{Norm.}").shift(LEFT*4.5+DOWN*0.57)
        self.play(DrawBorderThenFill(norm_text))


        netList = [8, 8, 8, 8, 8, 6]
        myNetwork = NeuralNetworkMobject(netList).shift(DOWN*0.7).scale(0.85)
        myNetwork.label_inputs(r"x")
        myNetwork.label_outputs(r"\hat{S}")
        myNetwork.weight_color().weight_width().nodes_color()

        self.play(Write(myNetwork))
        self.wait(0.2)

        ax_s = Axes(x_range=[0, 10, 1.0], y_range=[0, 1, 0.5], x_length=5, y_length=1.7, tips=False)\
                .to_edge(LEFT, buff=0.8).shift(UP*1.5).rotate(-90*DEGREES).to_edge(RIGHT,buff=0.8).to_edge(DOWN,buff=0.8)
        x_s_label = ax_s.get_x_axis_label(Tex(r"$\lambda$").scale(0.7), edge=DOWN, direction=RIGHT, buff=0.25)
        y_s_label = ax_s.get_y_axis_label(Tex(r"Spec.").scale(0.7), edge=UP, direction=UP, buff=0.15)
        ax_spec = VGroup(ax_s,x_s_label,y_s_label)

        specList = []
        for item in myNetwork.layers[5][0]:
            num = color_to_rgb(item.fill_color)
            specList.append(num[0])
        print(specList)
        def func(x):
            return specList[0]*np.exp(-pow(x-(10/12+0*10/6),2))+\
                    specList[1]*np.exp(-pow(x-(10/12+1*10/6),2))+\
                    specList[2]*np.exp(-pow(x-(10/12+2*10/6),2))+\
                    specList[3]*np.exp(-pow(x-(10/12+3*10/6),2))+\
                    specList[4]*np.exp(-pow(x-(10/12+4*10/6),2))+\
                    specList[5]*np.exp(-pow(x-(10/12+5*10/6),2))

        spec = ax_s.plot(func, color=YELLOW_D).set_color([PURPLE, BLUE, TEAL, GREEN, YELLOW_D, ORANGE, RED])

        self.play(DrawBorderThenFill(ax_spec))
        self.play(TransformFromCopy(myNetwork.layers[5][0],spec))
        
        # self.play(ApplyMethod(myNetwork.weight_color))
        for x in range(10):
            self.play(ApplyFunction(updateNetwork,myNetwork),FadeOut(spec))
            self.wait(0.2)
            specList = []
            for item in myNetwork.layers[5][0]:
                num = color_to_rgb(item.fill_color)
                specList.append(num[0])
            print(specList)
            def func(x):
                return specList[0]*np.exp(-pow(x-(10/12+0*10/6),2))+\
                        specList[1]*np.exp(-pow(x-(10/12+1*10/6),2))+\
                        specList[2]*np.exp(-pow(x-(10/12+2*10/6),2))+\
                        specList[3]*np.exp(-pow(x-(10/12+3*10/6),2))+\
                        specList[4]*np.exp(-pow(x-(10/12+4*10/6),2))+\
                        specList[5]*np.exp(-pow(x-(10/12+5*10/6),2))

            spec = ax_s.plot(func, color=YELLOW_D).set_color([PURPLE, BLUE, TEAL, GREEN, YELLOW_D, ORANGE, RED])

            self.play(TransformFromCopy(myNetwork.layers[5][0],spec))

        self.wait()
        

if __name__ == "__main__":
    import os

    os.system(r'cd G:\Order\MyPythonLib\Manim\PhdDissertation')
    os.system(r'manim -pqh DualSignalReconstruction.py NeuralNetworkReconstruction')