# Run the Python script
python src/main.py

# Change to the 'public' directory and start the HTTP server on port 8888
Set-Location -Path public
python -m http.server 8888
