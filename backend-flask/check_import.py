import importlib.util
import traceback

spec = importlib.util.spec_from_file_location('app', 'app.py')
app = importlib.util.module_from_spec(spec)
try:
    spec.loader.exec_module(app)
    print('IMPORT_OK')
except Exception:
    print('IMPORT_ERROR')
    traceback.print_exc()
