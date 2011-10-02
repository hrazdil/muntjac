# -*- coding: utf-8 -*-
from com.vaadin.demo.sampler.features.buttons.ButtonLink import (ButtonLink,)
from com.vaadin.demo.sampler.features.link.LinkCurrentWindow import (LinkCurrentWindow,)
from com.vaadin.demo.sampler.features.link.LinkSizedWindow import (LinkSizedWindow,)
from com.vaadin.demo.sampler.APIResource import (APIResource,)
from com.vaadin.demo.sampler.Feature import (Feature,)
Version = Feature.Version


class LinkNoDecorations(Feature):

    def getSinceVersion(self):
        return Version.OLD

    def getName(self):
        return 'Link, configure window'

    def getDescription(self):
        return 'Links can open new browser windows, and configure the amount of browser features shown, such as toolbar and addressbar.<br/>These links open a browser window without decorations.'

    def getRelatedAPI(self):
        return [APIResource(Link)]

    def getRelatedFeatures(self):
        return [LinkCurrentWindow, LinkSizedWindow, ButtonLink]

    def getRelatedResources(self):
        # TODO Auto-generated method stub
        return None
