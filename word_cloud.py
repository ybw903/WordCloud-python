# 워드 클라우드에 필요한 라이브러리를 불러옵니다.
from wordcloud import WordCloud
# 한국어 자연어 처리 라이브러리를 불러옵니다.
from konlpy.tag import Twitter
# 명사의 출현 빈도를 세는 라이브러리를 불러옵니다.
from collections import Counter
# 그래프 생성에 필요한 라이브러리를 불러옵니다.
import matplotlib.pyplot as plt
# Flask 웹 서버 구축에 필요한 라이브러리를 불러옵니다.
from flask import Flask, request, jsonify

# 플라스크 웹 서버 객체 생성합니다.
app = Flask(__name__)

#폰트 경로 설정
font_path ='NanumGothic.ttf'

def get_tags(text, max_count, min_length):
    t=Twitter()
    nouns = t.nouns(text)
    processed = [n for n in nouns if len(n) >= min_length]
    count = Counter(processed)
    result = {}
    for n, c in count.most_common(max_count):
        result[n] = c
    if len(result) == 0:
        result["내용이 없습니다."] = 1
    return count

def make_cloud_image(tags, file_name):
    # 만들고자 하는 워드 클라우드의 기본 설정을 진행합니다.
    word_cloud=WordCloud(
        font_path=font_path,
        width=800,
        height=800,
        background_color="white"
    )
    word_cloud = word_cloud.generate_from_frequencies(tags)
    fig = plt.figure(figsize=(10, 10))
    plt.imshow(word_cloud)
    plt.axis("off")
    # 만들어진 이미지 객체를 파일 형태로 저장합니다.
    fig.savefig("outputs/{0}.png".format(file_name))

def process_from_text(text, max_count, min_length, words):
    tags = get_tags(text, max_count, min_length)
    # 단어 가중치를 적용합니다.
    for n,c in words.items():
        if n in tags:
            tags[n] = tags[n] * int(words[n])
    make_cloud_image(tags, "output")

@app.route("/process", methods = ['GET','POST'])
def process():
    content = request.json
    words = {}
    if content['words'] is not None:
        for data in content['words'].values():
            words[data['word']] = data['weight']
    process_from_text(content['text'],content['maxCount'],content['minLength'],words)
    result = {'result': True}
    return jsonify(result)

if __name__ =='__main__':
    app.run('0.0.0.0',port=5000)