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

import sys
import traceback

try:
    from cStringIO import StringIO
except ImportError, e:
    from StringIO import StringIO

from muntjac.terminal.ErrorMessage import IErrorMessage


class SystemErr(RuntimeError, IErrorMessage):
    """<code>SystemError</code> is a runtime exception caused by error in
    system. The system error can be shown to the user as it implements
    <code>IErrorMessage</code> interface, but contains technical information
    such as stack trace and exception.

    @author IT Mill Ltd.
    @author Richard Lincoln
    @version @VERSION@
    @since 3.0
    """

    def __init__(self, *args):
        """Constructor for SystemError with error message specified.

        @param message
                   the Textual error description.
        ---
        Constructor for SystemError with causing exception and error message.

        @param message
                   the Textual error description.
        @param cause
                   the throwable causing the system error.
        ---
        Constructor for SystemError with cause.

        @param cause
                   the throwable causing the system error.
        """
        # The cause of the system error.
        self._cause = None

        nargs = len(args)
        if nargs == 1:
            if isinstance(args[0], Exception):
                self._cause = args[0]
            else:
                super(SystemErr, self)(args[0])
        elif nargs == 2:
            message, cause = args
            super(SystemErr, self)(message)
            self._cause = cause
        else:
            raise ValueError, 'too many arguments'


    def getErrorLevel(self):
        """@see com.vaadin.terminal.IErrorMessage#getErrorLevel()"""
        return IErrorMessage.SYSTEMERROR


    def paint(self, target):
        """@see com.vaadin.terminal.Paintable#paint(target)"""

        target.startTag('error')
        target.addAttribute('level', 'system')

        sb = StringIO()
        message = self.getLocalizedMessage()
        if message is not None:
            sb.write('<h2>')
            sb.write(message)
            sb.write('</h2>')
        # Paint the exception
        if self._cause is not None:
            sb.write('<h3>Exception</h3>')
            buff = StringIO()
            traceback.print_exception(sys.exc_type, self._cause,
                    sys.last_traceback, file=buff)  #@PydevCodeAnalysisIgnore
            sb.write('<pre>')
            sb.write(buff.getvalue())
            buff.close()
            sb.write('</pre>')
        target.addXMLSection('div', sb.getvalue(),
                'http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd')
        sb.close()
        target.endTag('error')


    def getCause(self):
        """Gets cause for the error.

        @return the cause.
        @see java.lang.Throwable#getCause()
        """
        return self._cause


    def addListener(self, listener):
        pass


    def removeListener(self, listener):
        pass


    def requestRepaint(self):
        pass


    def requestRepaintRequests(self):
        pass


    def getDebugId(self):
        return None


    def setDebugId(self, idd):
        raise NotImplementedError, \
                'Setting testing id for this Paintable is not implemented'