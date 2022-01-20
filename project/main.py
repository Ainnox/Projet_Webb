from flask import Blueprint, render_template, url_for, request, flash, redirect, session
from . import get_db_connection, get_perm, get_role
from werkzeug.exceptions import abort

main = Blueprint('main', __name__)


def get_post(id_post):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM Posts WHERE id_post = ?', (id_post,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post


@main.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Posts ORDER BY created DESC')
    posts = cur.fetchall()
    conn.close()

    return render_template('index.html', posts=posts)


@main.route('/', methods=('POST',))
def index_post():
    search = request.form['search']
    search = "%" + search + "%"
    co = get_db_connection()
    result = co.execute("SELECT * FROM Posts WHERE title_post LIKE ?", (search,)).fetchall()
    co.close()
    return render_template('index.html', posts=result)


@main.route('/<int:id_post>')
def post(id_post):
    post = get_post(id_post)
    co = get_db_connection()
    cur = co.cursor()
    cur.execute("SELECT * FROM liked WHERE email = ? AND id_post = ?", (session.get('email'), id_post))
    co.commit()
    result = cur.fetchall()
    co.close()

    if result:
        liked = 1
    else:
        liked = 0

    edit = get_perm("edit")

    return render_template('post.html', post=post, liked=liked, edit=edit)


@main.route('/create', methods=('GET', 'POST'))
def create():
    if not get_perm("create"):
        abort(401)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO Posts (title_post, content_post) VALUES (?, ?)',
                         (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('main.index'))
    return render_template('create.html')


@main.route('/<int:id_post>/edit', methods=('GET', 'POST'))
def edit(id_post):
    if not get_perm("edit"):
        abort(401)

    post = get_post(id_post)
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE Posts SET title_post = ?, content_post = ?'
                         ' WHERE id_post = ?',
                         (title, content, id))
            conn.commit()
            conn.close()
            return redirect(url_for('main.index'))

    return render_template('edit.html', post=post)


@main.route('/<int:id_post>/delete', methods=('POST',))
def delete(id_post):
    if not get_perm("delete"):
        abort(401)

    post = get_post(id_post)
    conn = get_db_connection()
    conn.execute('DELETE FROM Posts WHERE id_post = ?', (id_post,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['title_post']))
    return redirect(url_for('main.index'))


@main.route('/<int:id_post>/liked', methods=('POST', 'GET'))
def liked(id_post):
    co = get_db_connection()
    co.execute('INSERT INTO liked VALUES (?,?)', ((session.get('email')), id_post))
    co.commit()
    co.close()
    return redirect(url_for('main.post', id_post=id_post, liked=1))


@main.route('/<int:id_post>/unliked', methods=('POST', 'GET'))
def unliked(id_post):
    co = get_db_connection()
    co.execute('DELETE FROM liked WHERE email= ? AND id_post = ?', ((session.get('email')), id_post))
    co.commit()
    co.close()
    return redirect(url_for('main.post', id_post=id_post, liked=0))


@main.route('/users')
def users():
    if not get_role("admin"):
        abort(401)

    co = get_db_connection()
    users = co.execute("SELECT name,role_name FROM Users NATURAL JOIN Role ORDER BY role_name").fetchall()
    roles = co.execute("SELECT role_name FROM Role").fetchall()
    co.close()
    return render_template('users.html', users=users, roles=roles)


@main.route('/liked')
def posts_liked():
    co = get_db_connection()
    cur = co.cursor()
    cur.execute("SELECT * FROM liked NATURAL JOIN Posts WHERE email=?", (session.get('email'),))
    posts = cur.fetchall()
    co.close()

    return render_template('liked.html', posts=posts)
