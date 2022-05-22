import configparser
from flask import Flask, render_template, request
import numpy as np
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

from database import Database
from linear_regression import get_next_value_in_timeline

app = Flask(__name__)

config = configparser.ConfigParser()
config.read('config.ini')

db = Database()


def get_month_name(no):
    if no > 12:
        no -= 12
    months = ["Unknown",
              "January",
              "February",
              "March",
              "April",
              "May",
              "June",
              "July",
              "August",
              "September",
              "Oktober",
              "November",
              "December"]
    return months[no]


def get_last_months(start_date, months):
    for i in range(months):
        yield start_date.year, start_date.month
        start_date += relativedelta(months=-1)


def get_month_before(cur):
    given = datetime.strptime(cur, '%Y/%m')
    given += relativedelta(days=-1)
    return given


net_usage = dict()
last3month = list(get_last_months(datetime.today(), 3))

for m in last3month:
    year = m[0]
    month = str(m[1]).zfill(2)  # add leading zero
    rows = db.query(
        """SELECT DISTINCT net, 
        net_usage from net_stats WHERE timestamp 
        BETWEEN '{0}-{1}-01 00:00:00' AND '{0}-{1}-31 23:59:59' ORDER BY timestamp""".format(year, month),
    )
    for r in rows:
        net = r[0]
        usage = r[1]
        m = "{0}/{1}".format(year, month)
        if net not in net_usage.keys():
            net_usage[net] = list()
        net_usage[net].append((m, usage))

# fill
for key, value in net_usage.items():
    if len(value) < 3:
        for i in range(3 - len(value)):
            month = value[len(value) - 1][0]
            m = get_month_before(month).strftime('%Y/%m')
            net_usage[key].append((m, 0))

data_rows = []
for key, value in net_usage.items():
    a = value[2][1]  # 2 = month, 1 = tuple position
    b = value[1][1]
    c = value[0][1]
    if a < 90 and b < 90 and c < 90:  # check if net not full yet
        data_rows.append((key, a, b, c))

a_col = get_month_name(last3month[-1][1])
b_col = get_month_name(last3month[-2][1])
c_col = get_month_name(last3month[-3][1])
df = pd.DataFrame(data_rows, columns=("Network", a_col, b_col, c_col))


df = df.astype({a_col: np.float64})
df = df.astype({b_col: np.float64})
df = df.astype({c_col: np.float64})

tbl_overview = df.to_html(index=False)

col_names = df.columns
firstMonth = col_names[1]
secondMonth = col_names[2]
thirdMonth = col_names[3]

df_5percent = df.query("({0} > 95) | ({1} > 95) | ({2} > 95)".format(firstMonth, secondMonth, thirdMonth))
tbl_5percent = df_5percent.to_html(index=False)

df_10percent = df.query("({0} > 90) | ({1} > 90) | ({2} > 90)".format(firstMonth, secondMonth, thirdMonth))
tbl_10percent = df_10percent.to_html(index=False)

df_preview = pd.DataFrame(df["Network"])

preview_month = []
preview_month_nos = []
for r in range(1, 4):
    p_month = last3month[-3][1] + r
    preview_month_nos.append(p_month)
    preview_month.append(get_month_name(p_month))

# calculate preview
preview_rows = []
for ll in df.values.tolist():
    values = ll[1:]

    first_preview_month_value = get_next_value_in_timeline(preview_month_nos, values)
    merge = list()
    merge.append(str(ll[0]))
    merge.append(first_preview_month_value)

    next_values = values[1:]
    tmp = list()
    tmp.append(first_preview_month_value)
    next_values = next_values + tmp
    sec_preview_month_value = get_next_value_in_timeline(preview_month_nos, next_values)
    merge.append(sec_preview_month_value)

    next_values = values[1:]
    tmp = list()
    tmp.append(sec_preview_month_value)
    next_values = next_values + tmp
    third_preview_month_value = get_next_value_in_timeline(preview_month_nos, next_values)
    merge.append(third_preview_month_value)

    preview_rows.append(merge)

column_names = list()
column_names.append("Network")
for m in preview_month:
    column_names.append(m)
df_preview = pd.DataFrame(preview_rows, columns=column_names)
tbl_preview = df_preview.to_html(index=False)

a, b, c = preview_month
df_5percent_preview = df_preview.query("({0} > 95) | ({1} > 95) | ({2} > 95)".format(a, b, c))
tbl_5percent_preview = df_5percent_preview.to_html(index=False)

a, b, c = preview_month
df_10percent_preview = df_preview.query("({0} > 90) | ({1} > 90) | ({2} > 90)".format(a, b, c))
tbl_10percent_preview = df_10percent_preview.to_html(index=False)


@app.route('/', methods=['GET', 'POST'])
def html_table():
    return render_template('index.html', tables=[tbl_overview])


@app.route('/five', methods=['GET'])
def five():
    return render_template('index.html', tables=[tbl_5percent])


@app.route('/ten', methods=['GET'])
def ten():
    return render_template('index.html', tables=[tbl_10percent])


@app.route('/preview', methods=['GET'])
def preview():
    return render_template('index_vor.html', tables=[tbl_preview])


@app.route('/fivePreview', methods=['GET'])
def five_preview():
    return render_template('index_vor.html', tables=[tbl_5percent_preview])


@app.route('/tenPreview', methods=['GET'])
def ten_preview():
    return render_template('index_vor.html', tables=[tbl_10percent_preview])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
