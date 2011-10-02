# -*- coding: utf-8 -*-
from com.vaadin.demo.sampler.features.upload.ImmediateUpload import (ImmediateUpload,)
from com.vaadin.demo.sampler.features.upload.UploadWithProgressMonitoring import (UploadWithProgressMonitoring,)
from com.vaadin.demo.sampler.APIResource import (APIResource,)
from com.vaadin.demo.sampler.Feature import (Feature,)
Version = Feature.Version


class UploadBasic(Feature):

    def getSinceVersion(self):
        return Version.OLD

    def getDescription(self):
        return 'Upload component provides a method to handle ' + 'files uploaded from clients. ' + 'In this example we simply be ' + 'count line breaks of the uploaded file.' + 'The data could just as well be saved on ' + 'the server as file or inserted into a database.'

    def getName(self):
        return 'Basic upload'

    def getRelatedAPI(self):
        return [APIResource(Upload)]

    def getRelatedFeatures(self):
        return [ImmediateUpload, UploadWithProgressMonitoring]

    def getRelatedResources(self):
        # TODO Auto-generated method stub
        return None
