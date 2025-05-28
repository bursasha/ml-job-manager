from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv1D
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import MaxPooling1D
from tensorflow.keras.utils import to_categorical
from imblearn.over_sampling import SMOTE
from numpy.typing import NDArray

from src.active_ml.config import ActiveLearningConfig

def get_model(points: int, num_classes: int) -> Sequential:
    """
    Creates convolutional neural network model for spectrum classification 
    
    Parameters:
        points: number of uniform points, determines input layer size.
        num_classes: number of spectrum classification classes, determines output layer size.

    Returns:
        Sequential: The model for spectrum classification.
    """
    model = Sequential([
        Conv1D(64, 3, activation='relu', input_shape=(points, 1)),
        Conv1D(64, 3, activation='relu'),
        MaxPooling1D(2),
        Conv1D(128, 3, activation='relu'),
        Conv1D(128, 3, activation='relu'),
        MaxPooling1D(2),
        Conv1D(256, 3, activation='relu'),
        Conv1D(256, 3, activation='relu'),
        MaxPooling1D(2),
        Flatten(),
        Dense(512, activation='relu'),
        Dropout(0.5),
        Dense(512, activation='relu'),
        Dropout(0.5),
        Dense(num_classes, activation='softmax')
        ])
    model.compile(loss='categorical_crossentropy', optimizer='adam')
    return model


def train(model: Sequential, fluxes: NDArray[float], 
          labels: NDArray[int], points: int, num_classes: int, 
          config: ActiveLearningConfig) -> None:
    """
    Trains the given model
    
    1. Converts labels to one-hot encoding.
    2. Configurates early stopping.
    3. Runs model training.

    Parameters:
        model (Sequential): model to train.
        fluxes (NDArray[float]): 1D array of fluxes to train on.
        labels (NDArray[int]): 1D array of labels to train on.
        points (int): number of uniform points.
        num_classes (int): number of spectrum classification classes.
        config (ActiveLearningConfig): configuration for model training, loaded from configuration file.
    """

    one_hot_y = to_categorical(labels, num_classes=num_classes)
    callback = EarlyStopping(
            monitor='loss', min_delta=config.min_delta_train, patience=config.patience_train,
            restore_best_weights=True
            )
    model.fit(
            fluxes.reshape(-1, points, 1), one_hot_y, batch_size=config.batch_size_train, epochs=config.epochs_train,
            callbacks=[callback], verbose=0
            )


def predict(model: Sequential, fluxes: NDArray[float], 
            points: int, config: ActiveLearningConfig) -> NDArray[NDArray[float]]:
    """
    Runs model prediction

    Parameters:
        model (Sequential): model for prediction.
        fluxes (NDArray[float]): 1D array of fluxes to predict on.
        points (int): number of uniform points.
        config (ActiveLearningConfig): configuration for model prediction, loaded from configuration file.
    
    Returns (NDArray[NDArray[float]]): 
        2D array of predicted probabilities
    """
    fluxes = fluxes[...].reshape(-1, points, 1)
    return model.predict(fluxes, verbose=0, batch_size=config.batch_size_predict)

def balance(fluxes: NDArray[float], 
            labels: NDArray[int]
            ) -> tuple[NDArray[float], NDArray[int]]:
    """
    Balances dataset using SMOTE

    Parameters:
        fluxes (NDArray[float]): 1D array of fluxes, which need to be balanced.
        labels (NDArray[int]): 1D array of labels in integer, which need to be balanced.

    Returns (tuple[NDArray[float], NDArray[int]]):
        1D array of balanced fluxes.
        1D array of balaned labels.
    """
    return SMOTE().fit_resample(fluxes, labels)
