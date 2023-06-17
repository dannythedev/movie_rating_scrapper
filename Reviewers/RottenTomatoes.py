from Functions import exception_method, IMAGE_NOT_FOUND
from Reviewers.Reviewer import Reviewer


class RottenTomatoes(Reviewer):
    def __init__(self):
        super().__init__()
        self.url = 'https://www.rottentomatoes.com/m/'


    @exception_method
    def get_image(self, movie):
        if movie.image == IMAGE_NOT_FOUND:
            xpath = str(self.html.get_xpath("//tile-dynamic[@class='thumbnail']//@src")[0])
            if 'poster-default' not in xpath:
                movie.image = xpath


    @exception_method
    def get_duration(self, movie):
        if not movie.duration:
            movie.duration = str(self.html.get_xpath("//p[@class='info']/text()")[0].split(', ')[2])

    @exception_method
    def get_genre(self, movie):
        if not movie.genre:
            movie.genre = str(self.html.get_xpath("//p[@class='info']/text()")[0].split(', ')[1])

    def get_attributes(self, movie, url=''):
        super().get_attributes(movie=movie, url=self.url + movie.suffix.replace('-', '_'))
        board = self.html.find("score-board") # Rating
        if board is not None:
            if board["audiencescore"] == '' and board["tomatometerscore"] == '':
                return
            movie.rating.update({'Tomatometer Audience Score': int(board["audiencescore"]),
                                 'Tomatometer Critic Score': int(board["tomatometerscore"])})
