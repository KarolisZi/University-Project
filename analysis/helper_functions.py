import matplotlib.pyplot as plt

"""
================================================================================================

HELPER FUNCTIONS FOR SETTING UP MATPLOTLIB GRAPHS

================================================================================================
"""


def grid_and_spines(ax):
    # Removing frames
    for s in ['top', 'bottom', 'left', 'right']:
        ax.spines[s].set_visible(False)

    ax.grid(b=True, color='grey', linestyle='-.', linewidth=0.5, alpha=0.2)


def labels(x_label, x_size, y_label, y_size, title, title_size):
    plt.xlabel(x_label, fontsize=x_size)
    plt.ylabel(y_label, fontsize=y_size)
    plt.title(title, fontsize=title_size)


def ticks(ax, x_padding, y_paddnig, dictionary, invert):
    # Removing ticks "-"
    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('none')
    # Add padding
    ax.xaxis.set_tick_params(pad=x_padding)
    ax.yaxis.set_tick_params(pad=y_paddnig)
    if dictionary:
        plt.yticks(list(dictionary.keys()))

    if invert:
        ax.invert_yaxis()
