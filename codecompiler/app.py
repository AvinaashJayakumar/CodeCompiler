from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    code = ""
    input_data = ""
    result = ""
    error = ""
    lang = request.form.get("lang")

    if request.method == "POST":
        code = request.form.get("code")
        input_data = request.form.get("input_data")

        try:
            if lang == "python":
                result = execute_python(code, input_data)
            elif lang == "php":
                result = execute_php(code, input_data)
            elif lang == "c":
                result = execute_c(code, input_data)
            else:
                error = "Invalid language selected"
        except Exception as e:
            error = str(e)

    return render_template("index.html", code=code, input_data=input_data, result=result, error=error)

def execute_python(code, input_data):
    p = subprocess.Popen(["python", "-c", code], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, text=True)
    out, err = p.communicate(input=input_data)
    return out + err

def execute_php(code, input_data):
    p = subprocess.Popen(["php", "-r", code], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, text=True)
    out, err = p.communicate(input=input_data)
    return out + err

def execute_c(code, input_data):
    p = subprocess.Popen(["gcc", "-x", "c", "-o", "-", "-"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, text=True)
    out, err = p.communicate(input=code)
    if p.returncode == 0:
        p = subprocess.Popen(["./a.out"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, text=True)
        out, err = p.communicate(input=input_data)
    return out + err

if __name__ == "__main__":
    app.run(debug=True)
