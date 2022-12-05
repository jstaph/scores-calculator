from flask import Blueprint,render_template,request,flash,url_for,app
import pandas as pd
import numpy as np
import string
from os import path
views = Blueprint('views',__name__)

script_dir = path.dirname(path.abspath(__file__))

@views.route('/',methods=['POST','GET'])
def home():
    table = np.asarray([])
    h1,h2,h3,item,instrument,item="","","","","",""
    names_scores_zip = np.asarray([])
    scores = np.asarray([])
    if request.method == "POST":
        score = request.form.get('score')
        instrument = request.form.get('instrument_select')
        item = request.form.get('item_select')
        file="" 
        if item == "total":
            file = "crosswalk_total_df.csv"
        elif item == "trial 1":
            file = "crosswalk_t1_df.csv"
        elif item == "long delay":
            file = "crosswalk_ldfr_df.csv"
        elif item=="short delay":
            file = "crosswalk_sdfr_df.csv"
            if instrument=="hvlt":
                flash('Short delay is not recorded for HVLT',category='error')
                
        filefullpath = script_dir + f"//static//{file}"

        # Function to set table headings
        h1,h2,h3,maxim = headings_and_limits(item,instrument)
        # Return table
        table = filter_table(filefullpath,item,instrument)
        print(table)
        # Score constraints
        if score.isdigit() == False:
            flash('Please enter a valid integer score',category='error')
        elif int(score) < 0 or int(score) > maxim:
            flash(f'Input score must be in between 0 and {maxim}',category="error")
        # Output the scores.
        else:
            score = int(score)
            scores = np.array(table[table[:,0]==score]).T.flatten() if table.size > 0 else []
            if instrument=="cvlt":
                names = np.array(['CVLT','RAVLT','HVLT'])
                if item=="short delay":
                    scores = np.append(scores,[" "])
                names_scores_zip = np.array(list(zip(names,scores)))
            elif instrument=="ravlt":
                names = np.array(['RAVLT','HVLT','CVLT'])
                if item=="short delay":
                   scores = np.insert(scores,1," ")
                names_scores_zip = np.array(list(zip(names,scores)))
                # conv_scores =  np.roll(table[table[:,0]==score],1)
            elif instrument =="hvlt":
                names = np.array(['HVLT','CVLT','RAVLT'])
                names_scores_zip = np.array(list(zip(names,scores)))
                # conv_scores =  np.roll(table[table[:,0]==score],2)
    return render_template("home.html",table=table,item=string.capwords(item),instrument=instrument.upper(),h1=h1,h2=h2,h3=h3,scores=names_scores_zip)

def filter_table(filefullpath,item,instrument):
    if item!="short delay":
        cols_to_int = [0,4,8]
        section_array = [(0,3),(4,7),(8,11)]
    else:
        cols_to_int = [0,3]
        section_array = [(0,2),(3,5)]
    df = pd.read_csv(filefullpath)
    df.iloc[:,cols_to_int] = df.iloc[:,cols_to_int].astype('Int64')
    table = np.asarray([])
    if instrument == "cvlt":
        table = np.array(df.iloc[:,section_array[0][0]:section_array[0][1]].dropna())
    elif instrument=="ravlt":
        table = np.array(df.iloc[:,section_array[1][0]:section_array[1][1]].dropna())
    elif instrument=="hvlt" and item!="short delay":
        table = np.array(df.iloc[:,section_array[2][0]:section_array[2][1]].dropna())
    return table

def headings_and_limits(item,instrument):
    h1,h2,h3="","",""
    maxim = 0
    if item=="total":
        if instrument=="cvlt":
            h1 = "Measured score CVLT total T1-T5"
            h2 = "Estimated RAVLT total"
            h3 = "Estimated HVLT total"
            maxim = 80
        elif instrument=="ravlt":
            h1 = "Measured score RAVLT total T1-T5"
            h2 = "Estimated HAVLT total"
            h3 = "Estimated CVLT total"
            maxim = 75
        elif instrument =="hvlt":
            h1 = "Measured score HVLT total T1-T3"
            h2 = "Estimated CVLT total"
            h3 = "Estimated RAVLT total"
            maxim = 36
    elif item=="trial 1":
        if instrument=="cvlt":
            h1 = "Measured score CVLT trial 1"
            h2 = "Estimated RAVLT trial 1"
            h3 = "Estimated HVLT trial 1"
            maxim = 16
        elif instrument=="ravlt":
            h1 = "Measured score RAVLT trial 1"
            h2 = "Estimated HAVLT trial 1"
            h3 = "Estimated CVLT trial 1"
            maxim = 15
        elif instrument =="hvlt":
            h1 = "Measured score HVLT trial 1"
            h2 = "Estimated CVLT trial 1"
            h3 = "Estimated RAVLT trial 1"
            maxim = 12
    elif item=="long delay":
        if instrument=="cvlt":
            h1 = "Measured score CVLT long delay"
            h2 = "Estimated RAVLT long delay"
            h3 = "Estimated HVLT long delay"
            maxim = 16
        elif instrument=="ravlt":
            h1 = "Measured score RAVLT long delay"
            h2 = "Estimated HAVLT long delay"
            h3 = "Estimated CVLT long delay"
            maxim = 15
        elif instrument =="hvlt":
            h1 = "Measured score HVLT long delay"
            h2 = "Estimated CVLT long delay"
            h3 = "Estimated RAVLT long delay"
            maxim = 12
    elif item=="short delay":
        if instrument=="cvlt":
            h1 = "Measured score CVLT short delay"
            h2 = "Estimated RAVLT short delay"
            maxim = 16
        elif instrument=="ravlt":
            h1 = "Measured score RAVLT short delay"
            h2 = "Estimated CVLT short delay"
            maxim = 15
        elif instrument=="hvlt":
            maxim = 12
    return h1,h2,h3,maxim
    

