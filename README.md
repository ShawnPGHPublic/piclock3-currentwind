# PiClock3 CurrentWind

Displays current condition differently then standard current conditions plugin.  
Wind is more prominent, "feels like" and pressure is removed.

## Install
```
cd ~/PiClock3

git clone https://github.com/ShawnPGHPublic/piclock3-currentwind plugins/CurrentWind
```
## Test
```
python3 PyQtPiClock3.py examples/currentwind.yaml
```
------------------------------------------------------------------------

### Use it


```
current-conditions:
    plugin: PiClock3.CurrentWind
    region: current
    conditions-provider: openmeteo
`
