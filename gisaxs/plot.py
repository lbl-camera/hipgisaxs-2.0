import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

def image_show(img, qlims, vmin=None, vmax=None):

    img = np.log(img+1)
    if vmin is None:
        vmin = img.mean() - 3*img.std()
    if vmax is None:
        vmax = img.mean() + 3*img.std()

    fig, axs = plt.subplots()
    axs.imshow(img, extent=qlims, cmap='jet', origin='lower', vmin=vmin, vmax=vmax)
    plt.show()

def image_save(img, fname, qlims, clims=None):

    if clims is None:
        clims = [0, 1]

    fig, axs = plt.subplots()
    kwargs = {'extent': qlims, 'cmap':'jet', 'origin': 'lower', 
              'vmin': clims[0], 'vmax': clims[1]}
    axs.imshow(np.log(img+1), **kwargs)
    plt.savefig(fname, bbox_inches='tight', dpi=300)

def line_plot(prof, x_axis = None):

    fig, axs = plt.subplots()
    if x_axis is None:
        x_axis = np.arange(prof.shape[-1])
    axs.plot(x_axis, prof)
    fig.show()

def test_clims(img, qlims, vmin=None, vmax=None):
 
    img = np.log(img+1)
    if vmin is None:
        vmin = img.mean() - 3 * img.std()
    if vmax is None:
        vmax = img.mean() + 3 * img.std()

    fig, axs = plt.subplots()
    im = axs.imshow(img, extent=qlims, origin='lower', cmap='jet')
    im.set_clim(vmin, vmax)

    fig.subplots_adjust(bottom=0.5)

    # Make a horizontal slider to control the vmin
    vlow = img.mean() - 6 * img.std()
    vhigh = img.mean() + 6 * img.std()

    axvmin = fig.add_axes([0.25, 0.1, 0.65, 0.03])
    vmin_slider = Slider(
        ax=axvmin,
        label='Lower cmap limit',
        valmin=vlow,
        valmax=vhigh,
        valinit=vmin
    )

    # Make a horizontal slider to control the vmax
    axvmax = fig.add_axes([0.25, 0.25, 0.65, 0.03])
    vmax_slider = Slider(
        ax=axvmax,
        label='Upper cmap limit',
        valmin=vlow,
        valmax=vhigh,
        valinit=vmax
    )

    def updatel(val):
        im.set_clim(vmin=val)

    def updateu(val):
        im.set_clim(vmax=val)

    vmin_slider.on_changed(updatel)
    vmax_slider.on_changed(updateu)

    plt.show() 
    
