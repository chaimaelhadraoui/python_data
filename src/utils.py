import numpy as np
import itertools
import matplotlib.pyplot as plt
import seaborn as sns


class PlotUtils:
    @staticmethod
    def plot_histograms(dataframe):
        dataframe.hist()


    @staticmethod
    def plot_correlation_matrix(dataframe):
        corr_matrix = dataframe.corr()
        fig, ax = plt.subplots(figsize=(15, 10))
        ax = sns.heatmap(corr_matrix,
                         annot=True,
                         linewidth=0.5,
                         fmt=".2f",
                         cmap="YlGnBu");
        bottom, top = ax.get_ylim()
        ax.set_ylim(bottom + 0.5, top - 0.5)
        return fig

    @staticmethod
    def plot_confusion_matrix(cm, classes, title, normalize=False, cmap=plt.cm.Blues):
        title = 'Confusion Matrix of {}'.format(title)

        if normalize:
            cm = cm.astype(float) / cm.sum(axis=1)[:, np.newaxis]

        plt.imshow(cm, interpolation='nearest', cmap=cmap)
        plt.title(title)
        plt.colorbar()
        tick_marks = np.arange(len(classes))
        plt.xticks(tick_marks, classes, rotation=45)
        plt.yticks(tick_marks, classes)

        fmt = '.2f' if normalize else 'd'
        thresh = cm.max() / 2.
        for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
            plt.text(
                j,
                i,
                format(cm[i, j], fmt),
                horizontalalignment='center',
                color='white' if cm[i, j] > thresh else 'black'
            )

        plt.tight_layout()
        plt.ylabel('True label')
        plt.xlabel('Predicted label')
