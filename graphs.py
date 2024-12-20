import json
import os
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
if not os.path.exists("./graphs"):
    os.makedirs("./graphs")


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
matplotlib.rcParams["font.size"] = 16
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
    aps = apm[i] / 60
    app.append(aps/pps[i])

dss = []
for i in range(0, len(apm)):
    dss.append(vs[i]/100 - apm[i]/60)

ranks = collect(lambda a: a["league"]["rank"])
colors = collect(lambda a: color_from_rank(a["league"]["rank"]))

cheese = []
for i in range(0, len(dss)):
    dsp = dss[i] / pps[i]
    cheese.append(
        (dsp * 150) + ((vs[i]/apm[i] - 2) * 50) + (0.6 - app[i]) * 125)

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
    fit=Fit.Linear,
    invert_xaxis=False,
    filtered_colors=None,
):
    real_colors = None
    if filtered_colors is not None:
        real_colors = filtered_colors
    else:
        real_colors = colors

    if fit is None:
        plt.scatter(x, y, c=real_colors)
        m, b = np.polyfit(x, y, 1)
        r = np.corrcoef(x, y)[0, 1]
        r2 = r * r
        meanx = np.mean(x)
        medx = np.median(x)
        meany = np.mean(y)
        medy = np.median(y)
        print(
            "{}: m: {}, b: {}, R: {}, R^2: {}, mux: {}, muy: {}, mex: {}, mey: {}"
            .format(
                fname, m, b, r, r2, meanx, meany, medx, medy))
    else:
        plt.scatter(x, y, c=real_colors)
        m, b = np.polyfit(x, y, 1)
        r = np.corrcoef(x, y)[0, 1]
        r2 = r * r
        meanx = np.mean(x)
        medx = np.median(x)
        meany = np.mean(y)
        medy = np.median(y)
        print(
            "{}: m: {}, b: {}, R: {}, R^2: {}, mux: {}, muy: {}, mex: {}, mey: {}"
            .format(
                fname, m, b, r, r2, meanx, meany, medx, medy))
        xlim = plt.gca().get_xlim()
        ylim = plt.gca().get_ylim()
        plt.plot(x, m * np.array(x) + b, c="black")
        plt.gca().set_xlim(xlim)
        plt.gca().set_ylim(ylim)

    if invert_xaxis:
        plt.gca().invert_xaxis()

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(ylabel + " vs. " + xlabel)
    legend = plt.legend(handles=handles, loc="lower right", title="Rank")
    legend.get_frame().set_edgecolor("black")
    plt.savefig("./graphs/" + fname, dpi=200)
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
    "PPS (Pieces Per Second)",
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

make_plot(
    lbpos,
    tr,
    "Leaderboard Position",
    "TR",
    "trvslbpos.png",
    invert_xaxis=True
)

make_plot(
    lbpos,
    glicko,
    "Leaderboard Position",
    "Glicko",
    "glickovslbpos.png",
    invert_xaxis=True
)

make_plot(
    dss,
    tr,
    "DSS (Downstack Per Second)",
    "TR",
    "trvsdss.png",
    None
)

# make_plot(
#     np.log(dss),
#     tr,
#     "DSS (Downstack Per Second)",
#     "TR",
#     "trvslndss.png",
#     None
# )


make_plot(
    cheese,
    tr,
    "Cheese Index",
    "TR",
    "trvscheese.png",
)

filtered_data = list()
for user in decoded.data:
    if user["league"]["gamesplayed"] <= 500:
        filtered_data.append(user)

filtered_tr = list()
for user in filtered_data:
    filtered_tr.append(user["league"]["tr"])

filtered_games_played = list()
for user in filtered_data:
    filtered_games_played.append(user["league"]["gamesplayed"])

filtered_colors = list()
for user in filtered_data:
    filtered_colors.append(color_from_rank(user["league"]["rank"]))

make_plot(
    filtered_games_played,
    filtered_tr,
    "Games Played",
    "TR",
    "trvsgp-filtered.png",
    None,
    filtered_colors=filtered_colors
)
