import io, sys
import pydotplus
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import export_graphviz
from sklearn.tree._tree import TREE_LEAF

# Download and install graphviz from https://graphviz.gitlab.io/_pages/Download/Download_windows.html
# Uncomment the following and edit the path of the graphviz if its different for your machine
# import os
# os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'

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


# what classes might different descendents of a node predict?
def classes(t, index):
    if t.children_left[index] == TREE_LEAF and t.children_right[index] == TREE_LEAF:
        if t.value[index][0][1] > t.value[index][0][0]:
            return {1}
        else:
            return {0}
    return classes(t, t.children_left[index]) | classes(t, t.children_right[index])


# for our purposes, if all a node's descendents predict the same
# class, we want to collapse them
def prune_index(t, index):
    if t.children_left[index] != TREE_LEAF:
        prune_index(t, t.children_left[index])
        prune_index(t, t.children_right[index])
    if len(classes(t, index)) == 1:
        t.children_left[index] = TREE_LEAF
        t.children_right[index] = TREE_LEAF


def decision_tree_classifier(df, feature_cols, max_depth):
    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]
    clf = DecisionTreeClassifier(max_depth=max_depth, random_state=1)
    return clf.fit(X, y)


def main():
    if len(sys.argv) != 4:
        print("Usage: python gen_tree.py <data.csv> <tree-depth> <result.png>")
        return
    in_csv, depth, out_png = sys.argv[1:]
    df = pd.read_csv(in_csv)
    dt = decision_tree_classifier(df, df.columns, max_depth=int(depth))
    prune_index(dt.tree_, 0)
    dump_decision_tree(dt, df.columns[:-1], out_png)
    print("open %s to see the resulting tree" % out_png)


if __name__ == "__main__":
    main()
