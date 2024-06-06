import random
from collections import defaultdict
import re

states = ['very negative', 'negative', 'neutral', 'positive', 'very positive']
state_to_score = {'very negative': -1, 'negative': -0.5, 'neutral': 0, 'positive': 0.5, 'very positive': 1}

def assign_state_to_text(text):
    text = text.lower()

    very_positive_keywords = [
        "love", "great", "happy", "wonderful", "fantastic", "recommended", 
        "excellent", "amazing", "perfect", "outstanding", "incredible", "awesome", 
        "superb", "exceptional", "marvelous", "extraordinary", "brilliant"
    ]
    
    positive_keywords = [
        "like", "good", "satisfied", "pleased", "enjoyed", 
        "nice", "pleasing", "delighted", "content", "fine", "positive", 
        "fortunate", "agreeable", "gratifying", "favorable"
    ]
    
    very_negative_keywords = [
        "hate", "worst", "terrible", "disappointed", "awful", 
        "horrible", "abysmal", "dreadful", "appalling", "atrocious", 
        "disgusting", "deplorable", "shocking", "outrageous", "dire"
    ]
    
    negative_keywords = [
        "dislike", "bad", "unsatisfied", "unhappy", "poor", 
        "subpar", "inferior", "lacking", "deficient", "mediocre", 
        "unfortunate", "unpleasant", "displeased", "regretful", "dissatisfied"
    ]
    
    if any(keyword in text for keyword in very_positive_keywords):
        return 'very positive'
    elif any(keyword in text for keyword in positive_keywords):
        return 'positive'
    elif any(keyword in text for keyword in very_negative_keywords):
        return 'very negative'
    elif any(keyword in text for keyword in negative_keywords):
        return 'negative'
    else:
        return 'neutral'

# Example usage
data_input = [
  "I love this product! It's absolutely wonderful.",
  "I hate this item. It's the worst thing I've ever bought.",
  "This is good, but it could be better.",
  "I'm not very happy with this purchase.",
  "It's a decent item, nothing special.",
  "Absolutely fantastic experience!",
  "The quality is mediocre and I am dissatisfied.",
  "I am delighted with the service. It was exceptional!"
]

# Apply the function to each text in the input
for text in data_input:
    state = assign_state_to_text(text)
    print(f"Text: {text}\nSentiment State: {state}\n")


def build_transition_matrix(states, labels):
  transition_counts = defaultdict(lambda: defaultdict(int))
  for i in range(1, len(labels)):
      prev_state = labels[i - 1]
      curr_state = labels[i]
      transition_counts[prev_state][curr_state] += 1
  transition_matrix = {}
  for state, transitions in transition_counts.items():
      total = sum(transitions.values())
      transition_matrix[state] = {k: v / total for k, v in transitions.items()}
  return transition_matrix

def simulate_markov_chain(transition_matrix, initial_state, n_steps, states):
  current_state = initial_state
  states_sequence = [initial_state]
  for _ in range(n_steps):
      if current_state in transition_matrix:
          next_state = random.choices(list(transition_matrix[current_state].keys()),
                                      list(transition_matrix[current_state].values()))[0]
      else:
          next_state = random.choice(states)
      states_sequence.append(next_state)
      current_state = next_state
  return states_sequence

def calculate_sentiment_score(states_sequence, state_to_score):
  scores = [state_to_score[state] for state in states_sequence]
  return sum(scores) / len(scores)

def predict_markov_chain(transition_matrix, initial_state, sequence_length, states):
  state = initial_state
  predictions = []
  for _ in range(sequence_length):
      if state in transition_matrix:
          next_state = max(transition_matrix[state], key=transition_matrix[state].get)
      else:
          next_state = random.choice(states)
      predictions.append(next_state)
      state = next_state
  return predictions

def get_sentiment_score(data):
    data_with_states = [{'text': text, 'state': assign_state_to_text(text)} for text in data]
    labels = [entry['state'] for entry in data_with_states]
    transition_matrix = build_transition_matrix(states, labels)
    initial_state = labels[0]
    simulation_result = simulate_markov_chain(transition_matrix, initial_state, 10, states)
    print(simulation_result)
    sentiment_score = calculate_sentiment_score(simulation_result, state_to_score)
    return sentiment_score

def split_into_sentences(text):
    sentence_endings = re.compile(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s')
    return sentence_endings.split(text)
    