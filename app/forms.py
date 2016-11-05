# -*- coding: utf-8 -*-

from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, TextAreaField, SelectField
from wtforms.validators import InputRequired, Required, Length
from models import Commodity

class LoginForm(Form):
    phonenum = StringField(u'手机号', validators=[Required(), Length(10, 12, message=u'无效的手机号')])
    password = PasswordField(u'密码', validators=[Required()])
    submit = SubmitField(u'登录')

class RegisterForm(Form):
    username = StringField(u'昵称', validators=[Required()])
    phonenum = StringField(u'手机号', validators=[Required(), Length(10, 12, message=u'无效的手机号')])
    password = PasswordField(u'密码', validators=[Required()])
    submit = SubmitField(u'登录')


class CommodityForm(Form):
    name = StringField(u'商品名', validators=[Required()])
    description = TextAreaField(u'商品描述', validators=[Required()])
    price = IntegerField(u'价格')

    discount = IntegerField(u'可否讲价')
    location = StringField(u'交易地点')
    type = StringField(u'商品类型')

    qqnum = StringField(u'QQ号')
    wechatnum = StringField(u'微信号')
    #image = StringField(u'图片url')


class CommentForm(Form):
    body = StringField(u'添加你的评论', validators=[Required()])
    submit = SubmitField('Submit')