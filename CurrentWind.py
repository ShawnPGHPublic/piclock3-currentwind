"""Current conditions with wind on the line under the temperature.

Same picture, description and temperature as CurrentConditions.  Pressure
and feels-like are omitted.  Wind speed and gusts take the old pressure
line (same size).  Humidity sits near the bottom, above the observation
time.
"""
import logging

from PyQt5 import QtGui
from PyQt5.QtCore import Qt

from PiClock3.Widget import Widget

logger = logging.getLogger(__name__)


class CurrentWind(Widget):

    def __init__(self, piclock, name, config):
        super().__init__(piclock, name, config)
        self.provider = piclock.plugins[self.config['conditions-provider']]
        self.parts = {}
        self.observedFormat = None

    def start(self):
        self.observedFormat = self.strftimePortableFormat(
            self.config['observed-format'])
        for name in ('wxicon', 'wxdesc', 'temper', 'wind',
                     'humidity', 'wdate'):
            self.parts[name] = self.part(name,
                                         align=self.ALIGN['center-top'])
        self.provider.subscribe(self.draw)

    def pageChange(self):
        return

    def draw(self):
        c = self.provider.conditions()
        if not c:
            return
        temp, dew = c.get('temp'), c.get('dew')

        p = QtGui.QPixmap(self.icon(c.get('icon') or 'cloudy'))
        icon = self.parts['wxicon']
        icon.setPixmap(p.scaled(icon.width(), icon.height(),
                                Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.parts['wxdesc'].setText(
            self.piclock.condition(c.get('condition')))

        self.parts['temper'].setText(
            '' if temp is None
            else self.units('temperature', 'C', temp))

        self.parts['wind'].setText(self.wind(c, c.get('wind')))
        self.parts['humidity'].setText(self.humidity(c, temp, dew))

        when = c.get('when')
        self.parts['wdate'].setText(
            '' if when is None
            else '%s %s' % (when.strftime(self.observedFormat),
                            self.provider.attribution))

    def humidity(self, c, temp, dew):
        given = c.get('humidity')
        if given is None:
            return ''
        return '%s %.0f%%' % (self.piclock.language('humidity'), given)

    def wind(self, c, speed):
        if speed is None and c.get('gust') is None:
            return ''
        L = self.piclock.language
        s = ''
        if c.get('wind-dir') is not None:
            s += ' ' + self.units('direction', 'deg', c['wind-dir'])
        if speed is not None:
            s += ' %.1f' % speed
        if c.get('gust') is not None:
            s += ' / %.1f' % self.units('speed', 'kph', c['gust'])
        return s
