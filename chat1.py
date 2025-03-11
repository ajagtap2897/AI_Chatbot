import streamlit as st
import torch
import random
import json
from model import NeuralNet
from nitk_utils import bag_of_words, tokenize
import torch.backends.cudnn as cudnn

# Enable CUDNN benchmarking for performance
cudnn.benchmark = True

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Load intents
with open('intents.json', 'r') as f:
    intents = json.load(f)

# Load trained model
File = "data.pth"
data = torch.load(File)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data["all_words"]
tags = data["tags"]
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "Tor"

def get_response(sentence):
    sentence = tokenize(sentence)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)
    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]

    if prob.item() > 0.75:
        for intent in intents["intents"]:
            if tag == intent["tag"]:
                return random.choice(intent["responses"])
    else:
        return "I do not understand...."

def main():
    st.set_page_config(page_title="Chatbot UI", page_icon="🤖")
    st.title("🤖 Chatbot Interface")
    st.write("Ask me anything!")
    
    user_input = st.text_input("You:", "", key="input")
    if st.button("Get Response"):
        if user_input:
            response = get_response(user_input)
            st.text_area("Tor:", value=response, height=100, max_chars=None, key=None)
        else:
            st.warning("Please enter a message.")

    # Sidebar information
    with st.sidebar:
        st.title("ℹ️ About")
        st.markdown("""
        This is a simple chatbot interface using a neural network trained on predefined intents.
        
        **How to use:**
        1. Type your message in the input box.
        2. Click 'Get Response'.
        3. View the chatbot's reply.
        """)

if __name__ == "__main__":
    main()