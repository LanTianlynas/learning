from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///handle_exceptions.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uniq = db.Column(db.String(50), unique=True)

    def __repr__(self):
        return f'<User: {self.uniq}>'


@app.route("/<string:uniqtxt>")
def index(uniqtxt):
    # exist = User.query.filter_by(uniq=uniqtxt).first()
    # if exist:
    #     return f'{uniqtxt} already exists!'
    try:
        user = User(uniq=uniqtxt)
        db.session.add(user)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()  # 回滚, 避免出现异常前代码中还有其他的数据库操作。
        return f'{uniqtxt} already exists!'  # 重复的数据, 返回提示信息
    return f'{uniqtxt} added!' # 没有重复的数据, 返回提示信息


if __name__ == '__main__':
    app.run(debug=True)  # 开启调试模式
