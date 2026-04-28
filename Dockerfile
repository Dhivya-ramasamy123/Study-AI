# Use official Python image
FROM python:3.12-slim
 
# Set working directory
WORKDIR /app
 
# Copy requirements first (for layer caching)
COPY requirements.txt .
 
# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
 
# Copy the rest of the app
COPY . .
 
# Expose Streamlit default port
EXPOSE 8501
 
# Run the Streamlit app
CMD ["streamlit", "run", "application.py", "--server.port=8501", "--server.address=0.0.0.0"]
 