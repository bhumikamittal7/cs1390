import gradio as gr
import pandas as pd
import numpy as np
from datetime import date, datetime
from PIL import Image
import requests
import transformers as trf
import torch
import tensorflow as tf

gr.title('Mood Music Recommender - Noddy')

processor = trf.AutoProcessor.from_pretrained("openai/clip-vit-base-patch32")
model = trf.AutoModelForZeroShotImageClassification.from_pretrained("openai/clip-vit-base-patch32")

#get bert model
tokenizer = trf.AutoTokenizer.from_pretrained("finiteautomata/bertweet-base-sentiment-analysis")
model1 = trf.AutoModelForMaskedLM.from_pretrained("finiteautomata/bertweet-base-sentiment-analysis")

def get_mood(image):
    # image = image.convert('RGB')
    # image = image.resize((224, 224))
    image = np.array(image)
    image = np.expand_dims(image, axis=0)
    inputs = processor(text=["happy", "sad", "angry", "surprised", "disgusted", "calm", "neutral"], images=image, return_tensors="pt", padding=True)
    outputs = model(**inputs)
    logits_per_image = outputs.logits_per_image # this is the image-text similarity score
    probs = logits_per_image.softmax(dim=1) # we can take the softmax to get the label probabilities
    return probs

def get_productivity(image):
    # image = image.convert('RGB')
    # image = image.resize((224, 224))
    image = np.array(image)
    image = np.expand_dims(image, axis=0)
    inputs = processor(text=["low productivity", "medium productivity", "high productivity"], images=image, return_tensors="pt", padding=True)
    outputs = model(**inputs)
    logits_per_image = outputs.logits_per_image # this is the image-text similarity score
    probs = logits_per_image.softmax(dim=1) # we can take the softmax to get the label probabilities
    return probs

#from the prob array, get the index of the highest prob and return the label
def get_label_mood(probs):
    labels = ["happy", "sad", "angry", "surprised", "disgusted", "calm", "neutral"]
    index = torch.argmax(probs)
    return labels[index]

#from the prob array, get the index of the highest prob and return the label
def get_label_productivity(probs):
    labels = ["low", "medium", "high"]
    index = torch.argmax(probs)
    return labels[index]


#using bert model, get the sentiment of the text
def get_sentiment(mood, productivity):
    text = ["I am feeling " + str(mood) + " and my productivity is " + str(productivity)]
    inputs = tokenizer(text, return_tensors="pt")
    outputs = model1(**inputs)
    probs = outputs.logits.softmax(dim=1)
    labels = ["negative", "positive"]
    index = torch.argmax(probs)
    return labels[index]

# give playlist based on mood and productivity

def get_playlist(mood, productivity):
    if(mood == "happy" and productivity == "high"|productivity == "medium"| productivity =="low"):
        return "https://open.spotify.com/playlist/37i9dQZF1DXdPec7aLTmlC"
    elif(mood == "sad" and productivity == "high"|productivity == "medium"):
        return "https://open.spotify.com/album/7xSEO4RLeiTcVuwUFLb3UG"
    elif(mood == "sad" and productivity == "low"):
        return "https://open.spotify.com/album/0qRhFH2PLpHPPYUGxwFwHO"
    elif(mood == "calm" and productivity == "high"|productivity == "medium"):
        return "https://open.spotify.com/playlist/37i9dQZF1DWZeKCadgRdKQ"
    elif(mood == "calm" and productivity == "low"):
        return "https://open.spotify.com/playlist/37i9dQZF1DWWQRwui0ExPn"
    elif(mood == "angry" and productivity == "high"|productivity == "medium"|productivity =="low"):
        return "https://open.spotify.com/playlist/37i9dQZF1DX4sWSpwq3LiO"
    elif (mood == "disgusted" and productivity == "high" | productivity == "medium" | productivity == "low"):
        return "https://open.spotify.com/playlist/37i9dQZF1DXa2SPUyWl8Y5"
    elif (mood == "surprised" and productivity == "high" | productivity == "medium" | productivity == "low"):
        return "https://open.spotify.com/playlist/37i9dQZF1DWXti3N4Wp5xy"
    else:
        return "https://open.spotify.com/playlist/37i9dQZF1DX4SBhb3fqCJd"
    
#make an output function that takes in the image and returns the mood and productivity, and then the playlist
def out(image):
    mood = get_label_mood(get_mood(image))
    productivity = get_label_productivity(get_productivity(image))
    playlist = get_playlist(mood, productivity)
    sentiment = get_sentiment(mood, productivity)
    #output fun message based on mood
    if(mood == "happy"):
        m = "Yayy! Your current mood is " + str(mood) + " and your productivity is " + str(productivity) + ". Your overall sentiment is " +str(sentiment) +". \n You are doing great! Keep it up!  \n Here is a playlist for you: " + "<a href="+str(playlist)+">"+str(playlist)+"</a>"
    elif(mood == "sad"):
        m = "Aww! Your current mood is " + str(mood) + " and your productivity is " + str(productivity) + ". Your overall sentiment is " +str(sentiment) +". \n Don't worry, everything will be alright! \n Here is a playlist to cheer you up: " + "<a href="+str(playlist)+">"+str(playlist)+"</a>"
    elif(mood == "angry"):
        m = "Calm down Angry Bird! Your current mood is " + str(mood) + " and your productivity is " + str(productivity) + ". Your overall sentiment is " +str(sentiment) +". \n Take a deep breath and relax! \n Listn to some music: " + "<a href="+str(playlist)+">"+str(playlist)+"</a>"
    elif(mood == "surprised"):
        m = "Woah! Your current mood is " + str(mood) + " and your productivity is " + str(productivity) + ". Your overall sentiment is " +str(sentiment) +". \n All of us love surprieses. Here is another one for you " + "<a href="+str(playlist)+">"+str(playlist)+"</a>"
    elif(mood == "disgusted"):
        m = "Eww! Your current mood is " + str(mood) + " and your productivity is " + str(productivity) + ". Your overall sentiment is " +str(sentiment) +". \n Don't worry, everything will be alright! \n Here is a playlist to cheer you up: " +"<a href="+str(playlist)+">"+str(playlist)+"</a>"
    elif(mood == "calm"):
        m = "Amazing! Your current mood is " + str(mood) + " and your productivity is " + str(productivity) + ". Your overall sentiment is " +str(sentiment) +". \n You are doing great! Keep it up!  \n Here is a playlist for you: " + "<a href="+str(playlist)+">"+str(playlist)+"</a>"
    else:
        m = "Your current mood is " + str(mood) + " and your productivity is " + str(productivity) + ". Your overall sentiment is " +str(sentiment) +". \n Here is a playlist for you: " + "<a href="+str(playlist)+">"+str(playlist)+"</a>"
    return m

#import gradio
import gradio as gr

#image input
image = gr.inputs.Image(shape=(224, 224))

#interface
gr.Interface(fn=out, inputs=image, outputs=output, title="Mood Music Recommender - Noddy", description="Upload an image of yourself and we will recommend a playlist based on your mood and productivity level. \n I hope you have fun and I get grades Professor :) \n -Bhumika", allow_flagging=False, allow_screenshot=False, allow_embedding=False, theme="huggingface").launch()
