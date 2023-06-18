# Customer Call Analyzer

## Intro


This is the [final project](https://codelabs.cs.pdx.edu/labs/C08.4_final/index.html?index=..%2F..cs430#1) of the [Internet, Web & Cloud](https://thefengs.com/wuchang/courses/cs430/) class at PSU. 
In this web application, I used google cloud speech-to-text API and natural language processing API to analyze the customer calls and evaluate the sentiment of the customers. The integration is completed 
within the container hosted on Google Cloud Run. 


## Interface

1. Upload the audio file from local folders


![Interface for Uploading](https://github.com/IanZC0der/call_analysis_nlp/assets/116975970/8b6b1ff4-b53a-4b14-91f0-67cf547b03ff)


2. Analyze

The audio is first transcribed to text and then analyzed using Google Cloud NLP API. The results show the text, sentiment and the product(s) this customer could be complaining about.


![Analyze](https://github.com/IanZC0der/call_analysis_nlp/assets/116975970/c8626d26-5f89-4fbf-bd1c-f896e0c07724)

