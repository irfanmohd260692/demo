from flask import Flask, request, render_template
import joblib
import matplotlib.pyplot as plt
import os


app = Flask(__name__, static_url_path='/static')

@app.route("/", methods=['GET', 'POST'])
def index():
    model = joblib.load("modelActiveIndiaCases.pkl")
    future_forcast = joblib.load("future_forcast.pkl")
    india_active = joblib.load("india_active.pkl")
    adjusted_dates = future_forcast[:-10]
    india_active_predicted = model.predict(future_forcast[235:])
    listCnt = []
    listCnt.append(int(india_active[-1]))
    listCnt.append(int(india_active_predicted[-1]))

    #Graphical Presentation
    plt.figure(figsize=(16, 11))
    plt.plot(adjusted_dates, india_active)
    plt.plot(future_forcast[235:], india_active_predicted, linestyle='dashed', color='purple')
    plt.title('# of Coronavirus Cases Over Time', size=30)
    plt.xlabel('Days Since 1/22/2020', size=30)
    plt.ylabel('# of Cases', size=30)
    plt.legend(['India : Active Cases', 'Prediction'], prop={'size': 20})
    plt.xticks(size=20)
    plt.yticks(size=20)
    plt.axvline(x=adjusted_dates[-1], linestyle='--', color='red')

    fig1 = plt.gcf()

    plt.show()
    plt.draw()

    cntnme = "India"

    if request.method == 'POST':
        manufacturer = str(request.form['country'])
        cntnme = str(request.form['country'])

    current1 = f"{int(listCnt[0]):,}"
    total1 = f"{int(listCnt[1]):,}"
    manufacturer = "India"

    fig1.savefig(os.path.join(app.root_path, 'static/images/new_plotPred' + cntnme + '.png'))

    return render_template('index.html', current=current1, total=total1, title=manufacturer,
                           urlPred='images/new_plotPred' + manufacturer + '.png')


@app.route("/World")
def WorkData():
    return render_template('World.html', current=current, total=total, url='images/new_plot.png',urlPred='images/new_plotPredWorld.png')


if __name__=='__main__':
    app.run()

