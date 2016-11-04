# -*- coding: utf-8 -*-

from . import app, db
from flask import render_template, request, redirect, url_for, flash
from forms import LoginForm, RegisterForm, CommodityForm
from models import User, Commodity
from flask_login import current_user, login_user, logout_user, login_required
import os
from datetime import datetime

typename = ['最新发布', '图书教材', '运动棋牌', '电子数码', '代步工具', '美状衣物', '电器日用', '票券小物']
loc_name = ['交易地点', '全校', '南校区', '大学城', '珠海校区', '北校区']


@app.route('/')
def index():
    commoditys = Commodity.query.order_by(Commodity.timestamp.desc())
    return render_template('index.html', commoditys=commoditys)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(phonenum=form.phonenum.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            flash(u'登录成功！')
            return redirect(url_for('index'))
        flash(u'错误的手机号或密码')
    #print form.errors
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash(u'您已经退出登录。')
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User.query.filter_by(phonenum=form.phonenum.data).first()
        if user is not None:
            flash(u'该手机号已经使用')
            return render_template('login.html', form=form, isRegister=True)
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None:
            flash(u'该昵称已经注册，请重新输入')
            return render_template('login.html', form=form, isRegister=True)

        newuser = User(username=form.username.data, phonenum=form.phonenum.data, password=form.password.data)
        db.session.add(newuser)
        db.session.commit()
        flash(u'注册成功!')
        login_user(newuser)
        return redirect(url_for('index'))
    return render_template('login.html', form=form, isRegister=True)


@app.route('/post', methods=['GET', 'POST'])
@login_required
def post():
    form = CommodityForm()
    
    if form.validate_on_submit():
        file = request.files['file']
        if file:
            newName = str(current_user.id) + '_' + datetime.now().strftime('%Y_%m_%d_%H_%M_%S') + '.' + file.filename.split('.')[-1]
            file.save(os.path.join(app.static_folder, 'upload', newName))
            newCommodity = Commodity(name=form.name.data,
                                    description=form.description.data,
                                    price=form.price.data,
                                    discount=form.discount.data,
                                    location=form.location.data,
                                    type=form.type.data,
                                    wechatnum=form.wechatnum.data,
                                    qqnum=form.qqnum.data,
                                    image=url_for('static', filename='%s/%s' % ('upload', newName)),
                                    author=current_user._get_current_object()
                                    )
            db.session.add(newCommodity)
            db.session.commit()
            flash(u'发布成功!')
            return redirect(url_for('item', id=newCommodity.id))
        else:
            flash(u'似乎没有选择图片上传哦')
    return render_template('post.html', form=form)


@app.route('/modify/<int:id>', methods=['GET', 'POST'])
@login_required
def modify(id):
    commodity = Commodity.query.get_or_404(id)
    if current_user != commodity.author:
        abort(403)
    form = CommodityForm(obj=commodity)
    if form.validate_on_submit():
        commodity.name = form.name.data
        commodity.description = form.description.data
        commodity.price = form.price.data
        commodity.discount = form.discount.data
        commodity.location = form.location.data
        commodity.type = form.type.data
        commodity.wechatnum = form.wechatnum.data
        commodity.qqnum = form.qqnum.data
        db.session.add(commodity)
        db.session.commit()
        flash(u'修改成功!')
        return redirect(url_for('item', id=commodity.id))
    return render_template('post.html', form=form, action="modify")


@app.route('/item/<int:id>')
def item(id):
    item = Commodity.query.get_or_404(id)
    return render_template('detail.html', item=item)


@app.route('/user')
@login_required
def user():
    #user = User.query.filter_by(username=username).first_or_404()
    commodity = current_user.commodity.order_by(Commodity.timestamp.desc()).all()
    return render_template('user.html', commodity=commodity)
