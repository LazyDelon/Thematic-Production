import sqlite3
from turtle import pen

from flask import flash
from flask import request
from flask import url_for
from flask import redirect
from flask import render_template

from Stock_Widget.forms import LoginForm
from Stock_Widget.forms import RegistrationForm

from Stock_Widget import db
from Stock_Widget import app
from Stock_Widget import bcrypt

from flask_login import login_user
from flask_login import logout_user
from flask_login import current_user
from flask_login import login_required

from pyecharts.charts import Line
from pyecharts import options as opts

import numpy as np
from cmath import nan
from Stock_Widget.models import User, Post


@app.route("/")
@app.route("/home", methods=['GET', 'POST'])
def home():
    if request.method == "GET":
        languages = []

        with open('stock_number.csv', encoding="utf-8") as f: 
            slist = f.readlines() 

            for lst in slist: 
                s = lst.replace("\u3000", ",")
                s = s.split(',')

                languages.append("{}".format(s[0].strip()))
                
                # languages.append("{} {} {}".format(s[0].strip(), s[1].strip(), s[2].strip()))

        keyword = request.args.get('ID')
        
        print(keyword)
        try:
            conn = sqlite3.connect('Stock.db')
            sql = "SELECT 股票代碼, 股票名稱, 類股, 季別, ROE, ROA FROM Stock WHERE 股票代碼=" + str(keyword) + " ORDER BY 季別 DESC"
            cursor = conn.cursor()
            cursor.execute(sql)
            content = cursor.fetchall()
            field_name = [i[0] for i in cursor.description]
            content_none = []
            content_data = []
            count = 0
            judge = 0
            for i in content:
                for j in i:
                    if j == None:
                        content_none.append(count)
                        pass
                count=count+1
            for i in content:
                if judge in content_none:
                    break
                else:
                    for j in i :
                        content_data.append(i)
                        break
                judge = judge +1
            content = content_data
            cursor.execute(sql)
            sql = cursor.fetchall()

            # 計算SQL
            # conn = sqlite3.connect('Stock.db')
            # sql = "SELECT 股票代碼, 股票名稱, 類股, 季別, ROE, ROA FROM Stock WHERE 股票代碼=" + str(keyword) + " ORDER BY 季別 DESC"
            # cursor = conn.cursor()
            # cursor.execute(sql)
            # content = cursor.fetchall()
            # field_name = [i[0] for i in cursor.description]

            # cursor.execute(sql)
            # sql = cursor.fetchall()
            
            stock_name = "SELECT 股票名稱 FROM Stock WHERE 股票代碼 = " + str(keyword)
            cursor.execute(stock_name)
            stock_name = cursor.fetchall()
            for i in range(1):
                name = stock_name[i][0]
            none_data = []
            roa_res = []
            for i in range(len(stock_name)):
                roa = sql[i][5]
                if roa == None:
                    none_data.append(i)
                    break
                else:
                    roa_res.append(roa)

            roa_res = list(reversed(roa_res))

            roe_res = []
            for i in range(len(stock_name)):
                roe = sql[i][4]
                if roe == None:
                    break
                else:
                    roe_res.append(roe)

            roe_res = list(reversed(roe_res))
                
            season_res = []
            for i in range(len(stock_name)):
                if i in none_data:
                    break
                else:
                    season = sql[i][3]
                    season_res.append(season)

            season_res = list(reversed(season_res))
                
            c = (
                Line(init_opts=opts.InitOpts(width="800px",height='300px'))
                # https://tw511.com/a/01/32805.html 設定版面大小
                .add_xaxis(season_res)
                .add_yaxis("ROA", roa_res, areastyle_opts=opts.AreaStyleOpts(opacity=0.3),color = "#FFA500",symbol_size=10)
                .add_yaxis("ROE", roe_res, areastyle_opts=opts.AreaStyleOpts(opacity=0.3),color = "#00FF00",symbol_size=10)
                # https://www.796t.com/article.php?id=411538 圓心設定
                .set_series_opts(label_opts = opts.LabelOpts(color="#000000",font_size="15"))
                .set_global_opts(title_opts=opts.TitleOpts(title=keyword+" "+name+"  報酬率與季收盤價比較圖"),
                xaxis_opts = opts.AxisOpts(name="Season"),
                yaxis_opts = opts.AxisOpts(name="ROE、ROA"),#https://tw511.com/a/01/32805.html
                )
                )
            data_plot = c.render_embed()

            ####################################################
            
            conn = sqlite3.connect('Stock.db')
            sql2 = "SELECT 股票代碼, 股票名稱, 類股, 季別, 近四季ROE, 近四季ROA FROM Stock WHERE 股票代碼=" + str(keyword) + " ORDER BY 季別 DESC"
            cursor = conn.cursor()
            cursor.execute(sql2)
            content2 = cursor.fetchall()
            field_name2 = [i[0] for i in cursor.description]

            cursor.execute(sql2)
            sql2 = cursor.fetchall()

            content_none = [] #存放空值欄位數字
            content_data = [] #存放不為空值的資料
            count = 0
            judge = 0
            for i in content2: #使用for迴圈將資料一筆一筆列出
                for j in i: #使用for迴圈列出每一個資料
                    if j == None: #if資料為空
                        content_none.append(count) #儲存當前資料的位置
                        break
                count=count+1
            for i in content2:
                if judge in content_none: #如果judge在content_none陣列中
                    pass
                else:
                    for j in i :
                        content_data.append(i)
                        break
                judge = judge +1
            content2 = content_data

            none_data = []
            roa_res_four = []
            for i in range(len(stock_name)):
                roa = sql2[i][5]
                if roa == None:
                    none_data.append(i)
                    break
                else:
                    roa_res_four.append(roa)

            roa_res_four = list(reversed(roa_res_four))

            roe_res_four = []
            for i in range(len(stock_name)):
                roe = sql2[i][4]
                if roe == None:
                    break
                else:
                    roe_res_four.append(roe)

            roe_res_four = list(reversed(roe_res_four))

            season_res = []
            for i in range(len(stock_name)):
                if i in none_data:
                    break
                else:
                    season = sql2[i][3]
                    season_res.append(season)

            season_res = list(reversed(season_res))            

            d = (
                Line(init_opts=opts.InitOpts(width="800px",height='300px'))
                # https://tw511.com/a/01/32805.html 設定版面大小
                .add_xaxis(season_res)
                .add_yaxis("ROA", roa_res_four, areastyle_opts=opts.AreaStyleOpts(opacity=0.3),color = "#FFA500",symbol_size=10)
                .add_yaxis("ROE", roe_res_four, areastyle_opts=opts.AreaStyleOpts(opacity=0.3),color = "#00FF00",symbol_size=10)
                # https://www.796t.com/article.php?id=411538 圓心設定
                .set_series_opts(label_opts = opts.LabelOpts(color="#000000",font_size="15"))
                .set_global_opts(title_opts=opts.TitleOpts(title=keyword+" "+name+"  報酬率與季收盤價比較圖"),
                xaxis_opts = opts.AxisOpts(name="Season"),
                yaxis_opts = opts.AxisOpts(name="ROE、ROA"),
                )
            )

            data_plot_d = d.render_embed()

            ####################################################

            conn = sqlite3.connect('Stock.db')
            sql3 = "SELECT 股票代碼, 股票名稱, 季別, 年度, 年度ROE, 年度ROA FROM Stock WHERE 股票代碼=" + str(keyword) + " ORDER BY 季別 DESC"
            cursor = conn.cursor()
            cursor.execute(sql3)
            content3 = cursor.fetchall()
            field_name3 = [i[0] for i in cursor.description]

            cursor.execute(sql3)
            sql3 = cursor.fetchall()
            content_none = []
            content_data = []
            count = 0
            judge = 0
            for i in content3:
                for j in i:
                    if j == None:
                        content_none.append(count)
                        break
                count=count+1
            for i in content3:
                if judge in content_none:
                    pass
                else:
                    for j in i :
                        content_data.append(i)
                        break
                judge = judge +1
            content3 = content_data


            none_data = []
            roa_res_year = []

            for i in range(len(stock_name)):
                roa = sql3[i][5]
                if roa == None:
                    none_data.append(i)
                else:
                    roa_res_year.append(roa)

            roa_res_year = list(reversed(roa_res_year)) 

            roe_res_year = []
            for i in range(len(stock_name)):
                roe = sql3[i][4]
                if roe == None:
                    none_data.append(i)
                else:
                    roe_res_year.append(roe)
            
            roe_res_year = list(reversed(roe_res_year))    

            season_res = []
            for i in range(len(stock_name)):
                if i in none_data:
                    pass
                else:
                    season = sql3[i][3]
                    season_res.append(str(season))
            
            season_res = list(reversed(season_res))   

            y = (
                Line(init_opts=opts.InitOpts(width="800px",height='300px'))
                # https://tw511.com/a/01/32805.html 設定版面大小
                .add_xaxis(season_res)
                .add_yaxis("ROA", roa_res_year, areastyle_opts=opts.AreaStyleOpts(opacity=0.3),color = "#FFA500",symbol_size=10)
                .add_yaxis("ROE", roe_res_year, areastyle_opts=opts.AreaStyleOpts(opacity=0.3),color = "#00FF00",symbol_size=10)
                # https://www.796t.com/article.php?id=411538 圓心設定
                .set_series_opts(label_opts = opts.LabelOpts(color="#000000",font_size="15"))
                .set_global_opts(title_opts = opts.TitleOpts(title=keyword+" "+name+"  報酬率與季收盤價比較圖"),
                xaxis_opts = opts.AxisOpts(name="Season"),
                yaxis_opts = opts.AxisOpts(name="ROE、ROA"),
                )
            )
            data_plot_y = y.render_embed()

            
            # return render_template('home.html', languages=languages, labels=field_name, content=content)
            return render_template('home.html',languages=languages, labels3 = field_name3, content3 = content3, labels2 = field_name2, content2 = content2, labels=field_name, content=content, stock = keyword, data_plot = data_plot, data_plot_d = data_plot_d, roe_res_four = roe_res_four, data_plot_y=data_plot_y)
        except:
            return render_template('home.html', languages=languages)


@app.route("/calculate", methods=['GET','POST'])
def calculate():
    if request.method == "GET":
        languages = []

        with open('stock_number.csv', encoding="utf-8") as f: 
            slist = f.readlines() 

            for lst in slist: 
                s = lst.replace("\u3000", ",")
                s = s.split(',')

                languages.append("{}".format(s[2].strip()))

        ID = request.args.get('ID')
        
        print(ID)

        conn = sqlite3.connect('Stock.db')
        cur = conn.cursor()

        if ID == None:
            sql = "SELECT 類股, 股票代碼, 股票名稱, ROE, ROA FROM Stock WHERE 季別 = '2021Q3' ORDER BY ROE DESC"
            cur.execute(sql)
            content = cur.fetchall()
            field_name = [i[0] for i in cur.description]

        else:
            sql = "SELECT 類股, 股票代碼, 股票名稱, ROE, ROA FROM Stock WHERE 季別 = '2021Q3' AND 類股='{}' ORDER BY ROE DESC".format(ID)
            cur.execute(sql)
            content = cur.fetchall()
            field_name = [i[0] for i in cur.description]

        if ID == None:
            sql = "SELECT 季別, 類股, 股票代碼, 股票名稱, 近四季ROE FROM Stock"
            cur.execute(sql)
            content1 = cur.fetchall()
            field_name1 = [i[0] for i in cur.description]
        
        else:
            sql = "SELECT 季別, 類股, 股票代碼, 股票名稱, 近四季ROE FROM Stock WHERE 類股='{}'".format(ID)
            cur.execute(sql)
            content1 = cur.fetchall()
            field_name1 = [i[0] for i in cur.description]

        return render_template('calculate.html', content=content, labels=field_name, content1=content1, labels1=field_name1, languages=languages)

    return render_template('home.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect( url_for('home') )

    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! You are now able to log in', 'success')
        return redirect( url_for('login') )
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect( url_for('home') )

    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember = form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect( url_for('home') )
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user() 
    return redirect( url_for('home') )

    
@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')


