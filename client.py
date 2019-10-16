from douban import Douban
from wordcut import WordCut
from wordshow import WordShow

def test_spider():
    douban = Douban()
    douban.login('1234', '1234')
    url = douban.search_subject('活着')
    if url == 1:
        print('检索失败，程序退出')
        exit(1)
    douban.spider_all_comments(url, '活着.txt')

def test_words_show():
    wordcut = WordCut()
    word_list = wordcut.word_cut('活着.txt')

    word_show = WordShow()
    #设置停词
    stop_words = ['一个', '没有', '只是', '那么', '虽然', '原来', '其实', '这么',
                  '是', '看到', '看', '啊', '的', '不是', '但是', '了', '一', '挺',
                  '有', '不过', '这样', '哈哈哈', '那个', '这种', '已经', '因为',
                  '就是', '反正', '几个']
    word_show.word_image(word_list=word_list,stop_words=stop_words)

def client():
    #测试爬虫
    #test_spider()
    #测试分词及展示
    test_words_show()



if __name__ == '__main__':
    client()