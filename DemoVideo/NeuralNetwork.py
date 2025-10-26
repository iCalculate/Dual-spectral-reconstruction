from manim import *
import itertools as it

def updateNetwork(NeuralNetworkMobject):
    return NeuralNetworkMobject.weight_color().weight_width().nodes_color()


class myNeuralNetwork(Scene):
    def construct(self):
        title = Title(f"Neural Network Animation")

        netList = [4, 6, 6, 6, 6, 6, 4, 4, 2]
        myNetwork = NeuralNetworkMobject(netList).shift(DOWN*0.7)
        myNetwork.label_inputs(r"x")
        myNetwork.label_outputs(r"\hat{y}")
        myNetwork.weight_color().weight_width().nodes_color()

        self.play(Write(title))
        self.play(Write(myNetwork))
        self.wait(0.2)
        self.play(ApplyWave(myNetwork.edge_groups))
        # self.play(ApplyMethod(myNetwork.weight_color))
        # for x in range(2):
        #     self.play(ApplyFunction(updateNetwork,myNetwork))
        #     self.wait(0.2)




# A customizable Sequential Neural Network
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




if __name__ == "__main__":
    import os

    os.system(r'cd G:\Order\MyPythonLib\Manim\PhdDissertation')
    os.system(r'manim -pql NeuralNetwork.py ManimiCLogo')