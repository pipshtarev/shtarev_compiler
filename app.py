from flask import Flask, render_template, request, jsonify
import os
import subprocess


app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/compile", methods=["POST"])
def compile_code():
    data = request.json
    code = data.get("code", "")
    user_input = data.get("input", "")

    if not code:
        return jsonify({"output": "Error: Code editor is empty!"})

    # Get current directory
    current_dir = os.getcwd()
    temp_filename = os.path.join(current_dir, "temp_code.cpp")
    compiled_file = os.path.join(current_dir, "temp_executable")

    try:
        # Save the code to a temporary file
        with open(temp_filename, "w") as f:
            f.write(code)

        # Compile the code
        compile_command = ["g++", temp_filename, "-o", compiled_file]
        subprocess.run(compile_command, check=True, stderr=subprocess.PIPE)

        # Run the compiled executable with user input
        result = subprocess.run(
            [compiled_file], input=user_input, capture_output=True, text=True
        )
        output = result.stdout
    except subprocess.CalledProcessError as e:
        output = f"Compilation Error:\n{e.stderr.decode('utf-8')}"
    except Exception as e:
        output = f"Runtime Error:\n{str(e)}"
    finally:
        # Cleanup temporary files
        if os.path.exists(temp_filename):
            os.remove(temp_filename)
        if os.path.exists(compiled_file):
            os.remove(compiled_file)

    return jsonify({"output": output})

if __name__ == "__main__":
    print("Current working directory:", os.getcwd())
    app.run(debug=True)
