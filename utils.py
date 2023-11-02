import random
import pymongo
import datetime
import random
import dns.resolver
from constants import MONGODB_URI

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

suggestion_gifs = [
    "https://media0.giphy.com/media/7TqDUEMT50uAztuB83/giphy.gif?cid=ecf05e47952vhkf0meyq1yogmi7cagsmnk04ji3t3xzd3ss8&ep=v1_gifs_search&rid=giphy.gif&ct=g",
    "https://media4.giphy.com/media/3o6MboFf6raVHXAqha/giphy.gif?cid=ecf05e47952vhkf0meyq1yogmi7cagsmnk04ji3t3xzd3ss8&ep=v1_gifs_search&rid=giphy.gif&ct=g",
    "https://media3.giphy.com/media/3rYvT80acw5jfqTWlU/giphy.gif?cid=ecf05e47952vhkf0meyq1yogmi7cagsmnk04ji3t3xzd3ss8&ep=v1_gifs_search&rid=giphy.gif&ct=g"
]

feedback_gifs = [
    "https://media4.giphy.com/media/MFwBk6Ig786VhnbVwJ/giphy.gif?cid=ecf05e47wddjgovik0y4cww83b3pdzp1dln37miymuk15r80&ep=v1_gifs_search&rid=giphy.gif&ct=g",
    "https://media4.giphy.com/media/ZF8GoFOeBDwHFsVYqt/giphy.gif?cid=ecf05e47wddjgovik0y4cww83b3pdzp1dln37miymuk15r80&ep=v1_gifs_search&rid=giphy.gif&ct=g",
    "https://media1.giphy.com/media/h08E3tuV8LXswr6mF0/giphy.gif?cid=ecf05e47wddjgovik0y4cww83b3pdzp1dln37miymuk15r80&ep=v1_gifs_search&rid=giphy.gif&ct=g"
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


def mongo(db):
    dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
    dns.resolver.default_resolver.nameservers = ["8.8.8.8"]
    data = pymongo.MongoClient(MONGODB_URI)
    user = data[db]["users"]
    return user


def save_confession(data):
    db = mongo(db="secretSanctuary")
    db.insert_one(data)


def load_confessions(size):
    db = mongo(db="secretSanctuary")
    confessions = db.aggregate([{"$sample": {"size": size}}])
    confession = []
    for conf in confessions:
        confession.append(conf)
    return confession


def insert_suggestion(server_id, suggestion):
    db = mongo("servers")
    server = db.find_one({"_id": server_id})
    suggestions = server["suggestions"]
    identifier = random.randint(1000, 10000)
    append = {
        "feedback": suggestion,
        "date": datetime.date.today().strftime("%B %d, %Y"),
        "time_gmt": datetime.datetime.utcnow().strftime("%H:%M:%S"),
        "author": f"AnonymousUser#{identifier}",
    }
    suggestions.append(append)
    db.update_one({"_id": server_id}, {"$set": {"suggestions": suggestions}})


def insert_feedback(server_id, feedback):
    db = mongo("servers")
    server = db.find_one({"_id": server_id})
    feedbacks = server["feedbacks"]
    print(feedbacks)
    identifier = random.randint(1000, 10000)
    append = {
        "feedback": feedback,
        "date": datetime.date.today().strftime("%B %d, %Y"),
        "time_gmt": datetime.datetime.utcnow().strftime("%H:%M:%S"),
        "author": f"AnonymousUser#{identifier}",
    }
    feedbacks.append(append)
    db.update_one({"_id": server_id}, {"$set": {"feedbacks": feedbacks}})
