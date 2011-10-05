
from muntjac.ui import HorizontalLayout, Label, Slider, Alignment
from muntjac.data.property import IValueChangeListener


class SliderHorizontalExample(HorizontalLayout):

    def __init__(self):
        self.setSpacing(True)

        self.setWidth('100%')

        value = Label('0')
        value.setWidth('3em')

        slider = Slider('Select a value between 0 and 100')
        slider.setWidth('100%')
        slider.setMin(0)
        slider.setMax(100)
        slider.setImmediate(True)

        class SliderListener(IValueChangeListener):

            def __init__(self, value):
                self._value = value

            def valueChange(self, event):
                self._value.setValue(event.getProperty().getValue())

        slider.addListener( SliderListener(value) )

        self.addComponent(slider)
        self.setExpandRatio(slider, 1)
        self.addComponent(value)

        self.setComponentAlignment(value, Alignment.BOTTOM_LEFT)
