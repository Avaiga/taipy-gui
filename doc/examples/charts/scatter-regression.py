# Copyright 2023 Avaiga Private Limited
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
# an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.
# -----------------------------------------------------------------------------------------
# To execute this script, make sure that the taipy-gui package is installed in your
# Python environment and run:
#     python <script>
# You may need to install the sklearn.datasets and sklearn.linear_model packages as well.
# -----------------------------------------------------------------------------------------
from taipy import Gui
from os.path import exists
from sklearn.datasets import make_regression
from sklearn.linear_model import LinearRegression

n_samples = 300
X, y, coef = make_regression(n_samples=n_samples, n_features=1, n_informative=1, n_targets=1, noise=25, coef=True)

model = LinearRegression().fit(X, y)

x_data = X.flatten()
y_data = y.flatten()
predict = model.predict(X)

data = {
  "x": x_data,
  "y": y_data,
  "Regression": predict
}

page = """
# Scatter - Regression
<|toggle|theme|>

<|{data}|chart|x=x|y[1]=y|mode[1]=markers|y[2]=Regression|mode[2]=line|width=60%|>
"""

Gui(page).run(run_browser=False)
