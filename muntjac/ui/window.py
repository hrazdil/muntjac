# Copyright (C) 2010 IT Mill Ltd.
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

from urlparse import urljoin

from muntjac.event.shortcut_listener import ShortcutListener
from muntjac.terminal.URIHandler import IUriHandler
from muntjac.terminal.gwt.client.ui.VView import VView
from muntjac.terminal.ParameterHandler import IParameterHandler
from muntjac.terminal.Sizeable import ISizeable
from muntjac.terminal.gwt.client.ui.VWindow import VWindow

from muntjac.ui.ClientWidget import LoadStyle
from muntjac.ui.panel import Panel
from muntjac.ui.component import Event as ComponentEvent
from muntjac.ui.abstract_component import AbstractComponent

from muntjac.event.field_events import \
    (IFocusNotifier, IBlurNotifier, FocusEvent, BlurEvent)


class ICloseListener(object):
    """An interface used for listening to Window close events. Add the
    ICloseListener to a browser level window or a sub window and
    {@link ICloseListener#windowClose(CloseEvent)} will be called whenever
    the user closes the window.

    Since Vaadin 6.5, removing windows using {@link #removeWindow(Window)}
    does fire the ICloseListener.
    """

    def windowClose(self, e):
        """Called when the user closes a window. Use
        {@link CloseEvent#getWindow()} to get a reference to the
        {@link Window} that was closed.

        @param e: Event containing
        """
        raise NotImplementedError


class IResizeListener(object):
    """Listener for window resize events.

    @see com.vaadin.ui.Window.ResizeEvent
    """

    def windowResized(self, e):
        raise NotImplementedError


class Window(Panel, IUriHandler, IParameterHandler, IFocusNotifier,
            IBlurNotifier):
    """A component that represents an application (browser native) window or
    a sub window.

    If the window is a application window or a sub window depends on how it
    is added to the application. Adding a {@code Window} to a {@code Window}
    using {@link Window#addWindow(Window)} makes it a sub window and adding a
    {@code Window} to the {@code Application} using
    {@link Application#addWindow(Window)} makes it an application window.

    An application window is the base of any view in a Vaadin application. All
    applications contain a main application window (set using
    {@link Application#setMainWindow(Window)} which is what is initially shown
    to the user. The contents of a window is set using
    {@link #setContent(ComponentContainer)}. The contents can in turn contain
    other components. For multi-tab applications there is one window instance
    per opened tab.

    A sub window is floating popup style window that can be added to an
    application window. Like the application window its content is set using
    {@link #setContent(ComponentContainer)}. A sub window can be positioned on
    the screen using absolute coordinates (pixels). The default content of the
    Window is set to be suitable for application windows. For sub windows it
    might be necessary to set the size of the content to work as expected.

    Window caption is displayed in the browser title bar for application level
    windows and in the window header for sub windows.

    Certain methods in this class are only meaningful for sub windows and other
    parts only for application windows. These are marked using <b>Sub window
    only</b> and <b>Application window only</b> respectively in the javadoc.

    Sub window is to be split into a separate component in Vaadin 7.

    @author IT Mill Ltd.
    @author Richard Lincoln
    @version @VERSION@
    @since 3.0
    """

    #CLIENT_WIDGET = ClientWidget(VWindow, LoadStyle.EAGER)

    # <b>Application window only</b>. A border style used for opening
    # resources in a window without a border.
    BORDER_NONE = 0

    # <b>Application window only</b>. A border style used for opening
    # resources in a window with a minimal border.
    BORDER_MINIMAL = 1

    # <b>Application window only</b>. A border style that indicates that
    # the default border style should be used when opening resources.
    BORDER_DEFAULT = 2


    def __init__(self, caption='', content=None):
        """Creates a new unnamed window with the given content and title.

        @param caption
                   the title of the window.
        @param content
                   the contents of the window
        """

        # <b>Application window only</b>. The user terminal for this window.
        self._terminal = None

        # <b>Application window only</b>. The application this window is
        # attached to or null.
        self._application = None

        # <b>Application window only</b>. List of URI handlers for this
        # window.
        self._uriHandlerList = None

        # <b>Application window only</b>. List of parameter handlers for
        # this window.
        self._parameterHandlerList = None

        # <b>Application window only</b>. List of sub windows in this window.
        # A sub window cannot have other sub windows.
        self._subwindows = set()

        # <b>Application window only</b>. Explicitly specified theme of this
        # window or null if the application theme should be used.
        self._theme = None

        # <b>Application window only</b>. Resources to be opened automatically
        # on next repaint. The list is automatically cleared when it has been
        # sent to the client.
        self._openList = list()

        # <b>Application window only</b>. Unique name of the window used to
        # identify it.
        self._name = None

        # <b>Application window only.</b> Border mode of the Window.
        self._border = self.BORDER_DEFAULT

        # <b>Sub window only</b>. Top offset in pixels for the sub window
        # (relative to the parent application window) or -1 if unspecified.
        self._positionY = -1

        # <b>Sub window only</b>. Left offset in pixels for the sub window
        # (relative to the parent application window) or -1 if unspecified.
        self._positionX = -1

        # <b>Application window only</b>. A list of notifications that are
        # waiting to be sent to the client. Cleared (set to null) when the
        # notifications have been sent.
        self._notifications = None

        # <b>Sub window only</b>. Modality flag for sub window.
        self._modal = False

        # <b>Sub window only</b>. Controls if the end user can resize the
        # window.
        self._resizable = True

        # <b>Sub window only</b>. Controls if the end user can move the
        # window by dragging.
        self._draggable = True

        # <b>Sub window only</b>. Flag which is true if the window is
        # centered on the screen.
        self._centerRequested = False

        # Should resize recalculate layouts lazily (as opposed to immediately)
        self._resizeLazy = False

        # Component that should be focused after the next repaint. Null if no
        # focus change should take place.
        self._pendingFocus = None

        # <b>Application window only</b>. A list of javascript commands that
        # are waiting to be sent to the client. Cleared (set to null) when the
        # commands have been sent.
        self._jsExecQueue = None

        # The component that should be scrolled into view after the next
        # repaint. Null if nothing should be scrolled into view.
        self._scrollIntoView = None

        super(Window, self)(caption, content)

        self.setScrollable(True)

        self.setSizeUndefined()

        self._bringToFront = None

        # This sequesnce is used to keep the right order of windows if
        # multiple windows are brought to front in a single changeset.
        # Incremented and saved by childwindows. If sequence is not used,
        # the order is quite random (depends on the order getting to dirty
        # list. e.g. which window got variable changes).
        self._bringToFrontSequence = 0

        self.closeShortcut = None


    def addComponent(self, c):
        if isinstance(c, Window):
            raise ValueError, ('Window cannot be added to another '
                    'via addComponent. Use addWindow(Window) instead.')
        super(Window, self).addComponent(c)


    def getTerminal(self):
        """<b>Application window only</b>. Gets the user terminal.

        @return the user terminal
        """
        return self._terminal


    def getWindow(self):
        """Gets the parent window of the component.

        This is always the window itself.

        @see Component#getWindow()
        @return the window itself
        """
        return self


    def getApplication(self):
        if self.getParent() is None:
            return self._application

        return self.getParent().getApplication()


    def getParent(self):
        """Gets the parent component of the window.

        The parent of an application window is always null. The parent of a
        sub window is the application window the sub window is attached to.

        @return the parent window
        @see Component#getParent()
        """
        return super(Window, self).getParent()


    def addURIHandler(self, handler):
        """<b>Application window only</b>. Adds a new URI handler to this
        window. If this is a sub window the URI handler is attached to the
        parent application window.

        @param handler
                   the URI handler to add.
        """
        if self.getParent() is not None:
            # this is subwindow, attach to main level instead
            # TODO hold internal list also and remove on detach
            mainWindow = self.getParent()
            mainWindow.addURIHandler(handler)
        else:
            if self._uriHandlerList is None:
                self._uriHandlerList = list()
            if handler not in self._uriHandlerList:
                self._uriHandlerList.append(handler)


    def removeURIHandler(self, handler):
        """<b>Application window only</b>. Removes the URI handler from this
        window. If this is a sub window the URI handler is removed from the
        parent application window.

        @param handler
                   the URI handler to remove.
        """
        if self.getParent() is not None:
            # this is subwindow
            mainWindow = self.getParent()
            mainWindow.removeURIHandler(handler)
        else:
            if handler is None or self._uriHandlerList is None:
                return
            self._uriHandlerList.remove(handler)
            if len(self._uriHandlerList) == 0:
                self._uriHandlerList = None


    def handleURI(self, context, relativeUri):
        """<b>Application window only</b>. Handles an URI by passing the URI
        to all URI handlers defined using {@link #addURIHandler(IUriHandler)}.
        All URI handlers are called for each URI but no more than one handler
        may return a {@link DownloadStream}. If more than one stream is
        returned a {@code RuntimeException} is thrown.

        @param context
                   The URL of the application
        @param relativeUri
                   The URI relative to {@code context}
        @return A {@code DownloadStream} that one of the URI handlers
                returned, null if no {@code DownloadStream} was returned.
        """
        result = None

        if self._uriHandlerList is not None:
            handlers = list(self._uriHandlerList)

            for handler in handlers:
                ds = handler.handleURI(context, relativeUri)
                if ds is not None:
                    if result is not None:
                        raise RuntimeError(('handleURI for ' + context
                                + ' uri: \'' + relativeUri
                                + '\' returns ambigious result.'))
                    result = ds

        return result


    def addParameterHandler(self, handler):
        """<b>Application window only</b>. Adds a new parameter handler to
        this window. If this is a sub window the parameter handler is attached
        to the parent application window.

        @param handler
                   the parameter handler to add.
        """
        if self.getParent() is not None:
            # this is subwindow
            # TODO hold internal list also and remove on detach
            mainWindow = self.getParent()
            mainWindow.addParameterHandler(handler)
        else:
            if self._parameterHandlerList is None:
                self._parameterHandlerList = list()
            if handler not in self._parameterHandlerList:
                self._parameterHandlerList.addLast(handler)


    def removeParameterHandler(self, handler):
        """<b>Application window only</b>. Removes the parameter handler from
        this window. If this is a sub window the parameter handler is removed
        from the parent application window.

        @param handler
                   the parameter handler to remove.
        """
        if self.getParent() is not None:
            # this is subwindow
            mainWindow = self.getParent()
            mainWindow.removeParameterHandler(handler)
        else:
            if handler is None or self._parameterHandlerList is None:
                return
            self._parameterHandlerList.remove(handler)
            if len(self._parameterHandlerList) == 0:
                self._parameterHandlerList = None


    def handleParameters(self, parameters):
        """<b>Application window only</b>. Handles parameters by passing the
        parameters to all {@code IParameterHandler}s defined using
        {@link #addParameterHandler(IParameterHandler)}. All
        {@code IParameterHandler}s are called for each set of parameters.

        @param parameters
                   a map containing the parameter names and values
        @see IParameterHandler#handleParameters(Map)
        """
        if self._parameterHandlerList is not None:
            handlers = list(self._parameterHandlerList)
            for handler in handlers:
                handler.handleParameters(parameters)


    def getTheme(self):
        """<b>Application window only</b>. Gets the theme for this window.

        If the theme for this window is not explicitly set, the application
        theme name is returned. If the window is not attached to an
        application, the terminal default theme name is returned. If the theme
        name cannot be determined, null is returned

        Subwindows do not support themes and return the theme used by the
        parent window

        @return the name of the theme used for the window
        """
        if self.getParent() is not None:
            return self.getParent().getTheme()

        if self._theme is not None:
            return self._theme

        if self._application is not None \
                and self._application.getTheme() is not None:
            return self._application.getTheme()

        if self._terminal is not None:
            return self._terminal.getDefaultTheme()

        return None


    def setTheme(self, theme):
        """<b>Application window only</b>. Sets the name of the theme to
        use for this window. Changing the theme will cause the page to be
        reloaded.

        @param theme
                   the name of the new theme for this window or null to
                   use the application theme.
        """
        if self.getParent() is not None:
            raise NotImplementedError, \
                    'Setting theme for sub-windows is not supported.'
        self._theme = theme
        self.requestRepaint()


    def paintContent(self, target):
        # Sets the window name
        name = self.getName()
        target.addAttribute('name', '' if name is None else name)

        # Sets the window theme
        theme = self.getTheme()
        target.addAttribute('theme', '' if theme is None else theme)

        if self._modal:
            target.addAttribute('modal', True)

        if self._resizable:
            target.addAttribute('resizable', True)

        if self._resizeLazy:
            target.addAttribute(VView.RESIZE_LAZY, self._resizeLazy)

        if not self._draggable:
            # Inverted to prevent an extra attribute for
            # almost all sub windows
            target.addAttribute('fixedposition', True)

        if self._bringToFront is not None:
            target.addAttribute('bringToFront', int(self._bringToFront))
            self._bringToFront = None

        if self._centerRequested:
            target.addAttribute('center', True)
            self._centerRequested = False

        if self._scrollIntoView is not None:
            target.addAttribute('scrollTo', self._scrollIntoView)
            self._scrollIntoView = None

        # Marks the main window
        if (self.getApplication() is not None
                and self == self.getApplication().getMainWindow()):
            target.addAttribute('main', True)

        if self.getContent() is not None:
            if (self.getContent().getHeightUnits()
                        == ISizeable.UNITS_PERCENTAGE):
                target.addAttribute('layoutRelativeHeight', True)

            if (self.getContent().getWidthUnits()
                        == ISizeable.UNITS_PERCENTAGE):
                target.addAttribute('layoutRelativeWidth', True)

        # Open requested resource
        if len(self._openList) > 0:
            for ol in self._openList:
                ol.paintContent(target)
            self._openList.clear()

        # Contents of the window panel is painted
        super(Window, self).paintContent(target)

        # Add executable javascripts if needed
        if self._jsExecQueue is not None:
            for script in self._jsExecQueue:
                target.startTag('execJS')
                target.addAttribute('script', script)
                target.endTag('execJS')
            self._jsExecQueue = None

        # Window position
        target.addVariable(self, 'positionx', self.getPositionX())
        target.addVariable(self, 'positiony', self.getPositionY())

        # Window closing
        target.addVariable(self, 'close', False)

        if self.getParent() is None:
            # Paint subwindows
            for w in self._subwindows:
                w.paint(target)
        else:
            # mark subwindows
            target.addAttribute('sub', True)

        # Paint notifications
        if self._notifications is not None:
            target.startTag('notifications')
            for n in self._notifications:
                target.startTag('notification')
                if n.getCaption() is not None:
                    target.addAttribute('caption', n.getCaption())

                if n.getMessage() is not None:
                    target.addAttribute('message', n.getMessage())

                if n.getIcon() is not None:
                    target.addAttribute('icon', n.getIcon())

                target.addAttribute('position', n.getPosition())
                target.addAttribute('delay', n.getDelayMsec())

                if n.getStyleName() is not None:
                    target.addAttribute('style', n.getStyleName())

                target.endTag('notification')

            target.endTag('notifications')
            self._notifications = None

        if self._pendingFocus is not None:
            # ensure focused component is still attached to this main window
            if (self._pendingFocus.getWindow() == self
                    or self._pendingFocus.getWindow() is not None
                    and self._pendingFocus.getWindow().getParent() == self):
                target.addAttribute('focused', self._pendingFocus)

            self._pendingFocus = None


    def scrollIntoView(self, component):
        """Scrolls any component between the component and window to a
        suitable position so the component is visible to the user. The given
        component must be inside this window.

        @param component
                   the component to be scrolled into view
        @throws IllegalArgumentException
                    if {@code component} is not inside this window
        """
        if component.getWindow() != self:
            raise ValueError, ('The component where to scroll '
                    'must be inside this window.')
        self._scrollIntoView = component
        self.requestRepaint()


    def open(self, resource, windowName=None, width=-1, height=-1,
            border=None):  #@PydevCodeAnalysisIgnore
        """Opens the given resource in this window. The contents of this
        Window is replaced by the {@code Resource}.

        @param resource
                   the resource to show in this window
        ---
        Opens the given resource in a window with the given name.
        <p>
        The supplied {@code windowName} is used as the target name in a
        window.open call in the client. This means that special values such as
        "_blank", "_self", "_top", "_parent" have special meaning. An empty or
        <code>null</code> window name is also a special case.

        "", null and "_self" as {@code windowName} all causes the resource to
        be opened in the current window, replacing any old contents. For
        downloadable content you should avoid "_self" as "_self" causes the
        client to skip rendering of any other changes as it considers them
        irrelevant (the page will be replaced by the resource). This can speed
        up the opening of a resource, but it might also put the client side
        into an inconsistent state if the window content is not completely
        replaced e.g., if the resource is downloaded instead of displayed in
        the browser.

        "_blank" as {@code windowName} causes the resource to always be opened
        in a new window or tab (depends on the browser and browser settings).

        "_top" and "_parent" as {@code windowName} works as specified by the
        HTML standard.

        Any other {@code windowName} will open the resource in a window with
        that name, either by opening a new window/tab in the browser or by
        replacing the contents of an existing window with that name.

        @param resource
                   the resource.
        @param windowName
                   the name of the window.
        ---
        Opens the given resource in a window with the given size, border and
        name. For more information on the meaning of {@code windowName}, see
        {@link #open(Resource, String)}.

        @param resource
                   the resource.
        @param windowName
                   the name of the window.
        @param width
                   the width of the window in pixels
        @param height
                   the height of the window in pixels
        @param border
                   the border style of the window. See {@link #BORDER_NONE
                   Window.BORDER_* constants}
        """
        if border is None:
            border = self.BORDER_DEFAULT

        if resource not in self._openList:
            r = OpenResource(resource, windowName, width, height, border)
            self._openList.append(r)

        self.requestRepaint()


    def getURL(self):
        """Gets the full URL of the window. The returned URL is window
        specific and can be used to directly refer to the window.

        Note! This method can not be used for portlets.

        @return the URL of the window or null if the window is not attached
                to an application
        """
        if self._application is None:
            return None

        try:
            # FIXME: URL
            return urljoin(self._application.getURL(), self.getName() + '/')
        except Exception:
            raise RuntimeError, \
                    'Internal problem getting window URL, please report'


    def getName(self):
        """<b>Application window only</b>. Gets the unique name of the window.
        The name of the window is used to uniquely identify it.

        The name also determines the URL that can be used for direct access to
        a window. All windows can be accessed through
        {@code http://host:port/app/win} where {@code http://host:port/app} is
        the application URL (as returned by {@link Application#getURL()} and
        {@code win} is the window name.

        Note! Portlets do not support direct window access through URLs.

        @return the Name of the Window.
        """
        return self._name


    def getBorder(self):
        """Returns the border style of the window.

        @see #setBorder(int)
        @return the border style for the window
        """
        return self._border


    def setBorder(self, border):
        """Sets the border style for this window. Valid values are
        {@link Window#BORDER_NONE}, {@link Window#BORDER_MINIMAL},
        {@link Window#BORDER_DEFAULT}.

        <b>Note!</b> Setting this seems to currently have no effect
        whatsoever on the window.

        @param border
                   the border style to set
        """
        self._border = border


    def setApplication(self, application):
        """Sets the application this window is attached to.

        This method is called by the framework and should not be called
        directly from application code. {@link Application#addWindow(Window)}
        should be used to add the window to an application and
        {@link com.vaadin.Application#removeWindow(Window)} to remove the
        window from the application.

        This method invokes {@link Component#attach()} and
        {@link Component#detach()} methods when necessary.

        @param application
                   the application the window is attached to
        """
        # If the application is not changed, dont do nothing
        if application == self._application:
            return

        # Sends detach event if the window is connected to application
        if self._application is not None:
            self.detach()

        # Connects to new parent
        self._application = application

        # Sends the attach event if connected to a window
        if application is not None:
            self.attach()


    def setName(self, name):
        """<b>Application window only</b>. Sets the unique name of the window.
        The name of the window is used to uniquely identify it inside the
        application.

        The name also determines the URL that can be used for direct access to
        a window. All windows can be accessed through
        {@code http://host:port/app/win} where {@code http://host:port/app} is
        the application URL (as returned by {@link Application#getURL()} and
        {@code win} is the window name.

        This method can only be called before the window is added to an
        application.

        Note! Portlets do not support direct window access through URLs.

        @param name
                   the new name for the window or null if the application
                   should automatically assign a name to it
        @throws IllegalStateException
                    if the window is attached to an application
        """
        # The name can not be changed in application
        if self.getApplication() is not None:
            raise ValueError, ('Window name can not be changed while '
                    'the window is in application')
        self._name = name


    def setTerminal(self, typ):
        """Sets the user terminal. Used by the terminal adapter, should never
        be called from application code.

        @param type
                   the terminal to set.
        """
        self._terminal = typ


    def changeVariables(self, source, variables):

        sizeHasChanged = False
        # size is handled in super class, but resize events only in windows ->
        # so detect if size change occurs before super.changeVariables()
        if ('height' in variables
                and (self.getHeightUnits() != self.UNITS_PIXELS
                     or variables.get('height') != self.getHeight())):
            sizeHasChanged = True

        if ('width' in variables
                and (self.getWidthUnits() != self.UNITS_PIXELS
                     or variables['width'] != self.getWidth())):
            sizeHasChanged = True

        super(Window, self).changeVariables(source, variables)

        # Positioning
        positionx = variables.get('positionx')
        if positionx is not None:
            x = int(positionx)
            # This is information from the client so it is already using the
            # position. No need to repaint.
            self.setPositionX(-1 if x < 0 else x, False)

        positiony = variables.get('positiony')
        if positiony is not None:
            y = int(positiony)
            # This is information from the client so it is already using the
            # position. No need to repaint.
            self.setPositionY(-1 if y < 0 else y, False)

        if self.isClosable():
            # Closing
            close = variables.get('close')
            if close is not None and bool(close):
                close()

        # fire event if size has really changed
        if sizeHasChanged:
            self.fireResize()

        if FocusEvent.EVENT_ID in variables:
            self.fireEvent( FocusEvent(self) )

        elif BlurEvent.EVENT_ID in variables:
            self.fireEvent( BlurEvent(self) )


    def close(self):
        """Method that handles window closing (from UI).

        By default, sub-windows are removed from their respective parent
        windows and thus visually closed on browser-side. Browser-level windows
        also closed on the client-side, but they are not implicitly removed
        from the application.

        To explicitly close a sub-window, use {@link #removeWindow(Window)}.
        To react to a window being closed (after it is closed), register a
        {@link ICloseListener}.
        """
        parent = self.getParent()
        if parent is None:
            self.fireClose()
        else:
            # focus is restored to the parent window
            parent.focus()

            # subwindow is removed from parent
            parent.removeWindow(self)


    def getPositionX(self):
        """Gets the distance of Window left border in pixels from left border
        of the containing (main window).

        @return the Distance of Window left border in pixels from left border
                of the containing (main window). or -1 if unspecified.
        @since 4.0.0
        """
        return self._positionX


    def setPositionX(self, positionX, repaintRequired=True):
        """Sets the distance of Window left border in pixels from left border
        of the containing (main window).

        @param positionX
                   the Distance of Window left border in pixels from
                   left border of the containing (main window). or -1
                   if unspecified.
        @param repaintRequired
                   true if the window needs to be repainted, false otherwise
        @since 6.3.4
        """
        self._positionX = positionX
        self._centerRequested = False
        if repaintRequired:
            self.requestRepaint()


    def getPositionY(self):
        """Gets the distance of Window top border in pixels from top border
        of the containing (main window).

        @return Distance of Window top border in pixels from top border of
                the containing (main window). or -1 if unspecified.

        @since 4.0.0
        """
        return self._positionY


    def setPositionY(self, positionY, repaintRequired=True):
        """Sets the distance of Window top border in pixels from top border
        of the containing (main window).

        @param positionY
                   the Distance of Window top border in pixels from top border
                   of the containing (main window). or -1 if unspecified

        @since 4.0.0
        ---
        Sets the distance of Window top border in pixels from top border of
        the containing (main window).

        @param positionY
                   the Distance of Window top border in pixels from top border
                   of the containing (main window). or -1 if unspecified
        @param repaintRequired
                   true if the window needs to be repainted, false otherwise

        @since 6.3.4
        """
        self._positionY = positionY
        self._centerRequested = False
        if repaintRequired:
            self.requestRepaint()


    _WINDOW_CLOSE_METHOD = getattr(ICloseListener, 'windowClose')


    def addListener(self, listener):
        """Adds a ICloseListener to the window.

        For a sub window the ICloseListener is fired when the user closes it
        (clicks on the close button).

        For a browser level window the ICloseListener is fired when the
        browser level window is closed. Note that closing a browser level
        window does not mean it will be destroyed.

        <p>
        Since Vaadin 6.5, removing windows using {@link #removeWindow(Window)}
        does fire the ICloseListener.
        </p>

        @param listener
                   the ICloseListener to add.
        ---
        Add a resize listener.

        @param listener
        ---
        Note, that focus/blur listeners in Window class are only supported by
        sub windows. Also note that Window is not considered focused if its
        contained component currently has focus.

        @see FieldEvents.IFocusNotifier.addListener()
        ---
        Note, that focus/blur listeners in Window class are only supported by sub
        windows. Also note that Window is not considered focused if its contained
        component currently has focus.

        @see FieldEvents.IBlurNotifier.addListener()
        """
        if isinstance(listener, IBlurListener):
            AbstractComponent.addListener(self, BlurEvent.EVENT_ID,
                    BlurEvent, listener, IBlurListener.blurMethod)
        elif isinstance(listener, ICloseListener):
            AbstractComponent.addListener(self, CloseEvent, listener,
                    self._WINDOW_CLOSE_METHOD)
        elif isinstance(listener, IFocusListener):
            AbstractComponent.addListener(self, FocusEvent.EVENT_ID,
                    FocusEvent, listener, IFocusListener.focusMethod)
        else:
            AbstractComponent.addListener(self, ResizeEvent, listener,
                    self._WINDOW_RESIZE_METHOD)


    def removeListener(self, listener):
        """Removes the ICloseListener from the window.

        For more information on CloseListeners see {@link ICloseListener}.

        @param listener
                   the ICloseListener to remove.
        ---
        Remove a resize listener.

        @param listener
        """
        if isinstance(listener, IBlurListener):
            AbstractComponent.removeListener(self, BlurEvent.EVENT_ID,
                    BlurEvent, listener)
        elif isinstance(listener, ICloseListener):
            AbstractComponent.removeListener(self, CloseEvent, listener,
                    self._WINDOW_CLOSE_METHOD)
        elif isinstance(listener, IFocusListener):
            AbstractComponent.removeListener(self, FocusEvent.EVENT_ID,
                    FocusEvent, listener)
        else:
            AbstractComponent.removeListener(self, ResizeEvent, listener)


    def fireClose(self):
        # Method for the resize event.
        self.fireEvent( CloseEvent(self) )


    _WINDOW_RESIZE_METHOD = getattr(IResizeListener, 'windowResized')


    def fireResize(self):
        """Fire the resize event."""
        self.fireEvent( ResizeEvent(self) )


    def attachWindow(self, w):
        self._subwindows.add(w)
        w.setParent(self)
        self.requestRepaint()


    def addWindow(self, window):
        """Adds a window inside another window.

        Adding windows inside another window creates "subwindows". These
        windows should not be added to application directly and are not
        accessible directly with any url. Addding windows implicitly sets
        their parents.

        Only one level of subwindows are supported. Thus you can add windows
        inside such windows whose parent is <code>null</code>.

        @param window
        @throws IllegalArgumentException
                    if a window is added inside non-application level window.
        @throws NullPointerException
                    if the given <code>Window</code> is <code>null</code>.
        """
        if window is None:
            raise ValueError, 'Argument must not be null'

        if window.getApplication() is not None:
            raise ValueError, ('Window was already added to application'
                    ' - it can not be added to another window also.')

        elif self.getParent() is not None:
            raise ValueError, ('You can only add windows inside '
                    'application-level windows.')

        elif len(window.subwindows) > 0:
            raise ValueError, 'Only one level of subwindows are supported.'

        self.attachWindow(window)


    def removeWindow(self, window):
        """Remove the given subwindow from this window.

        Since Vaadin 6.5, {@link ICloseListener}s are called also when
        explicitly removing a window by calling this method.

        Since Vaadin 6.5, returns a boolean indicating if the window was
        removed or not.

        @param window
                   Window to be removed.
        @return true if the subwindow was removed, false otherwise
        """
        if not self._subwindows.remove(window):
            # Window window is not a subwindow of this window.
            return False

        window.setParent(None)
        window.fireClose()
        self.requestRepaint()

        return True


    def bringToFront(self):
        """If there are currently several sub windows visible, calling this
        method makes this window topmost.

        This method can only be called if this window is a sub window and
        connected a top level window. Else an illegal state exception is
        thrown. Also if there are modal windows and this window is not modal,
        and illegal state exception is thrown.

        <strong> Note, this API works on sub windows only. Browsers can't
        reorder OS windows.</strong>
        """
        parent = self.getParent()
        if parent is None:
            raise ValueError, ('Window must be attached to parent '
                    'before calling bringToFront method.')

        for w in parent.getChildWindows():
            if w.isModal() and not self.isModal():
                raise ValueError, ('There are modal windows currently '
                    'visible, non-modal window cannot be brought to front.')

        self._bringToFront = self.getParent().bringToFrontSequence

        self.getParent().bringToFrontSequence = \
                self.getParent().bringToFrontSequence + 1

        self.requestRepaint()


    def getChildWindows(self):
        """Get the set of all child windows.

        @return Set of child windows.
        """
        return set(self._subwindows)


    def setModal(self, modality):
        """Sets sub-window modal, so that widgets behind it cannot be
        accessed.
        <b>Note:</b> affects sub-windows only.

        @param modality
                   true if modality is to be turned on
        """
        self._modal = modality
        self.center()
        self.requestRepaint()


    def isModal(self):
        """@return true if this window is modal."""
        return self._modal


    def setResizable(self, resizeability):
        """Sets sub-window resizable. <b>Note:</b> affects sub-windows only.

        @param resizable
                   true if resizability is to be turned on
        """
        self._resizable = resizeability
        self.requestRepaint()


    def isResizable(self):
        """@return true if window is resizable by the end-user, otherwise
        false."""
        return self._resizable


    def isResizeLazy(self):
        """@return true if a delay is used before recalculating sizes,
                   false if sizes are recalculated immediately.
        """
        return self._resizeLazy


    def setResizeLazy(self, resizeLazy):
        """Should resize operations be lazy, i.e. should there be a delay
        before layout sizes are recalculated. Speeds up resize operations
        in slow UIs with the penalty of slightly decreased usability.

        Note, some browser send false resize events for the browser window
        and are therefore always lazy.

        @param resizeLazy
                   true to use a delay before recalculating sizes, false to
                   calculate immediately.
        """
        self._resizeLazy = resizeLazy
        self.requestRepaint()


    def center(self):
        """Request to center this window on the screen. <b>Note:</b> affects
        sub-windows only.
        """
        self._centerRequested = True
        self.requestRepaint()


    def showNotification(self, *args):
        """Shows a notification message on the middle of the window. The
        message automatically disappears ("humanized message").

        @see #showNotification(com.vaadin.ui.Window.Notification)
        @see Notification

        @param caption
                   The message
        ---
        Shows a notification message the window. The position and behavior
        of the message depends on the type, which is one of the basic types
        defined in {@link Notification}, for instance
        Notification.TYPE_WARNING_MESSAGE.

        @see #showNotification(com.vaadin.ui.Window.Notification)
        @see Notification

        @param caption
                   The message
        @param type
                   The message type
        ---
        Shows a notification consisting of a bigger caption and a smaller
        description on the middle of the window. The message automatically
        disappears ("humanized message").

        @see #showNotification(com.vaadin.ui.Window.Notification)
        @see Notification

        @param caption
                   The caption of the message
        @param description
                   The message description
        ---
        Shows a notification consisting of a bigger caption and a smaller
        description. The position and behavior of the message depends on the
        type, which is one of the basic types defined in {@link Notification},
        for instance Notification.TYPE_WARNING_MESSAGE.

        @see #showNotification(com.vaadin.ui.Window.Notification)
        @see Notification

        @param caption
                   The caption of the message
        @param description
                   The message description
        @param type
                   The message type
        ---
        Shows a notification message.

        @see Notification
        @see #showNotification(String)
        @see #showNotification(String, int)
        @see #showNotification(String, String)
        @see #showNotification(String, String, int)

        @param notification
                   The notification message to show
        """
        args = args
        nargs = len(args)
        if nargs == 1:
            if isinstance(args[0], Notification):
                notification, = args
                self.addNotification(notification)
            else:
                caption, = args
                self.addNotification( Notification(caption) )
        elif nargs == 2:
            if isinstance(args[1], int):
                caption, typ = args
                self.addNotification( Notification(caption, typ) )
            else:
                caption, description = args
                self.addNotification( Notification(caption, description) )
        elif nargs == 3:
            caption, description, typ = args
            self.addNotification( Notification(caption, description, typ) )
        else:
            raise ValueError, 'invalid number of arguments'


    def addNotification(self, notification):
        if self._notifications is None:
            self._notifications = list()

        self._notifications.append(notification)
        self.requestRepaint()


    def setFocusedComponent(self, focusable):
        """This method is used by Component.Focusable objects to request focus
        to themselves. Focus renders must be handled at window level (instead
        of Component.Focusable) due we want the last focused component to be
        focused in client too. Not the one that is rendered last (the case
        we'd get if implemented in Focusable only).

        To focus component from Vaadin application, use Focusable.focus().
        See {@link Focusable}.

        @param focusable
                   to be focused on next paint
        """
        if self.getParent() is not None:
            # focus is handled by main windows
            self.getParent().setFocusedComponent(focusable)
        else:
            self._pendingFocus = focusable
            self.requestRepaint()


    def executeJavaScript(self, script):
        """Executes JavaScript in this window.

        This method allows one to inject javascript from the server to client.
        A client implementation is not required to implement this
        functionality, but currently all web-based clients do implement this.

        Executing javascript this way often leads to cross-browser
        compatibility issues and regressions that are hard to resolve. Use of
        this method should be avoided and instead it is recommended to create
        new widgets with GWT. For more info on creating own, reusable
        client-side widgets in Java, read the corresponding chapter in Book of
        Vaadin.

        @param script
                   JavaScript snippet that will be executed.
        """
        if self.getParent() is not None:
            raise NotImplementedError, ('Only application level '
                    'windows can execute javascript.')

        if self._jsExecQueue is None:
            self._jsExecQueue = list()

        self._jsExecQueue.append(script)

        self.requestRepaint()


    def isClosable(self):
        """Returns the closable status of the sub window. If a sub window is
        closable it typically shows an X in the upper right corner. Clicking
        on the X sends a close event to the server. Setting closable to false
        will remove the X from the sub window and prevent the user from
        closing the window.

        Note! For historical reasons readonly controls the closability of the
        sub window and therefore readonly and closable affect each other.
        Setting readonly to true will set closable to false and vice versa.

        Closable only applies to sub windows, not to browser level windows.

        @return true if the sub window can be closed by the user.
        """
        return not self.isReadOnly()


    def setClosable(self, closable):
        """Sets the closable status for the sub window. If a sub window is
        closable it typically shows an X in the upper right corner. Clicking
        on the X sends a close event to the server. Setting closable to false
        will remove the X from the sub window and prevent the user from
        closing the window.

        Note! For historical reasons readonly controls the closability of the
        sub window and therefore readonly and closable affect each other.
        Setting readonly to true will set closable to false and vice versa.

        Closable only applies to sub windows, not to browser level windows.

        @param closable
                   determines if the sub window can be closed by the user.
        """
        self.setReadOnly(not closable)


    def isDraggable(self):
        """Indicates whether a sub window can be dragged or not. By default
        a sub window is draggable.

        Draggable only applies to sub windows, not to browser level windows.

        @param draggable
                   true if the sub window can be dragged by the user
        """
        return self._draggable


    def setDraggable(self, draggable):
        """Enables or disables that a sub window can be dragged (moved) by
        the user. By default a sub window is draggable.

        Draggable only applies to sub windows, not to browser level windows.

        @param draggable
                   true if the sub window can be dragged by the user
        """
        self._draggable = draggable
        self.requestRepaint()


    def setCloseShortcut(self, keyCode, *modifiers):
        """Makes is possible to close the window by pressing the given
        {@link KeyCode} and (optional) {@link ModifierKey}s.<br/>
        Note that this shortcut only reacts while the window has focus,
        closing itself - if you want to close a subwindow from a parent
        window, use {@link #addAction(com.vaadin.event.Action)} of the
        parent window instead.

        @param keyCode
                   the keycode for invoking the shortcut
        @param modifiers
                   the (optional) modifiers for invoking the shortcut,
                   null for none
        """
        if self.closeShortcut is not None:
            self.removeAction(self.closeShortcut)

        self.closeShortcut = CloseShortcut(self, keyCode, modifiers)

        self.addAction(self.closeShortcut)


    def removeCloseShortcut(self):
        """Removes the keyboard shortcut previously set with
        {@link #setCloseShortcut(int, int...)}.
        """
        if self.closeShortcut is not None:
            self.removeAction(self.closeShortcut)
            self.closeShortcut = None


    def focus(self):
        """{@inheritDoc}

        If the window is a sub-window focusing will cause the sub-window
        to be brought on top of other sub-windows on gain keyboard focus.
        """
        if self.getParent() is not None:
            # When focusing a sub-window it basically means it should be
            # brought to the front. Instead of just moving the keyboard
            # focus we focus the window and bring it top-most.
            self._bringToFront()
        else:
            super(Window, self).focus()


class OpenResource(object):
    """Private class for storing properties related to opening resources."""

    def __init__(self, resource, name, width, height, border):
        """Creates a new open resource.

        @param resource
                   The resource to open
        @param name
                   The name of the target window
        @param width
                   The width of the target window
        @param height
                   The height of the target window
        @param border
                   The border style of the target window
        """
        self._resource = resource

        # The name of the target window
        self._name = name

        # The width of the target window
        self._width = width

        # The height of the target window
        self._height = height

        # The border style of the target window
        self._border = border


    def paintContent(self, target):
        """Paints the open request. Should be painted inside the window.

        @param target
                   the paint target
        @throws PaintException
                    if the paint operation fails
        """
        target.startTag('open')
        target.addAttribute('src', self._resource)
        if self._name is not None and len(self._name) > 0:
            target.addAttribute('name', self._name)

        if self._width >= 0:
            target.addAttribute('width', self._width)

        if self._height >= 0:
            target.addAttribute('height', self._height)

        if self._border == Window.BORDER_MINIMAL:
            target.addAttribute('border', 'minimal')
        elif self._border == Window.BORDER_NONE:
            target.addAttribute('border', 'none')

        target.endTag('open')


class CloseEvent(ComponentEvent):

    def __init__(self, source):
        """@param source"""
        super(CloseEvent, self)(source)


    def getWindow(self):
        """Gets the Window.

        @return the window.
        """
        return self.getSource()


class ResizeEvent(ComponentEvent):
    """Resize events are fired whenever the client-side fires a resize-event
    (e.g. the browser window is resized). The frequency may vary across
    browsers.
    """

    def __init__(self, source):
        """@param source"""
        super(ResizeEvent, self)(source)


    def getWindow(self):
        """Get the window form which this event originated

        @return the window
        """
        return self.getSource()


class Notification(object):
    """A notification message, used to display temporary messages to the user -
    for example "Document saved", or "Save failed".

    The notification message can consist of several parts: caption,
    description and icon. It is usually used with only caption - one should
    be wary of filling the notification with too much information.

    The notification message tries to be as unobtrusive as possible, while
    still drawing needed attention. There are several basic types of messages
    that can be used in different situations:
    <ul>
    <li>TYPE_HUMANIZED_MESSAGE fades away quickly as soon as the user uses
    the mouse or types something. It can be used to show fairly unimportant
    messages, such as feedback that an operation succeeded ("Document Saved")
    - the kind of messages the user ignores once the application is familiar.
    </li>
    <li>TYPE_WARNING_MESSAGE is shown for a short while after the user uses
    the mouse or types something. It's default style is also more noticeable
    than the humanized message. It can be used for messages that do not
    contain a lot of important information, but should be noticed by the
    user. Despite the name, it does not have to be a warning, but can be used
    instead of the humanized message whenever you want to make the message a
    little more noticeable.</li>
    <li>TYPE_ERROR_MESSAGE requires to user to click it before disappearing,
    and can be used for critical messages.</li>
    <li>TYPE_TRAY_NOTIFICATION is shown for a while in the lower left corner
    of the window, and can be used for "convenience notifications" that do
    not have to be noticed immediately, and should not interfere with the
    current task - for instance to show "You have a new message in your
    inbox" while the user is working in some other area of the application.</li>
    </ul>

    In addition to the basic pre-configured types, a Notification can also be
    configured to show up in a custom position, for a specified time (or
    until clicked), and with a custom stylename. An icon can also be added.
    </p>
    """

    TYPE_HUMANIZED_MESSAGE = 1
    TYPE_WARNING_MESSAGE = 2
    TYPE_ERROR_MESSAGE = 3
    TYPE_TRAY_NOTIFICATION = 4

    POSITION_CENTERED = 1
    POSITION_CENTERED_TOP = 2
    POSITION_CENTERED_BOTTOM = 3
    POSITION_TOP_LEFT = 4
    POSITION_TOP_RIGHT = 5
    POSITION_BOTTOM_LEFT = 6
    POSITION_BOTTOM_RIGHT = 7

    DELAY_FOREVER = -1
    DELAY_NONE = 0

    def __init__(self, *args):
        """Creates a "humanized" notification message.

        @param caption
                   The message to show
        ---
        Creates a notification message of the specified type.

        @param caption
                   The message to show
        @param type
                   The type of message
        ---
        Creates a "humanized" notification message with a bigger caption and
        smaller description.

        @param caption
                   The message caption
        @param description
                   The message description
        ---
        Creates a notification message of the specified type, with a bigger
        caption and smaller description.

        @param caption
                   The message caption
        @param description
                   The message description
        @param type
                   The type of message
        """
        self._caption = None
        self._description = None
        self._icon = None
        self._position = self.POSITION_CENTERED
        self._delayMsec = 0
        self._styleName = None

        nargs = len(args)
        if nargs == 1:
            caption, = args
            self.__init__(caption, None, self.TYPE_HUMANIZED_MESSAGE)
        elif nargs == 2:
            if isinstance(args[1], int):
                caption, typ = args
                self.__init__(caption, None, typ)
            else:
                caption, description = args
                self.__init__(caption, description, self.TYPE_HUMANIZED_MESSAGE)
        elif nargs == 3:
            caption, description, typ = args
            self._caption = caption
            self._description = description
            self.setType(typ)
        else:
            raise ValueError, 'invalid number of arguments'


    def setType(self, typ):
        if typ == self.TYPE_WARNING_MESSAGE:
            self._delayMsec = 1500
            self._styleName = 'warning'
        elif typ == self.TYPE_ERROR_MESSAGE:
            self._delayMsec = -1
            self._styleName = 'error'
        elif typ == self.TYPE_TRAY_NOTIFICATION:
            self._delayMsec = 3000
            self._position = self.POSITION_BOTTOM_RIGHT
            self._styleName = 'tray'
        elif typ == self.TYPE_HUMANIZED_MESSAGE:
            pass
        else:
            pass


    def getCaption(self):
        """Gets the caption part of the notification message.

        @return The message caption
        """
        return self._caption


    def setCaption(self, caption):
        """Sets the caption part of the notification message

        @param caption
                   The message caption
        """
        self._caption = caption


    def getMessage(self):
        """@deprecated Use {@link #getDescription()} instead.
        @return
        """
        return self._description


    def setMessage(self, description):
        """@deprecated Use {@link #setDescription(String)} instead.
        @param description
        """
        self._description = description


    def getDescription(self):
        """Gets the description part of the notification message.

        @return The message description.
        """
        return self._description


    def setDescription(self, description):
        """Sets the description part of the notification message.

        @param description
        """
        self._description = description


    def getPosition(self):
        """Gets the position of the notification message.

        @return The position
        """
        return self._position


    def setPosition(self, position):
        """Sets the position of the notification message.

        @param position
                   The desired notification position
        """
        self._position = position


    def getIcon(self):
        """Gets the icon part of the notification message.

        @return The message icon
        """
        return self._icon


    def setIcon(self, icon):
        """Sets the icon part of the notification message.

        @param icon
                   The desired message icon
        """
        self._icon = icon


    def getDelayMsec(self):
        """Gets the delay before the notification disappears.

        @return the delay in msec, -1 indicates the message has to be
                clicked.
        """
        return self._delayMsec


    def setDelayMsec(self, delayMsec):
        """Sets the delay before the notification disappears.

        @param delayMsec
                   the desired delay in msec, -1 to require the user to click
                   the message
        """
        self._delayMsec = delayMsec


    def setStyleName(self, styleName):
        """Sets the style name for the notification message.

        @param styleName
                   The desired style name.
        """
        self._styleName = styleName


    def getStyleName(self):
        """Gets the style name for the notification message.

        @return
        """
        return self._styleName


class CloseShortcut(ShortcutListener):
    """A {@link ShortcutListener} specifically made to define a keyboard
    shortcut that closes the window.

    <pre>
    <code>
     // within the window using helper
     subWindow.setCloseShortcut(KeyCode.ESCAPE, null);

     // or globally
     getWindow().addAction(new Window.CloseShortcut(subWindow, KeyCode.ESCAPE));
    </code>
    </pre>
    """

    def __init__(self, *args):
        """Creates a keyboard shortcut for closing the given window using
        the shorthand notation defined in {@link ShortcutAction}.

        @param window
                   to be closed when the shortcut is invoked
        @param shorthandCaption
                   the caption with shortcut keycode and modifiers indicated
        ---
        Creates a keyboard shortcut for closing the given window using the
        given {@link KeyCode} and {@link ModifierKey}s.

        @param window
                   to be closed when the shortcut is invoked
        @param keyCode
                   KeyCode to react to
        @param modifiers
                   optional modifiers for shortcut
        ---
        Creates a keyboard shortcut for closing the given window using the
        given {@link KeyCode}.

        @param window
                   to be closed when the shortcut is invoked
        @param keyCode
                   KeyCode to react to
        """
        self.window = None

        nargs = len(args)
        if nargs == 2:
            if isinstance(args[1], int):
                window, keyCode = args
                self.__init__(window, keyCode, None)
            else:
                window, shorthandCaption = args
                super(CloseShortcut, self)(shorthandCaption)
                self.window = window
        elif nargs == 3:
            window, keyCode = args[:2]
            modifiers = args[2:]
            super(CloseShortcut, self)(None, keyCode, modifiers)
            self.window = window
        else:
            raise ValueError, 'invalid number of arguments'


    def handleAction(self, sender, target):
        self.window.close()