from langchain_core.pydantic_v1 import BaseModel, Field

class ReplyComment(BaseModel):
    commentAuthor: str = Field(description="The author of the comment.")
    commentContent: str = Field(description="The content of the comment.")
    commentLikesCount: int = Field(description="The number of likes the comment has.")

class PostComment(BaseModel):
    commentAuthor: str = Field(description="The author of the comment.")
    commentContent: str = Field(description="The content of the comment.")
    commentAttitude: str = Field(description="The attitude of the comment. Can be Negative/Neutral/Positive.")
    commentLikesCount: int = Field(description="The number of likes the comment has.")
    commentRepliesCount: int = Field(description="The number of replies the comment has.")
    commentReplies: list[ReplyComment] = Field(description="Replies to the comment")

class FacebookPost(BaseModel):
    postType: str = Field(description="The type of the post. Can be Group/Generic.")
    postGroup: str = Field(description="""The group name if the post is a group post. If the post type is "group", 
                           THE FIRST ELEMENT from the "content" field WILL ALWAYS BE THE GROUP NAME""")
    postAuthor: str = Field(description="""The author of the post. 
                            If it is a "group" post, the SECOND ELEMENT WILL ALWAYS BE THE POST AUTHOR. 
                            If it is a "generic" post, THE FIRST ELEMENT from the "content" field WILL ALWAYS BE THE POST AUTHOR.""")
    postCaption: str = Field(description="""The caption of the post. CHOOSE ONLY ONE HIGHLY PLAUSIBLE ELEMENT FROM THE 'content' FIELD. BE AWARE OF VERY LONG CAPTIONS. 
                             THERE SHOULD NOT BE ANY "||" CHARACTER IN THE CAPTION.""")
    postAttachments: str = Field(description="""Possible attachments related to the post. Can be Video/Image/None. 
                                 The "content" field could contains hints to whether the post has attachments or not (timestamps = videos, links = images), be aware.""")
    postLikesCount: int = Field(description="The number of likes the post has.")
    postCommentsCount: int = Field(description="The number of comments the post has.")
    postSharesCount: int = Field(description="The number of shares the post has.")
    postComments: list[PostComment] = Field(description="Comments related to the post.")

