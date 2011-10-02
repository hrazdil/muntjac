# -*- coding: utf-8 -*-
from com.vaadin.demo.sampler.FeatureSet import (FeatureSet,)
from com.vaadin.demo.sampler.features.windows.SubwindowSized import (SubwindowSized,)
from com.vaadin.demo.sampler.APIResource import (APIResource,)
from com.vaadin.demo.sampler.Feature import (Feature,)
Version = Feature.Version


class SubwindowAutoSized(Feature):

    def getSinceVersion(self):
        return Version.OLD

    def getName(self):
        return 'Window, automatic size'

    def getDescription(self):
        return 'The window will be automatically sized to fit the contents,' + ' if the size of the window (and it\'s layout) is undefined.<br/>' + ' Note that by default Window contains a VerticalLayout that' + ' is 100% wide.'

    def getRelatedAPI(self):
        return [APIResource(Window)]

    def getRelatedFeatures(self):
        return [SubwindowSized, FeatureSet.Windows]

    def getRelatedResources(self):
        return None
