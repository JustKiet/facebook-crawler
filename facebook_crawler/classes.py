class Post:
    def __init__(self, post: dict) -> None:
        self.__post = post
        self.__type = post["post_type"]
        self.__interactions = post["interactions"]
        self.__reactions = self.__interactions["reactions"]
        self.__comments = self.__interactions["comments"]
        self.__content = self.clean_duplicated_strings()

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
    
    def clean_duplicated_strings(self):
        useless_strings = ["|| Thích || Bình luận || Chia sẻ ", "|| Thích || Bình luận || Gửi || Chia sẻ "]

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