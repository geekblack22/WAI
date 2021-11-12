from networkx.algorithms.bipartite.basic import color
import numpy as np
import matplotlib.pyplot as plt
from numpy.core.defchararray import startswith
import twitterInterface 
import os
import algos
import datetime
import database
from dotenv import load_dotenv
from scipy.stats import chi2, loglaplace
from datetime import timedelta  
from labellines import labelLine, labelLines
from matplotlib import rcParams, cycler
import matplotlib.backends.backend_pdf
import visualizer as vis
import networkx as nx
import random
from pyvis.network import Network
from bs4 import BeautifulSoup
retweeters = [2721413702,2897373563,1282456897,2541012107,1039900418686500865,1016733350785007616,388736352,239619301,803939316871393280,767270527,317302594,985220102483333120,2335406749,2609222612,2721957062]
n = np.arange(len(retweeters))
y = np.zeros_like(n) + 1
users = []
dates = []
load_dotenv()
consumer_key = os.getenv('consumer_key')
consumer_secret = os.getenv('consumer_secret')
bearer_token = os.getenv('test_token')
server_1 = os.getenv('server_1')
uid_1 = os.getenv('uid_1')
database_1 = os.getenv('database_1')
pwd_1 = os.getenv('pwd_1')
server_2 = os.getenv('server_2')
database_2 = os.getenv('database_2')
uid_2 = os.getenv('uid_2')
pwd_2 = os.getenv('pwd_2')
db = database.Database(server_1,database_1,uid_1,pwd_1)
db2 = database.Database(server_2,database_2,uid_2,pwd_2)

users = db2.getAllUsers()
tw = twitterInterface.TwitterInterface(consumer_key,consumer_secret,bearer_token)
clusters = algos.fingerprintCluster(users, 30)
cluster_maps = [vis.engagementMap(cluster) for cluster in clusters]
cluster_users = [item for sublist in clusters for item in sublist]
full_map = vis.engagementMap(cluster_users)
full_user_map = vis.engagementMap(users)

labeldict = {}

color_inds = [i/len(clusters) for i in range(len(clusters))]
colors = {"ru":"#ff009d","ch":"#00ff2a","ir":"#0099ff"}
i  = 0
def plotClusterEngagement(cluster,cluster_map,ind):
    # plt.figure(figsize=(50,50))
    G = nx.Graph()
    net = Network("1500px", "1500px",notebook= True)
    for user in cluster:
        label= clusters.index(cluster)
        G.add_node(user.IDstr.strip(),label = " ",color = addColor(user))
        labeldict[user.IDstr.strip()] = str(1+label)
    engagementEdges(cluster_map,G,ind)
    pos = nx.spring_layout(G,k=1,scale = 20)
    nx.draw_networkx_nodes(G, pos)
    nx.draw_networkx_edges(
    G, pos,arrowstyle = '-',
    connectionstyle="arc3,rad=0.5",width= 1.5)
    net.from_nx(G)
    html_name = "cluster_"+str(ind)+"_.html"
    net.show("cluster_"+str(ind)+"_.html")

    htmlDoc =  open(html_name)
    with htmlDoc as fp:
       soup = BeautifulSoup(fp, 'html.parser')
    print(soup)
    style = soup.find('style', type='text/css')
    body = soup.find('body')
    css = """/* basic positioning */
        .legend { list-style: none; }
        .legend li { float: left; margin-right: 10px; }
        .legend span { border: 1px solid #ccc; float: left; width: 12px; height: 12px; margin: 2px; }
        /* your colors */
        .legend .Russia { background-color: #ff009d; }
        .legend .China { background-color:#00ff2a; }
        .legend .Iran { background-color: #0099ff; }"""
    html_piece = """<ul class="legend">
        <li><span class="Russia"></span> Russia</li>
        <li><span class="China"></span> China</li>
        <li><span class="Iran"></span> Iran</li>
    </ul>"""
    html_piece = BeautifulSoup(str(html_piece),'html.parser')
    style.append(css)
    body.insert_before(html_piece)
    print(soup)
    htmlDoc.close()
    html = soup.prettify("utf-8")
    with open(html_name, "wb") as file:
        file.write(html)
    # nx.draw_networkx_edge_labels(G,pos)
def addColor(user):
    countries = user.getCountries(db)
    color = colors[max(zip(countries.values(), countries.keys()))[1]]
    return color
def engagementEdges(cluster_map,G,i):
   
    for key,engagers in cluster_map.items():
        users = [user.IDstr.strip() for user in engagers]
        label = db.getCountry(str(key))
        user_name = db.getUsername(str(key))
       
        if(len(engagers) > 1):
            print(len(engagers))
            weight = len(engagers)/10
            if i == 4 or i == 12:
                 weight = .005
            print(weight)
            weight = min(weight,5)
            G.add_edges_from(vis.pairEngagement(users),color = colors[label])

# for cluster in clusters:
#     for user in cluster:
       
#         label= clusters.index(cluster)
#         G.add_node(user.IDstr.strip())
#         labeldict[user.IDstr.strip()] = str(1+label)
#         colors.append(color_inds[label])
       
for i in range(len(clusters)):

    plotClusterEngagement(clusters[i],cluster_maps[i],i)
