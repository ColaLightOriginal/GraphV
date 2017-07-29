from gi.repository import Gtk, Gdk, GdkPixbuf, GObject, Pango
from graph_tool.all import *
import cairo
import sys

class GraphWindowMain(Gtk.Window):

    g = None
    graph = None
    fOn = False
    fFirst = False
    def __init__(self, graphClass, g, pos, geometry, vprops=None, eprops=None, vorder=None,
                 eorder=None, nodesfirst=False, update_layout=True, **kwargs):

        self.g = g
        self.g2 = self.g.copy()
        self.graph = graphClass

        self.eFilter = self.graph.epropFilter.copy()
        self.vFilter = self.graph.vpropFilter.copy()

        Gtk.Window.__init__(self, title="Widget window")

        buttonWidth = 5
        grid=Gtk.Grid()
        self.validPaths = []
        self.pathsIter = 0
        self.add(grid)
        self.set_border_width(10)
        #grid.override_background_color(Gtk.StateType.NORMAL, Gdk.RGBA())

        #GraphArea
        self.graphArea = GraphWidget(g, pos, vprops, eprops, vorder, eorder,
                                    nodesfirst, update_layout,display_props=self.graph.vpropSurname, **kwargs)


        s = Gdk.Screen.get_default()
        self.set_size_request(s.get_width(),s.get_height()-20)
        self.graphArea.set_size_request(s.get_width()-240,s.get_height()-250);
        #self.graphArea.set_size_request(s.get_width()-500,s.get_height()-500);

        #Buttons
        self.buttonFind = Gtk.Button(label="Find vertice")
        self.buttonFind.connect("button_press_event", self.findEmp)
        self.buttonFind.set_border_width(buttonWidth)

        self.comboChooseAlg = Gtk.ComboBoxText()
        self.comboChooseAlg.append("0", "Path searching:")
        # self.comboChooseAlg.append("1", "BFS")
        self.comboChooseAlg.append("2", "A*")
        self.comboChooseAlg.connect("changed", self.algChoose)
        self.comboChooseAlg.set_active(0)

        self.buttonFit = Gtk.Button(label="Fit graph to window")
        self.buttonFit.connect("button_press_event", self.fitToWindow)
        self.buttonFit.set_border_width(buttonWidth)

        self.comboChooseFilt = Gtk.ComboBoxText()
        self.comboChooseFilt.append("0", "=")
        self.comboChooseFilt.append("1", ">")
        self.comboChooseFilt.append("1", "<")

        self.buttonFiltering = Gtk.Button(label="Filter/Unfilter")
        self.buttonFiltering.connect("button_press_event", self.filter)
        self.buttonFiltering.set_border_width(buttonWidth)

        self.buttonFilteringSection = Gtk.Button(label="Filter/Unfilter Section")
        self.buttonFilteringSection.connect("button_press_event", self.filterSection)
        self.buttonFilteringSection.set_border_width(buttonWidth)

        #TextBox
        self.textBoxFind = Gtk.Entry()
        self.textBoxFrom = Gtk.Entry()
        self.textBoxTo = Gtk.Entry()
        self.textBoxFilt = Gtk.Entry()

        self.textBoxSection1 = Gtk.Entry()
        self.textBoxSection2 = Gtk.Entry()

        #Labels
        self.labelFind = Gtk.Label("")
        self.labelFrom = Gtk.Label("From:")
        self.labelTo = Gtk.Label("To:")
        self.labelClear = Gtk.Label("Press C to clear all selected vertices")
        self.labelCoauthors = Gtk.Label("Press spacebar to show neigbours of all selected vertices")

        #List box
        self.software_liststore = Gtk.ListStore(int,str,str,str,str,str)
        self.current_filter_language = None

        self.language_filter = self.software_liststore.filter_new()
        self.language_filter.set_visible_func(self.language_filter_func)

        self.treeview = Gtk.TreeView.new_with_model(self.software_liststore)

        self.column = [None] * 6 # Make a list of 5 None's
        for i in xrange(6):
            self.column[i] = 1
        for i, column_title in enumerate(["Num/D","Source vertice", "Destination vertice", "Value","Section", "Specialization"]):
            renderer = Gtk.CellRendererText()
            self.column[i] = Gtk.TreeViewColumn(column_title, renderer, text=i)
            self.column[i].set_sort_column_id(i)
            self.treeview.append_column(self.column[i])

        self.scrollable_treelist = Gtk.ScrolledWindow()
        self.scrollable_treelist.set_vexpand(True)
        self.scrollable_treelist.add(self.treeview)
        self.scrollable_treelist.set_border_width(buttonWidth)

        #AddWidgets
        grid.attach(self.graphArea,0,0,1,25)

        grid.attach(self.textBoxFind,1,1,1,1)
        grid.attach(self.buttonFind,1,2,1,1)

        grid.attach(self.labelFrom,1,8,1,1)
        grid.attach(self.textBoxFrom,1,9,1,1)
        grid.attach(self.labelTo,1,10,1,1)
        grid.attach(self.textBoxTo,1,11,1,1)
        grid.attach(self.comboChooseAlg,1,12,1,1)

        grid.attach(self.buttonFit,1,19,1,1)
        grid.attach(self.textBoxFilt,1,23,1,1)
        grid.attach(self.comboChooseFilt,1,24,1,1)
        grid.attach(self.buttonFiltering,1,25,1,1)

        grid.attach(self.scrollable_treelist,0,26,1,8)

        grid.attach(self.textBoxSection1, 1, 31, 1,1)
        grid.attach(self.textBoxSection2, 1, 32, 1,1)
        grid.attach(self.buttonFilteringSection, 1, 33, 1,1)

        #Key connectors
        self.connect("key_press_event", self.showNeighbours)
        self.connect("key_press_event", self.showPaths)

    def language_filter_func(self, model, iter, data):
        if self.current_filter_language is None or self.current_filter_language == "None":
            return True
        else:
            return model[iter][2] == self.current_filter_language

    def showB(self):
        print "dziala"

    #Key pressed methods
    def clearPress(self,widget,event):
        if event.keyval == Gdk.KEY_c:
            for v in self.g.vertices():
                self.graphArea.selected[v] = False
            self.graphArea.queue_draw()

    def showSurnames(self,widget,event):
        if event.keyval == Gdk.KEY_0:
            # self.graphArea.=self.graph.vpropSurname
            self.graphArea.queue_draw()

    def showNeighbours(self,widget,event):

        if event.keyval == Gdk.KEY_Tab:
            vertexList = []
            for v in self.g.vertices():
                if ( self.graphArea.selected[v] == True ):
                    for w in v.out_neighbours():
                        vertexList.append(w)

            for i in vertexList:
                self.graphArea.selected[i] = True

            self.graphArea.queue_draw()

    def fitToWindow(self,widget,event):
        self.graphArea.fit_to_window()

        pointer = [5, 5]

        self.graphArea.fit_to_window()
        self.graphArea.regenerate_surface()
        self.graphArea.queue_draw()

        zoom = 0.99
        center = pointer
        cpos = self.graphArea.pos_from_device(center)

        m = cairo.Matrix()
        m.scale(zoom, zoom)

        self.graphArea.tmatrix = self.graphArea.tmatrix.multiply(m)

        ncpos = self.graphArea.pos_from_device(center)
        self.graphArea.tmatrix.translate(ncpos[0] - cpos[0],
                               ncpos[1] - cpos[1])
        self.graphArea.lazy_regenerate = True

        self.graphArea.queue_draw()

    def fitToWindow1(self):
        self.graphArea.fit_to_window()

        pointer = [5, 5]

        self.graphArea.regenerate_surface()
        self.graphArea.queue_draw()

        zoom = 0.99
        center = pointer
        cpos = self.graphArea.pos_from_device(center)

        m = cairo.Matrix()
        m.scale(zoom, zoom)

        self.graphArea.tmatrix = self.graphArea.tmatrix.multiply(m)

        ncpos = self.graphArea.pos_from_device(center)
        self.graphArea.tmatrix.translate(ncpos[0] - cpos[0],
                               ncpos[1] - cpos[1])
        self.graphArea.lazy_regenerate = True

        self.graphArea.queue_draw()

    def findEmp(self,widget,event):
        empSurname = self.textBoxFind.get_text()

        self.software_liststore.clear()
        check = False
        vertex = None
        for v in self.g.vertices():
            if ( self.graph.vpropSurname[v] == empSurname):
                check = True
                self.graphArea.selected[v] = True
                vertex = v
            elif(self.graphArea.selected[v] == True):
                self.graphArea.selected[v] = False

        if check == False:
            for i in self.column:
                i.set_visible(True)
            self.column[0].set_visible(False)
            self.column[3].set_visible(False)
            self.column[4].set_visible(False)
            self.software_liststore.insert(0,[None,empSurname, "Cannot find node",None,None,None])
            return
        else:
            for i in self.column:
                i.set_visible(True)

            specials = ""
            for specs in self.graph.vpropSpecializations[vertex]:
                specials += specs + "  "

            self.software_liststore.insert(0,[None,empSurname, None, str(self.graph.vpropNeighbours[vertex]),self.graph.vpropMail[vertex], specials])
            self.graphArea.queue_draw()

            for i, e in enumerate(vertex.out_neighbours()):

                specials = ""
                for specs in self.graph.vpropSpecializations[vertex]:
                    if specs in self.graph.vpropSpecializations[e]:
                        specials += specs + "  "

                self.software_liststore.append([
                    i,
                    self.graph.vpropSurname[vertex],
                    self.graph.vpropSurname[e],
                    str(self.graph.epropCounter[self.g.edge( vertex, e)]),
                    self.graph.vpropMail[vertex] + " " + self.graph.vpropMail[e],
                    specials
                    ])

    def zoomToSelected(self):
        zoom = 0.9999

        dy = 1

        center = [5,5]
        cpos = self.graphArea.pos_from_device(center)

        m = cairo.Matrix()
        m.scale(zoom, zoom)
        self.graphArea.tmatrix = self.graphArea.tmatrix.multiply(m)

        ncpos = self.graphArea.pos_from_device(center)
        self.graphArea.tmatrix.translate(ncpos[0] - cpos[0],
                               ncpos[1] - cpos[1])
        self.graphArea.lazy_regenerate = True
        self.graphArea.queue_draw()

    def showPaths(self, widget, event):

        if event.keyval == Gdk.KEY_F2 or event.keyval == Gdk.KEY_F1:
            if event.keyval == Gdk.KEY_F2:
                self.pathsIter += 1
                if self.pathsIter >= len(self.validPaths):
                    self.pathsIter = len(self.validPaths)-1
            elif event.keyval == Gdk.KEY_F1:
                self.pathsIter -= 1
                if self.pathsIter < 0:
                    self.pathsIter = 0

            self.software_liststore.clear()
            self.clear()
            for i in self.column:
                i.set_visible(True)
            jterator = 0
            try:
                for j in self.validPaths[self.pathsIter][:-1]:
                    #Insert data to listbox

                    specials = ""
                    for specs in self.graph.vpropSpecializations[self.validPaths[self.pathsIter][jterator]]:
                        if specs in self.graph.vpropSpecializations[self.validPaths[self.pathsIter][jterator+1]]:
                            specials += specs + "  "

                    self.software_liststore.append(
                          [
                          jterator,
                          self.graph.vpropSurname[self.validPaths[self.pathsIter][jterator]],
                          self.graph.vpropSurname[self.validPaths[self.pathsIter][jterator+1]],
                          str(self.graph.epropCounter[self.g.edge( self.validPaths[self.pathsIter][jterator], self.validPaths[self.pathsIter][jterator+1] ) ]),
                          self.graph.vpropMail[self.validPaths[self.pathsIter][jterator]] + " " + self.graph.vpropMail[self.validPaths[self.pathsIter][jterator+1]],
                          specials
                          ])
                    jterator += 1
                    self.graphArea.selected[j] = True
                self.graphArea.selected[self.validPaths[self.pathsIter][-1]] = True
                counter = 0
                self.graphArea.sel_edge_filt.fa = True
                self.graphArea.queue_draw()
            except Exception as e:
                print e

    def algChoose(self,event):

        if self.comboChooseAlg.get_active() == 1:
            self.findShortestPath()
        elif self.comboChooseAlg.get_active() == 2:
            self.findA()

    def findA(self):
        source = self.textBoxFrom.get_text()
        destination = self.textBoxTo.get_text()

        for i in self.column:
            i.set_visible(True)

        dist, pred,destinationV,touch_v,touch_e, target = self.graph.findPathA(source,destination)

        self.software_liststore.clear()

        ecolor = self.g.new_edge_property("string")
        ewidth = self.g.new_edge_property("double")
        ewidth.a = 1

        for e in self.g.edges():
            ecolor[e] = "#3465a4" if touch_e[e] else "#d3d7cf"

        v = target
        path = []
        while v != self.g.vertex(destinationV):
             p = self.g.vertex(pred[v])
             for e in v.out_edges():
                 if e.target() == p:
                    ecolor[e] = "#a40000"
                    ewidth[e] = 3
                    path.append(e)
             v = p

        for i,j in enumerate(path):
            specials = ""
            for specs in self.graph.vpropSpecializations[j.source()]:
                if specs in self.graph.vpropSpecializations[j.target()]:
                    specials += specs + "  "

            #Insert data to listbox
            self.software_liststore.append([
                i,
                self.graph.vpropSurname[j.source()],
                self.graph.vpropSurname[j.target()],
                str(self.graph.epropCounter[self.g.edge( j.source(), j.target() )]),
                self.graph.vpropMail[j.source()] + " " + self.graph.vpropMail[j.target()],
                specials
                ])
            self.graphArea.selected[j.source()] = True
        self.graphArea.selected[path[-1].target()] = True
        self.graphArea.sel_edge_filt.fa = True
        self.graphArea.queue_draw()

    def findShortestPath(self):

        source = self.textBoxFrom.get_text()
        destination = self.textBoxTo.get_text()


        self.software_liststore.clear()

        self.validPaths = []
        self.validPaths = self.graph.findPath(source, destination)

        if self.validPaths == False:
            self.software_liststore.append([source, destination, "There is no connection:",None,None])
        else:

            self.software_liststore.clear()
            self.clear()

            for i in self.column:
                i.set_visible(True)
            jterator = 0
            try:
                for j in self.validPaths[self.pathsIter][:-1]:

                    specials = ""
                    for specs in self.graph.vpropSpecializations[self.validPaths[self.pathsIter][jterator]]:
                        if specs in self.graph.vpropSpecializations[self.validPaths[self.pathsIter][jterator+1]]:
                            specials += specs + "  "

                    #Insert data to listbox
                    self.software_liststore.append([
                        jterator,
                        self.graph.vpropSurname[self.validPaths[self.pathsIter][jterator]],
                        self.graph.vpropSurname[self.validPaths[self.pathsIter][jterator+1]],
                        str(self.graph.epropCounter[self.g.edge( self.validPaths[self.pathsIter][jterator], self.validPaths[self.pathsIter][jterator+1] ) ]),
                        self.graph.vpropMail[self.validPaths[self.pathsIter][jterator]] + " "+ self.graph.vpropMail[self.validPaths[self.pathsIter][jterator+1]],
                        specials
                        ])
                    jterator += 1
                    self.graphArea.selected[j] = True
                self.graphArea.selected[self.validPaths[self.pathsIter][-1]] = True
                self.graphArea.sel_edge_filt.fa = True
                self.graphArea.queue_draw()
            except:
                pass

    def clear(self):
        for v in self.g.vertices():
            self.graphArea.selected[v] = False
        self.graphArea.queue_draw()

    def filter(self,widget, event):
        if self.fOn == False:
            if self.fFirst == False:
                for e in self.g.edges():
                    self.eFilter[e] = 1
                for v in self.g.vertices():
                    self.vFilter[v] = 1
                self.fFirst = True

            for e in self.g.edges():
                self.eFilter[e] = 1
            for v in self.g.vertices():
                self.vFilter[v] = 1
            self.fFirst = True
            text = float(self.textBoxFilt.get_text())

            for e in self.g.edges():
                #Delete every if...
                if self.comboChooseFilt.get_active() == 0:
                    if self.graph.epropCounter[e] < text or self.graph.epropCounter[e] > text :
                        self.eFilter[e] = 0
                    else:
                        self.eFilter[e] = 1
                        # self.vFilter[e.source()] = 1
                        # self.vFilter[e.target()] = 1

                elif self.comboChooseFilt.get_active() == 1:
                    if self.graph.epropCounter[e] <= text:
                        self.eFilter[e] = 0
                    else:
                        self.eFilter[e] = 1
                        # self.vFilter[e.source()] = 1
                        # self.vFilter[e.target()] = 1

                elif self.comboChooseFilt.get_active() == 2:
                    if self.graph.epropCounter[e] >= text:
                        self.eFilter[e] = 0
                    else:
                        self.eFilter[e] = 1
                        # self.vFilter[e.source()] = 1
                        # self.vFilter[e.target()] = 1


            self.g.set_edge_filter(self.eFilter)
            self.g.set_vertex_filter(self.vFilter)

            for v in self.g.vertices():
                check = 0
                for n in v.out_neighbours():
                    check +=1
                if check == 0:
                    self.vFilter[v] = 0

            self.zoomToSelected()
            self.graphArea.queue_draw()
            self.fOn = True
        else:
            self.unfilter()

    def unfilter(self):
        self.g.clear_filters()

        self.zoomToSelected()
        self.graphArea.queue_draw()
        self.fOn = False

    def filterSection(self,widget, event):
        if self.fOn == False:
            if self.fFirst == False:
                for e in self.g.edges():
                    self.eFilter[e] = 1
                for v in self.g.vertices():
                    self.vFilter[v] = 1
                self.fFirst = True

            for e in self.g.edges():
                self.eFilter[e] = 1
            for v in self.g.vertices():
                self.vFilter[v] = 1
            self.fFirst = True


            for e in self.g.edges():
                if (self.graph.vpropMail[e.source()] == self.textBoxSection1.get_text() or self.graph.vpropMail[e.source()] == self.textBoxSection2.get_text()) and (self.graph.vpropMail[e.target()] == self.textBoxSection1.get_text() or self.graph.vpropMail[e.target()] == self.textBoxSection2.get_text()):
                    self.eFilter[e] = 1
                #Delete every else
                else:
                    self.eFilter[e] = 0
                        # self.vFilter[e.source()] = 1
                        # self.vFilter[e.target()] = 1


            self.g.set_edge_filter(self.eFilter)
            self.g.set_vertex_filter(self.vFilter)

            for v in self.g.vertices():
                check = 0
                for n in v.out_neighbours():
                    check +=1
                if check == 0:
                    self.vFilter[v] = 0

            self.zoomToSelected()
            self.graphArea.queue_draw()
            self.fOn = True
        else:
            self.unfilter()
