document.addEventListener("DOMContentLoaded", () => {
    const codeEditor = CodeMirror.fromTextArea(document.getElementById("code-editor"), {
        mode: "text/x-c++src",
        lineNumbers: true,
        theme: "default",
    });

    // Добавляем стартовый код
    const defaultCode = `#include <iostream>
using namespace std;

int main() {
    string input;
    cin >> input;
    cout << "You entered: " << input << endl;
    return 0;
}`;
    codeEditor.setValue(defaultCode);

    document.getElementById("run-button").addEventListener("click", async () => {
        const code = codeEditor.getValue();
        const input = document.getElementById("program-input").value;

        const response = await fetch("/compile", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ code, input }),
        });

        const result = await response.json();
        document.getElementById("program-output").value = result.output;
    });

    document.getElementById("reset-button").addEventListener("click", () => {
        codeEditor.setValue(defaultCode);
        document.getElementById("program-input").value = "";
        document.getElementById("program-output").value = "";
    });
});
