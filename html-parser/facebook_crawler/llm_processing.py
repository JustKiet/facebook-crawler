from bs4 import BeautifulSoup
from typing import Optional
import json
import os
import re

import langchain
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field

from facebook_crawler.pydantic_objects import FacebookPost, PostComment, ReplyComment 
from facebook_crawler.classes import Post   

def FacebookPostAnalyst(post: Post, model):

    parser = JsonOutputParser(pydantic_object=FacebookPost)

    prompt = PromptTemplate(
        template="""You are a Facebook Data Analyst. You are trying to retrieve related information 
        from a pre-processed Vietnamese Facebook post in JSON format.\n
        --------------------------------\n
        IMPORTANT NOTES - MUST FOLLOW:\n
        - In the "content" field, each parts of the post will be SEPERATED by ||. They will be called as ELEMENTS. This field 
        contains the main caption of the posts and alot of gibberish. You need to extract the plausible caption from this field.\n
        - The "content" field could contains hints to whether the post has media content or not (timestamps, links, image caption), figure out if the post has any.\n
        - In the "reaction" field, there should be 3 SEPERATE FIELDS which in order, should be "likes", 
        "comments", and "shares".\n
        - In the "comments" field, each comment should have the following fields: "author", "content" & "likes". 
        Be aware that some comments might be replies to other comments. Try to identify them accordingly.\n
        - The "group_name" field will contain the name of the group if the post is a group post.\n
        - The "post_author" field will contain the author of the post.\n
        --------------------------------\n
        Here is the post:\n
        --------------------------------\n
        {post}
        --------------------------------\n
        You need to extract the following information from the post:\n
        {format_instructions}
        --------------------------------\n

        """,
        input_variables=[{"post"}],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )

    chain = prompt | model | parser

    output = chain.invoke({"post": post.post})

    return output


    


