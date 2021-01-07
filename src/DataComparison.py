import matplotlib
import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':


    #def __init__(self):



    # ---------------shortest_path--------------#
    title = "shortest path run time"
    labels = ['G10', 'G1K', 'G20K', 'G30K', 'G100K_1M']
    nx_runtime = [0.0, 0.004000, 0.120001, 0.197962, 1.258011]
    ga_runtime = [0.0, 0.009001, 0.320001, 0.662059, 4.903963]
    ga_java_runtime = [1, 1, 1, 1, 1]
    # -----------connected_components-----------#
    # title="connected_components run time"
    # labels = ['G10', 'G1K', 'A5', 'G100K', 'G5']
    # nx_runtime = [0.0, 0.015972, 0.0, 0.013471, 0.00]
    # ga_runtime = [0.003988, 0.008812, 0.0, 0.01246, 0.002]
    # ga_java_runtime = [0.1, 0.005, 0.465, 3.6, 0.002]
    # -----------connected_component-----------#
    # title="connected_component run time"
    # labels = ['G10', 'G1K', 'A5', 'G100K', 'G100']
    # nx_runtime = [0.0, 0.021676,0.001008, 0.108131, 0.005307]
    # ga_runtime = [0.0, 0.014198, 0.0, 0.236313, 0.0]
    # ga_java_runtime = [0.1, 0.005, 0.465, 3.6, 0.002]

    x = np.arange(len(labels))  # the label locations
    width = 0.2  # the width of the bars

    fig, ax = plt.subplots()
    nx = ax.bar(x - width, nx_runtime, width, label='networkx')
    ga = ax.bar(x , ga_runtime, width, label='GraphAlgo')
    ga_java = ax.bar(x+width, ga_java_runtime, width, label='DW_GraphAlgo-java')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('runtime-seconds')
    ax.set_title(title)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()


    def autolabel(rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')


    autolabel(nx)
    autolabel(ga)
    autolabel(ga_java)
    fig.tight_layout()

    plt.show()
