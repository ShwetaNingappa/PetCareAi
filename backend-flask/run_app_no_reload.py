import importlib.util, traceback
spec = importlib.util.spec_from_file_location('app', 'app.py')
appm = importlib.util.module_from_spec(spec)
try:
    spec.loader.exec_module(appm)
    print('IMPORT_OK')
    appm.app.run(host='127.0.0.1', port=5000, debug=True, use_reloader=False)
except Exception:
    traceback.print_exc()
