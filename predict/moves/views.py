from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import pandas as pd

# Create your views here.
@csrf_exempt
def index(request):
    try:
        the_post = json.loads(request.body)
        p_object = []
        p_time = []
        p_x = []
        p_y = []
        for i,line in enumerate(the_post):
            print("Next line",i)
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
        print(df)
        

    except:
        return render(request, "index.html", context={})

    context = {}

    return render(request, "index.html", context=context)