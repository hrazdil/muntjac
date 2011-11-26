# Copyright (C) 2011 Vaadin Ltd.
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
#
# Note: This is a modified file from Vaadin. For further information on
#       Vaadin please visit http://www.vaadin.com.

"""Interface for classes supporting registration of methods as event
receivers."""


class IMethodEventSource(object):
    """Interface for classes supporting registration of methods as event
    receivers.

    For more information on the inheritable event mechanism see the
    L{muntjac.event package documentation<muntjac.event>}.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.0.4
    """

    def addListener(self, eventType, obj, method):
        """Registers a new event listener with the specified activation method
        to listen events generated by this component. If the activation method
        does not have any arguments the event object will not be passed to it
        when it's called.

        For more information on the inheritable event mechanism see the
        L{muntjac.event package documentation<muntjac.event>}.

        @param eventType:
                   the type of the listened event. Events of this type or its
                   subclasses activate the listener.
        @param obj:
                   the object instance who owns the activation method.
        @param method:
                   the activation method or the name of the activation method.
        @raise ValueError:
                    unless C{method} has a match in C{object}
        """
        raise NotImplementedError


    def removeListener(self, eventType, obj, method):
        """Removes all registered listeners matching the given parameters.
        Since this method receives the event type and the listener object as
        parameters, it will unregister all C{object}'s methods that are
        registered to listen to events of type C{eventType} generated by this
        component.

        For more information on the inheritable event mechanism see the
        L{muntjac.event package documentation<muntjac.event>}.

        @param eventType:
                   the exact event type the C{object} listens to.
        @param obj:
                   the target object that has registered to listen to events
                   of type eventType with one or more methods.
        @param method:
                   the method owned by the target that's registered to listen
                   to events of type eventType. Or the name of the method owned
                   by C{target} that's registered to listen to events of type
                   C{eventType}.
        """
        raise NotImplementedError
