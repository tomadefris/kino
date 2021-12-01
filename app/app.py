from flask import Flask
from flask import render_template,request
import json
import sys
import requests

app = Flask(__name__)

@app.route("/")
def index():
    fname = request.args.get("fname")
    if fname:
        returned = get_sorted_recommendations(extract_movie_titles(get_movies_from_tastedive(fname)))
    else:
        returned = "Nothing"
    return render_template("index.html", len=len(returned),returned = returned)


def get_movies_from_tastedive(s):
    par={}
    Similar={}
    url="https://tastedive.com/api/similar"
    par["q"]=s
    par["type"]="movies"
    par["limit"]=5
    par["key"]="383771-testapp-8C59GIP3"
    resp=requests.get(url, params = par)
    Similar=resp.json()
    #print(resp.url)
    return Similar

def extract_movie_titles(x):
    result=[]
    for j in x["Similar"]["Results"]:
        if not j in result:
            result.append(j["Name"])
    return result

def get_related_titles(x): 
    ix=[]
    ix1=[]
    if x == []: 
        return []
    for i in x:  
        j=extract_movie_titles(get_movies_from_tastedive(i)) 
        if not j in ix:
            ix.append(j)
        for k in ix:
            for q in k:
                if not q in ix1:
                    ix1.append(q)
    return ix1

def get_movie_data(s): 
    url= 'https://www.omdbapi.com/?apikey=5d654365&' 
    par={} 
    par['t']=s 
    par['r']='json'
    resp=requests.get(url,params=par) 
    jsonx=resp.json() 
    return jsonx 
def get_movie_rating(s): 
    if len(s["Ratings"]) < 3: 
    	return 0
    rating=s["Ratings"][1]["Value"]
    rating=int(rating[:-1]) 
    return rating 
def get_sorted_recommendations(x): 
    ix=[] 
    rt=[] 
    if x==[]: 
        return [] 
    i1=get_related_titles(x) 
    for i in i1: 
        if not i in ix: 
            ix.append(i) 
            rt.append(get_movie_rating(get_movie_data(i))) 
    zipCode=sorted(zip(rt,ix), reverse=True) 
    return zipCode 

