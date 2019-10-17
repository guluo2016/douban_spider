import jieba

class WordCut:
    def word_cut(self,file_path):
        """
        读取指定文档中的数据，并使用结巴分词器进行分词处理
        :param file_path:
        :return:
        """
        with open(file_path, "r", encoding='utf-8') as file:
            comment = file.read()
            wordlist = jieba.cut(comment, cut_all=True)
            wl = ' '.join(wordlist)
            return wl