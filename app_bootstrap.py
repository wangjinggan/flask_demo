from flask import Flask,render_template,redirect,url_for,request,flash,Markup
from flask_wtf import CSRFProtect
from forms import *
from flask_bootstrap import Bootstrap4

#数据库
from flask_sqlalchemy import SQLAlchemy
import config

app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)
#使用bootstrap4
bootstrap = Bootstrap4(app)
csrf = CSRFProtect(app)
app.secret_key = 'secret'

class Astock(db.Model):
    __tablename__ = 'enterprise_baseinfo'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    e_name = db.Column(db.String(64))
    econ_kind = db.Column(db.String(64))
    oper_name = db.Column(db.String(64))
    e_status = db.Column(db.String(64))
    baseInfo = db.relationship("Basicinfo", back_populates="name")
#

class Basicinfo(db.Model):
    __tablename__ = "basicinfo"
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    scope = db.Column(db.String(2000))
    company_id = db.Column(db.Integer,db.ForeignKey("enterprise_baseinfo.id"), FOREIGN_KEY=True,autoincrement=True)
    name = db.relationship("Astock", back_populates="baseInfo")

@app.route('/')
def hello():
    return 'Hello 2020'

@app.route('/table', methods=['GET', 'POST'])
def test_table():
    company = Astock.query
    if request.method == 'GET':
        s = SearchForm()
    else:
        s = SearchForm(request.form)
        name = s.name.data
        if name != '':
            company = company.filter(Astock.e_name.like(f'%{name}%'))
    page = request.args.get('page', 1, type=int)
    pagination = company.paginate(page=page, per_page=30)
    messages = pagination.items
    titles = [('id','#'),('e_name', '公司名称'),('econ_kind', '企业类型'),('oper_name', '法定代表人'),('e_status', '状态')]
    return render_template('index.html', pagination=pagination, messages=messages, titles=titles, Astock=Astock,search=s)


@app.route('/table/<int:message_id>/view')
def view_message(message_id):
    message = Basicinfo.query.get(message_id)
    print(message)
    if message:
        titles = [('id', '#'), ('scope', '经营范围')]
        return render_template('company.html',messages=[message],titles=titles,Basicinfo=Basicinfo)
    return f'Could not view message {message_id} as it does not exist. Return to <a href="/table">table</a>.'
@app.route('/china')
def test_china():
    return render_template('china.html')
@app.route('/echarts')
def test_echarts():
    return render_template('echarts.html')
if __name__ == '__main__':
    app.run()
