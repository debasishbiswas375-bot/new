FROM python:3.11-slim

# Create a non-root user (Hugging Face security requirement)
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH
WORKDIR $HOME/app

# Copy and install dependencies
COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Copy application files
COPY --chown=user . .

# Expose port 7860 (Hugging Face's default)
EXPOSE 7860

# Production run command for Solara
CMD ["solara", "run", "app.py", "--host=0.0.0.0", "--port=7860", "--production"]
