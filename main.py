import re
from flask import Flask, jsonify, request
from youtube_transcript_api import YouTubeTranscriptApi

app = Flask(__name__)

def clean_text(text):
    text = re.sub(r'[\u266a\u266b\u2669\u266c]', '', text)
    text = re.sub(r'\[.*?\]', '', text)
    text = re.sub(r'\(.*?\)', '', text)
    text = text.replace('\\n', ' ').replace('\n', ' ')
    text = re.sub(r'\s+', ' ', text).strip()
    return text

@app.route('/transcript')
def transcript():
    video_id = request.args.get('id')
    if not video_id:
        return jsonify({'error': 'Потрібен параметр id'}), 400
    try:
        ytt = YouTubeTranscriptApi()
        data = ytt.fetch(video_id, languages=['uk', 'ru', 'en'])
        text = clean_text(' '.join([s.text for s in data]))
        return jsonify({'transcript': text, 'video_id': video_id})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
