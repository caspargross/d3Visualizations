from flask import Flask, render_template, request, redirect, url_for, abort, sessions
import csv
import os
import json

app = Flask(__name__)


# .ordered == MY_ORDER &&
#             d.mass_g != 0 &&
#             d.newborn_g != 0 &&
#             d.gestation_mo != 0 ) {
#
#                 d.familyName = d.family;
#                 d.taxonName = d.genus + " " + d.species;
#                 d.massParent = +d.mass_g;
#                 d.massChild = +d.newborn_g;
#                 d.gestation = +d.gestation_mo;

orders = list();

def readdatafile():
    path = os.path.join(os.path.dirname(__file__), 'static/mammal_life_hist_species.csv')
    with open(path) as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        cleanrows = list()


        for row in rows:
            try:
                cleanrows.append(convert(row))
            except:
                pass;
    return json.dumps(cleanrows)


# Changes row datatype and filters empty values
def convert(row):
    if row['newborn_g'] and row['mass_g'] and row['ordered'] and row['gestation_mo']:

        cleanrow = {k: float(row[k]) for k in ('mass_g', 'newborn_g', 'gestation_mo')}
        cleanrow.update({k: row[k] for k in ('ordered', 'family')})
        cleanrow.update({'taxonName' : row['genus'] + " " + row['species']})

        myOrder = cleanrow['ordered']
        if myOrder not in orders:
            orders.append(myOrder)

        print myOrder
        return cleanrow

    else:
        raise NameError('Empty fields')


@app.route('/')
def index():
    return redirect(url_for('bubbleChart'))

@app.route('/bubbleChart')
def bubbleChart():
    dat = readdatafile()
    return render_template('bubbleChartV6.html', data=dat, orderList=orders)

@app.route('/network')
def network():
    data = {"nodes": [{"name": "node1", "group": 1},
                      {"name": "node2", "group": 2},
                      {"name": "node3", "group": 2},
                      {"name": "node4", "group": 3}],
            "links": [{"source": 2, "target": 1, "weight": 1},
                      {"source": 0, "target": 2, "weight": 3}]}

    return render_template('network_graph.html', data=json.dumps(data))


if __name__ == '__main__':
    app.run(debug = True)
