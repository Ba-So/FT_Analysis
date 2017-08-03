import Nio
import Ngl
import numpy as np

def print_xy_ngl(data, name, odir):
    """Prints xy Plots of input data"""
    
    # - prepare data
    fname   = name
    x       = data[0]  
    print 'x'
    print x
    y       = data[1]
    print 'y'
    print y


    # - resources for workstation:
    wkres           = Ngl.Resources()
    wkres.wkWidth   = 500
    wkres.wkHeight  = 500
    wks_type        = 'png'

    # - open workstation
    wks             = Ngl.open_wks(wks_type, (odir + fname), wkres)
    
    # - resources for x-y plot
    res                 = Ngl.Resources()
    # - strings for picture
    res.tiMainString    = fname
    res.tiYAxisString   = (fname + ' in Eiern')
    res.tiXAxisString   = 'Number of Timesteps'
    res.tiMainFont      = 'Helvetica'
    res.tiXAxisFont     = 'Helvetica'
    res.tiYAxisFont     = 'Helvetica'
    # - characteristics of plot
    res.xyLineColors    = [189, 107, 24]
    res.xyLineThicknesses   = [1., 2., 5.]
    # - some nice markers
    #res.xyMarkLineModes = ["Lines", "Markers", "MarkLines"]
    #res.xyMarkers       = [0, 1, 3]
    #res.xyMarkerColor  = 107
    #res.xyMarkerSizeF   = 0.03


    plot = Ngl.xy(wks, x, y, res) 
    
    # - Clean up
    del plot
    del res

    print 'printed {}'.format(fname)
    return

def print_xy_ngl_dict(val_dic, name_list, odir, keys):
    """Prints xy Plots of input data"""
    # - prepare data
    # - compute number of timesteps from runday and dtime
    x           = int(name_list['run_day'] * 86400 / name_list['dtime'])
    x           = [i for i in range(1, x+1)]

    # - split the val_dic up in the values and their names
    # - this is a transformation from one dict to two arrays
    # - for plot_xy
    numkeys = 0
    y       = []
    names   = {}
    for key, value in val_dic.iteritems():
        if       -1 == key.find('_mean') and key in keys:
            # - assign values of the variable to array
            y.append(val_dic[key])
            # - assign i as key to the name of the variable
            names[numkeys] = key
            numkeys += 1


        if not -1 == key.find('_mean') and key in keys:
            # - assign mean_value to an array for printing
            y.append([value for i in range(0, len(x))])
            # - assign i as key to the name of the variable
            names[numkeys] = key
            numkeys += 1
    fname = ''
    for key in val_dic:
        if key in keys:
            fname = (fname + key +'-') 
            break
    fname = fname.strip('-')


    # - resources for workstation:
    wkres           = Ngl.Resources()
    wkres.wkWidth   = 1500 
    wkres.wkHeight  = 750
    wkres.wkColorMap = 'WhiteBlueGreenYellowRed'
    wks_type        = 'png'

    # - open workstation
    wks             = Ngl.open_wks(wks_type, (odir + fname), wkres)
    
    # - resources for x-y plot
    # set up the Ressources for the many plottings...
    su_res              = Ngl.Resources() 
    
    # - strings for picture, to be printed only once
    su_res.tiMainString    = fname
    su_res.tiYAxisString   = (fname + ' in Eiern')
    su_res.tiXAxisString   = 'Number of Timesteps'
    su_res.tiMainFont      = 'Helvetica'
    su_res.tiXAxisFont     = 'Helvetica'
    su_res.tiYAxisFont     = 'Helvetica'

    # - Define a Colormap:

    #cmap       = Ngl.retrieve_colormap(wks) 
    #ncmap      = cmap.shape[0]
    #colormap   = cmap[:ncmap:12,:]
    colormap    = [i for i in range(0, 255, 10)] 
    ncol        = len(colormap)
    
    # - Set up Text resource for Legend
    txres               = Ngl.Resources()
    txres.txFont        = 21
    txres.txFontHeightF = 0.03
    txx                 = 1.5
    txy                 = 2.2

    # - characteristics of plot
    su_res.nglFrame            = False
    #su_res.xyLineColors        = colormap[ij]
    su_res.xyLineThicknesses   = [1., 2., 5.]

    # - some nice markers
    #res.xyMarkLineModes = ["Lines", "Markers", "MarkLines"]
    #res.xyMarkers       = [0, 1, 3]
    #res.xyMarkerColor   = 107
    #res.xyMarkerSizeF   = 0.03
    y = np.array(y)
    plot = Ngl.xy(wks, x, y, su_res) 
    #txy += 0.03
    #Ngl.text(wks, plot, key, txx, txy, txres) 


    Ngl.frame(wks) 
    # - Clean up
    del plot
    del su_res

    print 'printed {}'.format(fname)
    return

def print_xy_ngl_ft(val_dic, name_list, odir):
    """Prints xy Plots of input data"""
    # - prepare data
    # - compute number of timesteps from runday and dtime
    #x           = int(name_list['run_day'] * 86400 / name_list['dtime'])
    x           = val_dic['xval']

    # - split the val_dic up in the values and their names
    # - this is a transformation from one dict to two arrays
    # - for plot_xy
    numkeys = 0
    y       = []
    names   = {}
    for key, value in val_dic.iteritems():
        if key != 'xval':     
            # - assign values of the variable to array
            y.append(value)
            # - assign i as key to the name of the variable
            names[numkeys] = key
            numkeys += 1
    # interpolate, so all arrays have same values

    fname = ''
    for key in val_dic:
        if key != 'xval':
            fname = (fname + key +'-') 
            break
    fname = fname.strip('-')


    # - resources for workstation:
    wkres           = Ngl.Resources()
    wkres.wkWidth   = 1500 
    wkres.wkHeight  = 750
    wkres.wkColorMap = 'WhiteBlueGreenYellowRed'
    wks_type        = 'png'

    # - open workstation
    wks             = Ngl.open_wks(wks_type, (odir + fname), wkres)
    
    # - resources for x-y plot
    # set up the Ressources for the many plottings...
    su_res              = Ngl.Resources() 
    
    # - strings for picture, to be printed only once
    su_res.tiMainString    = fname
    su_res.tiYAxisString   = (fname + ' in Eiern')
    su_res.tiXAxisString   = 'Number of Timesteps'
    su_res.tiMainFont      = 'Helvetica'
    su_res.tiXAxisFont     = 'Helvetica'
    su_res.tiYAxisFont     = 'Helvetica'

    # - Define a Colormap:

    #cmap       = Ngl.retrieve_colormap(wks) 
    #ncmap      = cmap.shape[0]
    #colormap   = cmap[:ncmap:12,:]
    colormap    = [i for i in range(0, 255, 10)] 
    ncol        = len(colormap)
    
    # - Set up Text resource for Legend
    txres               = Ngl.Resources()
    txres.txFont        = 21
    txres.txFontHeightF = 0.03
    txx                 = 1.5
    txy                 = 2.2

    # - characteristics of plot
    su_res.nglFrame            = False
    #su_res.xyLineColors        = colormap[ij]
    su_res.xyLineThicknesses   = [1., 2., 5.]

    # - some nice markers
    #res.xyMarkLineModes = ["Lines", "Markers", "MarkLines"]
    #res.xyMarkers       = [0, 1, 3]
    #res.xyMarkerColor   = 107
    #res.xyMarkerSizeF   = 0.03
    y = np.array(y)
    plot = Ngl.xy(wks, x, y, su_res) 
    #txy += 0.03
    #Ngl.text(wks, plot, key, txx, txy, txres) 


    Ngl.frame(wks) 
    # - Clean up
    del plot
    del su_res

    print 'printed {}'.format(fname)
    return
