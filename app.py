from flask import render_template
from flask import Flask
from flask import request
from flask import jsonify
from flask import redirect
    
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,  TextAreaField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config['SECRET_KEY'] = ';lindakdhndsjdvahwnvajvakmjcah8&@*uyw7qwhds89(Y@E('
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://wbjehjlqokdpbs:e65fb3c157275422ac58cb40ae4ddc2feb886b9eb898f02577610f140ba540c5@ec2-3-223-242-224.compute-1.amazonaws.com:5432/dd5knvj2vq5jr'
# app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///books.db'
db = SQLAlchemy(app)

class bookCreateForm(FlaskForm):
        book_title = StringField('اسم الكتاب', [DataRequired("Please enter title.")] )
        author = StringField('اسم المؤلف ', [DataRequired("Please enter title.")] )
        country = StringField('البلد', [DataRequired("Please enter title.")] )
        book_link = TextAreaField('رابط الكتاب')
        author_link = TextAreaField('رابط المؤلف')
        country_link = TextAreaField('رابط البلد')
        submit = SubmitField()

# read data form 
class bookForm(FlaskForm): 
    book_title= StringField('اسم الكتاب', [DataRequired("Please enter title.")] )
    submit = SubmitField('Delet book')

class books(db.Model):
    book_id =  db.Column(db.Integer, primary_key=True)
    book_title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(150), nullable=False)
    country = db.Column(db.String(70), nullable=False)
    book_link =  db.Column(db.Text(), default=None, nullable=True)
    author_link =  db.Column(db.Text(),default=None,  nullable=True)
    country_link =  db.Column(db.Text(),default=None,  nullable=True)
    def __repr__(self) -> str:
        return '<name %r>' %self.book_id
    def __str__(self) -> str:
        return f"""
        id: {self.book_id},
        title: {self.book_title},
        author: {self.author},
        country: {self.country},
        ____-------------_____------------____--
        """


def existed(book_title): 
    id = books.query.filter_by(book_title=book_title).first()
    # print(id)
    if id is None:  
        return False
    return True

@app.route('/')
def index(message=None): 
    return render_template('home.html', message=message)


@app.route('/readData', methods=['GET'])
def getData():
    data = books.query.order_by(books.book_id)
    print(data.count())
    context = {
        'data':data,
        'Text':'all available Books in the stock',
    }
    return render_template('readData.html' , context=context ) 
       
@app.route('/createData/', methods=['GET','POST'])
def createData(): 
    form = bookCreateForm()
    # data = pd.read_csv('tableData.csv')
    # id = data['الترتيب'].iloc[-1] +1 
    # book=[id] 
    
    if request.method == 'POST':
        book = books(

            book_title=form.data.get('book_title'),
            book_link=form.data.get('book_link'),
            author=form.data.get('author'),
            author_link=form.data.get('author_link'),
            country=form.data.get('country'),
            country_link=form.data.get('country_link')
        )
    
        message ={}
        
        if not existed(book.book_title):
            db.session.add(book)
            db.session.commit()

            message['message'] = f' {book.book_title} has been added'
            return  index(message=message)
        
        message['message'] = 'this book is existed in the data'
        
        return  index(message=message)


    return render_template('createData.html', form=form)

@app.route('/updateData/', methods=['GET','POST', 'PUT'])
def updateData(): 
    form = bookCreateForm()
    book = books()
    message ={}        
    
    if request.method ==  'POST' or request.method ==  'PUT':
        title= str(form.data.get('book_title'))
        if existed(title):
            try:

                db.session.query(books).filter(
                books.book_title == title).update(dict(
                book_title   = title,
                book_link    = form.data.get('book_link'),
                author       = form.data.get('author'),
                author_link  = form.data.get('author_link'),
                country      = form.data.get('country'),
                country_link = form.data.get('country_link')
            ))               
                db.session.commit()                
                message['message'] = f' {book.book_title} has been updated'

            except: 
                message['message'] = f' an error occurred with {title} '
            
            return  index(message=message)
        else: 
            message['message'] = f' this book is not in the store {title} '
            return  index(message=message)
    
    return render_template('updateData.html', form=form)

    
@app.route('/deleteData', methods=['GET','DELETE','POST'])
def deleteData():

    form = bookForm()
    message ={}
    if form.validate_on_submit(): 
        book_title = form.book_title.data
        form.book_title.data= ''
        book = books.query.filter_by(book_title=book_title).first()
        if request.method == 'POST' or request.method == 'DELETE':
            try: 
                db.session.delete(book)
                db.session.commit()            
                message['message'] = f' {book_title} has been deleted'
            except: 
                message['message'] = f' {book_title} has not been deleted :( :( '
            return  index(message=message)

    return render_template('deleteData.html', form=form)


@app.errorhandler(404)
def page_not_fount(e): 
    return render_template('404.html'),404
@app.errorhandler(500)
def page_not_fount(e): 
    return render_template('500.html'),500


if __name__=="__main__":
    app.run(debug=True)


