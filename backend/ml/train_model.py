import os
import joblib
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)

from config import Config


# =====================================================
# Model Trainer
# =====================================================

class LandslideModelTrainer:

    def __init__(self):

        self.dataset_path = os.path.join(

            Config.DATASET_FOLDER,

            "landslide_dataset.csv"

        )

        self.model_path = os.path.join(

            Config.MODEL_FOLDER,

            "model.pkl"

        )

        self.encoder_path = os.path.join(

            Config.MODEL_FOLDER,

            "label_encoder.pkl"

        )

        self.data = None

        self.features = None

        self.target = None

        self.label_encoder = LabelEncoder()


    # =================================================
    # Load Dataset
    # =================================================

    def load_dataset(self):

        if not os.path.exists(

            self.dataset_path

        ):

            raise FileNotFoundError(

                f"Dataset not found:\n{self.dataset_path}"

            )

        self.data = pd.read_csv(

            self.dataset_path

        )

        print(

            f"Dataset Loaded Successfully "

            f"({len(self.data)} records)"

        )

        return self.data


    # =================================================
    # Dataset Information
    # =================================================

    def dataset_information(self):

        return {

            "rows": len(self.data),

            "columns": len(self.data.columns),

            "column_names": list(

                self.data.columns

            )

        }


    # =================================================
    # Remove Missing Values
    # =================================================

    def clean_dataset(self):

        before = len(self.data)

        self.data = self.data.dropna()

        after = len(self.data)

        print(

            f"Removed {before-after} incomplete rows."

        )


    # =================================================
    # Encode Target Column
    #
    # Low -> 0
    # Medium -> 1
    # High -> 2
    # =================================================

    def encode_target(self):

        self.data["risk"] = self.label_encoder.fit_transform(

            self.data["risk"]

        )

        joblib.dump(

            self.label_encoder,

            self.encoder_path

        )

        print(

            "Label Encoder Saved."

        )


    # =================================================
    # Select Features
    #
    # Keep this order SAME as
    # prediction.py
    # =================================================

    def prepare_features(self):

        feature_columns = [

            "rainfall",

            "humidity",

            "temperature",

            "wind_speed",

            "pressure",

            "visibility"

        ]

        self.features = self.data[

            feature_columns

        ]

        self.target = self.data[

            "risk"

        ]

        print(

            "Training Features Prepared."

        )


    # =================================================
    # Train/Test Split
    # =================================================

    def split_dataset(self):

        return train_test_split(

            self.features,

            self.target,

            test_size=0.2,

            random_state=42,

            stratify=self.target

        )
# =====================================================
# Train Random Forest Model
# =====================================================

    def train_model(self):

        (
            X_train,
            X_test,
            y_train,
            y_test

        ) = self.split_dataset()

        self.model = RandomForestClassifier(

            n_estimators=200,

            max_depth=10,

            random_state=42,

            min_samples_split=5,

            min_samples_leaf=2,

            class_weight="balanced"

        )

        self.model.fit(

            X_train,

            y_train

        )

        print(

            "Random Forest Model Trained Successfully."

        )

        self.X_test = X_test

        self.y_test = y_test

        return self.model


# =====================================================
# Predict Test Dataset
# =====================================================

    def predict_test_data(self):

        predictions = self.model.predict(

            self.X_test

        )

        return predictions


# =====================================================
# Calculate Accuracy
# =====================================================

    def calculate_accuracy(self):

        predictions = self.predict_test_data()

        accuracy = accuracy_score(

            self.y_test,

            predictions

        )

        return round(

            accuracy * 100,

            2

        )


# =====================================================
# Evaluate Model
# =====================================================

    def evaluate_model(self):

        predictions = self.predict_test_data()

        results = {

            "accuracy":

                round(

                    accuracy_score(

                        self.y_test,

                        predictions

                    ) * 100,

                    2

                ),

            "precision":

                round(

                    precision_score(

                        self.y_test,

                        predictions,

                        average="weighted"

                    ) * 100,

                    2

                ),

            "recall":

                round(

                    recall_score(

                        self.y_test,

                        predictions,

                        average="weighted"

                    ) * 100,

                    2

                ),

            "f1_score":

                round(

                    f1_score(

                        self.y_test,

                        predictions,

                        average="weighted"

                    ) * 100,

                    2

                )

        }

        print("\nModel Evaluation")

        print("-" * 40)

        for key, value in results.items():

            print(

                f"{key}: {value}%"

            )

        return results


# =====================================================
# Classification Report
# =====================================================

    def classification_report(self):

        predictions = self.predict_test_data()

        report = classification_report(

            self.y_test,

            predictions,

            target_names=self.label_encoder.classes_

        )

        return report


# =====================================================
# Confusion Matrix
# =====================================================

    def confusion_matrix(self):

        predictions = self.predict_test_data()

        matrix = confusion_matrix(

            self.y_test,

            predictions

        )

        return matrix
# =====================================================
# Save Trained Model
# =====================================================

    def save_model(self):

        if self.model is None:

            raise Exception(

                "No trained model found."

            )

        joblib.dump(

            self.model,

            self.model_path

        )

        print(

            f"Model saved successfully:\n{self.model_path}"

        )


# =====================================================
# Feature Importance
# =====================================================

    def feature_importance(self):

        importance = self.model.feature_importances_

        columns = self.features.columns

        feature_scores = []

        for feature, score in zip(

            columns,

            importance

        ):

            feature_scores.append({

                "feature": feature,

                "importance": round(

                    score,

                    4

                )

            })

        feature_scores.sort(

            key=lambda x: x["importance"],

            reverse=True

        )

        return feature_scores


# =====================================================
# Print Feature Importance
# =====================================================

    def print_feature_importance(self):

        print()

        print("=" * 50)

        print("Feature Importance")

        print("=" * 50)

        for item in self.feature_importance():

            print(

                f'{item["feature"]:<20}'

                f'{item["importance"]:.4f}'

            )


# =====================================================
# Training Summary
# =====================================================

    def training_summary(self):

        evaluation = self.evaluate_model()

        return {

            "dataset_rows":

                len(self.data),

            "features":

                list(

                    self.features.columns

                ),

            "accuracy":

                evaluation["accuracy"],

            "precision":

                evaluation["precision"],

            "recall":

                evaluation["recall"],

            "f1_score":

                evaluation["f1_score"]

        }


# =====================================================
# Complete Training Pipeline
# =====================================================

    def train(self):

        self.load_dataset()

        self.clean_dataset()

        self.encode_target()

        self.prepare_features()

        self.train_model()

        self.save_model()

        summary = self.training_summary()

        self.print_feature_importance()

        return summary
# =====================================================
# Health Check
# =====================================================

    def health_check(self):

        return {

            "dataset_exists":

                os.path.exists(

                    self.dataset_path

                ),

            "model_exists":

                os.path.exists(

                    self.model_path

                ),

            "label_encoder_exists":

                os.path.exists(

                    self.encoder_path

                )

        }


# =====================================================
# Reload Saved Model
# =====================================================

    def reload_model(self):

        if not os.path.exists(

            self.model_path

        ):

            return {

                "success": False,

                "message": "Trained model not found."

            }

        self.model = joblib.load(

            self.model_path

        )

        return {

            "success": True,

            "message": "Model loaded successfully."

        }


# =====================================================
# Test Saved Model
# =====================================================

    def test_saved_model(self):

        if self.model is None:

            self.reload_model()

        sample = np.array([

            30,      # rainfall (mm)

            85,      # humidity (%)

            20,      # temperature (°C)

            10,      # wind_speed (km/h)

            1008,    # pressure (hPa)

            5000     # visibility (m)

        ]).reshape(1, -1)

        prediction = self.model.predict(

            sample

        )[0]

        risk = self.label_encoder.inverse_transform(

            [prediction]

        )[0]

        return {

            "prediction": risk

        }


# =====================================================
# Create Model Directory
# =====================================================

    def create_directories(self):

        os.makedirs(

            Config.MODEL_FOLDER,

            exist_ok=True

        )
# =====================================================
# Singleton Instance
# =====================================================

trainer = LandslideModelTrainer()
# =====================================================
# Utility Functions
# =====================================================

def train_model():

    return trainer.train()


def model_health():

    return trainer.health_check()


def reload_model():

    return trainer.reload_model()


def training_summary():

    return trainer.training_summary()


def feature_importance():

    return trainer.feature_importance()


def test_model():

    return trainer.test_saved_model()
# =====================================================
# Run Training
# =====================================================

if __name__ == "__main__":

    print("=" * 60)
    print("PAHADSURAKSHA LANDSLIDE AI MODEL TRAINING")
    print("=" * 60)

    trainer.create_directories()

    summary = trainer.train()

    print()

    print("=" * 60)
    print("TRAINING SUMMARY")
    print("=" * 60)

    for key, value in summary.items():

        print(f"{key} : {value}")

    print()

    print("=" * 60)
    print("MODEL HEALTH")
    print("=" * 60)

    print(model_health())

    print()

    print("=" * 60)
    print("MODEL TEST")
    print("=" * 60)

    print(test_model())

    print()

    print("=" * 60)
    print("Training Completed Successfully")
    print("=" * 60)