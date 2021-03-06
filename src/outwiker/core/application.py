#!/usr/bin/env python
#-*- coding: utf-8 -*-

from .i18n import init_i18n, getLanguageFromConfig
from .config import Config
from .event import Event
from .recent import RecentWiki
from .pluginsloader import PluginsLoader


class ApplicationParams (object):
    def __init__ (self):
        # Открытая в данный момент wiki
        self.__wikiroot = None

        # Главное окно приложения
        self.__mainWindow = None
        self.config = None
        self.recentWiki = None
        self.plugins = PluginsLoader (self)

        # Создать экземпляры событий

        # Открытие вики
        # Параметр: root - корень новой вики (возможно, None)
        self.onWikiOpen = Event()

        # Закрытие вики
        # Параметр: root - корень закрываемой вики (возможно, None)
        self.onWikiClose = Event()

        # Обновление страницы
        # Параметры: sender
        self.onPageUpdate = Event()

        # Создание страницы
        # Параметры: sender
        self.onPageCreate = Event()

        # Обновление дерева
        # Параметры: sender - из-за кого обновляется дерево
        self.onTreeUpdate = Event()
        
        # Выбор новой страницы
        # Параметры: новая выбранная страница
        self.onPageSelect = Event()

        # Пользователь хочет скопировать выбранные файлы в страницу
        # Параметры: fnames - выбранные имена файлов (basename без путей)
        self.onAttachmentPaste = Event()

        # Изменение списка закладок
        # Параметр - экземпляр класса Bookmarks
        self.onBookmarksChanged = Event()

        # Удаленеи страницы
        # Параметр - удаленная страница
        self.onPageRemove = Event()

        # Переименование страницы.
        # Параметры: page - переименованная страница, oldSubpath - старый относительный путь до страницы
        self.onPageRename = Event()

        # Начало сложного обновления дерева
        # Параметры: root - корень дерева
        self.onStartTreeUpdate = Event()

        # Конец сложного обновления дерева
        # Параметры: root - корень дерева
        self.onEndTreeUpdate = Event()

        # Начало рендеринга HTML
        # Параметры: 
        # page - страница, которую рендерят
        # htmlView - окно, где будет представлен HTML
        self.onHtmlRenderingBegin = Event()

        # Завершение рендеринга HTML
        # Параметры: 
        # page - страница, которую рендерят
        # htmlView - окно, где будет представлен HTML
        self.onHtmlRenderingEnd = Event()

        # Изменение порядка страниц
        # Параметры: page - страница, положение которой изменили
        self.onPageOrderChange = Event()

        # Событие на принудительное сохранение состояния страницы
        # Например, при потере фокуса приложением или по таймеру.
        # Параметры: нет
        self.onForceSave = Event()

        # Событие вызывается после создания википарсера (Parser), но до его использования
        # Параметры: экземпляр Parser
        self.onWikiParserPrepare = Event ()

        # Событие вызывается, когда создается диалог с настройками
        # Параметры: экземпляр класса outwiker.gui.preferences.prefdialog.PrefDialog
        self.onPreferencesDialogCreate = Event()

        # Событие вызывается, когда закрывается диалог с настройками
        # Параметры: экземпляр класса outwiker.gui.preferences.prefdialog.PrefDialog
        self.onPreferencesDialogClose = Event()

        # Событие вызывается после (!) создания представления страницы в CurrentPagePanel
        # Параметры: page - новая выбранная страница,
        self.onPageViewCreate = Event()

        # Событие вызывается перед (!) удалением представления страницы в CurrentPagePanel
        # Параметры: page - текущая выбранная страница,
        self.onPageViewDestroy = Event()

        # Событие вызывается в конце создания всплывающего меню при нажатии правой кнопки на дереве заметок
        # Параметр: menu - созданное всплывающее меню,
        # page - страница, соответствующая заметке, на которую нажали правой кнопкой мыши
        self.onTreePopupMenu = Event()

        # Событие вызывается в конце создания всплывающего меню при нажатии правой кнопки на иконку в трее
        # Параметр: menu - созданное всплывающее меню,
        # tray - экземпля класса OutwikerTrayIcon
        self.onTrayPopupMenu = Event()

    
    def init (self, configFilename):
        """
        Инициализировать конфиг и локаль
        """
        self.config = Config (configFilename)
        self.recentWiki = RecentWiki (self.config)
        self.__initLocale()


    @property
    def wikiroot (self):
        """
        Возвращает корень открытой в данный момент вики или None, если нет открытой вики
        """
        return self.__wikiroot


    @wikiroot.setter
    def wikiroot (self, value):
        """
        Установить текущую вики
        """
        self.onWikiClose (self.__wikiroot)

        if self.__wikiroot != None:
            self.__unbindWikiEvents (self.__wikiroot)

        self.__wikiroot = value

        if self.__wikiroot != None:
            self.__bindWikiEvents (self.__wikiroot)

        self.onWikiOpen (self.__wikiroot)


    @property
    def mainWindow (self):
        """
        Возвращает главное окно программы или None, если оно еще не создано
        """
        return self.__mainWindow


    @mainWindow.setter
    def mainWindow (self, value):
        """
        Установить главное окно программы
        """
        self.__mainWindow = value


    def __bindWikiEvents (self, wiki):
        """
        Подписка на события, связанные с открытой вики для передачи их дальше
        """
        wiki.onPageSelect += self.onPageSelect
        wiki.onPageUpdate += self.onPageUpdate
        wiki.onTreeUpdate += self.onTreeUpdate
        wiki.onStartTreeUpdate += self.onStartTreeUpdate
        wiki.onEndTreeUpdate += self.onEndTreeUpdate
        wiki.onPageOrderChange += self.onPageOrderChange
        wiki.onPageRename += self.onPageRename
        wiki.onPageCreate += self.onPageCreate
        wiki.onPageRemove += self.onPageRemove
        wiki.bookmarks.onBookmarksChanged += self.onBookmarksChanged


    def __unbindWikiEvents (self, wiki):
        """
        Отписаться от события, связанных с открытой вики
        """
        wiki.onPageSelect -= self.onPageSelect
        wiki.onPageUpdate -= self.onPageUpdate
        wiki.onTreeUpdate -= self.onTreeUpdate
        wiki.onStartTreeUpdate -= self.onStartTreeUpdate
        wiki.onEndTreeUpdate -= self.onEndTreeUpdate
        wiki.onPageOrderChange -= self.onPageOrderChange
        wiki.onPageRename -= self.onPageRename
        wiki.onPageCreate -= self.onPageCreate
        wiki.onPageRemove -= self.onPageRemove
        wiki.bookmarks.onBookmarksChanged -= self.onBookmarksChanged


    @property
    def selectedPage (self):
        """
        Вернуть текущую страницу или None, если страница не выбрана или вики не открыта
        """
        if self.__wikiroot == None:
            return None

        return self.__wikiroot.selectedPage


    @selectedPage.setter
    def selectedPage (self, page):
        """
        Установить текущую страницу
        """
        if self.__wikiroot != None and self.__wikiroot.selectedPage != page:
            self.__wikiroot.selectedPage = page


    def __initLocale (self):
        """
        Инициализации локализаций интерфейса
        """
        language = getLanguageFromConfig (self.config)

        try:
            init_i18n (language)
        except IOError:
            print u"Can't load language: %s" % language


Application = ApplicationParams()
