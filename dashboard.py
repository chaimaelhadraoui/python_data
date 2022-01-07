import time
import streamlit as st
import requests
from PIL import Image

from src.api.model import result_model
from src.constants import INFERENCE_EXAMPLE, CM_PLOT_PATH, MODELS
from src.preparation import PreparationPipeline
from src.training.train_pipeline import TrainingPipeline
from src.eda.eda import EDA
from src.api.sqlalchemy_local import get_objects

st.title("Card Fraud Detection Dashboard")
st.sidebar.title("By Chaimae Elhadraoui")

sidebar_options = st.sidebar.selectbox(
    "Options",
    ("EDA", "Preparation", "Training", "Inference")
)
# Exploratory Data Analysis

if sidebar_options == "EDA":
    st.header("Exploratory Data Analysis")
    st.info("In this section, we will explore our data set by given some charts.")
    try:
        eda = EDA()

        st.subheader("Dataset overview")
        st.text(eda.overview())

        st.subheader("Dataset information")
        st.text(eda.info())

        st.subheader("Dataset statistical description")
        st.dataframe(eda.description())

        st.subheader("Sum of null values (NaN)")
        st.text(eda.null_sum())

        st.subheader("Head of Dataset head")
        st.dataframe(eda.head())

        st.subheader("Dataset tail")
        st.dataframe(eda.tail())

        st.subheader("Amount column description")
        st.table(eda.column_description('Amount'))

        st.subheader("Target column values")
        st.text(eda.column_unique_values(column_name='Class'))

        st.subheader("Count target column values")
        data = eda.column_count_unique_values(target_column_name='Class')
        st.table(data)
        st.bar_chart(data=data, use_container_width=True)

        st.subheader("Correlation matrix")
        st.pyplot(eda.render_correlation_matrix())

        st.subheader("Histograms")
        eda.render_histogram()
        plot_path = str(CM_PLOT_PATH).replace('cm_plot.png', 'histograms.png')
        st.image(Image.open(plot_path))

    except Exception as e:
        st.error('Failed to explore the dataset!')
        st.exception(e)


elif sidebar_options == "Preparation":
    st.header("Data Preparation")
    st.info("In this section, we will prepare the dataset to be normalized and standardized.")
    dataset_name = st.text_input('Output Prepared Dataset name', placeholder='if empty default name is '
                                                                             'prepared_data.csv')

    serialize = st.checkbox('Save dataset')
    prepare = st.button('Prepare Model')

    if prepare:
        with st.spinner('Prepare dataset, please wait...'):
            try:
                pp = PreparationPipeline()
                st.progress(value=50)
                pp.prepare(serialize=serialize, prepared_dataset_name=dataset_name)
                st.progress(value=100)
                st.success('Done, please go for training now!')
                if dataset_name == '':
                    dataset_name = 'prepared_data.csv'
                st.subheader(dataset_name + " head")
                st.dataframe(pp.result_dataset_head())
                st.warning("Do not forget to copy the Dataset name!")

            except Exception as e:
                st.error('Failed to prepare dataset!')
                st.exception(e)

elif sidebar_options == "Training":
    st.header("Model Training")
    st.info("Before you proceed to training your model. Make sure you "
            "have checked your training pipeline code and that it is set properly.")

    name = st.text_input('Result Model name', placeholder='decisiontree')
    models = st.multiselect(
        'Chose models you want to aggregate:', list(MODELS.keys()))

    dataset_name = st.text_input('Dataset name', placeholder='Please do not put anything here if you want to use '
                                                             'original dataset.')

    serialize = st.checkbox('Save model')
    train = st.button('Train Model')

    if train:
        with st.spinner('Training model, please wait...'):
            time.sleep(1)
            try:
                tp = TrainingPipeline(dataset_name=dataset_name)
                tp.train(serialize=serialize, result_model_name=name, models=models)
                tp.render_confusion_matrix(plot_name=name, model_name=name)
                accuracy, f1 = tp.get_model_perfomance()
                col1, col2 = st.columns(2)
                col1.metric(label="Accuracy score", value=str(round(accuracy, 4)))
                col2.metric(label="F1 score", value=str(round(f1, 4)))

                if name == '':
                    name = 'cm_plot'
                plot_path = str(CM_PLOT_PATH).replace('cm_plot.png', name + '.png')
                st.image(Image.open(plot_path))

            except Exception as e:
                st.error('Failed to train model!')
                st.exception(e)

# test the model

else:
    st.header("Fraud Inference")
    st.info("This section simplifies the inference process. "
            "You can tweak the values of feature 6, 11, 13, "
            "and the transaction amount and observe how your model reacts to these changes.")

    feature_6 = st.slider('Transaction Feature 6', -26.1605, 73.3016, step=0.001, value=2.630)
    feature_11 = st.slider('Transaction Feature 11', -4.7975, 12.0189, step=0.001, value=-4.075)
    feature_13 = st.slider('Transaction Feature 13', -5.7919, 7.1269, step=0.001, value=0.963)

    amount = st.number_input('Transaction Amount', value=1000, min_value=0, max_value=int(1e10), step=100)
    infer = st.button('Run Fraud Inference')

    INFERENCE_EXAMPLE[6] = feature_6
    INFERENCE_EXAMPLE[11] = feature_11
    INFERENCE_EXAMPLE[13] = feature_13
    INFERENCE_EXAMPLE[28] = amount

    if infer:
        with st.spinner('Running inference...'):
            time.sleep(1)
            try:
                result = requests.post(
                    'http://localhost:5000/api/inference',
                    json=INFERENCE_EXAMPLE
                )
                if int(int(result.text) == 1):
                    result_prediction = "Transaction: Fraudulent"
                    st.success('Done!')
                    st.metric(label="Status", value="Transaction: Fraudulent")
                else:
                    result_prediction = "Transaction: Clear"
                    st.success('Done!')
                    st.metric(label="Status", value="Transaction: Clear")

            except Exception as e:
                st.error('Failed to call Inference API!')
                st.exception(e)
        with st.spinner('Save result...'):
            time.sleep(1)
            try:
                result = requests.post(
                    'http://localhost:5000/api/save',
                    json={'result': result_prediction}
                )
                st.text(result.text)

                # read from sqlite alchemy
                results = []
                fetched_results = get_objects(result_model.Result)
                if fetched_results:
                    for a_result in fetched_results:
                        result_format = {'id_result': a_result.id_result,
                                         'result': a_result.result}

                        results.append(result_format)
                st.table(results)
            except Exception as e:
                st.error('Failed to call Save API!')
                st.exception(e)
