��          D      l       �   �  �      #     ,     F  �  M  �  �     �	  )   �	     
                          Add command (:spoiler:) in wiki parser.

<B>Usage:</B>
<PRE>(:spoiler:)
Text
(:spoilerend:)</PRE>

For nested spoilers use (:spoiler0:), (:spoiler1:)... (:spoiler9:) commands. 

<U>Example:</U>

<PRE>(:spoiler:)
Text
&nbsp;&nbsp;&nbsp;(:spoiler1:)
&nbsp;&nbsp;&nbsp;Nested spoiler
&nbsp;&nbsp;&nbsp;(:spoiler1end:)
(:spoilerend:)</PRE>

<B>Params:</B>
<U>inline</U> - Spoiler will be in inline mode.
<U>expandtext</U> - Link text for the collapsed spoiler. Default: "Expand".
<U>collapsetext</U> - Link text for the expanded spoiler. Default: "Collapse".

<U>Example:</U>

<PRE>(:spoiler expandtext="More..." collapsetext="Less" inline :)
Text
(:spoilerend:)</PRE>
 Collapse Collapse text (:spoiler:) Expand Project-Id-Version: spoiler
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2012-04-25 22:02+0400
PO-Revision-Date: 2012-04-25 22:07+0300
Last-Translator: Jenyay <jenyay.ilin@gmail.com>
Language-Team: Jenyay <jenyay.ilin@gmail.com>
Language: 
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
X-Poedit-Language: Russian
X-Poedit-Country: RUSSIAN FEDERATION
X-Poedit-SourceCharset: utf-8
 Добавляет вики-команду (:spoiler:) для скрытия части текста на странице (вставка спойлеров).

<B>Использование:</B>
<PRE>(:spoiler:)
Текст
(:spoilerend:)</PRE>

Для вложенных спойлеров используйте команды (:spoiler0:), (:spoiler1:)... (:spoiler9:). 

<U>Пример:</U>

<PRE>(:spoiler:)
Текст
&nbsp;&nbsp;&nbsp;(:spoiler1:)
&nbsp;&nbsp;&nbsp;Вложенный спойлер
&nbsp;&nbsp;&nbsp;(:spoiler1end:)
(:spoilerend:)</PRE>

<B>Параметры:</B>
<U>inline</U> - Спойлер будет оформлен в виде текста без выделения блока.
<U>expandtext</U> - Текст для ссылок, который будет показан, пока спойлер свернут. Значение по умолчанию: "Развернуть".
<U>collapsetext</U> - Текст для ссылок, который будет показан, пока спойлер развернут. Значение по умолчанию: "Свернуть".

<U>Пример:</U>

<PRE>(:spoiler expandtext="Раскукожить" collapsetext="Скукожить" inline:)
Текст
(:spoilerend:)</PRE>
 Свернуть Свёрнутый текст (:spoiler:) Развернуть 