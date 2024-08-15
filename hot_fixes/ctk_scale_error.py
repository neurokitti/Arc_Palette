# Built-in libraries
from typing import Union
# Standard GUI and image related libraries
from customtkinter.windows.widgets.scaling import CTkScalingBaseClass

# Patch based upon: https://github.com/TomSchimansky/CustomTkinter/issues/571#issuecomment-1823438190
def apply_widget_scaling(self, value: Union[int, float]) -> Union[float, int]:
    if hasattr(self, "__scaling_type"):
        assert self.__scaling_type == "widget"
    if isinstance(value, float):
        return value * self._get_widget_scaling()
    else:
        return int(value * self._get_widget_scaling())

def reverse_widget_scaling(self, value: Union[int, float]) -> Union[float, int]:
    if hasattr(self, "__scaling_type"):
        assert self.__scaling_type == "widget"
    if isinstance(value, float):
        return value / self._get_widget_scaling()
    else:
        return int(value / self._get_widget_scaling())

CTkScalingBaseClass._apply_widget_scaling = apply_widget_scaling
CTkScalingBaseClass._reverse_widget_scaling = reverse_widget_scaling
