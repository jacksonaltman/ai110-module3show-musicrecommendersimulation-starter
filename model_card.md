# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

The recommender compares every song in the catalog to one listener's taste profile and gives each song a score out of 6 points. A song earns 2 points if its mood matches the mood the listener wants, and 1 point if its genre matches. It earns up to 2 more points for how close its energy is to the listener's target, so a calm song scores high for someone who wants calm music and low for someone who wants a workout. Finally, it earns 1 point if its sound is acoustic and the listener likes acoustic music, or if it is not acoustic and the listener doesn't.

The songs are then sorted from highest score to lowest, and the top five are shown. Each one comes with the reasons that earned it points, such as "mood match: chill (+2.0)", so you can see why it was picked. Tempo, valence and danceability are loaded from the data but are not used in the score yet.

This system has no data about other listeners, so unlike Spotify or YouTube it can only recommend songs that look like what the user says they want. It can't discover surprising favorites from what similar people played.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
