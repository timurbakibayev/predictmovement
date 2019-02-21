from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import pandas as pd
from os.path import join
from predict import settings

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

        # Here: prediction, matplotlib -> file
        #

        path = join(settings.MEDIA_ROOT, 'df.csv')
        print("writing csv", path)

        df.to_csv(path)

        return HttpResponse("OK")

    except Exception as e:
        print(str(e))
        return render(request, "index.html", context={})
