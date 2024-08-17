class Post:
    def __init__(self, post: dict) -> None:
        self.__post = post
        self.__type = post["post_type"]
        self.__interactions = post["interactions"]
        self.__reactions = self.__interactions["reactions"]
        self.__comments = self.__interactions["comments"]
        self.__content = self.__clean_duplicated_strings()

        if self.__type == "group":
            self.__extract_group_name()
            self.__extract_group_post_author()
        elif self.__type == "generic":
            self.__extract_generic_post_author()

    @property
    def post(self) -> dict:
        return self.__post
    
    @property
    def type(self) -> str:
        return self.__type
    
    @property
    def content(self) -> str:
        return self.__content
    
    @property
    def interactions(self) -> dict:
        return self.__interactions
    
    @property
    def reactions(self) -> dict:
        return self.__reactions
    
    @property
    def comments(self) -> dict:
        return self.__comments
    
    def __clean_duplicated_strings(self):
        useless_strings = ["|| Thích || Bình luận || Chia sẻ ", 
                           "|| Thích || Bình luận || Gửi || Chia sẻ ", 
                           "|| Thích || Bình luận || Gửi "]

        if self.__reactions in self.__post["content"]:
            self.__post["content"] = self.__post["content"].replace(self.__reactions, "")

        for comment in self.__comments:
            if comment in self.__post["content"]:
                self.__post["content"] = self.__post["content"].replace(comment, "")
            
            strings = comment.split(" || ")
            for string in strings:
                if string in self.__post["content"]:
                    self.__post["content"] = self.__post["content"].replace(string, "")

        for string in useless_strings:
            if string in self.__post["content"]:
                self.__post["content"] = self.__post["content"].replace(string, "")

        return self.__post["content"]
    
    def __extract_group_name(self):
        if self.__type == "group":
            pos = list(self.__post.keys()).index("content")
            items = list(self.__post.items())
            items.insert(pos, ("group_name", self.__content.split(" || ")[0]))
            self.__post = dict(items)

        if self.__post["group_name"] in self.__post["content"]:
            self.__post["content"] = self.__post["content"].replace(self.__post["group_name"], "")

        return None
    
    def __extract_group_post_author(self):
        if self.__type == "group":
            pos = list(self.__post.keys()).index("content")
            items = list(self.__post.items())
            items.insert(pos, ("post_author", self.__content.split(" || ")[1]))
            self.__post = dict(items)
        
        if self.__post["post_author"] in self.__post["content"]:
            self.__post["content"] = self.__post["content"].replace(self.__post["post_author"], "")

        return None
    
    def __extract_generic_post_author(self):
        if self.__type == "generic":
            pos = list(self.__post.keys()).index("content")
            items = list(self.__post.items())
            items.insert(pos, ("post_author", self.__content.split(" || ")[0]))
            self.__post = dict(items)

        if self.__post["post_author"] in self.__post["content"]:
            self.__post["content"] = self.__post["content"].replace(self.__post["post_author"], "")
        return None