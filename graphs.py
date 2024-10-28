import json
from typing import List
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


class Data:
    def __init__(self, created, cache_until, data: List):
        self.created = created
        self.cache_until = cache_until
        self.data = data


json_fd = open(r"./leaderboard.json", "r")
json_data = json_fd.read()
json_fd.close()
decoded = Data(**json.loads(json_data))


def collect(func):
    ret = list()

    for user in decoded.data:
        ret.append(func(user))

    return ret


rank_to_color = {
    "d": "#846a83",
    "d+": "#7f577f",
    "c-": "#6d417c",
    "c": "#67277b",
    "c+": "#522178",
    "b-": "#594abf",
    "b": "#4256b5",
    "b+": "#4880b3",
    "a-": "#35aa8c",
    "a": "#3ea650",
    "a+": "#35b726",
    "s-": "#b79f2b",
    "s": "#dea31c",
    "s+": "#ffda0c",
    "ss": "#ffa830",
    "u": "#ff5d15",
    "x": "#ff5aff",
    "x+": "#b60f3f"
}


def color_from_rank(rank):
    return rank_to_color[rank]


matplotlib.rcParams["figure.figsize"] = 9, 9
tr = collect(lambda a: a["league"]["tr"])
apm = collect(lambda a: a["league"]["apm"])
pps = collect(lambda a: a["league"]["pps"])
vs = collect(lambda a: a["league"]["vs"])
gp = collect(lambda a: a["league"]["gamesplayed"])
gw = collect(lambda a: a["league"]["gameswon"])
rd = collect(lambda a: a["league"]["rd"])
glicko = collect(lambda a: a["league"]["glicko"])
lbpos = list(range(0, len(rd)))

wl = []
for i in range(0, len(gp)):
    wl.append(gw[i]/gp[i])
app = []
for i in range(0, len(apm)):
    aps = apm[i] * 60
    app.append(aps/pps[i])

ranks = collect(lambda a: a["league"]["rank"])
colors = collect(lambda a: color_from_rank(a["league"]["rank"]))

handles = []
for key in rank_to_color:
    handles.append(mpatches.Patch(color=rank_to_color[key], label=key.upper()))
handles.reverse()


def make_plot(x, y, xlabel, ylabel, title, fname):
    plt.scatter(x, y, c=colors)
    m, b = np.polyfit(x, y, 1)
    plt.plot(x, m * np.array(x) + b)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    legend = plt.legend(handles=handles, loc="lower right", title="Rank")
    legend.get_frame().set_edgecolor("black")
    plt.savefig(fname, dpi=200)
    plt.close()


make_plot(
    apm,
    tr,
    "APM (Attack Per Minute)",
    "TR",
    "TR vs Attack Per Minute",
    "apmvstr.png"
)

make_plot(
    pps,
    tr,
    "PPS (Pieces Per Second)",
    "TR",
    "TR vs Attack Per Minute",
    "ppsvstr.png"
)

make_plot(
    app,
    tr,
    "APP (Attack Per Piece)",
    "TR",
    "TR vs Attack Per Piece",
    "appvstr.png"
)

make_plot(
    apm,
    pps,
    "APM (Attack Per Minute)",
    "PPS",
    "PPS vs Attack Per Minute",
    "ppvsapm.png"
)

make_plot(
    gp,
    tr,
    "Games Played",
    "TR",
    "Games Played vs TR",
    "gpvstr.png"
)

make_plot(
    vs,
    tr,
    "VS",
    "TR",
    "VS vs TR",
    "vsvstr.png"
)

make_plot(
    vs,
    tr,
    "VS",
    "TR",
    "VS vs TR",
    "vsvstr.png"
)

make_plot(
    wl,
    tr,
    "Win Loss Ratio",
    "TR",
    "TR vs Win Loss Ratio",
    "wlrvstr.png"
)

make_plot(
    vs,
    apm,
    "VS",
    "APM (Attack Per Minute)",
    "VS vs Attack Per Minute",
    "apmvsvs.png"
)

make_plot(
    vs,
    pps,
    "VS",
    "PPS (Pieces Per Second)",
    "VS vs Pieces Per Second",
    "ppsvsvs.png"
)

make_plot(
    glicko,
    tr,
    "Glicko",
    "TR",
    "TR vs Glicko",
    "trvsglicko.png"
)

make_plot(
    apm,
    glicko,
    "APM (Attack Per Minute)",
    "Glicko",
    "Glicko vs APM",
    "glickovsapm.png"
)

plt.scatter(lbpos, tr, c=colors)
m, b = np.polyfit(lbpos, tr, 1)
plt.plot(lbpos, m * np.array(lbpos) + b)
plt.xlabel("Leaderboard Position")
plt.ylabel("TR")
plt.title("TR vs Leaderboard Position")
legend = plt.legend(handles=handles, loc="lower right", title="Rank")
legend.get_frame().set_edgecolor("black")
plt.gca().invert_xaxis()
plt.savefig("trvslbpos.png", dpi=200)
plt.close()


plt.scatter(lbpos, glicko, c=colors)
m, b = np.polyfit(lbpos, glicko, 1)
plt.plot(lbpos, m * np.array(lbpos) + b)
plt.xlabel("Leaderboard Position")
plt.ylabel("Glicko")
plt.title("Glicko vs Leaderboard Position")
legend = plt.legend(handles=handles, loc="lower right", title="Rank")
legend.get_frame().set_edgecolor("black")
plt.gca().invert_xaxis()
plt.savefig("glickovslbpos.png", dpi=200)
plt.close()
