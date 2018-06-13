import pydotplus
from sklearn.externals.six import StringIO
from sklearn.feature_extraction import DictVectorizer
from sklearn.tree import DecisionTreeClassifier, export_graphviz

from tree import table, results

v = DictVectorizer(sparse=False)
v.fit_transform(table)
X = v.fit_transform(table)
Y = results
dt = DecisionTreeClassifier()
result = dt.fit(X, Y)
result_file = open('tree_file', 'w')
result_file.write(str(dt))

dot_data = StringIO()
export_graphviz(
    dt,
    out_file=dot_data,
    feature_names=v.get_feature_names(),
    filled=True,
    rounded=True,
    impurity=False,
)
graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
graph.write_pdf('decision_tree.pdf')
