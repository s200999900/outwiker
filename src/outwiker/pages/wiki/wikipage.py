#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Необходимые классы для создания страниц с HTML
"""

from outwiker.core.tree import WikiPage
from wikipanel import WikiPagePanel
from wikipreferences import WikiPrefGeneralPanel
from outwiker.core.factory import PageFactory
from outwiker.gui.preferences.preferencepanelinfo import PreferencePanelInfo


class WikiWikiPage (WikiPage):
    """
    Класс wiki-страниц
    """
    def __init__ (self, path, title, parent, readonly = False):
        WikiPage.__init__ (self, path, title, parent, readonly)
    

    @staticmethod
    def getTypeString ():
        return u"wiki"


class WikiPageFactory (PageFactory):
    @staticmethod
    def getPageType():
        return WikiWikiPage

    # Обрабатываемый этой фабрикой тип страниц (имеется в виду тип, описываемый строкой)
    @staticmethod
    def getTypeString ():
        return WikiPageFactory.getPageType().getTypeString()

    # Название страницы, показываемое пользователю
    title = _(u"Wiki Page")


    def __init__ (self):
        pass


    @staticmethod
    def create (parent, title, tags):
        """
        Создать страницу. Вызывать этот метод вместо конструктора
        """
        return PageFactory.createPage (WikiPageFactory.getPageType(), parent, title, tags)


    @staticmethod
    def getPageView (parent):
        """
        Вернуть контрол, который будет отображать и редактировать страницу
        """
        panel = WikiPagePanel (parent)

        return panel


    @staticmethod
    def getPrefPanels (parent):
        """
        Получить список панелей для окна настроек
        Возвращает список кортежей ("название", Панель)
        """
        generalPanel = WikiPrefGeneralPanel (parent)

        return [ PreferencePanelInfo (generalPanel, _(u"General") ) ]

