from wordcloud import WordCloud
from matplotlib import pyplot as plt

class WordShow:
    def word_image(self,word_list,stop_words):
        font_path = 'simhei.ttf'
        wc = WordCloud(collocations=False, width=1400, height=1400, margin=2, font_path=font_path,
                       stopwords=stop_words).generate(word_list)
        plt.imshow(wc)
        plt.axis("off")
        plt.show()
