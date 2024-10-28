import json
from enum import Enum
from typing import List
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


class Fit(Enum):
    Linear = 1
    Quadratic = 2
    Cubic = 3
    Quartic = 4
    Quintic = 5
    Logarithmic = 6
    Exponential = 7


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


def make_plot(
    x,
    y,
    xlabel,
    ylabel,
    fname,
    fit=Fit.Linear
):
    if fit is None:
        plt.scatter(x, y, c=colors)
        m, b = np.polyfit(x, y, 1)
        r = np.corrcoef(x, y)[0, 1]
        r2 = r * r
        print("{}: m: {}, b: {}, R: {}, R^2: {}".format(fname, m, b, r, r2))
    else:
        plt.scatter(x, y, c=colors)
        m, b = np.polyfit(x, y, 1)
        r = np.corrcoef(x, y)[0, 1]
        r2 = r * r
        print("{}: m: {}, b: {}, R: {}, R^2: {}".format(fname, m, b, r, r2))
        xlim = plt.gca().get_xlim()
        ylim = plt.gca().get_ylim()
        plt.plot(x, m * np.array(x) + b, c="black")
        plt.gca().set_xlim(xlim)
        plt.gca().set_ylim(ylim)

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(ylabel + " vs. " + xlabel)
    legend = plt.legend(handles=handles, loc="lower right", title="Rank")
    legend.get_frame().set_edgecolor("black")
    plt.savefig(fname, dpi=200)
    plt.close()


make_plot(
    apm,
    tr,
    "APM (Attack Per Minute)",
    "TR",
    "apmvstr.png",
    None
)

make_plot(
    np.log(apm),
    tr,
    "ln(APM) (Attack Per Minute)",
    "TR",
    "lnapmvstr.png",
)

make_plot(
    pps,
    tr,
    "PPS (Pieces Per Second)",
    "TR",
    "ppsvstr.png",
    None
)

make_plot(
    np.log(pps),
    tr,
    "ln(PPS) (Pieces Per Second)",
    "TR",
    "lnppsvstr.png",
)

make_plot(
    app,
    tr,
    "APP (Attack Per Piece)",
    "TR",
    "trvsapp.png",
    None
)

make_plot(
    np.log(app),
    tr,
    "ln(APP) (Attack Per Piece)",
    "TR",
    "trvslnapp.png",
)

make_plot(
    apm,
    pps,
    "APM (Attack Per Minute)",
    "PPS",
    "ppvsapm.png"
)

make_plot(
    gp,
    tr,
    "Games Played",
    "TR",
    "gpvstr.png",
    None,
)

make_plot(
    vs,
    tr,
    "VS",
    "TR",
    "vsvstr.png",
    None
)

make_plot(
    np.log(vs),
    tr,
    "ln(VS)",
    "TR",
    "lnvsvstr.png"
)

make_plot(
    wl,
    tr,
    "Win Loss Ratio",
    "TR",
    "wlrvstr.png",
    None
)

make_plot(
    wl,
    np.log(tr),
    "Win Loss Ratio",
    "ln(TR)",
    "wlrvslntr.png"
)

make_plot(
    vs,
    apm,
    "VS",
    "APM (Attack Per Minute)",
    "apmvsvs.png"
)

make_plot(
    vs,
    pps,
    "VS",
    "PPS (Pieces Per Second)",
    "ppsvsvs.png"
)

make_plot(
    glicko,
    tr,
    "Glicko",
    "TR",
    "trvsglicko.png",
    None
)

make_plot(
    apm,
    glicko,
    "APM (Attack Per Minute)",
    "Glicko",
    "glickovsapm.png"
)

plt.scatter(lbpos, tr, c=colors)
# m, b = np.polyfit(lbpos, tr, 1)
# plt.plot(lbpos, m * np.array(lbpos) + b, c="black")
plt.xlabel("Leaderboard Position")
plt.ylabel("TR")
plt.title("TR vs. Leaderboard Position")
legend = plt.legend(handles=handles, loc="lower right", title="Rank")
legend.get_frame().set_edgecolor("black")
plt.gca().invert_xaxis()
plt.savefig("trvslbpos.png", dpi=200)
plt.close()

plt.scatter(lbpos, glicko, c=colors)
# m, b = np.polyfit(lbpos, glicko, 1)
# plt.plot(lbpos, m * np.array(lbpos) + b, c="black")
plt.xlabel("Leaderboard Position")
plt.ylabel("Glicko")
plt.title("Glicko vs. Leaderboard Position")
legend = plt.legend(handles=handles, loc="lower right", title="Rank")
legend.get_frame().set_edgecolor("black")
plt.gca().invert_xaxis()
plt.savefig("glickovslbpos.png", dpi=200)
plt.close()
