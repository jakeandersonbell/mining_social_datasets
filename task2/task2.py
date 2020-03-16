import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import webbrowser
import folium
import branca.colormap as cm
from sklearn.datasets import fetch_california_housing
from sklearn import preprocessing

pd.set_option('display.max_columns', 500)

cal_housing = fetch_california_housing()

housing_data = cal_housing.data


"""Preprocessing features"""

qt = preprocessing.QuantileTransformer(output_distribution='normal', random_state=0)

for i in range(housing_data.shape[1]):
    if cal_housing.feature_names[i] != 'Latitude' and cal_housing.feature_names[i] != 'Longitude':
        housing_data[:, i] = preprocessing.scale(housing_data[:, i])
        print("Scaled " + cal_housing.feature_names[i] + "\nMean: " + str(np.mean(housing_data[:, i])) +
              "\nstd: " + str(np.std(housing_data[:, i])))
        housing_data[:, i] = qt.fit_transform(housing_data[:, i].reshape(-1, 1)).flatten()
        print("Normalized " + cal_housing.feature_names[i])
        plt.hist(housing_data[:, i])
        plt.title(label=cal_housing.feature_names[i])
        plt.show()
    else:
        pass
        print("Skipped " + cal_housing.feature_names[i])


X = pd.DataFrame(cal_housing.data, columns=cal_housing.feature_names)

for i in X.iloc[1]:
    print(type(i))

"""Visualisation"""

# This has been done in Jupyter so the code will be moved when
# the figs are needed


def visualise_data(file_path, X):
    m = folium.Map(location=[np.mean(X['Latitude']), np.mean(X['Longitude'])])

    for i, v in enumerate(X[1:].iterrows()):
        print(v[1])
        print(v[1]['Latitude'], v[1]['Longitude'])
        folium.Marker(
            location=[v[1]['Latitude'], v[1]['Longitude']],
            icon=folium.Icon()
        ).add_to(m)

    m.save(file_path)
    webbrowser.open(file_path)


# visualise_data('map_1.html', X[:10])

def corr_plot():
    f = plt.figure(figsize=(10, 10))
    plt.matshow(X.corr(), fignum=f.number)
    plt.xticks(range(X.shape[1]), X.columns, fontsize=14, rotation=45)
    plt.yticks(range(X.shape[1]), X.columns, fontsize=14)
    cb = plt.colorbar()
    cb.ax.tick_params(labelsize=14)
    plt.show()


# Normalising distribution


# Target value is median house price for california districts
y = cal_housing.target
