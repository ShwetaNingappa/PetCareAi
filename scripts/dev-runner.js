const { spawn } = require('child_process');
const path = require('path');

function findPython() {
  const venvPython = path.join(__dirname, '..', 'backend-flask', '.venv', 'Scripts', 'python.exe');
  try {
    require('fs').accessSync(venvPython);
    return venvPython;
  } catch (e) {
    return 'python';
  }
}

const python = findPython();
const concurrently = require('concurrently');

// Build a concurrently command that runs three processes:
// 1) Tailwind watch to rebuild CSS on changes
// 2) Frontend dev server (npm start in frontend-react)
// 3) Backend Flask app using the selected python executable
// Use the frontend npm script for tailwind watch so that local node_modules binaries are used.
const cmd = `npx concurrently "npm run tw:watch --prefix frontend-react" "npm start --prefix frontend-react" "${python} backend-flask/app.py"`;
// Run the whole command string in a shell to preserve quoting and ensure npx
// and concurrently receive the intended arguments.
const child = spawn(cmd, { stdio: 'inherit', shell: true });

child.on('close', (code) => {
  process.exit(code);
});
