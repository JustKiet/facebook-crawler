from facebook_crawler.llm_processing import FacebookPostAnalyst
from facebook_crawler.llm_processing import Post
import json
import os
from Secret.secret import OpenAIKey

os.environ["OPENAI_API_KEY"] = OpenAIKey()

output = []

with open("facebook_posts.json", "r", encoding="utf-8") as file:
    facebook_posts = json.load(file)

for post in facebook_posts:
    try:
        post_obj = Post(post)
        
        post_formatted = FacebookPostAnalyst(post_obj)

        output.append(post_formatted)

        print(json.dumps(post_formatted, ensure_ascii=False, indent=4))
    except Exception:
        continue

with open("output.json", "w", encoding="utf-8") as file:
    json.dump(output, file, ensure_ascii=False, indent=4)