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
# clusters = algos.fingerprintCluster(users, 30)
# # vis.plotfcs(clusters)
# cluster_maps = [vis.engagementMap(cluster) for cluster in clusters]
# cluster_users = [item for sublist in clusters for item in sublist]
# full_map = vis.engagementMap(cluster_users)
full_user_map = vis.engagementMap(users)

labeldict = {}

# color_inds = [i/len(clusters) for i in range(len(clusters))]
colors = {"ru":"#ff009d","ch":"#00ff2a","ir":"#0099ff"}
i  = 0
css = """/* basic positioning */
	.legend { list-style: none; }
	.legend li { float: left; margin-right: 10px; }
	.legend span { border: 1px solid #ccc; float: left; width: 12px; height: 12px; margin: 2px; }
	/* your colors */
	"""
html_piece = """<ul class="legend">"""
html_end = "</ul>"
def addLabel(label, color):
	global html_piece, css
	piece = f"""<li><span class="{label}"></span> {label}</li>\n"""
	stylepiece = f""".legend .{label} {{ background-color:{color}; }}\n"""
	html_piece += piece
	css += stylepiece

	
addLabel("Russia","#ff009d")
addLabel("China","#00ff2a")
addLabel("Iran","#0099ff")

def plotClusterEngagement(cluster,cluster_map,ind):
	# plt.figure(figsize=(50,50))
	global html_piece, css
	G = nx.Graph()
	net = Network("1500px", "1500px",notebook= True)
	for user in cluster:
		# label= clusters.index(cluster)
		G.add_node(user.IDstr.strip(),label = " ",color = addColor(user))
		# labeldict[user.IDstr.strip()] = str(1+label)
	engagementEdges(cluster_map,G)
	pos = nx.spring_layout(G,k=1,scale = 20)
	nx.draw_networkx_nodes(G, pos)
	nx.draw_networkx_edges(
	G, pos,arrowstyle = '-',
	connectionstyle="arc3,rad=0.5",width= 1.5)
	net.from_nx(G)
	net.show_buttons(filter_ = ["physics"])
	html_name = "cluster_"+str(ind)+"_.html"
	net.show("cluster_"+str(ind)+"_.html")
	path = "./" + html_name
	htmlDoc =  open(path)
	
	
	with htmlDoc as fp:

		soup = BeautifulSoup(fp, 'html.parser')
	
	style = soup.find('style', type='text/css')
	body = soup.find('body')
	
	piece = BeautifulSoup(str(html_piece)+str(html_end),'html.parser')
	style.append(css)

	body.insert_before(piece)
	# image = BeautifulSoup(f"""<img src="Cluster_{ind}_Fingerprint.jpeg" alt="Italian Trulli">""",'html.parser')
	# body.insert_after(image)
	print(soup)

	htmlDoc.close()
	html = soup.prettify("utf-8")
	with open(path, "wb") as file:
		file.write(html)
	file.close()
	# nx.draw_networkx_edge_labels(G,pos)
def addColor(user):
	countries = user.getCountries(db)
	color = colors[max(zip(countries.values(), countries.keys()))[1]]
	return color


def engagementEdges(cluster_map,G):
	colors = {"ru":"#5194c0","ch":"#00ff2a","ir":"#74a981"}
	for key,engagers in cluster_map.items():
		users = [user.IDstr.strip() for user in engagers]
		label = db.getCountry(str(key))
		user_name = db.getUsername(str(key))
		# addColor(users,G,colors[label])
		for user,idstr in zip(engagers,users):
			name = False
			info = db2.getInfo(user.ID)
			if info is not None:
				name = info[4]
			if name:
				print(idstr)
				G.nodes[idstr]["color"] = "#111111"
		if(len(engagers) > 1):
			print(len(engagers))
			weight = len(engagers)/10
			print(weight)
			weight = min(weight,5)
			G.add_edges_from(vis.pairEngagement(users),weight=weight,color = colors[label])


# for cluster in clusters:
#     for user in cluster:
	   
#         label= clusters.index(cluster)
#         G.add_node(user.IDstr.strip())
#         labeldict[user.IDstr.strip()] = str(1+label)
#         colors.append(color_inds[label])
	   
# for i in range(len(clusters)):

plotClusterEngagement(users,full_user_map,"All")
print(full_user_map)

