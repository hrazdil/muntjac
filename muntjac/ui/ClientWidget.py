# Copyright (C) 2011 Vaadin Ltd
# Copyright (C) 2011 Richard Lincoln
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


class LoadStyle(object):
    # The widget is included in the initial JS sent to the client.
    EAGER = 'EAGER'

    # Not included in the initial set of widgets, but added to queue from
    # which it will be loaded when network is not busy or the
    # implementation is required.
    DEFERRED = 'DEFERRED'

    # Loaded to the client only if needed.
    LAZY = 'LAZY'


class ClientWidget(object):  # FIXME: implement annotation
    """Annotation defining the default client side counterpart in GWT terminal for
    {@link Component}.
    <p>
    With this annotation server side Vaadin component is marked to have a client
    side counterpart. The value of the annotation is the class of client side
    implementation.
    <p>
    Note, even though client side implementation is needed during development,
    one may safely remove them from the classpath of the production server.
    """

    # the client side counterpart for the annotated component
    value = None

    # Depending on the used WidgetMap generator, these optional hints may be
    # used to define how the client side components are loaded by the browser.
    # The default is to eagerly load all widgets
    # {@link EagerWidgetMapGenerator}, but if the {@link WidgetMapGenerator} is
    # used by the widgetset, these load style hints are respected.
    # <p>
    # Lazy loading of a widget implementation means the client side component
    # is not included in the initial JavaScript application loaded when the
    # application starts. Instead the implementation is loaded to the client
    # when it is first needed. Lazy loaded widget can be achieved by giving
    # {@link LoadStyle#LAZY} value in ClientWidget annotation.
    # <p>
    # Lazy loaded widgets don't stress the size and startup time of the client
    # side as much as eagerly loaded widgets. On the other hand there is a
    # slight latency when lazy loaded widgets are first used as the client side
    # needs to visit the server to fetch the client side implementation.
    # <p>
    # The {@link LoadStyle#DEFERRED} will also not stress the initially loaded
    # JavaScript file. If this load style is defined, the widget implementation
    # is preemptively loaded to the browser after the application is started
    # and the communication to server idles. This load style kind of combines
    # the best of both worlds.
    # <p>
    # Fine tunings to widget loading can also be made by overriding
    # {@link WidgetMapGenerator} in the GWT module. Tunings might be helpful if
    # the end users have slow connections and especially if they have high
    # latency in their network. The {@link CustomWidgetMapGenerator} is an
    # abstract generator implementation for easy customization. Vaadin package
    # also includes {@link LazyWidgetMapGenerator} that makes as many widgets
    # lazily loaded as possible.
    #
    # @return the hint for the widget set generator how the client side
    #         implementation should be loaded to the browser
    loadStyle = LoadStyle.DEFERRED
