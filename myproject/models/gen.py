#pip install nbconvert
from nbconvert import PythonExporter
import nbformat
from IPython.display import display

notebook_path = 'myproject//models//final_prompts.ipynb'
with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = nbformat.read(f, as_version=4)

py_exporter = PythonExporter()
py_script, _ = py_exporter.from_notebook_node(nb)
exec(py_script)
query=input('input user query: ')
result = query_result(query)
print(result)