#files import
from Database_Class import *
import Graph_Class as GC
from Main_Window_Class import *

#Database Connection
# db = Database("root", "max696029135", "localhost")

#Creating graph
graph = GC.Graph()

#return distinct mails
# mails = db.returnDistinctMails()
# graph.mailToColor(mails)
#
# #Adding employess to graph
# employess = db.returnTable("employess")
# graph.addEmp(employess)
#
# #Adding couathors Edges to graph
# coauthors = db.returnTable("coauthors")
# graph.addCoauthors(coauthors)

#graph.graphWidget()
window = MainWindow(graph)
window.connect("delete_event", Gtk.main_quit)
window.show_all()
settings = Gtk.Settings.get_default()
settings.props.gtk_button_images = True
Gtk.main()
