# Process Resource Monitor

A lightweight Python tool to monitor CPU and RAM usage of a process and its children, with real-time stats and resettable max counters.

## Features
- Monitor CPU and RAM usage of a process and its child processes.
- Reset max counters with a simple key press.
- Lightweight and easy to use.

## Usage
1. Install dependencies:
```bash
pip install -r requirements.txt
```
2. Run the script:
```bash
python src/monitor.py <PID>
```

## Requirements
- Python 3.6+
- psutil

## Contributing
Contributions are welcome! If you have an idea for improving the project, feel free to open an issue or submit a pull request.

To contribute:
1. Fork the repository.
2. Create a new branch for your feature or bugfix:
```bash
git checkout -b feature-name
```
3. Commit your changes and push the branch
```bash
git commit -m "Describe your changes"
git push origin feature-name
```
4. Open a pull request.