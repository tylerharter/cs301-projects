import io, sys
import pydotplus
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import export_graphviz

# draw decision tree and save it to filename
def dump_decision_tree(clf, feature_cols, filename):
    dot_data = io.StringIO()
    export_graphviz(clf, out_file=dot_data,
                    filled=True, rounded=True,
                    special_characters=True,
                    feature_names = feature_cols,
                    impurity=False,
                    class_names=['0','1'])
    graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
    graph.write_png(filename)
    

# create decision tree classifier
def decision_tree_classifier(df, feature_cols, max_depth):
    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]
    clf = DecisionTreeClassifier(criterion="entropy", max_depth=max_depth, random_state=1)
    return clf.fit(X, y)


def main():
    if len(sys.argv) != 4:
        print("Usage: python gen_tree.py <data.csv> <tree-depth> <result.png>")
        return
    in_csv, depth, out_png = sys.argv[1:]
    df = pd.read_csv(in_csv)
    clf = decision_tree_classifier(df, df.columns, max_depth=int(depth))
    dump_decision_tree(clf, df.columns[:-1], out_png)
    print("open %s to see the resulting tree" % out_png)


if __name__ == "__main__":
    main()
