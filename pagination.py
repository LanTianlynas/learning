from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///paginate.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Thread(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))

@app.route('/threads/<int:page_num>')
def threads(page_num):
    threads = Thread.query.paginate(per_page=5, page=page_num, error_out=True)
    return render_template('pagination_learning.html', threads=threads)


if __name__ == '__main__':
    app.run(debug=True)  # 开启调试模式
