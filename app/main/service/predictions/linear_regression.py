import numpy as np 
from sklearn.linear_model import LinearRegression

class Lr_Predict:
    def simple_prediction(self, x_value, y_value, x_max, start_number):
        x = np.array(x_value).reshape((-1,1))
        y = np.array(y_value)
        x_data = x if len(x) > 0  else np.array([0]).reshape((-1,1))
        y_data = x if len(x) > 0  else np.array([0]).reshape((-1,1))
        model = LinearRegression().fit(x_data,y_data)

        x_new = np.arange(x_max).reshape((-1, 1))
        y_new = model.predict(x_new).reshape((-1,1))
        no = start_number
        prediction = {100:'Prediction'}
        for pred in y_new:
            prediction[no] = pred[0]
            no += 1
        return prediction

    def simple_prediction_pivot(self, x_value, y_value, x_max):
        x = np.array(x_value).reshape((-1,1))
        y = np.array(y_value)

        model = LinearRegression().fit(x,y)

        x_new = np.arange(x_max).reshape((-1,1))
        y_pred = model.predict(x_new).reshape((-1,1))

        prediction = []
        for i in y_pred:
            prediction.append(i[0])

        return prediction