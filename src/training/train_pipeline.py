import pandas as pd
import matplotlib.pyplot as plt

from sklearn.metrics import accuracy_score, f1_score, confusion_matrix
from sklearn.model_selection import train_test_split

from src.constants import AGGREGATOR_MODEL_PATH, DATASET_PATH, CM_PLOT_PATH,PREPARED_DATASET_PATH,MODELS
from src.models.aggregator_model import AggregatorModel
from src.models.decision_tree_model import DecisionTreeModel
from src.models.svc_model import SVCModel
from src.utils import PlotUtils


class TrainingPipeline:
    def __init__(self, dataset_name: str = 'prepared_dataset.csv'):
        if dataset_name == '':
            df = pd.read_csv(DATASET_PATH)
        else:
            dataset_path = str(PREPARED_DATASET_PATH).replace('prepared_dataset.csv', dataset_name)
            df = pd.read_csv(dataset_path)
        df.drop('Time', axis=1, inplace=True)
        features = df.drop('Class', axis=1).values
        y = df['Class'].values

        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(
            features,
            y,
            test_size=0.2,
            random_state=0
        )

        self.model = None

    def train(self, serialize: bool = True, result_model_name: str = "model.joblib", models: list = []):
        self.model = AggregatorModel(models=[MODELS[key] for key in models])

        self.model.fit(
            self.x_train,
            self.y_train
        )

        if result_model_name == '':
            model_path = str(AGGREGATOR_MODEL_PATH)
        else:
            model_path = str(AGGREGATOR_MODEL_PATH).replace('aggregator_model.joblib', result_model_name+'.joblib')
        if serialize:
            AggregatorModel.save(
                self.model,
                model_path
            )

    def get_model_perfomance(self) -> tuple:
        predictions = self.model.predict(self.x_test)
        return accuracy_score(self.y_test, predictions), f1_score(self.y_test, predictions)

    def render_confusion_matrix(self, plot_name: str = 'cm_plot', model_name: str = 'Current Model'):

        predictions = self.model.predict(self.x_test)
        cm = confusion_matrix(self.y_test, predictions, labels=[0, 1])
        plt.rcParams['figure.figsize'] = (6, 6)

        if model_name == '':
            model_name = 'Current Model'
        PlotUtils.plot_confusion_matrix(
            cm,
            classes=['Clear(0)', 'Fraudulent(1)'],
            normalize=False,
            title=model_name
        )

        if plot_name == '':
            plot_name = 'cm_plot'
        plot_path = str(CM_PLOT_PATH).replace('cm_plot.png', plot_name + '.png')
        plt.savefig(plot_path)
        plt.show()


if __name__ == "__main__":
    tp = TrainingPipeline()
    tp.train(serialize=True)
    accuracy, f1 = tp.get_model_perfomance()
    tp.render_confusion_matrix()
    print("ACCURACY = {}, F1 = {}".format(accuracy, f1))
