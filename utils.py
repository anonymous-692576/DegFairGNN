import torch
import numpy as np
from sklearn.metrics import f1_score, accuracy_score
import scipy.sparse as sp
import scipy.stats as st
import math


def accuracy(output, labels):
    preds = output.max(1)[1].type_as(labels)
    correct = preds.eq(labels).double()
    correct = correct.sum()
    return correct / len(labels)


def confidence_interval(arr=None):
    mean = np.mean(arr)
    ci = 1.96 * st.sem(arr) / math.sqrt(len(arr))
    
    print("Mean: {:.4f}, CI: {:.4f}".format(mean, ci))
    return


def get_str_info(adj, n_layers=2):
    
    str_info = adj
    for i in range(n_layers):
        str_info = torch.matmul(str_info, adj)

    torch.set_printoptions(profile='full')
    print('struc: ', str_info)
    return torch.sum(str_info, dim=1)


def evaluate_fairness(pred, data, groups, embed=None, name=None):

    def fair_metric(p):
        groups = np.copy(data_groups)
        groups = -1

        # mask 2 groups
        groups = np.where(data_groups <= p[0], 0., groups)
        groups = np.where(data_groups > p[1] , 1., groups)

        idx_s0 = np.where(groups == 0)[0]
        idx_s1 = np.where(groups == 1)[0]

        SP = []
        EO = []

        for i in range(data.labels.max()+1):
            # SP
            p_i0 = np.where(pred[idx_s0] == i)[0]
            p_i1 = np.where(pred[idx_s1] == i)[0]
           
            sp = abs((p_i0.shape[0]/idx_s0.shape[0]) - (p_i1.shape[0]/idx_s1.shape[0]))
            SP.append(sp)

            # EO
            p_y0 = np.where(labels[idx_s0] == i)[0]
            p_y1 = np.where(labels[idx_s1] == i)[0]
           
            p_iy0 = np.where(pred[p_y0] == i)[0]
            p_iy1 = np.where(pred[p_y1] == i)[0]

            if p_y0.shape[0] == 0 or p_y1.shape[0] == 0:
                eo = 0
            else:
                eo = abs((p_iy0.shape[0]/p_y0.shape[0]) - (p_iy1.shape[0]/p_y1.shape[0]))
            EO.append(eo)

        #group accuracy
        head_acc = accuracy_score(labels[idx_s0], pred[idx_s0])
        tail_acc = accuracy_score(labels[idx_s1], pred[idx_s1])

        return np.asarray(SP)*100, np.asarray(EO)*100, head_acc*100, tail_acc*100

    data_groups = groups[data.idx_test]
    pred = pred.cpu()
    labels = data.labels[data.idx_test].cpu()
    np.set_printoptions(precision=3, suppress=True)

    # Equal group: 20, 30
    portion = [20] #30 
    output = []

    for por in portion:
        p = np.percentile(data_groups, [por, 100-por])
        sp, eo, head, tail = fair_metric(p)

        print('{:d} split: Mean SP={:.2f}, Mean EO={:.2f}' \
            .format(por, np.mean(sp), np.mean(eo)))
        print('Head Acc: {:.4f}, Tail Acc: {:.4f}'.format(head, tail))
        
        output = [np.mean(sp), np.mean(eo), head, tail]

    return output

