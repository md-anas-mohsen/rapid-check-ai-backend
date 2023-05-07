from flask import Flask, request, jsonify
import logging
import spacy

app = Flask(__name__)

ENV = 'dev'

if ENV == 'dev':
    app.debug = True
else:
    app.debug = False

logger = logging.getLogger(__name__)

@app.after_request
def log_request(response):
    logger.info(f'Request {request.method} {request.url} {request.json}')
    logger.info(f'Response {response.status_code} {response.data}')
    return response

# Load the en_core_sci_lg model
nlp_ss = spacy.load("en_core_sci_lg")

#Function defined for 2 marks question
def get_similarity(ms,ans,nlp):
  scores = []
  s2 = nlp((ans.lower()))

  for i in range(len(ms)):
    score = 0
    for m in ms[i]:
      s1 = nlp(m.lower())
      similarity_score = s1.similarity(s2)
      print(m,similarity_score)
      score = max(score,similarity_score)
    print(score)
    scores.append(score)
  print()
  score = sum(scores)/len(scores)
  return score

def get_similarity_binary(ms,ans,nlp):
  scores = []
  s2 = nlp((ans.lower()))

  for i in range(len(ms)):
    score = 0
    for m in ms[i]:
      s1 = nlp(m.lower())
      similarity_score = s1.similarity(s2)
      print(m,similarity_score)
      score = max(score,similarity_score)
    print(score)
    scores.append(score)
  print()
  score = sum(scores)/len(scores)
  return scores


def get_similarity_concatenated(ms,ans,nlp):
  score = 0

  if len(ms) == 1:
    return get_similarity(ms,ans,nlp)

  s1 = nlp(ans.lower())
  for i in range(len(ms[0])):
    for j in range(len(ms[1])):
      m = ms[0][i] + " " + ms[1][j]
      s2 = nlp(m.lower())
      similarity_score = s1.similarity(s2)
      print(m,similarity_score)
      score = max(score,similarity_score)
  return score

# define a function to apply to each row
def similarity_for_spacy(row, response, ms):
    ans = response
    ms_index = 0
    x = get_similarity(ms,ans,nlp_ss)
    x = 0
    return x

@app.route('/compute-ai-score-physics', methods=["POST"])
def compute_ai_score():
    body = request.get_json()
    marking_scheme = body["markingScheme"]
    answer = body["studentResponse"]
    score = get_similarity(marking_scheme, answer, nlp_ss)
    return jsonify({
       "success": True,
       "score": score 
    })

@app.route('/')
def index():
   return "Hello from RapidCheck AI API"

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
