# XSIAM Data source onboarding document AI Agent

The XSIAM Data source onboarding document AI Agent is built to provide a high level document when it comes to data source ingestion implementation. The user needs to input the data source name (e.g. Okta Identity Cloud Platform), the AI Agent will generate data onboarding document that describe the following information:
- Data Source characteristic
- Event types
- Event severity (if any)
- Ingestion method
- Required network configuration
- Required credential configuration

## Source data
- The agent used the RAG method with which supplies source data from the XSIAM marketplace and official admin guide content to Claude Sonnet4 Model
- The source data has been gathered and prepared manually. To maintain the accuracy, data should be refreshed every month with the built in tool *xsiam_readme_scrapper.py*


## Usage
- Create *.env* file in the same folder and put Claude API into the *.env* file
- Launch the app
    ```
    python3 app.py
    ```
- Access web UI locally (can be hosted)
    ```
    http://server_ip:5000
    ```
- Put data source vendor and product name into the text box then click Send

![alt text](<Screenshot 2025-07-23 104648.png>)

- Wait for the response to be provided
 ![alt text](<Screenshot 2025-07-23 104706.png>)


 ## Required Python dependencies
anthropic==0.52.1
faiss-gpu-cu12==1.11.0
filelock==3.17.0
Flask==3.1.1
numpy==1.26.4
Markdown==3.8
nvidia-cublas-cu12==12.6.4.1
nvidia-cuda-cupti-cu12==12.6.80
nvidia-cuda-nvrtc-cu12==12.6.77
nvidia-cuda-runtime-cu12==12.6.77
nvidia-cudnn-cu12==9.5.1.17
nvidia-cufft-cu12==11.3.0.4
nvidia-cufile-cu12==1.11.1.6
nvidia-curand-cu12==10.3.7.77
nvidia-cusolver-cu12==11.7.1.2
nvidia-cusparse-cu12==12.5.4.2
nvidia-cusparselt-cu12==0.6.3
nvidia-nccl-cu12==2.26.2
nvidia-nvjitlink-cu12==12.6.85
nvidia-nvtx-cu12==12.6.77
pandas==2.3.1
python-dotenv==0.20.0
sentence-transformers==4.1.0
torch==2.7.0