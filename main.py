from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blog-post:AcuraRSX1@localhost:8889/blog-post'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):
   
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(5000))
    

    def __init__(self, title, body):
        
        self.title = title
        self.body = body


@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    
    if request.method == 'POST':
        blog_title = request.form['blogtitle']
        blog_body = request.form['blogbody']
        if blog_title == "" and blog_body == "":
            title_error = 'Your blog needs a title home boy!'
            body_error = 'Your blog needs a body bruh!'
            return render_template('newpost.html', title_error=title_error, body_error=body_error)
        elif blog_title == "":
            title_error = 'Your blog needs a title silly!'
            return render_template('newpost.html', title_error=title_error)
        elif blog_body == "":
            body_error = 'Your blog needs a body bruh!'
            return render_template('newpost.html', body_error=body_error)      
        else:
            new_blog = Blog(blog_title, blog_body)
            db.session.add(new_blog)
            db.session.commit()
            newID = new_blog.id
            redirect_str = "?"+ "id=" + str(newID)

        return redirect('/blog' + redirect_str)
        
                
    return render_template('newpost.html')

      
@app.route('/blog', methods=['POST', 'GET'])
def blog():
    if request.args:
        blog_id = request.args.get('id')
        blog = Blog.query.get(blog_id)
        return render_template('singleblog.html', blog=blog)
    else:   
        
        blog = Blog.query.all()
        return render_template('blog.html', blogs=blog)

    
@app.route('/', methods=['POST', 'GET'])
def index():
    
    return redirect('/blog')


if __name__ == '__main__':
    app.run()