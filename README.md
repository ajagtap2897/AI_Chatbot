# AI_Chatbot

## Project Overview

This project is an AI-powered chatbot that leverages deep learning techniques to understand and respond to user queries. It consists of two implementations:

A PyTorch-based chatbot trained on predefined intents for structured conversations.

A Streamlit-based UI to provide an interactive user interface for engaging with the chatbot.

The chatbot utilizes natural language processing (NLP) techniques to interpret user input and generate appropriate responses, making it adaptable for various chatbot applications.
---------
## Installation Steps

To set up and run the project, follow these steps:

1. Clone the Repository:
```bash
git clone https://github.com/ajagtap2897/AI_Chatbot
cd AI_Chatbot
```

2. Create a Virtual Environment (Recommended)
```bash
python -m venv chatbot_env
source chatbot_env/bin/activate  # On Windows use: chatbot_env\Scripts\activate
```

3. Install Dependencies

Ensure you have Python installed, then install the required dependencies using:
```bash
pip install -r requirements.txt
```
If requirements.txt is missing, manually install key libraries:

```bash
pip install torch torchvision torchaudio nltk numpy pandas streamlit
```

4. Download Required NLTK Data

Before running the chatbot, ensure necessary NLP datasets are available:

```bash
import nltk
nltk.download('punkt')
```

## Usage Instructions

Running the Chatbot (CLI-based version)

To start the chatbot in the command-line interface:
```bash
python chat1.py
```
Running the Streamlit UI Chatbot

For a graphical user interface (GUI) version, run:
```bash
streamlit run chat1.py
```
This will launch a web-based chatbot interface powered by Streamlit.
![image alt](https://github.com/ajagtap2897/AI_Chatbot/blob/9fc7526f28b4d5001386ca806b98a89354a87235/Screenshot%202025-03-12%20194807.png)
## Data Files

This chatbot relies on a predefined intents dataset (intents.json). Ensure this file is present in the project directory before training or running the model.

If you want to modify the chatbot's responses, edit the intents.json file and retrain the model:
```bash
python train.py
```
## Customization

This chatbot can be adapted for different applications by modifying the intents.json file and retraining the model. You can integrate it into various platforms such as websites, customer service applications, or personal assistants.
