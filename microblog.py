from ttb import app, db
from ttb.models import User, Post, Follow, Comment, Role, Permission
from flask_migrate import upgrade, Migrate


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Follow=Follow, Role=Role,
                Permission=Permission, Post=Post, Comment=Comment)



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

@app.cli.command()



def deploy():
    """Run deployment tasks."""
    # migrate database to latest revision
    upgrade()


    
