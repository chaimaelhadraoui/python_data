import pandas as pd
import matplotlib.pyplot as plt
from src.constants import DATASET_PATH, PREPARED_DATASET_PATH
from sklearn.preprocessing import StandardScaler, MinMaxScaler


class PreparationPipeline:
    def __init__(self):
        df = pd.read_csv(DATASET_PATH)
        self._time_column = df['Time']
        df.drop('Time', axis=1, inplace=True)
        self._features = df.drop('Class', axis=1)
        self._y = df['Class']
        self._output_dataset = None

    def prepare(self, serialize: bool = True, prepared_dataset_name: str = 'prepared_dataset.csv'):
        # Standardization
        standardized_data = StandardScaler().fit_transform(self._features)

        # Normalization
        normalized_data = MinMaxScaler().fit_transform(standardized_data)

        self._features = pd.DataFrame(normalized_data, columns=self._features.columns)
        self._output_dataset = self._features.join(self._time_column).join(self._y)

        if serialize:
            if prepared_dataset_name == '':
                dataset_path = str(PREPARED_DATASET_PATH)
            else:
                dataset_path = str(PREPARED_DATASET_PATH).replace('prepared_dataset.csv', prepared_dataset_name)
            pd.DataFrame.to_csv(self._output_dataset, dataset_path)

    def result_dataset_head(self):
        return self._output_dataset.head()



if __name__ == '__main__':
    pp = PreparationPipeline()
    pp.prepare(serialize=False)
