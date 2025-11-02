// Proxy server to run Flask backend alongside Vite frontend
const { spawn } = require('child_process');
const path = require('path');

console.log('Starting RJMS application...');

// Start Flask backend
const backend = spawn('python', ['run.py'], {
  cwd: path.join(__dirname, 'backend'),
  stdio: 'inherit'
});

backend.on('error', (error) => {
  console.error('Failed to start backend:', error);
});

backend.on('close', (code) => {
  console.log(`Backend process exited with code ${code}`);
});

// Start Vite dev server
const { spawn: spawnVite } = require('child_process');
const vite = spawnVite('npx', ['vite', '--port', '5173', '--host', '0.0.0.0'], {
  cwd: __dirname,
  stdio: 'inherit'
});

vite.on('error', (error) => {
  console.error('Failed to start Vite:', error);
});

vite.on('close', (code) => {
  console.log(`Vite process exited with code ${code}`);
  backend.kill();
});

// Handle shutdown
process.on('SIGINT', () => {
  console.log('\nShutting down...');
  backend.kill();
  vite.kill();
  process.exit();
});
