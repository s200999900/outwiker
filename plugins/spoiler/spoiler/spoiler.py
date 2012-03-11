#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os.path

from outwiker.core.pluginbase import Plugin
from outwiker.core.system import getOS
from outwiker.pages.wiki.wikipanel import WikiPagePanel

from .commandspoiler import SpoilerCommand


class PluginSpoiler (Plugin):
    """
    Плагин, добавляющий обработку команды spoiler в википарсер
    """
    def __init__ (self, application):
        """
        application - экземпляр класса core.application.ApplicationParams
        """
        Plugin.__init__ (self, application)
        self.__maxCommandIndex = 9


    def __onWikiParserPrepare (self, parser):
        parser.addCommand (SpoilerCommand (parser, "spoiler", _))

        for index in range (self.__maxCommandIndex + 1):
            commandname = "spoiler{index}".format (index=index)
            parser.addCommand (SpoilerCommand (parser, commandname, _) )


    ###################################################
    # Свойства и методы, которые необходимо определить
    ###################################################

    def initialize(self):
        self._application.onWikiParserPrepare += self.__onWikiParserPrepare
        self._application.onPageViewCreate += self.__onPageViewCreate
        self.__initlocale()


    def __initlocale (self):
        domain = u"spoiler"

        langdir = unicode (os.path.join (os.path.dirname (__file__), "locale"), getOS().filesEncoding)
        global _

        try:
            _ = self._init_i18n (domain, langdir)
        except BaseException as e:
            print e


    def __onPageViewCreate(self, page):
        """Обработка события после создания представления страницы"""
        assert self._application.mainWindow != None

        if page.getTypeString() != u"wiki":
            return

        pageView = self.__getPageView()

        helpString = _(u"Collapse text (:spoiler:)")

        pageView.addTool (pageView.commandsMenu, 
                "ID_PLUGIN_SPOILER", 
                self.__onInsertCommand, 
                helpString, 
                helpString, 
                None)


    def __onInsertCommand (self, event):
        startCommand = u'(:spoiler:)\n'
        endCommand = u'\n(:spoilerend:)'

        pageView = self.__getPageView()
        pageView.codeEditor.turnText (startCommand, endCommand)


    def __getPageView (self):
        """
        Получить указатель на панель представления страницы
        """
        pageView = self._application.mainWindow.pagePanel.pageView
        assert type (pageView) == WikiPagePanel

        return pageView


    @property
    def name (self):
        return u"Spoiler"

    
    @property
    def description (self):
        return _(u"Add command (:spoiler:) in wiki parser")


    @property
    def version (self):
        return u"1.0"


    def destroy (self):
        """
        Уничтожение (выгрузка) плагина. Здесь плагин должен отписаться от всех событий
        """
        self._application.onWikiParserPrepare -= self.__onWikiParserPrepare

    #############################################
