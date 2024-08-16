from bs4 import BeautifulSoup
from typing import Optional
import json
import os
import re

import langchain
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from Secret.secret import OpenAIKey

from facebook_crawler.pydantic_objects import FacebookPost, PostComment, ReplyComment 
from facebook_crawler.classes import Post   

def FacebookPostAnalyst(post: Post):
    api_key = OpenAIKey()

    model = ChatOpenAI(model="gpt-4o-mini")

    parser = JsonOutputParser(pydantic_object=FacebookPost)

    prompt = PromptTemplate(
        template="""You are a Facebook Data Analyst. You are trying to retrieve related information 
        from a pre-processed Facebook post in JSON format.\n
        --------------------------------\n
        IMPORTANT NOTES - MUST FOLLOW:\n
        - In the "content" field, each parts of the post will be SEPERATED by ||. They will be called as ELEMENTS. This field contains everything related to the post (Group name(if it is a group post), 
        post author, post caption and alot of gibberish).\n
        - The post_type can be either a "group" or a "generic" post:\n
        + If it is a "group" post, THE FIRST ELEMENT from the "content" field WILL ALWAYS BE THE GROUP NAME and the SECOND ELEMENT WILL ALWAYS BE THE POST AUTHOR.\n
        + If it is a "generic" post, THE FIRST ELEMENT from the "content" field WILL ALWAYS BE THE POST AUTHOR.\n
        - The "content" field could contains hints to whether the post has attachments or not (timestamps, links), be aware.\n
        - In the "reaction" field, there should be 3 SEPERATE FIELDS which in order, should be "likes", 
        "comments", and "shares".\n
        - In the "comments" field, each comment should have the following fields: "author", "content" & "likes". 
        Be aware that some comments might be replies to other comments. Try to identify them accordingly.\n
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


    


