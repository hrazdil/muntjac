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

from muntjac.ui.abstract_component_container import AbstractComponentContainer
from muntjac.ui.component import Event as ComponentEvent
from muntjac.ui.abstract_component import AbstractComponent


class IPopupVisibilityListener(object):
    """Defines a listener that can receive a PopupVisibilityEvent when the
    visibility of the popup changes.
    """

    def popupVisibilityChange(self, event):
        """Pass to {@link PopupView#PopupVisibilityEvent} to start listening
        for popup visibility changes.

        @param event: the event

        @see {@link PopupVisibilityEvent}
        @see {@link PopupView#addListener(IPopupVisibilityListener)}
        """
        raise NotImplementedError


class SingleComponentIterator(object):
    """Iterator for the visible components (zero or one components), used by
    {@link PopupView#getComponentIterator()}.
    """

    def __init__(self, component):
        self._component = component
        self._first = component is None


    def __iter__(self):
        return self


    def hasNext(self):
        return not self._first


    def next(self):  #@PydevCodeAnalysisIgnore
        if not self._first:
            self._first = True
            return self._component
        else:
            return None


    def remove(self):
        raise NotImplementedError


class PopupView(AbstractComponentContainer):
    """A component for displaying a two different views to data. The minimized
    view is normally used to render the component, and when it is clicked the
    full view is displayed on a popup. The class {@link PopupView.IContent} is
    used to deliver contents to this component.

    @author IT Mill Ltd.
    @author Richard Lincoln
    """

    #CLIENT_WIDGET = ClientWidget(VPopupView, LoadStyle.EAGER)

    _POPUP_VISIBILITY_METHOD = getattr(IPopupVisibilityListener,
            'popupVisibilityChange')

    def __init__(self, *args):
        """A simple way to create a PopupPanel. Note that the minimal
        representation may not be dynamically updated, in order to achieve
        this create your own IContent object and use
        {@link PopupView#PopupView(IContent)}.

        @param small: the minimal textual representation as HTML
        @param large: the full, Component-type representation
        ---
        Creates a PopupView through the PopupView.IContent interface.
        This allows the creator to dynamically change the contents of
        the PopupView.

        @param content
                   the PopupView.IContent that contains the information
                   for this
        """
        self._content = None
        self._hideOnMouseOut = None
        self._visibleComponent = None

        nargs = len(args)
        if nargs == 1:
            content, = args
            super(PopupView, self)()
            self._hideOnMouseOut = True
            self.setContent(content)
        elif nargs == 2:
            small, large = args

            class InnerContent(IContent):

                def __init__(self, small, large):
                    self._small = small
                    self._large = large

                def getMinimizedValueAsHTML(self):
                    return self._small

                def getPopupComponent(self):
                    return self._large

            c = InnerContent(small, large)
            self.__init__(c)
        else:
            raise ValueError, 'invalid number of arguments'


    def setContent(self, newContent):
        """This method will replace the current content of the panel with
        a new one.

        @param newContent
                   PopupView.IContent object containing new information
                   for the PopupView
        @throws IllegalArgumentException
                    if the method is passed a null value, or if one of
                    the content methods returns null
        """
        if newContent is None:
            raise ValueError, 'IContent must not be null'
        self._content = newContent
        self.requestRepaint()


    def getContent(self):
        """Returns the content-package for this PopupView.

        @return the PopupView.IContent for this object or null
        """
        return self._content


    def setPopupVisibility(self, visible):
        """@deprecated Use {@link #setPopupVisible()} instead."""
        raise DeprecationWarning, 'use setPopupVisible() instead'
        self.setPopupVisible(visible)

    def getPopupVisibility(self):
        """@deprecated Use {@link #isPopupVisible()} instead."""
        raise DeprecationWarning, 'use isPopupVisible() instead'
        return self.isPopupVisible()


    def setPopupVisible(self, visible):
        """Set the visibility of the popup. Does not hide the minimal
        representation.

        @param visible
        """
        if self.isPopupVisible() != visible:
            if visible:
                self._visibleComponent = self._content.getPopupComponent()
                if self._visibleComponent is None:
                    raise ValueError, ('PopupView.IContent did not return '
                            'Component to set visible')
                super(PopupView, self).addComponent(self._visibleComponent)
            else:
                super(PopupView, self).removeComponent(self._visibleComponent)
                self._visibleComponent = None
            self.fireEvent( PopupVisibilityEvent(self) )
            self.requestRepaint()


    def isPopupVisible(self):
        """Return whether the popup is visible.

        @return true if the popup is showing
        """
        return self._visibleComponent is not None


    def isHideOnMouseOut(self):
        """Check if this popup will be hidden when the user takes the mouse
        cursor out of the popup area.

        @return true if the popup is hidden on mouse out, false otherwise
        """
        return self._hideOnMouseOut

    # Methods inherited from AbstractComponentContainer. These are unnecessary
    # (but mandatory). Most of them are not supported in this implementation.

    def setHideOnMouseOut(self, hideOnMouseOut):
        """Should the popup automatically hide when the user takes the mouse
        cursor out of the popup area? If this is false, the user must click
        outside the popup to close it. The default is true.

        @param hideOnMouseOut
        """
        self._hideOnMouseOut = hideOnMouseOut


    def getComponentIterator(self):
        """This class only contains other components when the popup is
        showing.

        @see com.vaadin.ui.ComponentContainer#getComponentIterator()
        """
        return SingleComponentIterator(self._visibleComponent)


    def getComponentCount(self):
        """Gets the number of contained components. Consistent with the
        iterator returned by {@link #getComponentIterator()}.

        @return the number of contained components (zero or one)
        """
        return 1 if self._visibleComponent is not None else 0


    def removeAllComponents(self):
        """Not supported in this implementation.

        @see com.vaadin.ui.AbstractComponentContainer#removeAllComponents()
        @throws UnsupportedOperationException
        """
        raise NotImplementedError


    def moveComponentsFrom(self, source):
        """Not supported in this implementation.

        @see AbstractComponentContainer.moveComponentsFrom()
        @throws UnsupportedOperationException
        """
        raise NotImplementedError


    def addComponent(self, c):
        """Not supported in this implementation.

        @see AbstractComponentContainer.addComponent()
        @throws UnsupportedOperationException
        """
        raise NotImplementedError


    def replaceComponent(self, oldComponent, newComponent):
        """Not supported in this implementation.

        @see ComponentContainer.replaceComponent()
        @throws UnsupportedOperationException
        """
        raise NotImplementedError


    def removeComponent(self, c):
        """Not supported in this implementation

        @see AbstractComponentContainer.removeComponent()
        """
        raise NotImplementedError

    # Methods for server-client communications.

    def paintContent(self, target):
        """Paint (serialize) the component for the client.

        @see AbstractComponent.paintContent()
        """
        # Superclass writes any common attributes in the paint target.
        super(PopupView, self).paintContent(target)

        html = self._content.getMinimizedValueAsHTML()
        if html is None:
            html = ''

        target.addAttribute('html', html)
        target.addAttribute('hideOnMouseOut', self._hideOnMouseOut)

        # Only paint component to client if we know that the popup is showing
        if self.isPopupVisible():
            target.startTag('popupComponent')
            self._visibleComponent.paint(target)
            target.endTag('popupComponent')

        target.addVariable(self, 'popupVisibility', self.isPopupVisible())


    def changeVariables(self, source, variables):
        """Deserialize changes received from client.

        @see AbstractComponent.changeVariables()
        """
        if 'popupVisibility' in variables:
            self.setPopupVisible( bool(variables.get('popupVisibility')) )


    def addListener(self, listener):
        """Add a listener that is called whenever the visibility of the popup
        is changed.

        @param listener: the listener to add
        @see IPopupVisibilityListener
        @see PopupVisibilityEvent
        @see #removeListener(IPopupVisibilityListener)
        """
        AbstractComponent.addListener(self, PopupVisibilityEvent, listener,
                self._POPUP_VISIBILITY_METHOD)


    def removeListener(self, listener):
        """Removes a previously added listener, so that it no longer receives
        events when the visibility of the popup changes.

        @param listener: the listener to remove
        @see IPopupVisibilityListener
        @see #addListener(IPopupVisibilityListener)
        """
        AbstractComponent.removeListener(self, PopupVisibilityEvent, listener,
                self._POPUP_VISIBILITY_METHOD)


class PopupVisibilityEvent(ComponentEvent):
    """This event is received by the PopupVisibilityListeners when the
    visibility of the popup changes. You can get the new visibility directly
    with {@link #isPopupVisible()}, or get the PopupView that produced the
    event with {@link #getPopupView()}.
    """

    def __init__(self, source):
        super(PopupVisibilityEvent, self)(source)


    def getPopupView(self):
        """Get the PopupView instance that is the source of this event.

        @return the source PopupView
        """
        return self.getSource()


    def isPopupVisible(self):
        """Returns the current visibility of the popup.

        @return true if the popup is visible
        """
        return self.getPopupView().isPopupVisible()


class IContent(object):
    """Used to deliver customized content-packages to the PopupView. These
    are dynamically loaded when they are redrawn. The user must take care
    that neither of these methods ever return null.
    """

    def getMinimizedValueAsHTML(self):
        """This should return a small view of the full data.

        @return value in HTML format
        """
        raise NotImplementedError


    def getPopupComponent(self):
        """This should return the full Component representing the data

        @return a Component for the value
        """
        raise NotImplementedError