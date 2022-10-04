from flask import (
    Flask,
    render_template,
    redirect,
    flash,
    url_for,
    request
)

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import (
    IntegrityError,
    DataError,
    DatabaseError,
    InterfaceError,
    InvalidRequestError
)
from datetime import datetime




app = Flask (__name__)
app.secret_key = 'secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
 
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()            
            flash(f"Salvo com sucesso!", "success")
            return redirect(url_for("index"))

        except InvalidRequestError:
            db.session.rollback()
            flash(f"Algo deu errado!", "danger")
        except IntegrityError:
            db.session.rollback()
            flash(f"O registro já existe!.", "warning")
        except DataError:
            db.session.rollback()
            flash(f"Entrada inválida", "warning")
        except InterfaceError:
            db.session.rollback()
            flash(f"Erro ao conectar ao banco de dados", "danger")
        except DatabaseError:
            db.session.rollback()
            flash(f"Erro ao conectar ao banco de dados", "danger")
            
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)
   
           

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        flash(f"Excluído com sucesso!", "success")
        return redirect(url_for("index"))
        
    except InvalidRequestError:
        db.session.rollback()
        flash(f"Algo deu errado!", "danger")
    except IntegrityError:
        db.session.rollback()
        flash(f"O registro já existe!.", "warning")
    except DataError:
        db.session.rollback()
        flash(f"Entrada inválida", "warning")
    except InterfaceError:
        db.session.rollback()
        flash(f"Erro ao conectar ao banco de dados", "danger")
    except DatabaseError:
        db.session.rollback()
        flash(f"Erro ao conectar ao banco de dados", "danger")

    
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    now = datetime.now()

    if request.method == 'POST':
        task.content = request.form['content']
        
        try:
            db.session.commit()
            flash(f"Atualizado com sucesso!", "success")
            return redirect(url_for("index"))

        except InvalidRequestError:
            db.session.rollback()
            flash(f"Algo deu errado!", "danger")
        except IntegrityError:
            db.session.rollback()
            flash(f"O registro já existe!.", "warning")
        except DataError:
            db.session.rollback()
            flash(f"Entrada inválida", "warning")
        except InterfaceError:
            db.session.rollback()
            flash(f"Erro ao conectar ao banco de dados", "danger")
        except DatabaseError:
            db.session.rollback()
            flash(f"Erro ao conectar ao banco de dados", "danger")
        
    else:
        return render_template('update.html', task=task, datetime = str(now.strftime("%d/%m/%Y %H:%M:%S")))


if __name__ == '__main__':
    app.run(debug=True)