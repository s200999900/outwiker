#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import unittest
import os.path

from outwiker.core.search import Searcher, AllTagsSearchStrategy, \
        AnyTagSearchStrategy

from outwiker.pages.search.searchpage import SearchPageFactory, SearchWikiPage, GlobalSearch
from test.utils import removeWiki
from outwiker.core.tree import WikiDocument
from outwiker.pages.text.textpage import TextPageFactory
from outwiker.core.attachment import Attachment


class SearcherTest(unittest.TestCase):
    def setUp(self):
        # Здесь будет создаваться вики
        self.path = u"../test/testwiki"
        removeWiki (self.path)

        self.rootwiki = WikiDocument.create (self.path)

        TextPageFactory.create (self.rootwiki, u"page 1", [u"метка 1", u"Метка 2"])
        TextPageFactory.create (self.rootwiki, u"Страница 2", [u"Метка 1", u"Метка 3"])
        TextPageFactory.create (self.rootwiki[u"Страница 2"], u"Страница 3", [u"Метка 2"])
        TextPageFactory.create (self.rootwiki[u"Страница 2/Страница 3"], u"Страница 4", [u"Метка 1"])
        TextPageFactory.create (self.rootwiki[u"page 1"], u"page 5", [u"Метка 1", u"метка 2"])
        
        self.rootwiki[u"page 1"].content = ur"1  декабря. (Перечеркнуто, поправлено) 1 января 1925 г. Фотографирован \
            утром. Счастливо лает 'абыр', повторяя это слово громко и как бы радостно."

        self.rootwiki[u"page 1/page 5"].content = ur"Сегодня после того, как у него отвалился хвост, он  произнес совершенно\
            отчетливо слово 'пивная'"

        self.rootwiki[u"Страница 2"].content = ur"30  Декабря. Выпадение  шерсти  приняло  характер  общего  облысения.\
            Взвешивание  дало неожиданный  результат - 30 кг  за счет роста (удлинение)\
            костей. Пес по-прежнему лежит."

        self.rootwiki[u"Страница 2/Страница 3"].content = ur"29 Декабря. Внезапно обнаружено выпадение  шерсти на лбу  \
            и на боках туловища."

        self.rootwiki[u"Страница 2/Страница 3/Страница 4"].content = ur"2 Января. Фотографирован во время  улыбки при магнии. \
            Встал с постели и уверенно держался полчаса на задних лапах. Моего почти роста."


        filesPath = u"../test/samplefiles/"
        self.files = [u"accept.png", u"add.png", u"anchor.png", u"файл с пробелами.tmp", u"dir"]
        self.fullFilesPath = [os.path.join (filesPath, fname) for fname in self.files]

        Attachment (self.rootwiki[u"page 1"]).attach (self.fullFilesPath)
        Attachment (self.rootwiki[u"Страница 2/Страница 3"]).attach (self.fullFilesPath[0:3])
        Attachment (self.rootwiki[u"Страница 2"]).attach ([self.fullFilesPath[0]])
    

    def testSearchContentAll (self):
        phrase = u"Декабря"
        tags = []

        searcher = Searcher (phrase, tags, AllTagsSearchStrategy)
        pages = searcher.find (self.rootwiki)

        self.assertEqual (len (pages), 3)
        self.assertTrue (self.rootwiki[u"page 1"] in pages)
        self.assertTrue (self.rootwiki[u"Страница 2"] in pages)
        self.assertTrue (self.rootwiki[u"Страница 2/Страница 3"] in pages)


    def testSearchAttach1 (self):
        phrase = u"accept"
        tags = []

        searcher = Searcher (phrase, tags, AllTagsSearchStrategy)
        pages = searcher.find (self.rootwiki)

        self.assertEqual (len (pages), 3)

        self.assertTrue (self.rootwiki[u"page 1"] in pages)
        self.assertTrue (self.rootwiki[u"Страница 2/Страница 3"] in pages)
        self.assertTrue (self.rootwiki[u"Страница 2"] in pages)


    def testSearchAttach2 (self):
        phrase = u"anchor"
        tags = []

        searcher = Searcher (phrase, tags, AllTagsSearchStrategy)
        pages = searcher.find (self.rootwiki)

        self.assertEqual (len (pages), 2)

        self.assertTrue (self.rootwiki[u"page 1"] in pages)
        self.assertTrue (self.rootwiki[u"Страница 2/Страница 3"] in pages)


    def teatDown (self):
        if os.path.exists (self.path):
            removeWiki (self.path)


    def testSearchAttach3 (self):
        phrase = u"файл с пробелами"
        tags = []

        searcher = Searcher (phrase, tags, AllTagsSearchStrategy)
        pages = searcher.find (self.rootwiki)

        self.assertEqual (len (pages), 1)

        self.assertTrue (self.rootwiki[u"page 1"] in pages)


    def testSearchAttach4 (self):
        phrase = u"dir.xxx"
        tags = []

        searcher = Searcher (phrase, tags, AllTagsSearchStrategy)
        pages = searcher.find (self.rootwiki)

        self.assertEqual (len (pages), 1)

        self.assertTrue (self.rootwiki[u"page 1"] in pages)


    def testSearchAttach5 (self):
        phrase = u"SubdIr2"
        tags = []

        searcher = Searcher (phrase, tags, AllTagsSearchStrategy)
        pages = searcher.find (self.rootwiki)

        self.assertEqual (len (pages), 1)

        self.assertTrue (self.rootwiki[u"page 1"] in pages)


    def testSearchAttach6 (self):
        phrase = u"ApplicAtiOn.pY"
        tags = []

        searcher = Searcher (phrase, tags, AllTagsSearchStrategy)
        pages = searcher.find (self.rootwiki)

        self.assertEqual (len (pages), 1)

        self.assertTrue (self.rootwiki[u"page 1"] in pages)


    def testSearchTagsContent1 (self):
        phrase = u"метка"
        tags = []

        searcher = Searcher (phrase, tags, AllTagsSearchStrategy)
        pages = searcher.find (self.rootwiki)

        self.assertEqual (len (pages), 5)


    def testSearchTagsContent2 (self):
        phrase = u"МеТкА 1"
        tags = []

        searcher = Searcher (phrase, tags, AllTagsSearchStrategy)
        pages = searcher.find (self.rootwiki)

        self.assertEqual (len (pages), 4)
        self.assertTrue (self.rootwiki[u"page 1"] in pages)
        self.assertTrue (self.rootwiki[u"Страница 2"] in pages)
        self.assertTrue (self.rootwiki[u"Страница 2/Страница 3/Страница 4"] in pages)
        self.assertTrue (self.rootwiki[u"page 1/page 5"] in pages)


    
    def testSearchContentAny (self):
        phrase = u"Декабря"
        tags = []

        searcher = Searcher (phrase, tags, AnyTagSearchStrategy)
        pages = searcher.find (self.rootwiki)

        self.assertEqual (len (pages), 3)
        self.assertTrue (self.rootwiki[u"page 1"] in pages)
        self.assertTrue (self.rootwiki[u"Страница 2"] in pages)
        self.assertTrue (self.rootwiki[u"Страница 2/Страница 3"] in pages)
    

    def testSearchAllAll (self):
        phrase = u""
        tags = []

        searcher = Searcher (phrase, tags, AllTagsSearchStrategy)
        pages = searcher.find (self.rootwiki)

        self.assertEqual (len (pages), 5)

    
    def testSearchAllAny (self):
        phrase = u""
        tags = []

        searcher = Searcher (phrase, tags, AnyTagSearchStrategy)
        pages = searcher.find (self.rootwiki)

        self.assertEqual (len (pages), 5)

    
    def testSearchSingleTagAll (self):
        phrase = u""
        tags = [u"Метка 1"]

        searcher = Searcher (phrase, tags, AllTagsSearchStrategy)
        pages = searcher.find (self.rootwiki)

        self.assertEqual (len (pages), 4)
        self.assertTrue (self.rootwiki[u"page 1"] in pages)
        self.assertTrue (self.rootwiki[u"Страница 2"] in pages)
        self.assertTrue (self.rootwiki[u"Страница 2/Страница 3/Страница 4"] in pages)
        self.assertTrue (self.rootwiki[u"page 1/page 5"] in pages)

    
    def testSearchSingleTagAny (self):
        phrase = u""
        tags = [u"Метка 1"]

        searcher = Searcher (phrase, tags, AnyTagSearchStrategy)
        pages = searcher.find (self.rootwiki)

        self.assertEqual (len (pages), 4)
        self.assertTrue (self.rootwiki[u"page 1"] in pages)
        self.assertTrue (self.rootwiki[u"Страница 2"] in pages)
        self.assertTrue (self.rootwiki[u"Страница 2/Страница 3/Страница 4"] in pages)
        self.assertTrue (self.rootwiki[u"page 1/page 5"] in pages)
    

    def testSearchTag2All (self):
        phrase = u""
        tags = [u"МеткА 1", u"МетКа 2"]

        searcher = Searcher (phrase, tags, AllTagsSearchStrategy)
        pages = searcher.find (self.rootwiki)

        self.assertEqual (len (pages), 2)
        self.assertTrue (self.rootwiki[u"page 1"] in pages)
        self.assertTrue (self.rootwiki[u"page 1/page 5"] in pages)
    

    def testSearchTag2Any (self):
        phrase = u""
        tags = [u"МеткА 1", u"МетКа 3"]

        searcher = Searcher (phrase, tags, AnyTagSearchStrategy)
        pages = searcher.find (self.rootwiki)

        self.assertEqual (len (pages), 4)
        self.assertTrue (self.rootwiki[u"page 1"] in pages)
        self.assertTrue (self.rootwiki[u"Страница 2"] in pages)
        self.assertTrue (self.rootwiki[u"Страница 2/Страница 3/Страница 4"] in pages)
        self.assertTrue (self.rootwiki[u"page 1/page 5"] in pages)
    

    def testSearchFullAll (self):
        phrase = u"Декабря"
        tags = [u"Метка 2"]

        searcher = Searcher (phrase, tags, AllTagsSearchStrategy)
        pages = searcher.find (self.rootwiki)
        
        self.assertEqual (len (pages), 2)
        self.assertTrue (self.rootwiki[u"page 1"] in pages)
        self.assertTrue (self.rootwiki[u"Страница 2/Страница 3"] in pages)


    def testSearchFullAny (self):
        phrase = u"Декабря"
        tags = [u"Метка 2"]

        searcher = Searcher (phrase, tags, AnyTagSearchStrategy)
        pages = searcher.find (self.rootwiki)
        
        self.assertEqual (len (pages), 2)
        self.assertTrue (self.rootwiki[u"page 1"] in pages)
        self.assertTrue (self.rootwiki[u"Страница 2/Страница 3"] in pages)


class SearchPageTest (unittest.TestCase):
    """
    Тест на создание страниц с поиском
    """
    def setUp(self):
        # Здесь будет создаваться вики
        self.path = u"../test/testwiki"
        removeWiki (self.path)

        self.rootwiki = WikiDocument.create (self.path)

        TextPageFactory.create (self.rootwiki, u"page 1", [u"Метка 1", u"Метка 2"])
        TextPageFactory.create (self.rootwiki, u"Страница 2", [u"Метка 1", u"Метка 3"])
        TextPageFactory.create (self.rootwiki[u"Страница 2"], u"Страница 3", [u"Метка 2"])
        TextPageFactory.create (self.rootwiki[u"Страница 2/Страница 3"], u"Страница 4", [u"Метка 1"])
        TextPageFactory.create (self.rootwiki[u"page 1"], u"page 5", [u"Метка 4"])

        self.rootwiki[u"page 1"].content = ur"1  декабря. (Перечеркнуто, поправлено) 1 января 1925 г. Фотографирован \
            утром. Счастливо лает 'абыр', повторяя это слово громко и как бы радостно."

        self.rootwiki[u"page 1/page 5"].content = ur"Сегодня после того, как у него отвалился хвост, он  произнес совершенно\
            отчетливо слово 'пивная'"

        self.rootwiki[u"Страница 2"].content = ur"30  Декабря. Выпадение  шерсти  приняло  характер  общего  облысения.\
            Взвешивание  дало неожиданный  результат - 30 кг  за счет роста (удлинение)\
            костей. Пес по-прежнему лежит."

        self.rootwiki[u"Страница 2/Страница 3"].content = ur"29 Декабря. Внезапно обнаружено выпадение  шерсти на лбу  \
            и на боках туловища."

        self.rootwiki[u"Страница 2/Страница 3/Страница 4"].content = ur"2 Января. Фотографирован во время  улыбки при магнии. \
            Встал с постели и уверенно держался полчаса на задних лапах. Моего почти роста."
    

    def testCreateDefaultPage (self):
        GlobalSearch.create (self.rootwiki)
        page = self.rootwiki[GlobalSearch.pageTitle]

        self.assertTrue (page != None)
        self.assertEqual (self.rootwiki.selectedPage, page)
        self.assertEqual (page.phrase, u"")
        self.assertEqual (len (page.searchTags ), 0)
        self.assertEqual (page.strategy, AllTagsSearchStrategy)
    

    def testCreateSearchTagsPage (self):
        GlobalSearch.create (self.rootwiki, tags = [u"Метка 1", u"Метка 2"])
        page = self.rootwiki[GlobalSearch.pageTitle]

        self.assertTrue (page != None)
        self.assertEqual (self.rootwiki.selectedPage, page)
        self.assertEqual (page.phrase, u"")
        self.assertEqual (len (page.searchTags), 2)
        self.assertTrue (u"Метка 1" in page.searchTags )
        self.assertTrue (u"Метка 2" in page.searchTags)
        self.assertEqual (page.strategy, AllTagsSearchStrategy)
    

    def testCreateSearchPhrasePage (self):
        GlobalSearch.create (self.rootwiki, phrase = u"декабрь")
        page = self.rootwiki[GlobalSearch.pageTitle]

        self.assertTrue (page != None)
        self.assertEqual (self.rootwiki.selectedPage, page)
        self.assertEqual (page.phrase, u"декабрь")
        self.assertEqual (len (page.searchTags), 0)
        self.assertEqual (page.strategy, AllTagsSearchStrategy)

    
    def testCreateSearchAllPage (self):
        GlobalSearch.create (self.rootwiki, 
                phrase = u"декабрь", 
                tags = [u"Метка 1", u"Метка 2"],
                strategy = AllTagsSearchStrategy)

        page = self.rootwiki[GlobalSearch.pageTitle]

        self.assertTrue (page != None)
        self.assertEqual (self.rootwiki.selectedPage, page)
        self.assertEqual (page.phrase, u"декабрь")
        self.assertEqual (len (page.searchTags), 2)
        self.assertTrue (u"Метка 1" in page.searchTags)
        self.assertTrue (u"Метка 2" in page.searchTags)
        self.assertEqual (page.strategy, AllTagsSearchStrategy)
    

    def testLoadSearchPage (self):
        GlobalSearch.create (self.rootwiki, 
                phrase = u"декабрь", 
                tags = [u"Метка 1", u"Метка 2"],
                strategy = AllTagsSearchStrategy)

        wiki = WikiDocument.load (self.path)
        page = wiki[GlobalSearch.pageTitle]

        self.assertTrue (page != None)
        self.assertEqual (page.phrase, u"декабрь")
        self.assertEqual (len (page.searchTags), 2)
        self.assertTrue (u"Метка 1" in page.searchTags)
        self.assertTrue (u"Метка 2" in page.searchTags)
        self.assertEqual (page.strategy, AllTagsSearchStrategy)
    

    def testManySearchPages1 (self):
        GlobalSearch.create (self.rootwiki)

        GlobalSearch.create (self.rootwiki, 
                phrase = u"декабрь", 
                tags = [u"Метка 1", u"Метка 2"],
                strategy = AllTagsSearchStrategy)

        wiki = WikiDocument.load (self.path)
        page = wiki[GlobalSearch.pageTitle]

        self.assertEqual (wiki[GlobalSearch.pageTitle + u" 2"], None)
        self.assertTrue (page != None)
        self.assertEqual (page.phrase, u"декабрь")
        self.assertEqual (len (page.searchTags), 2)
        self.assertTrue (u"Метка 1" in page.searchTags)
        self.assertTrue (u"Метка 2" in page.searchTags)
        self.assertEqual (page.strategy, AllTagsSearchStrategy)
    

    def testManySearchPages2 (self):
        TextPageFactory.create (self.rootwiki, GlobalSearch.pageTitle, [])

        GlobalSearch.create (self.rootwiki, 
                phrase = u"декабрь", 
                tags = [u"Метка 1", u"Метка 2"],
                strategy = AllTagsSearchStrategy)

        wiki = WikiDocument.load (self.path)
        page = wiki[GlobalSearch.pageTitle + u" 2"]

        self.assertTrue (page != None)
        #self.assertEqual (wiki.selectedPage, page)
        self.assertEqual (page.phrase, u"декабрь")
        self.assertEqual (len (page.searchTags), 2)
        self.assertTrue (u"Метка 1" in page.searchTags)
        self.assertTrue (u"Метка 2" in page.searchTags)
        self.assertEqual (page.strategy, AllTagsSearchStrategy)
    

    def testManySearchPages3 (self):
        TextPageFactory.create (self.rootwiki, GlobalSearch.pageTitle, [])
        TextPageFactory.create (self.rootwiki, GlobalSearch.pageTitle + u" 2", [])
        TextPageFactory.create (self.rootwiki, GlobalSearch.pageTitle + u" 3", [])
        TextPageFactory.create (self.rootwiki, GlobalSearch.pageTitle + u" 4", [])

        GlobalSearch.create (self.rootwiki, 
                phrase = u"декабрь", 
                tags = [u"Метка 1", u"Метка 2"],
                strategy = AllTagsSearchStrategy)

        wiki = WikiDocument.load (self.path)
        page = wiki[GlobalSearch.pageTitle + u" 5"]

        self.assertTrue (page != None)
        #self.assertEqual (wiki.selectedPage, page)
        self.assertEqual (page.phrase, u"декабрь")
        self.assertEqual (len (page.searchTags), 2)
        self.assertTrue (u"Метка 1" in page.searchTags)
        self.assertTrue (u"Метка 2" in page.searchTags)
        self.assertEqual (page.strategy, AllTagsSearchStrategy)
    

    def testSetPhrase (self):
        """
        Тест на то, что сохраняется искомая фраза
        """
        page = GlobalSearch.create (self.rootwiki)

        self.assertEqual (page.phrase, u"")
        self.assertEqual (page.searchTags, [])

        # Поменяем параметры через свойства
        page.phrase = u"Абырвалг"
        self.assertEqual (page.phrase, u"Абырвалг")

        # Загрузим вики и прочитаем установленные параметры
        wiki = WikiDocument.load (self.path)
        searchPage = wiki[GlobalSearch.pageTitle]

        self.assertTrue (searchPage != None)
        self.assertEqual (searchPage.phrase, u"Абырвалг")

    
    def testSetTags (self):
        """
        Тест на то, что сохраняется искомая фраза
        """
        page = GlobalSearch.create (self.rootwiki)

        self.assertEqual (page.phrase, u"")
        self.assertEqual (page.searchTags, [])

        # Поменяем параметры через свойства
        page.searchTags = [u"тег1", u"тег2"]
        self.assertEqual (page.searchTags, [u"тег1", u"тег2"])

        # Загрузим вики и прочитаем установленные параметры
        wiki = WikiDocument.load (self.path)
        searchPage = wiki[GlobalSearch.pageTitle]

        self.assertTrue (searchPage != None)
        self.assertEqual (searchPage.searchTags, [u"тег1", u"тег2"])
    

    def testSetStrategy1 (self):
        """
        Тест на то, что сохраняется искомая фраза
        """
        page = GlobalSearch.create (self.rootwiki)

        self.assertEqual (page.phrase, u"")
        self.assertEqual (page.searchTags, [])

        # Поменяем параметры через свойства
        page.strategy = AllTagsSearchStrategy
        self.assertEqual (page.strategy, AllTagsSearchStrategy)

        # Загрузим вики и прочитаем установленные параметры
        wiki = WikiDocument.load (self.path)
        searchPage = wiki[GlobalSearch.pageTitle]

        self.assertTrue (searchPage != None)
        self.assertEqual (searchPage.strategy, AllTagsSearchStrategy)
    

    def testSetStrategy2 (self):
        """
        Тест на то, что сохраняется искомая фраза
        """
        page = GlobalSearch.create (self.rootwiki)

        self.assertEqual (page.phrase, u"")
        self.assertEqual (page.searchTags, [])

        # Поменяем параметры через свойства
        page.strategy = AnyTagSearchStrategy
        self.assertEqual (page.strategy, AnyTagSearchStrategy)

        # Загрузим вики и прочитаем установленные параметры
        wiki = WikiDocument.load (self.path)
        searchPage = wiki[GlobalSearch.pageTitle]

        self.assertTrue (searchPage != None)
        self.assertEqual (searchPage.strategy, AnyTagSearchStrategy)
