
import re
import locale

from muntjac.demo.sampler.ExampleUtil import ExampleUtil

from muntjac.ui import VerticalLayout, Table
from muntjac.ui.window import Notification
from muntjac.ui.table import IHeaderClickListener, IFooterClickListener


class TableClickListenersExample(VerticalLayout):

    def __init__(self):
        super(TableClickListenersExample, self)()

        # Create our data source
        dataSource = ExampleUtil.getOrderContainer()

        # Calculate total sum
        totalSum = 0.0
        for i in range(len(dataSource)):
            item = dataSource.getItem(dataSource.getIdByIndex(i))
            value = item.getItemProperty(ExampleUtil.ORDER_ITEMPRICE_PROPERTY_ID).getValue()

            #amount = NumberFormat.getCurrencyInstance().parse(str(value))
            amount = re.search(ur'([£$€])(\d+(?:\.\d{2})?)', str(value)).groups()[1]

            totalSum += float(amount)

        # Create table
        table = Table('', ExampleUtil.getOrderContainer())
        table.setColumnExpandRatio(ExampleUtil.ORDER_DESCRIPTION_PROPERTY_ID, 1)
        table.setSortDisabled(True)
        table.setWidth('100%')
        table.setPageLength(6)
        table.setFooterVisible(True)
        table.setImmediate(True)

        # Add some total sum and description to footer
        table.setColumnFooter(ExampleUtil.ORDER_DESCRIPTION_PROPERTY_ID,
                'Total Price')
        table.setColumnFooter(ExampleUtil.ORDER_ITEMPRICE_PROPERTY_ID,
                locale.currency(totalSum, grouping=True))

        # Add a header click handler
        class HeaderListener(IHeaderClickListener):

            def __init__(self, c):
                self._c = c

            def headerClick(self, event):
                # Show a notification help text when the user clicks on a
                # column header
                self._c.showHeaderHelpText(event.getPropertyId())

        table.addListener( HeaderListener(self) )

        # Add a footer click handler
        class FooterListener(IFooterClickListener):

            def __init__(self, c):
                self._c = c

            def footerClick(self, event):
                # Show a notification help text when the user clicks on a
                # column footer
                self._c.showFooterHelpText(event.getPropertyId())

        table.addListener( FooterListener(self) )
        self.addComponent(table)


    def showHeaderHelpText(self, column):
        """Shows some help text when clicking on the header

        @param column
        """
        notification = None
        # Description
        if column == ExampleUtil.ORDER_DESCRIPTION_PROPERTY_ID:
            notification = Notification(str(column) + '<br>',
                    'The description describes the type of product '
                    'that has been ordered.')
        # Item price
        elif column == ExampleUtil.ORDER_ITEMPRICE_PROPERTY_ID:
            notification = Notification(str(column) + '<br>',
                    'The item price is calculated by multiplying '
                    'the unit price with the quantity.')
        # Quantity
        elif column == ExampleUtil.ORDER_QUANTITY_PROPERTY_ID:
            notification = Notification(str(column) + '<br>',
                    'The quantity describes how many items has been ordered.')
        # Unit price
        elif column == ExampleUtil.ORDER_UNITPRICE_PROPERTY_ID:
            notification = Notification(str(column) + '<br>',
                    'The unit price is how much a single items costs. '
                    'Taxes included.')
        else:
            return

        self.getWindow().showNotification(notification)


    def showFooterHelpText(self, column):
        """Shows a footer help text

        @param column
        """
        notification = Notification('Total Price<br>',
                'The total price is calculated by summing every items '
                'item price together.')

        self.getWindow().showNotification(notification)
