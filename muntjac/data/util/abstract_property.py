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

from muntjac.data import property
from muntjac.util import EventObject


class AbstractProperty(property.IProperty, property.IValueChangeNotifier,
            property.IReadOnlyStatusChangeNotifier):
    """Abstract base class for {@link IProperty} implementations.

    Handles listener management for {@link ValueChangeListener}s and
    {@link IReadOnlyStatusChangeListener}s.

    @since 6.6
    """

    def __init__(self):
        # List of listeners who are interested in the read-only status
        # changes of the IProperty
        self._readOnlyStatusChangeListeners = None

        # List of listeners who are interested in the value changes of
        # the IProperty
        self._valueChangeListeners = None

        # Is the IProperty read-only?
        self._readOnly = None


    def isReadOnly(self):
        """{@inheritDoc}

        Override for additional restrictions on what is considered a
        read-only property.
        """
        return self._readOnly


    def setReadOnly(self, newStatus):
        oldStatus = self.isReadOnly()
        self._readOnly = newStatus
        if oldStatus != self.isReadOnly():
            self.fireReadOnlyStatusChange()


    def toString(self):
        """Returns the value of the <code>IProperty</code> in human readable
        textual format. The return value should be assignable to the
        <code>setValue</code> method if the IProperty is not in read-only mode.

        @return String representation of the value stored in the IProperty
        """
        value = self.getValue()
        if value is None:
            return None
        return str(value)


    def addListener(self, listener):
        """Registers a new read-only status change listener for this IProperty.

        @param listener
                   the new Listener to be registered.
        """
        if isinstance(listener, property.IReadOnlyStatusChangeListener):
            if self._readOnlyStatusChangeListeners is None:
                self._readOnlyStatusChangeListeners = list()

            self._readOnlyStatusChangeListeners.adppend(listener)
        else:
            if self._valueChangeListeners is None:
                self._valueChangeListeners = list()

            self._valueChangeListeners.append(listener)


    def removeListener(self, listener):
        """Removes a previously registered read-only status change listener.

        @param listener
                   the listener to be removed.
        """
        if isinstance(listener, property.IReadOnlyStatusChangeListener):
            if self._readOnlyStatusChangeListeners is not None:
                self._readOnlyStatusChangeListeners.remove(listener)
        else:
            if self._valueChangeListeners is not None:
                self._valueChangeListeners.remove(listener)


    def fireReadOnlyStatusChange(self):
        """Sends a read only status change event to all registered listeners."""
        if self._readOnlyStatusChangeListeners is not None:
            l = list(self._readOnlyStatusChangeListeners)
            event = property.IReadOnlyStatusChangeEvent(self)
            for listener in l:
                listener.readOnlyStatusChange(event)


    def fireValueChange(self):
        """Sends a value change event to all registered listeners."""
        if self._valueChangeListeners is not None:
            l = list(self._valueChangeListeners)
            event = property.ValueChangeEvent(self)
            for listener in l:
                listener.valueChange(event)


    def getListeners(self, eventType):
        if issubclass(eventType, ValueChangeEvent):
            if self._valueChangeListeners is None:
                return list()
            else:
                return list(self._valueChangeListeners)
        elif issubclass(eventType, property.IReadOnlyStatusChangeEvent):
            if self._readOnlyStatusChangeListeners is None:
                return list()
            else:
                return list(self._readOnlyStatusChangeListeners)
        return list()


class IReadOnlyStatusChangeEvent(EventObject, property.IProperty,
            property.IReadOnlyStatusChangeEvent):
    """An <code>Event</code> object specifying the IProperty whose read-only
    status has been changed.
    """

    def __init__(self, source):
        """Constructs a new read-only status change event for this object.

        @param source
                   source object of the event.
        """
        super(IReadOnlyStatusChangeEvent, self)(source)


    def getProperty(self):
        """Gets the IProperty whose read-only state has changed.

        @return source IProperty of the event.
        """
        return self.getSource()


class ValueChangeEvent(EventObject, property.ValueChangeEvent):
    """An <code>Event</code> object specifying the IProperty whose value has been
    changed.
    """

    def __init__(self, source):
        """Constructs a new value change event for this object.

        @param source
                   source object of the event.
        """
        super(ValueChangeEvent, self)(source)


    def getProperty(self):
        """Gets the IProperty whose value has changed.

        @return source IProperty of the event.
        """
        return self.getSource()
