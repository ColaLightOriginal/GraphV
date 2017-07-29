from gi.repository import Gtk, Gdk, GdkPixbuf, GObject, Pango
from Database_Class import *

class DatabaseWindow(Gtk.Window):

    def __init__(self,graph):

        self.graph = graph

        Gtk.Window.__init__(self, title="Database connector")

        self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        grid=Gtk.Grid()
        self.add(grid)

        self.labelDatabaseName = Gtk.Label("Database name:")
        grid.attach(self.labelDatabaseName,0,0,1,1)

        self.textBoxDatabaseName = Gtk.Entry()
        grid.attach(self.textBoxDatabaseName,2,0,1,1)

        self.labelUsername = Gtk.Label("Username:")
        grid.attach(self.labelUsername,0,2,1,1)

        self.textBoxUsername = Gtk.Entry()
        grid.attach(self.textBoxUsername,2,2,1,1)

        self.labelHost = Gtk.Label("Host:")
        grid.attach(self.labelHost,0,4,1,1)

        self.textBoxHost = Gtk.Entry()
        grid.attach(self.textBoxHost,2,4,1,1)

        self.labelPassword = Gtk.Label("Password:")
        grid.attach(self.labelPassword,0,6,1,1)

        self.textBoxPassword = Gtk.Entry()
        self.textBoxPassword.set_visibility(False)
        grid.attach(self.textBoxPassword,2,6,1,1)

        self.buttonConnect = Gtk.Button("Connect")
        self.buttonConnect.connect("button_press_event", self.databaseConnectDef)
        grid.attach(self.buttonConnect,1,7,1,1)

    def databaseConnectDef(self,widget,event):
        databaseName = self.textBoxDatabaseName.get_text()
        username = self.textBoxUsername.get_text()
        password = self.textBoxPassword.get_text()
        host = self.textBoxHost.get_text()

        try:
            db = Database(username, password, host)
        except:
            self.set_title("ERROR IN CONNECTION")
            return

        try:
            #Adding to graph
            mails = db.returnDistinctMails(databaseName)
            self.graph.mailToColor(mails)
            employess = db.returnTable("employess",databaseName)
            self.graph.addEmp(employess)
            coauthors = db.returnTable("coauthors",databaseName)
            self.graph.addCoauthors(coauthors)
        except:
            self.set_title("ERROR IN DATABASE IMPORT")
            return

        # mails = db.returnDistinctMails()
        # self.graph.mailToColor(mails)
        # employess = db.returnTable("employess",databaseName)
        # self.graph.addEmp(employess)
        # coauthors = db.returnTable("coauthors",databaseName)
        # self.graph.addCoauthors(coauthors)


        self.set_title("Connected")
