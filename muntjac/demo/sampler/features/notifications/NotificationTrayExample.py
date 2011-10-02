# -*- coding: utf-8 -*-


class NotificationTrayExample(VerticalLayout):

    def __init__(self):
        self.setSpacing(True)
        self.setWidth(None)
        # layout will grow with content
        caption = TextField('Caption', 'New message')
        caption.setWidth('200px')
        self.addComponent(caption)
        description = TextField('Description', '<b>John:</b> Could you upload Invoices-2008.csv so that...')
        description.setWidth('300px')
        self.addComponent(description)

        class _0_(Button.ClickListener):

            def buttonClick(self, event):
                self.getWindow().showNotification(self.caption.getValue(), self.description.getValue(), Notification.TYPE_TRAY_NOTIFICATION)

        _0_ = _0_()
        show = Button('Show notification', _0_)
        self.addComponent(show)
        self.setComponentAlignment(show, Alignment.MIDDLE_RIGHT)
