from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import pandas as pd
from os.path import join
from predict import settings
from moves.models import Last
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import random
import os

# Create your views here.
@csrf_exempt
def index(request):

    if len(Last.objects.all()) == 0:
        last = Last()
        last.save()

    last = Last.objects.all()[0]

    try:

        the_post = json.loads(request.body)

        p_object = []
        p_time = []
        p_x = []
        p_y = []

        for i,line in enumerate(the_post):
            for j, coords in enumerate(line):
                print(coords,j)
                p_object.append(i)
                p_time.append(j)
                p_x.append(coords["x"])
                p_y.append(coords["y"])

        df = pd.DataFrame({
            "object": p_object,
            "time": p_time,
            "x": p_x,
            "y": p_y,
        })

        df["y"] = 400-df["y"]

        # Here: prediction, matplotlib -> file
        #

        path = join(settings.MEDIA_ROOT, 'df.csv')
        print("writing csv", path)
        df.to_csv(path)

        plt.clf()

        for i in df["object"].unique():
            dfi = df[df.object == i]
            plt.plot(dfi["x"], dfi["y"])
        df["nx"] = df["x"].shift(-1)
        df["ny"] = df["y"].shift(-1)
        df["n_object"] = df["object"].shift(-1)
        df["dx"] = df["nx"] - df["x"]
        df["dy"] = df["ny"] - df["y"]
        df = df[df["object"] == df["n_object"]]
        df["x2"] = df["x"] ** 2
        df["y2"] = df["y"] ** 2
        df["xy"] = df["x"] * df["y"]

        df.head()

        lin_x = LinearRegression()
        lin_y = LinearRegression()
        lin_x.fit(df[["x", "y", "x2", "y2", "xy"]], df["dx"])
        lin_y.fit(df[["x", "y", "x2", "y2", "xy"]], df["dy"])

        for x in range(10, 1000, 50):
            for y in range(10, 1000, 50):
                dx = lin_x.predict([[x, y, x ** 2, y ** 2, x * y]])[0]
                dy = lin_y.predict([[x, y, x ** 2, y ** 2, x * y]])[0]
                plt.arrow(x, y, dx, dy, color="blue", head_length=10, head_width=10)

        try:
            os.remove(join(settings.MEDIA_ROOT, last.last_file))
        except:
            pass

        last.last_file = 'df' + str(random.randint(1111,9999)) + '.png'
        path = join(settings.MEDIA_ROOT, last.last_file)
        last.save()
        print("writing png", path)
        plt.savefig(path)

        return HttpResponse("OK")

    except Exception as e:
        print(str(e))
    return render(request, "index.html", context={"first":True,"file":last.last_file})


def result(request):
    if len(Last.objects.all()) == 0:
        last = Last()
        last.save()

    last = Last.objects.all()[0]

    return render(request, "index.html", context={"first": False,"file":last.last_file})
