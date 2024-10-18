# Image Classification

This project addresses basic image classification, a fundamental task in computer vision that supports higher-level tasks like object detection, segmentation, and tracking. Using a dataset of 50,000 facial images (178x218x3 in JPG format) with annotations in anno.csv for 40 head-related features, the objective is to solve two classification problems:

1. **Binary Classification**: Classify images based on whether the person is smiling.
2. **Five-class Classification**: Classify images based on the person’s hair color (Black, Blond, Brown, Gray, Others).

For both tasks, the project involves model design, implementation, evaluation, and analysis.



## **Files Included**

- `project2.ipynb`: Contains the source code with detailed annotations.

- `report.pdf`: The project summary report.

- `result.txt`: Records the model training results.


## **How to Run the Source Code**

1. Modify lines 62-67 in the “Dataset Preprocessing” section:

   - To train a binary classification model, comment out lines 66 and 67.

   - To train a five-class classification model, comment out lines 63 and 64.

2. Additionally, manually modify line 5 in the “Model Training and Testing” section:

   - For a binary classification model, set the value to 2.

   - For a five-class classification model, set the value to 5.

3. Click “Run All” to start training.

## **Notes**

1. The code is currently set to train a binary classification model, with results saved for 5 epochs.

2. Ensure that both project2.ipynb and the data_face_imgs folder are located in the same directory for the code to run properly.