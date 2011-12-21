# -*- coding: utf-8 -*-
from org.vaadin.svg.SvgComponent import (SvgComponent,)
from org.vaadin.svg.test.ExamplePanel import (ExamplePanel,)
# from com.vaadin.Application import (Application,)
# from com.vaadin.terminal.ClassResource import (ClassResource,)
# from com.vaadin.ui.Label import (Label,)
# from com.vaadin.ui.Panel import (Panel,)
SvgMessageListener = SvgComponent.SvgMessageListener


class AnimationExample(ExamplePanel):

    def __init__(self, a):
        self.setCaption('Simple example from svg file')
        self.addComponent(Label('A simple example from an svg file. Also demonstrates SVG animations. Note that, IE/svgweb not 100% compatible here (fonts).'))
        svg = SvgComponent()
        svg.setWidth('800px')
        svg.setHeight('400px')
        classResource = ClassResource(self.getClass(), 'svg2009.svg', a)
        svg.setSource(classResource)
        # Also note the simpler method to set svg:
        # svg.setSvg(getClass().getResourceAsStream("pull.svg"));
        self.addComponent(svg)

        class _0_(SvgMessageListener):

            def handleMessage(self, event):
                event.getComponent().getWindow().showNotification(event.getMessage())

        _0_ = _0_()
        svg.addListener(_0_)