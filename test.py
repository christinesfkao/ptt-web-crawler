# vim: set ts=4 sw=4 et: -*- coding: utf-8 -*-
import unittest
import crawler
import codecs, json, os

class TestCrawler(unittest.TestCase):
    def test_parse(self):
        self.link = 'https://www.ptt.cc/bbs/PublicServan/M.1409529482.A.9D3.html'
        self.article_id = 'M.1409529482.A.9D3'
        self.board = 'PublicServan'
        jsondata = json.loads(crawler.parse(self.link, self.article_id, self.board))
        self.assertEqual(jsondata['article_id'], self.article_id)
        self.assertEqual(jsondata['board'], self.board)
        self.assertEqual(jsondata['message_conut']['count'], 55)
    
    def test_parse_with_structured_push_contents(self):
        self.link = 'https://www.ptt.cc/bbs/Gossiping/M.1425003598.A.630.html'
        self.article_id = 'M.1425003598.A.630'
        self.board = 'Gossiping'
        jsondata = json.loads(crawler.parse(self.link, self.article_id, self.board))
        self.assertEqual(jsondata['article_id'], self.article_id)
        self.assertEqual(jsondata['board'], self.board)
        isCatched = False
        for msg in jsondata['messages']:
            if u'http://ppt.cc/FMSc' in msg['push_content']:
                isCatched = True
        self.assertTrue(isCatched)

    
    def test_crawler(self):
        crawler.crawler(['-b', 'PublicServan', '-i', '1', '2'])
        filename = 'PublicServan-1-2.json'
        with codecs.open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # M.1127808641.A.C03.html is empty, so decrease 1 from 40 articles
            self.assertEqual(len(data['articles']), 39)  
            os.remove(filename)
    

if __name__ == '__main__':
    unittest.main()