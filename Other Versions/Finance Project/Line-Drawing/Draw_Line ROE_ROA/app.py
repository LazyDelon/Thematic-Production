import sqlite3
import string
from flask import Flask, render_template
from flask import request
from pyecharts import options as opts
from pyecharts.charts import Line
import numpy as np
app = Flask(__name__, static_folder="templates")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():
    key = request.args.get('wd')
    #conn.execute("SELECT * FROM Stock WHERE 股票代碼=%s", (key))
    # "SELECT * FROM stocks WHERE symbol = '%s'" % symbol
    # SELECT * FROM stocks WHERE symbol=?', t
    conn = sqlite3.connect("stock.db")
    sql = "SELECT 季別,ROE,ROA FROM Stock WHERE 股票代碼 = " + str(key)
    cursor = conn.cursor()
    cursor.execute(sql)
    content = cursor.fetchall()
    field_name = [i[0] for i in cursor.description]
    cursor.execute(sql)
    sql = cursor.fetchall()
    stock_name = "SELECT 股票名稱 FROM Stock WHERE 股票代碼 = " + str(key)
    cursor.execute(stock_name)
    stock_name = cursor.fetchall()
    for i in range(1):
        name = stock_name[i][0]
    roa_res = []
    for i in range(len(stock_name)):
        roa = sql[i][2]
        roa_res.append(roa)
    roe_res = []
    for i in range(len(stock_name)):
        roe = sql[i][1]
        roe_res.append(roe)
    season_res = []
    for i in range(len(stock_name)):
        season = sql[i][0]
        season_res.append(season)
    c = (
        Line(init_opts=opts.InitOpts(width="600px",height='300px'))
        # https://tw511.com/a/01/32805.html 設定版面大小
        .add_xaxis(season_res)
        .add_yaxis("ROA", roa_res, areastyle_opts=opts.AreaStyleOpts(opacity=0.3),color = "#00FF00",symbol_size=10)
        .add_yaxis("ROE", roe_res, areastyle_opts=opts.AreaStyleOpts(opacity=0.3),color = "#FFA500",symbol_size=10)
        # https://www.796t.com/article.php?id=411538 圓心設定
        .set_series_opts(label_opts = opts.LabelOpts(color="#000000",font_size="15"))
        .set_global_opts(title_opts=opts.TitleOpts(title=key+" "+name+"  報酬率與季收盤價比較圖"),
        xaxis_opts = opts.AxisOpts(name="Season"),
        yaxis_opts = opts.AxisOpts(name="ROE"),
        )
        )
    data_plot = c.render_embed()
    sql = "SELECT 季別,近四季ROE,近四季ROA FROM Stock WHERE 股票代碼 = " + str(key)
    cursor = conn.cursor()
    cursor.execute(sql)
    content_four = cursor.fetchall()
    field_name_four = [i[0] for i in cursor.description]
    cursor.execute(sql)
    sql = cursor.fetchall()
    roa_res_four = []
    for i in range(len(stock_name)):
        roa = sql[i][2]
        roa_res_four.append(roa)
    roe_res_four = []
    for i in range(len(stock_name)):
        roe = sql[i][1]
        roe_res_four.append(roe)
    season_res = []
    for i in range(len(stock_name)):
        season = sql[i][0]
        season_res.append(season)
    d = (
        Line(init_opts=opts.InitOpts(width="600px",height='300px'))
        # https://tw511.com/a/01/32805.html 設定版面大小
        .add_xaxis(season_res)
        .add_yaxis("ROA", roa_res_four, areastyle_opts=opts.AreaStyleOpts(opacity=0.3),color = "#00FF00",symbol_size=10)
        .add_yaxis("ROE", roe_res_four, areastyle_opts=opts.AreaStyleOpts(opacity=0.3),color = "#FFA500",symbol_size=10)
        # https://www.796t.com/article.php?id=411538 圓心設定
        .set_series_opts(label_opts = opts.LabelOpts(color="#000000",font_size="15"))
        .set_global_opts(title_opts=opts.TitleOpts(title=key+" "+name+"  報酬率與季收盤價比較圖"),
        xaxis_opts = opts.AxisOpts(name="Season"),
        yaxis_opts = opts.AxisOpts(name="ROE"),
        )
        )

    data_plot_d = d.render_embed()
    return render_template('search.html', labels=field_name,labels_four = field_name_four, content=content,
                                            stock = key,data_plot = data_plot,
                                            data_plot_d = data_plot_d,content_four = content_four)
if __name__ == "__main__":
    app.run()