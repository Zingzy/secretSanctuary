import json
import random
import dns.reslover

waiting_gifs = [
    "https://media3.giphy.com/media/l0HlBO7eyXzSZkJri/giphy.gif?cid=ecf05e475p246q1gdcu96b5mkqlqvuapb7xay2hywmki7f5q&ep=v1_gifs_search&rid=giphy.gif&ct=g",
    "https://media2.giphy.com/media/QBd2kLB5qDmysEXre9/giphy.gif?cid=ecf05e47ha6xwa7rq38dcst49nefabwwrods631hvz67ptfg&ep=v1_gifs_search&rid=giphy.gif&ct=g",
    "https://media2.giphy.com/media/ZgqJGwh2tLj5C/giphy.gif?cid=ecf05e47gflyso481izbdcrw7y8okfkgdxgc7zoh34q9rxim&ep=v1_gifs_search&rid=giphy.gif&ct=g",
    "https://media0.giphy.com/media/EWhLjxjiqdZjW/giphy.gif?cid=ecf05e473fifxe2bg4act0zq73nkyjw0h69fxi52t8jt37lf&ep=v1_gifs_search&rid=giphy.gif&ct=g",
]

confession_gifs = [
    "https://media1.giphy.com/media/yow6i0Zmp7G24/giphy.gif?cid=ecf05e471kc1phnsh0kov28u8y1lhkaicca5tw9iyr2feypm&ep=v1_gifs_search&rid=giphy.gif&ct=g",
    "https://media4.giphy.com/media/UONBsB5PqE6ty/giphy.gif?cid=ecf05e47nsu1j9zbolmns3l5h9m9qv18cj1cvfpbbqe5a8e5&ep=v1_gifs_search&rid=giphy.gif&ct=g",
    "https://media1.giphy.com/media/7jnPK8t4QBuOdE3ouE/giphy.gif?cid=ecf05e47ryv2afuiv8wd2evwuuwxw7fy8xgebgoy44qhjwtb&ep=v1_gifs_search&rid=giphy.gif&ct=g",
]


# def load_confessions():
#     try:
#         with open(r"data/confessions.json", "r") as f:
#             data = f.read()
#         try:
#             return json.loads(data)
#         except:
#             return {}
#     except FileNotFoundError:
#         return {}


# def save_confession(data):
#     with open(r"data/confessions.json", "w") as f:
#         f.write(json.dumps(data, indent=4))


def random_pfp():
    with open(r"data/pfps.txt", "r") as f:
        data = f.read()

    data = data.split("\n")
    return random.choice(data).strip()



def mongo():
    dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
    dns.resolver.default_resolver.nameservers = ["8.8.8.8"]
    data = pymongo.MongoClient("mongodb://localhost:27017/")
    user = data["secretSanctuary"]["users"]
    return user

def save_confessions(data):
    db = mongo()
    db.insert_one(data)


def load_confessions():
    user = mongo()
    confession = db.find()
    return confession
