import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import numpy as np
from sklearn.metrics import auc, precision_recall_curve, average_precision_score
from sklearn.metrics import roc_curve, f1_score, classification_report
from sklearn.metrics import precision_score, recall_score
from collections import defaultdict
import seaborn as sns
import csv, os
import pickle
from sklearn import cross_validation


def plotCurves(fpr, tpr, cl, fn=None):
    if len(fpr) != 0:
        roc_auc = auc(fpr, tpr)
        plt.plot(fpr, tpr, 'b', label='AUC = %0.2f' % roc_auc)
    if fn == None:
        fn = 'all features'
    plt.title('ROC: Predicting {0} boundaries using {1}'.format(cl, fn))
    plt.legend(loc='lower right')
    plt.plot([0, 1], [0, 1], 'r--')
    ax = plt.gca()
    ax.grid(True)
    plt.ylabel('True Positive Rate')
    plt.xlabel('False Positive Rate')
    plt.show()
    plt.close()


def OneVsAll():
    weights = defaultdict(list)
    cells = ['HeLa', 'HMEC', 'HUVEC', 'NHEK', 'K562']
    for cell in cells:
        toconcat = []

        ocl = [k for k in cells if k != cell]
        for t in ocl:
            path = 'data/PairwiseFeatures(global)/{}_testData'.format(t)
            df = pd.read_csv(path, header=0, index_col=0, sep='\t')
            toconcat.append(df)
        train = pd.concat(toconcat)
        test = pd.read_csv('data/PairwiseFeatures(global)/{}_testData'.format(cell), header=0,
                           index_col=0, sep='\t')

        clf = RandomForestClassifier(n_estimators=200, criterion='gini',
                                     n_jobs=-1, max_depth=5)

        Xtrain = train[train.columns.values[:-1]]
        ytrain = train['Class']
        Xtest = test[test.columns.values[:-1]]
        ytest = test['Class']
        header = Xtrain.columns
        plt.subplot(1,2,1)

        clf.fit(Xtrain, ytrain)

        for i, feature in enumerate(header):
            if feature == 'Correlation':
                weights[feature].append(clf.feature_importances_[i])
            else:
                weights[feature[:-2]].append(clf.feature_importances_[i])

        # print(clf.best_params_)
        scores = clf.predict_proba(Xtest)
        posScores = scores[:, 1].reshape(scores.shape[0])
        fpr, tpr, _ = roc_curve(ytest, posScores)


        ##############PLOT################

        roc_auc = round(auc(fpr, tpr), 3)
        print('AUROC for {}: {}'.format(cell, roc_auc))
        plt.plot(fpr, tpr, label='AUC for {} = {}'.format(roc_auc, cell))

    plt.subplot(1, 2, 1)
    plt.legend(loc='lower right')
    plt.plot([0, 1], [0, 1], 'r--')
    plt.ylabel('True Positive Rate')
    plt.xlabel('False Positive Rate')
    plt.subplot(1, 2, 2)
    weights = {key: sum(value)/len(value) for key, value in weights.items()}
    weights = pd.DataFrame(weights, index=[0])
    sns.barplot(data=weights)
    plt.ylabel('Peak strengths')
    plt.xticks(rotation='vertical')
    plt.suptitle('ROC plot and feature Importances',
                 fontsize=16, fontweight='bold')
    plt.show()
    plt.close()



def singleCellLine():
    for cl in ['HeLa', 'HMEC', 'HUVEC', 'NHEK', 'K562']:
        master = []
        with open('data/PairwiseFeatures(global)/{}_testData'.format(cl), 'r') as f:
            reader = csv.reader(f, delimiter='\t')
            for line in reader:
                    master.append(list(line))
        header = master.pop(0)
        master = pd.DataFrame(master, columns=header)
        y = master['Class']
        X = master.drop('Class', axis=1)
        cv = cross_validation.StratifiedKFold(y, n_folds=5, shuffle=True)
        y = y.values
        X_idx = X.featureID
        X = X.drop('featureID', axis=1).values
        auroc = 0
        plt.subplot(1, 2, 1)
        weights = defaultdict(list)

        for fold, (train_index, test_index) in enumerate(cv):
            outf = '{}_singlecellpreds.txt'.format(cl)
            y_train, y_test = y[train_index], y[test_index]
            x_train, x_test = X[train_index], X[test_index]

            clf = RandomForestClassifier(n_estimators=200, criterion='gini',
                                         n_jobs=-1, max_depth=5)
            clf.fit(x_train, y_train)
            predictions = clf.predict(x_test)
            scores = clf.predict_proba(x_test)
            posScores = scores[:, 1].reshape(-1, 1).tolist()

            with open(outf, 'w') as f:
                out = []
                for i, line in enumerate(predictions):
                    out.append([cl, X_idx.iloc[test_index[i]], predictions[i], y_test[i]])
                csv.writer(f, delimiter='\t').writerows(out)

            for i, feature in enumerate(header[1:-1]):
                if feature == 'Correlation':
                    weights[feature].append(clf.feature_importances_[i])
                    continue
                weights[feature[:-2]].append(clf.feature_importances_[i])


            fpr, tpr, _ = roc_curve(y_test, posScores, pos_label='1')
            auc_roc = round(auc(fpr, tpr), 3)
            plt.subplot(1, 2, 1)
            plt.plot([0, 1], [0, 1], 'r--')
            plt.xlabel('False Positive Rate')
            plt.ylabel('True Positive Rate')
            plt.plot(fpr, tpr, label='ROC on fold {}: {}'.format(fold, auc_roc))
            print('AUC on fold {} for {}:'.format(fold, cl), auc_roc)
            auroc += auc(fpr, tpr)

        print('Average AUC for {} = {}'.format(cl, auroc/5))
        plt.legend(loc='lower right')
        plt.subplot(1, 2, 2)
        for t in weights:
            weights[t] = sum(weights[t]) / len(weights[t])
        weights = pd.DataFrame(weights, index=[0])
        sns.barplot(data=weights)
        plt.xticks(rotation='vertical')
        plt.ylabel('Feature importance')
        plt.suptitle('ROC plot and feature Importances for {}'.format(cl),
                     fontsize=16, fontweight='bold')
        plt.show()



singleCellLine()
OneVsAll()


