# -*- coding: utf-8 -*-
from com.vaadin.demo.sampler.features.notifications.NotificationHumanized import (NotificationHumanized,)
from com.vaadin.demo.sampler.features.notifications.NotificationWarning import (NotificationWarning,)
from com.vaadin.demo.sampler.features.notifications.NotificationError import (NotificationError,)
from com.vaadin.demo.sampler.NamedExternalResource import (NamedExternalResource,)
from com.vaadin.demo.sampler.APIResource import (APIResource,)
from com.vaadin.demo.sampler.features.notifications.NotificationCustom import (NotificationCustom,)
from com.vaadin.demo.sampler.Feature import (Feature,)
Version = Feature.Version


class NotificationTray(Feature):

    def getSinceVersion(self):
        return Version.OLD

    def getName(self):
        return 'Tray notification'

    def getDescription(self):
        return '<p>The <i>Tray</i> notification shows up in the lower right corner,' + ' and is meant to interrupt the user as little as possible' + ' even if it\'s shown for a while. ' + 'The <i>Tray</i> message fades away after a few moments' + ' once the user interacts with the application (e.g. moves' + ' mouse, types)</p><p>Candidates for a' + ' <i>Tray</i> notification include \'New message received\',' + ' \'Job XYZ completed\' &ndash; generally notifications about events' + ' that have been delayed, or occur in the background' + ' (as opposed to being a direct result of the users last action.)</p>'

    def getRelatedAPI(self):
        return [APIResource(Window), APIResource(Window.Notification)]

    def getRelatedFeatures(self):
        return [NotificationHumanized, NotificationWarning, NotificationError, NotificationCustom]

    def getRelatedResources(self):
        return [NamedExternalResource('Monolog Boxes and Transparent Messages', 'http://humanized.com/weblog/2006/09/11/monolog_boxes_and_transparent_messages/')]
