from gi.repository import Gtk, Gdk, GdkPixbuf, GObject, Pango
from graph_tool.all import *
from Database_Window import *
from About import *
import numpy as np
from numpy.random import random
import matplotlib

import shutil
import os
from operator import itemgetter

class MainWindow(Gtk.Window):

    graph = None
    def __init__(self, graph):
        Gtk.Window.__init__(self, title = "MainWindow")

        self.graph = graph
        self.set_border_width(10)
        self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)

        grid = Gtk.Grid()
        self.add(grid)
        pathsIter = 0
        validPaths = []

        screen = Gdk.Screen.get_default()

        buttonWidth = 3

        #Row1 - Buttons

        self.buttonOpen = Gtk.Button.new_from_stock(Gtk.STOCK_CONNECT)
        self.buttonOpen.connect("clicked", self.openDatabase)
        self.buttonOpen.set_border_width(buttonWidth)
        grid.attach(self.buttonOpen,1,0,1,1)

        # self.buttonOpenFile = Gtk.Button.new_from_stock(Gtk.STOCK_OPEN)
        # self.buttonOpenFile.connect("clicked", self.onFileClicked)
        # self.buttonOpenFile.set_border_width(buttonWidth)
        # grid.attach(self.buttonOpenFile,2,0,1,1)

        self.buttonSave = Gtk.Button.new_from_stock(Gtk.STOCK_SAVE)
        self.buttonSave.connect("clicked", self.onFolderClicked)
        self.buttonSave.set_border_width(buttonWidth)
        grid.attach(self.buttonSave,3,0,1,1)

        self.buttonAbout = Gtk.Button.new_from_stock(Gtk.STOCK_ABOUT)
        self.buttonAbout.connect("clicked", self.onAboutClicked)
        self.buttonAbout.set_border_width(buttonWidth)
        grid.attach(self.buttonAbout,2,0,1,1)

        self.logo = Gtk.Image()
        self.logo.set_from_file('./Resources/logo.png')
        grid.attach(self.logo,2,2,1,1)

        self.labelTitle = Gtk.Label("GraphV")
        self.labelTitle.modify_font(Pango.FontDescription("Ubuntu 50"))
        self.labelTitle.set_xalign(0.5)
        self.labelTitle.set_size_request(400,100)
        grid.attach(self.labelTitle,0,2,3,1)

        #Row3
        self.labelStatistics = Gtk.Label("Statistics Menu")
        self.labelStatistics.modify_font(Pango.FontDescription("Ubuntu 16"))
        self.labelStatistics.set_xalign(0.5)
        self.labelStatistics.set_size_request(100,75)
        grid.attach(self.labelStatistics,0,3,4,1)

        #Row4
        self.labelShow = Gtk.Label("Show")
        self.labelShow.modify_font(Pango.FontDescription("Ubuntu 12"))
        self.labelShow.set_xalign(0.5)
        self.labelShow.set_yalign(0.5)
        self.labelShow.set_size_request(50,35)
        grid.attach(self.labelShow,0,4,1,1)

        self.combo = Gtk.ComboBoxText()
        self.combo.append("0", "")
        self.combo.append("1", "Vertices")
        self.combo.append("2", "Edges")
        self.combo.connect("changed", self.comboShow)
        grid.attach(self.combo,1,4,1,1)

        #Row5
        self.labelFind = Gtk.Label("Find Employee")
        self.labelFind.modify_font(Pango.FontDescription("Ubuntu 12"))
        self.labelFind.set_xalign(0.5)
        self.labelFind.set_yalign(0.5)
        self.labelFind.set_size_request(50,50)
        grid.attach(self.labelFind,0,5,1,1)

        self.textBoxFind = Gtk.Entry()
        grid.attach(self.textBoxFind,1,5,1,1)

        self.labelFind = Gtk.Label("Deep")
        self.labelFind.modify_font(Pango.FontDescription("Ubuntu 12"))
        self.labelFind.set_xalign(0.5)
        self.labelFind.set_yalign(0.5)
        self.labelFind.set_size_request(50,50)
        grid.attach(self.labelFind,2,5,1,1)

        self.comboDeep = Gtk.ComboBoxText()
        self.comboDeep.append("0", "")
        self.comboDeep.append("1", "0")
        self.comboDeep.append("2", "1")
        self.comboDeep.append("3", "2")
        self.comboDeep.append("4", "3")
        self.comboDeep.connect("changed", self.printFind)
        grid.attach(self.comboDeep,3,5,1,1)

        #Row6
        self.labelFindSpec = Gtk.Label("Find Specialization")
        self.labelFindSpec.modify_font(Pango.FontDescription("Ubuntu 12"))
        self.labelFindSpec.set_xalign(0.5)
        self.labelFindSpec.set_yalign(0.5)
        self.labelFindSpec.set_size_request(50,50)
        grid.attach(self.labelFindSpec,0,6,1,1)

        self.textBoxFindSpec = Gtk.Entry()
        self.textBoxFindSpec.connect("key_press_event", self.printSpecs)
        grid.attach(self.textBoxFindSpec,1,6,1,1)

        #Row7
        self.comboChooseAlg = Gtk.ComboBoxText()
        self.comboChooseAlg.append("0", "Path searching:")
        # self.comboChooseAlg.append("1", "BFS")
        self.comboChooseAlg.append("2", "A*")
        grid.attach(self.comboChooseAlg,0,7,1,1)
        self.comboChooseAlg.set_active(0)

        self.textBoxFrom = Gtk.Entry()
        self.textBoxFrom.connect("key_press_event", self.chooseSearchAlg)
        grid.attach(self.textBoxFrom,1,7,1,1)

        self.labelTo = Gtk.Label("To")
        self.labelTo.modify_font(Pango.FontDescription("Ubuntu 12"))
        self.labelTo.set_xalign(0.5)
        self.labelTo.set_yalign(0.5)
        self.labelTo.set_size_request(50,50)
        grid.attach(self.labelTo,2,7,1,1)

        self.textBoxTo = Gtk.Entry()
        self.textBoxTo.connect("key_press_event", self.chooseSearchAlg)
        grid.attach(self.textBoxTo,3,7,1,1)

        #Row8
        self.labelTitle = Gtk.Label("Graphic Menu")
        self.labelTitle.modify_font(Pango.FontDescription("Ubuntu 16"))
        self.labelTitle.set_xalign(0.5)
        self.labelTitle.set_size_request(100,75)
        grid.attach(self.labelTitle,0,8,4,1)

        #Row9
        self.labelTitleAdds = Gtk.Label("Graph of:")
        self.labelTitleAdds.modify_font(Pango.FontDescription("Ubuntu 12"))
        self.labelTitleAdds.set_xalign(0.5)
        self.labelTitleAdds.set_size_request(50,50)
        grid.attach(self.labelTitleAdds,0,9,1,1)

        self.comboChooseAdd = Gtk.ComboBoxText()
        self.comboChooseAdd.append("0", "All")
        self.comboChooseAdd.append("1", "Specialization")
        self.comboChooseAdd.append("2", "Magazine")
        grid.attach(self.comboChooseAdd,1,9,1,1)
        self.comboChooseAdd.connect("changed", self.setActive)
        self.comboChooseAdd.set_active(0)

        self.labelTitleAddsPick = Gtk.Label("Spec/Mag:")
        self.labelTitleAddsPick.modify_font(Pango.FontDescription("Ubuntu 12"))
        self.labelTitleAddsPick.set_xalign(0.5)
        self.labelTitleAddsPick.set_size_request(50,50)
        grid.attach(self.labelTitleAddsPick,2,9,1,1)

        self.textBoxAddons = Gtk.Entry()
        grid.attach(self.textBoxAddons,3,9,1,1)
        self.textBoxAddons.set_sensitive(False)

        #Row10
        self.labelExportPng = Gtk.Label("Export PNG image")
        self.labelExportPng.modify_font(Pango.FontDescription("Ubuntu 12"))
        self.labelExportPng.set_xalign(0)
        self.labelExportPng.set_yalign(0.5)
        self.labelExportPng.set_size_request(50,50)
        grid.attach(self.labelExportPng,0,10,1,1)

        self.comboLayout = Gtk.ComboBoxText()
        self.comboLayout.append("0", "")
        self.comboLayout.append("1", "Arf")
        self.comboLayout.append("2", "Fruchterman Reingold")
        grid.attach(self.comboLayout,1,10,1,1)

        self.labelFileName = Gtk.Label("File name:")
        self.labelFileName.modify_font(Pango.FontDescription("Ubuntu 12"))
        self.labelFileName.set_xalign(0.5)
        self.labelFileName.set_yalign(0.5)
        self.labelFileName.set_size_request(50,50)
        grid.attach(self.labelFileName,2,10,1,1)

        self.textBoxFilename = Gtk.Entry()
        self.textBoxFilename.connect("key_press_event", self.generateImage)
        grid.attach(self.textBoxFilename,3,10,1,1)

        #Row11
        self.labelInteractive = Gtk.Label("Interactive window")
        self.labelInteractive.modify_font(Pango.FontDescription("Ubuntu 12"))
        self.labelInteractive.set_xalign(0)
        self.labelInteractive.set_yalign(0.5)
        self.labelInteractive.set_size_request(50,50)
        grid.attach(self.labelInteractive,0,11,1,1)
        self.labelInteractive.set_sensitive(False)

        self.buttonInteractive = Gtk.Button(label="Execute")
        #self.buttonInteractive.connect("button_press_event", self.findEmp)
        self.buttonInteractive.set_border_width(buttonWidth)
        self.buttonInteractive.connect("button_press_event", self.generateInteractive)
        grid.attach(self.buttonInteractive,1,11,1,1)
        self.buttonInteractive.set_sensitive(False)

        #Row12
        self.labelWidget = Gtk.Label("Widget window")
        self.labelWidget.modify_font(Pango.FontDescription("Ubuntu 12"))
        self.labelWidget.set_xalign(0)
        self.labelWidget.set_yalign(0.5)
        self.labelWidget.set_size_request(50,50)
        grid.attach(self.labelWidget,0,12,1,1)

        self.buttonWidget = Gtk.Button(label="Execute")
        self.buttonWidget.set_border_width(buttonWidth)
        self.buttonWidget.connect("button_press_event", self.generateWidget)
        grid.attach(self.buttonWidget,1,12,1,1)

        # self.buttonClear = Gtk.Button(label="Clear table")
        # self.buttonClear.set_border_width(buttonWidth)
        # grid.attach(self.buttonClear,3,11,1,1)

        #Column5 Statistic List
        self.software_liststore = Gtk.ListStore(int,str,str,int,str,str)
        self.current_filter_language = None

        self.language_filter = self.software_liststore.filter_new()
        self.language_filter.set_visible_func(self.language_filter_func)

        self.treeview = Gtk.TreeView.new_with_model(self.software_liststore)
        self.treesorted = Gtk.TreeModelSort(self.software_liststore)

        self.column = [None] * 6
        for i in xrange(6):
            self.column[i] = 1
        for i, column_title in enumerate(["Num/D","Source vertice", "Destination vertice", "Value","Section","Specialization"]):
            renderer = Gtk.CellRendererText()
            self.column[i] = Gtk.TreeViewColumn(column_title, renderer, text=i)
            self.column[i].set_sort_column_id(i)
            self.treeview.append_column(self.column[i])

        self.scrollable_treelist = Gtk.ScrolledWindow()
        self.scrollable_treelist.set_vexpand(True)
        self.scrollable_treelist.add(self.treeview)
        self.scrollable_treelist.set_border_width(buttonWidth)
        self.scrollable_treelist.set_size_request(700,300)

        grid.attach(self.scrollable_treelist,4,2,1,10)
        self.connect("key_press_event", self.showPaths)

    def showPaths(self,widget,event):
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

            jterator = 0
            for i in self.column:
                i.set_visible(True)

            try:
                for j in self.validPaths[self.pathsIter][:-1]:

                    #Same specializations
                    specials = ""
                    for specs in self.graph.vpropSpecializations[self.validPaths[self.pathsIter][jterator]]:
                        if specs in self.graph.vpropSpecializations[self.validPaths[self.pathsIter][jterator+1]]:
                            specials += specs + "  "

                    #Insert data to
                    self.software_liststore.append(
                          [jterator,
                          self.graph.vpropSurname[self.validPaths[self.pathsIter][jterator]],
                          self.graph.vpropSurname[self.validPaths[self.pathsIter][jterator+1]],
                          int(self.graph.epropCounter[self.graph.g.edge( self.validPaths[self.pathsIter][jterator], self.validPaths[self.pathsIter][jterator+1] ) ]),
                          specials])
                    jterator += 1
            except:
                pass

    def chooseSearchAlg(self, widget, event):
        if event.keyval == Gdk.KEY_Return:
            if self.comboChooseAlg.get_active() == 2:
                self.findA()
            elif self.comboChooseAlg.get_active() == 1:
                self.findFromTo()

    def findA(self):

        source = self.textBoxFrom.get_text()
        destination = self.textBoxTo.get_text()

        dist, pred,destinationV,touch_v,touch_e, target = self.graph.findPathA(source,destination)

        self.software_liststore.clear()


        ecolor = self.graph.g.new_edge_property("string")
        ewidth = self.graph.g.new_edge_property("double")
        ewidth.a = 1

        for e in self.graph.g.edges():
            ecolor[e] = "#3465a4" if touch_e[e] else "#d3d7cf"


        v = target
        path = []
        while v != self.graph.g.vertex(destinationV):
             p = self.graph.g.vertex(pred[v])
             for e in v.out_edges():
                 if e.target() == p:
                    ecolor[e] = "#a40000"
                    ewidth[e] = 3
                    path.append(e)
             v = p

        self.software_liststore.clear()
        for i in self.column:
            i.set_visible(True)

        for i, j in enumerate(path):

            specials = ""
            for specs in self.graph.vpropSpecializations[j.source()]:
                if specs in self.graph.vpropSpecializations[j.target()]:
                    specials += specs + "  "

            self.software_liststore.append([i,
                                        self.graph.vpropSurname[j.source()],
                                        self.graph.vpropSurname[j.target()],
                                        int(self.graph.epropCounter[self.graph.g.edge( j.source(), j.target() )]),
                                        self.graph.vpropMail[j.source()] + " " + self.graph.vpropMail[j.target()],
                                        specials
                                         ])

        graph_draw(self.graph.g, pos=self.graph.GlobalPos, output_size=(300, 300), vertex_fill_color=touch_v,
                        vcmap=matplotlib.cm.binary, edge_color=ecolor,
                        edge_pen_width=ewidth, output="astar-delaunay.pdf")

    def generateImage(self,widget,event):
        if event.keyval == Gdk.KEY_Return:
            fileName = self.textBoxFilename.get_text()
            fileDir = self.onFolderClicked1()

            if self.comboLayout.get_active() == 1:
                self.graph.drawGraphArfLayout(fileName)
            elif self.comboLayout.get_active() == 2:
                self.graph.drawGraphFruchtermanReingoldLayout(fileName)
            shutil.move(os.getcwd()+"/"+fileName+".png",fileDir)

    def generateInteractive(self,widget,event):
        self.graph.interactiveWindow()

    def generateWidget(self,widget,event):
        self.graph.graphWidget(self.comboChooseAdd.get_active(), self.textBoxAddons.get_text() )

    def findFromTo(self):
        source = self.textBoxFrom.get_text()
        destination = self.textBoxTo.get_text()

        self.software_liststore.clear()

        self.validPaths = []
        self.validPaths = self.graph.findPath(source, destination)

        if bool(self.validPaths) == False:
            return
        for i in self.column:
            i.set_visible(True)
        else:
                #try:
            self.pathsIter = 0
            jterator = 0
            for j in self.validPaths[self.pathsIter][:-1]:
                    #Same specializations
                specials = ""
                for specs in self.graph.vpropSpecializations[self.validPaths[self.pathsIter][jterator]]:
                    if specs in self.graph.vpropSpecializations[self.validPaths[self.pathsIter][jterator+1]]:
                        specials += specs + "  "
                    #Insert data to liststore
                self.software_liststore.append(
                      [jterator,
                      self.graph.vpropSurname[self.validPaths[self.pathsIter][jterator]],
                      self.graph.vpropSurname[self.validPaths[self.pathsIter][jterator+1]],
                      int(self.graph.epropCounter[self.graph.g.edge( self.validPaths[self.pathsIter][jterator], self.validPaths[self.pathsIter][jterator+1] ) ]),
                      specials
                      ])
                jterator += 1

    def comboShow(self,widget):
        #Set sortable
        j = 0
        for i in self.column:
            i.set_sort_column_id(j)
            j += 1

        #Show all the vertices of the graph
        if self.combo.get_active() == 1:
            self.software_liststore.clear()
            for i in self.column:
                i.set_visible(True)
            self.column[2].set_visible(False)
            for v in self.graph.g.vertices():
                #Print specializations
                specials = ""
                for j in self.graph.vpropSpecializations[v]:
                    specials += j + "  "

                self.software_liststore.append([
                    int(v),
                    self.graph.vpropSurname[self.graph.g.vertex(v)],
                    None,
                    int(self.graph.vpropNeighbours[v]),
                    self.graph.vpropMail[self.graph.g.vertex(v)],
                    specials
                    ])
            #self.software_liststore.set_sort_column_id(2, 1)
            #self.combo.set_active(0)

        #Show all edges of the graph
        if self.combo.get_active() == 2:
            self.software_liststore.clear()
            for i in self.column:
                i.set_visible(True)
            for iterator,e in enumerate(self.graph.g.edges()):

                #Print the same specializations
                specials = ""
                for j in self.graph.vpropSpecializations[self.graph.g.vertex(e.source())]:
                    if j in self.graph.vpropSpecializations[self.graph.g.vertex(e.target())]:
                        specials += j + "  "

                self.software_liststore.append([
                iterator,
                self.graph.vpropSurname[self.graph.g.vertex(e.source())],
                self.graph.vpropSurname[self.graph.g.vertex(e.target())],
                int(self.graph.epropCounter[self.graph.g.edge( e.source(), e.target())]),
                self.graph.vpropMail[self.graph.g.vertex(e.source())] + " " + self.graph.vpropMail[self.graph.g.vertex(e.target())],
                specials
                ])
            #self.combo.set_active(0)

    def printSpecs(self,widget,event):
        if event.keyval == Gdk.KEY_Return:

            self.software_liststore.clear()
            for i in self.column:
                i.set_visible(True)
            self.column[3].set_visible(False)
            spec = self.textBoxFindSpec.get_text()

            iterator = 0
            for v in self.graph.g.vertices():
                if spec in self.graph.vpropSpecializations[v]:
                    self.software_liststore.append([iterator,self.graph.vpropSurname[v],None,None, self.graph.vpropMail[v],spec])
                    iterator += 1

            for e in self.graph.g.edges():
                if (spec in self.graph.vpropSpecializations[e.source()]) and (spec in self.graph.vpropSpecializations[e.target()]):
                    self.software_liststore.append([iterator,self.graph.vpropSurname[e.source()],self.graph.vpropSurname[e.target()],None,self.graph.vpropMail[e.source()] + " " + self.graph.vpropMail[e.target()],spec,])
                    iterator += 1

    def printFind(self,widget):

        iterator = self.comboDeep.get_active_id()
        self.software_liststore.clear()
        find = None
        for v in self.graph.g.vertices():
            #Find vertex
            if self.graph.vpropSurname[v] == self.textBoxFind.get_text():
                find = v
                break

        if bool(find) == False:
            self.software_liststore.append(["Node not found", None, None, None, None])
            return

        elif int(iterator)-1 == 0:
            for i in self.column:
                i.set_visible(True)
            self.column[0].set_visible(False)
            self.column[3].set_visible(False)

            specials = ""
            for j in self.graph.vpropSpecializations[v]:
                specials += j + "  "

            self.software_liststore.append([None,self.graph.vpropSurname[v], "Node has been found", int(self.graph.vpropNeighbours[v]), self.graph.vpropMail[v], specials])
        #Find neighbours

        visited = []
        selected = []
        tmp = []
        self.column[0].set_visible(True)
        self.column[3].set_visible(True)
        selected.append(int(find))
        for i in xrange(0, int(iterator)-1):
            for v in self.graph.g.vertices():
                if (int(v) in selected) and (int(v) not in visited):
                    for e in v.out_neighbours():
                        if int(e) not in visited:

                            #Same specializations
                            specials = ""
                            for j in self.graph.vpropSpecializations[self.graph.g.vertex(v)]:
                                if j in self.graph.vpropSpecializations[self.graph.g.vertex(e)]:
                                    specials += j + "  "

                            tmp.append(int(e))
                            self.software_liststore.append([
                                i+1,
                                self.graph.vpropSurname[v],
                                self.graph.vpropSurname[e],
                                int(self.graph.epropCounter[self.graph.g.edge( v, e)]),
                                self.graph.vpropMail[v] + " " + self.graph.vpropMail[e],
                                specials
                                ])
                    visited.append(int(v))
            for t in tmp:
                selected.append(t)
            tmp = []

    def language_filter_func(self, model, iter, data):
        if self.current_filter_language is None or self.current_filter_language == "None":
            return True
        else:
            return model[iter][0] == self.current_filter_language

    def onFileClicked(self, widget):
        dialog = Gtk.FileChooserDialog("Please choose a file", self,
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        self.addFilters(dialog)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print("Open clicked")
            print("File selected: " + dialog.get_filename())
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")

        dialog.destroy()

    def addFilters(self, dialog):
        filter_text = Gtk.FileFilter()
        filter_text.set_name("Text files")
        filter_text.add_mime_type("text/plain")
        dialog.add_filter(filter_text)

        filter_py = Gtk.FileFilter()
        filter_py.set_name("Python files")
        filter_py.add_mime_type("text/x-python")
        dialog.add_filter(filter_py)

        filter_any = Gtk.FileFilter()
        filter_any.set_name("Any files")
        filter_any.add_pattern("*")
        dialog.add_filter(filter_any)

    def onFolderClicked(self, widget):
        dialog = Gtk.FileChooserDialog("Please choose a folder", self,
            Gtk.FileChooserAction.SELECT_FOLDER,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             "Select", Gtk.ResponseType.OK))
        dialog.set_default_size(800, 400)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            fileDir = dialog.get_filename()
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")
        dialog.destroy()

        try:
            self.graph.g.save("my_self.graph.graphml")
            shutil.move(os.getcwd()+"/my_self.graph.graphml",fileDir)
        except:
            print "AAAA"

    def onFolderClicked1(self):
        dialog = Gtk.FileChooserDialog("Please choose a folder", self,
            Gtk.FileChooserAction.SELECT_FOLDER,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             "Select", Gtk.ResponseType.OK))
        dialog.set_default_size(800, 400)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            tmp = dialog.get_filename()
            dialog.destroy()
            return tmp
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")

        dialog.destroy()

    def onAboutClicked(self, widget):
        win = About()

        win.connect("delete_event", Gtk.main_quit)
        win.show_all()
        Gtk.main()

    def h(self, v, target, pos):
        return np.sqrt(sum((pos[v].a - pos[target].a) ** 2))

    def setActive(self,widget):
        if self.comboChooseAdd.get_active() == 1 or self.comboChooseAdd.get_active() == 2:
            self.textBoxAddons.set_sensitive(True)
        else:
            self.textBoxAddons.set_text("")
            self.textBoxAddons.set_sensitive(False)

    def openDatabase(self,widget):
        win = DatabaseWindow(self.graph)
        win.connect("delete_event", Gtk.main_quit)
        win.show_all()
        Gtk.main()
