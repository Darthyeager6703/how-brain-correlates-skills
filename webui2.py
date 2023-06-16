from flask import Flask, render_template, request
import including_accessing_nodes as codefile


app = Flask(__name__)

@app.route('/')
def index():
    css_file = 'static/cyberpunk.css'  # Path to your CSS file
    return render_template('index.html', css_file=css_file)


# @app.route('/print_message1')
# def print_message1():
#     message = "Hello World"
#     return render_template('index.html', message=message)


# @app.route('/print_message2')
# def print_message2():
#     message = "Message from 2nd function"
#     return render_template('index.html', message=message)

@app.route('/print_graph')
def print_graph():
    codefile.graph.print_graph()
    message= "See the next page for graph"
    return render_template("index.html",message=message)

@app.route('/read_input', methods = ['GET','POST'])
def read_input():
    if request.method == 'POST':
        message = "Vertex added.... I guess"
        vertex = request.form.get('vertex')
        tag = request.form.get('tag')
        codefile.graph.add_vertex(vertex, tag= tag)
        return render_template("index.html", message = message)
    
@app.route('/read_input_page')
def redirect():
    return render_template("learn-something.html")

@app.route('/search_input', methods = ['GET','POST'])
def search_input():
    if request.method == 'POST':
        search_vertex = request.form.get("search_vertex")
        result =codefile.graph.access_vertex_by_name(search_vertex)

        if result:
            message = "The Core Memory is present"
        else:
            message = "The core Memory Doesn't exist. Please learn it"
    
    return render_template("index.html",message=message)

@app.route('/search')
def searchfile():
    message = "search page accessed"
    return render_template("search.html", message=message)

@app.route('/a-star')
def star():
    message = "A * algorithm under use"
    return render_template("tracer.html",message=message)

@app.route('/tracer_input', methods = ['GET','POST'])
def tracer_input():
    if request.method == 'POST':
        trace_vertex = request.form.get("trace_vertex")
        message =codefile.graph.a_star("Brain", trace_vertex)

        return render_template("index.html",message=message)

if __name__ == '__main__':
    app.run()
