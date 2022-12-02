""" Generate audit specific charts.
"""
#%%
import logging
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt


logger = logging.getLogger(__name__)


def chart_bar(df, title, x_axis, y_axis, output_path=None):
    """
    Creates a bar chart from a dataframe.
    """
    # We validate and standardise the input
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df must be a pandas DataFrame")
    if not isinstance(title, str):
        raise TypeError("title must be a string")
    if not isinstance(x_axis, str):
        raise TypeError("x_axis must be a string")
    if not isinstance(y_axis, str):
        raise TypeError("y_axis must be a string")

    # We create the chart
    fig, ax = plt.subplots()
    ax.bar(df[x_axis], df[y_axis])
    ax.set_title(title)
    ax.set_xlabel(x_axis)
    ax.set_ylabel(y_axis)
    if output_path:
        fig.savefig(output_path)

    plt.show()
    # plt.close(fig)


#%%
if __name__ == "__main__":
    df = pd.DataFrame(np.random.randn(1000, 4), columns=list("ABCD"))

    chart_bar(df, "Test", "A", "B", "test.png")

# %%
