from facebook_crawler.llm_processing import FacebookPostAnalyst
from facebook_crawler.llm_processing import Post
import json
import os
from Secret.secret import GeminiKey

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

os.environ["GOOGLE_API_KEY"] = GeminiKey()

output = []

with open("facebook_posts.json", "r", encoding="utf-8") as file:
    facebook_posts = json.load(file)

for post in facebook_posts:
    try:
        post_obj = Post(post)
        
        post_formatted = FacebookPostAnalyst(post=post_obj, 
                                             model=ChatGoogleGenerativeAI(model="gemini-1.5-flash"))

        output.append(post_formatted)

        print(json.dumps(post_formatted, ensure_ascii=False, indent=4))
    except Exception as e:
        print(e)
        continue

with open("output.json", "w", encoding="utf-8") as file:
    json.dump(output, file, ensure_ascii=False, indent=4)