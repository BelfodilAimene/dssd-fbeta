#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from os.path import basename, splitext,abspath, dirname,isdir,join
from os import listdir
import math

# --------------------------------------------------------------------
TOP=1000
FONTSIZE=20
# --------------------------------------------------------------------
def evaluate(element) :
    try :
        return int(element)
    except Exception :
        return float("inf")
# --------------------------------------------------------------------
def boxplot(baseFolder, measureName):
    iterations = [ name for name in listdir(baseFolder) if isdir(join(baseFolder, name))]
    iterations = sorted(iterations, key = evaluate)
    toPlotFiles = [baseFolder+"/"+it+"/"+measureName+"/measures.csv" for it in iterations]
    listData = []
    times=[]
    for valuefile in toPlotFiles :
        with open(valuefile,"r") as f :
            times.append(float(f.readlines()[-1].strip().split(" ")[2]))
        data = pd.read_csv(valuefile,sep=',',header=0, index_col = None, comment="#")
        listData.append(np.array(data[list(data)[0]][:min(TOP,len(data[list(data)[0]]))]))
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_ylabel("quality",fontsize=FONTSIZE)
    ax.set_xlabel("iterations",fontsize=FONTSIZE)
    ax.tick_params(axis='y', labelsize=FONTSIZE)
    ax.tick_params(labelsize=FONTSIZE)
    timeAx = ax.twinx()
    timeAx.set_yscale("log")
    timeAx.set_ylabel("Execution time (ms)", fontsize=FONTSIZE)
    timeAx.errorbar(range(1,len(toPlotFiles)+1),times, fmt = 'o-',color = "red",linewidth=4,markersize=8, label="execution time (ms)")
    timeAx.tick_params(labelsize=FONTSIZE)
    plt.boxplot(listData)
    plt.xticks(range(1,len(toPlotFiles)+1), iterations, rotation=30)
    xlabels = ax.get_xticklabels()
    for label in xlabels:
        label.set_rotation(45) 
    legend = timeAx.legend(loc='upper left', shadow=False,fontsize=FONTSIZE)
    fig.tight_layout()
    plt.savefig(baseFolder+"/boxplot-"+measureName+".pdf",bbox_inches='tight')

boxplot(sys.argv[1],sys.argv[2])
