import urllib.request

def get_graph(time, panelId, ImageName):
    image_url = "http://51.210.255.2:3000/render/d-solo/ZZTOZx5nz/new-dashboard-copy?orgId=1&from=now-{}&to=now&panelId={}&width=1000&height=500&tz=Europe%2FBrussels".format(time, panelId, ImageName)
    urllib.request.urlretrieve(image_url, "{}.jpg".format(ImageName))

get_graph("7d", "39", "CO2")