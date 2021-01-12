import matplotlib
import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':
    # ---------------shortest path--------------#
    # title = "Shortest path"
    # labels = ['G10', 'G1K', 'G20K', 'G30K']
    # nx_runtime = [0.0, 0.004000, 0.120001, 0.197962]
    # ga_runtime = [0.0, 0.009001, 0.320001, 0.662059]
<<<<<<< HEAD
    # ga_java_runtime = [0, 0.001, 0.221, 0.316]
    # -----------connected_components-----------#
    title = "node's strongly connected component"
    labels = ['G10', 'G1K', 'A5']
    nx_runtime = [0.0, 0.015972, 0.0]
    ga_runtime = [0.003988, 0.008812, 0.0]
    ga_java_runtime = [0, 0, 0]
    # -----------connected_component-----------#
    # title="connected_component run time"
=======
    # ga_java_runtime = [0, 0.001, 0.221,0.316]
    # -----------Connected components-----------#
    # title = "Connected components "
    # labels = ['G10', 'G1K', 'A5']
    # nx_runtime = [0.0, 0.015972, 0.0]
    # ga_runtime = [0.003988, 0.008812, 0.0]
    # ga_java_runtime = [0, 0.01219, 0]
    # -----------Connected component-----------#
    # title="Connected component"
>>>>>>> 83d8f1cfa69d578cbb0d12a8766e60f57dba8a1d
    # labels = ['G10', 'G1K', 'A5',]
    # nx_runtime = [0.0, 0.021676,0.001008]
    # ga_runtime = [0.0, 0.014198, 0.0]
    # ga_java_runtime = [0, 0, 0.009,]
    # ----------------- on circle -----------------#
    # ---------------shortest_path--------------#
    # title = "Shortest path"
    # labels = ['G30K', 'G20K', 'G10K']
    # nx_runtime = [0.899918, 0.151634, 0.199136]
    # ga_runtime = [2.143094, 0.419052, 0.864932]
    # -----------Connected components-----------#
    # title = "Connected components"
    # labels = ['G30K', 'G20K', 'G10K']
    # nx_runtime = [0.0, 0.0, 0.0]
    # ga_runtime = [0.860833, 0.727657, 0.484948]
    # -----------Connected component-----------#
    title="Connected component"
    labels = ['G30K', 'G20K', 'G10K']
    nx_runtime = [0.835775, 0.888256,0.204939]
    ga_runtime = [1.837091, 0.936692, 0.306809]

    x = np.arange(len(labels))  # the label locations
    width = 0.2  # the width of the bars

    fig, ax = plt.subplots(figsize=(9.0, 9.0))
    nx = ax.bar(x - width, nx_runtime, width, label='networkx')
    ga = ax.bar(x, ga_runtime, width, label='GraphAlgo')
<<<<<<< HEAD
    ga_java = ax.bar(x+width, ga_java_runtime, width, label='DW_GraphAlgo-java')
=======
    #ga_java = ax.bar(x + width, ga_java_runtime, width, label='DW_GraphAlgo-java')
>>>>>>> 83d8f1cfa69d578cbb0d12a8766e60f57dba8a1d

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
    #autolabel(ga_java)
    fig.tight_layout()

    plt.show()
