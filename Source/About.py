from gi.repository import Gtk, Gdk, GdkPixbuf, GObject, Pango
from Database_Class import *

class About(Gtk.Window):

    def __init__(self):

        Gtk.Window.__init__(self, title="About/Color legend")

        self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        grid=Gtk.Grid()
        self.add(grid)

        self.labelCreated = Gtk.Label("Created by:")
        self.labelCreated.modify_font(Pango.FontDescription("Ubuntu 12"))
        grid.attach(self.labelCreated,0,0,1,1)

        self.labelSurname = Gtk.Label("Patryk Rutkowski")
        self.labelSurname.modify_font(Pango.FontDescription("Ubuntu 12"))
        grid.attach(self.labelSurname,2,0,1,1)

        self.labelLicense = Gtk.Label("License:")
        self.labelLicense.modify_font(Pango.FontDescription("Ubuntu 12"))
        grid.attach(self.labelLicense,0,2,1,1)

        self.labelLicenseName = Gtk.Label("Open public license")
        self.labelLicenseName.modify_font(Pango.FontDescription("Ubuntu 12"))
        grid.attach(self.labelLicenseName,2,2,1,1)

        self.labelLegend = Gtk.Label("Colors legend")
        self.labelLegend.modify_font(Pango.FontDescription("Ubuntu 12"))
        grid.attach(self.labelLegend,1,4,1,1)

        #LEGEND
        self.color1 = Gtk.Label("Red")
        self.color1.modify_font(Pango.FontDescription("Ubuntu 12"))
        grid.attach(self.color1,0,6,1,1)
        self.section1 = Gtk.Label("Undefined")
        self.section1.modify_font(Pango.FontDescription("Ubuntu 12"))
        grid.attach(self.section1,2,6,1,1)

        self.color2 = Gtk.Label("Bottle green")
        self.color2.modify_font(Pango.FontDescription("Ubuntu 12"))
        grid.attach(self.color2,0,8,1,1)
        self.section2 = Gtk.Label("Physics")
        self.section2.modify_font(Pango.FontDescription("Ubuntu 12"))
        grid.attach(self.section2,2,8,1,1)

        self.color3 = Gtk.Label("Light green")
        self.color3.modify_font(Pango.FontDescription("Ubuntu 12"))
        grid.attach(self.color3,0,10,1,1)
        self.section3 = Gtk.Label("Astronomy")
        self.section3.modify_font(Pango.FontDescription("Ubuntu 12"))
        grid.attach(self.section3,2,10,1,1)

        self.color4 = Gtk.Label("Navy blue")
        self.color4.modify_font(Pango.FontDescription("Ubuntu 12"))
        grid.attach(self.color4,0,12,1,1)
        self.section4 = Gtk.Label("Astronomy Center")
        self.section4.modify_font(Pango.FontDescription("Ubuntu 12"))
        grid.attach(self.section4,2,12,1,1)

        self.color5 = Gtk.Label("Yellow")
        self.color5.modify_font(Pango.FontDescription("Ubuntu 12"))
        grid.attach(self.color5,0,14,1,1)
        self.section5 = Gtk.Label("Chemistry")
        self.section5.modify_font(Pango.FontDescription("Ubuntu 12"))
        grid.attach(self.section5,2,14,1,1)

        self.color6 = Gtk.Label("Turquoise")
        self.color6.modify_font(Pango.FontDescription("Ubuntu 12"))
        grid.attach(self.color6,0,16,1,1)
        self.section6 = Gtk.Label("Collegium Medicum")
        self.section6.modify_font(Pango.FontDescription("Ubuntu 12"))
        grid.attach(self.section6,2,16,1,1)

        self.color7 = Gtk.Label("Blue")
        self.color7.modify_font(Pango.FontDescription("Ubuntu 12"))
        grid.attach(self.color7,0,18,1,1)
        self.section7 = Gtk.Label("Maths")
        self.section7.modify_font(Pango.FontDescription("Ubuntu 12"))
        grid.attach(self.section7,2,18,1,1)

        self.color8 = Gtk.Label("Purple")
        self.color8.modify_font(Pango.FontDescription("Ubuntu 12"))
        grid.attach(self.color8,0,20,1,1)
        self.section8 = Gtk.Label("Law")
        self.section8.modify_font(Pango.FontDescription("Ubuntu 12"))
        grid.attach(self.section8,2,20,1,1)

        self.color9 = Gtk.Label("Gray")
        self.color9.modify_font(Pango.FontDescription("Ubuntu 12"))
        grid.attach(self.color9,0,22,1,1)
        self.section9 = Gtk.Label("Economy")
        self.section9.modify_font(Pango.FontDescription("Ubuntu 12"))
        grid.attach(self.section9,2,22,1,1)

        self.color10 = Gtk.Label("Black")
        self.color10.modify_font(Pango.FontDescription("Ubuntu 12"))
        grid.attach(self.color10,0,24,1,1)
        self.section10 = Gtk.Label("PhD Student")
        self.section10.modify_font(Pango.FontDescription("Ubuntu 12"))
        grid.attach(self.section10,2,24,1,1)
