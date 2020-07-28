# -*- coding: utf8 -*-

import requests, json
import time
import networkx as nx
import matplotlib.pyplot as plt
import hashlib


def get_hash_key(text):
    return hashlib.md5(text.encode("utf8")).hexdigest()

def generate_graph(tokens, beginOffset=0):
    G = nx.DiGraph()
    # tokens = s['tokens']
    for i, token in enumerate(tokens):
        node_id = "tok_{}".format(i)
        headTokenIndex = token['dependencyEdge']['headTokenIndex'] - beginOffset

        G.add_node(node_id, label=token['lemma'])

        if headTokenIndex >= 0:
            src_id = "tok_{}".format(headTokenIndex)
            G.add_edge(
                src_id,
                node_id,
                label=token['dependencyEdge']['label'],
                key="parse_{}_{}".format(node_id, src_id))
    return G


def draw_label_graph(G, font_name='NanumGothic'):
    plt.figure(figsize=(20, 10))
    pos = nx.fruchterman_reingold_layout(G)
    labels = {}
    for node in G.nodes(data=True):
        if 'label' in node[1]:
            labels[node[0]] = node[1]['label']
        else:
            labels[node[0]] = ""

    nx.draw_networkx_nodes(G, pos, node_color='r', node_size=500, alpha=0.8)
    nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5)
    nx.draw_networkx_labels(G, pos, labels, font_size=16, font_family=font_name);
    plt.axis('off')
    plt.show()


def get_result(s):
    # 문장 토큰 정보 분리기

    idx_sents = 0
    pre_idx = 0
    len_tokens = len(s['tokens'])
    result = []

    list_beginOffset = [i['text']['beginOffset'] for i in s['sentences']]
    list_beginOffset.append(s['tokens'][-1]['text']['beginOffset'])

    # Start
    for idx, token in enumerate(s['tokens']):
        beginOffset = token['text']['beginOffset']
        if beginOffset in list_beginOffset[1:]:
            if idx == len_tokens - 1:
                # 마지막꺼
                selected_tokens = s['tokens'][pre_idx:]
            else:
                selected_tokens = s['tokens'][pre_idx:idx]
    #         print(pre_idx, beginOffset)
            # Align of results
            G = generate_graph(selected_tokens, pre_idx)
            sent = s['sentences'][idx_sents]
            result.append([G, sent])

            pre_idx = idx
            idx_sents += 1
    #         print(G.nodes(data=True))
    #         print("")
    #         print(selected_tokens)
    #         print("=====")
    #     print(num, token['text']['content'])

    return result