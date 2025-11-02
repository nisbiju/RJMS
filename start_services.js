#!/usr/bin/env node

const { spawn } = require('child_process');
const path = require('path');

console.log('\n==============================================');
console.log('Starting RJMS Application');
console.log('==============================================\n');

// Start Flask backend
console.log('▶ Starting Flask backend (port 5000)...');
const backend = spawn('python', ['run.py'], {
  cwd: path.join(__dirname, 'backend'),
  stdio: ['ignore', 'pipe', 'pipe']
});

backend.stdout.on('data', (data) => {
  console.log(`[Backend] ${data.toString().trim()}`);
});

backend.stderr.on('data', (data) => {
  console.log(`[Backend] ${data.toString().trim()}`);
});

backend.on('error', (error) => {
  console.error('Failed to start backend:', error);
  process.exit(1);
});

// Wait for backend to start
setTimeout(() => {
  console.log('✓ Backend started\n');
  console.log('▶ Starting Vue.js frontend (port 5173)...');
  
  // Start Vite dev server  
  const vite = spawn('npx', ['vite', '--host', '0.0.0.0', '--port', '5173'], {
    cwd: __dirname,
    stdio: ['ignore', 'inherit', 'inherit']
  });

  vite.on('error', (error) => {
    console.error('Failed to start Vite:', error);
    backend.kill();
    process.exit(1);
  });

  vite.on('close', (code) => {
    console.log(`\nVite exited with code ${code}`);
    backend.kill();
    process.exit(code);
  });

  // Handle shutdown
  process.on('SIGINT', () => {
    console.log('\n\nShutting down services...');
    backend.kill();
    vite.kill();
    process.exit(0);
  });

  process.on('SIGTERM', () => {
    console.log('\n\nShutting down services...');
    backend.kill();
    vite.kill();
    process.exit(0);
  });
}, 3000);

backend.on('close', (code) => {
  console.log(`\nBackend exited with code ${code}`);
  process.exit(code);
});
