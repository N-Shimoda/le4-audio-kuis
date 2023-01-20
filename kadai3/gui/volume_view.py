import tkinter as tk

class VolumeView(tk.Canvas):

  VOLUME_MIN = -120
  VOLUME_MAX = -10
  vol = -50

  x0 = 10
  y0 = 10
  width = 120
  height = 300


  def __init__(self, master=None):

    super().__init__(
      master,
      width = self.width + self.x0 * 2,
      height = self.height + self.y0 * 2
    )

    self.create_rectangle(
      self.x0, self.y0, self.x0+self.width, self.y0+self.height,
      fill="orange",
      tag="rectangle"
    )

    self.create_line(
      0, self._get_volume_height(), self.width + self.x0 * 2, self._get_volume_height(),
      fill="green",
      width=4,
      tag="hline"
    )


  def set_volume(self, volume):

    # update volume
    self.vol = volume

    # update hline of volume
    self.coords(
      "hline",
      self._get_hline_pos()
    )


  def _get_hline_pos(self):
    return 0, self._get_volume_height(), self.width + self.x0 * 2, self._get_volume_height()


  def _get_volume_height(self):

    range = self.VOLUME_MAX - self.VOLUME_MIN
    return self.height * (1 - (self.vol - self.VOLUME_MIN) / range)