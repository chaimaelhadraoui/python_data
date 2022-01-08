from src.constants import DATASET_PATH, CM_PLOT_PATH
import pandas as pd
import io
import matplotlib.pyplot as plt

from src.utils import PlotUtils


class EDA:
    def __init__(self):
        self._df = pd.read_csv(DATASET_PATH)

    def dataset(self):
        return self._df[::]

    def info(self):
        buffer = io.StringIO()
        self._df.info(buf=buffer, null_counts=True)
        return buffer.getvalue()

    def overview(self):
        return self._df

    def description(self):
        return self._df.describe()

    def head(self):
        return self._df.head()

    def tail(self):
        return self._df.tail()

    def column_description(self, column_name: str = ""):
        return self._df[column_name].describe()

    def column_unique_values(self, column_name: str = ""):
        return self._df[column_name].unique()

    def column_count_unique_values(self, target_column_name: str = "y"):
        return self._df[target_column_name].value_counts()

    def null_sum(self):
        return self._df.isnull().values.sum()

    def render_histogram(self):
        PlotUtils.plot_histograms(self._df)
        plot_path = str(CM_PLOT_PATH).replace('cm_plot.png',  'histograms.png')
        plt.savefig(plot_path)
        plt.show()

    def render_correlation_matrix(self):
        return PlotUtils.plot_correlation_matrix(self._df)
