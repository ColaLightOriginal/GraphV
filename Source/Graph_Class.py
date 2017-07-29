# -*- coding: utf-8 -*-

from graph_tool.all import *
from Queue_Class import *
from Visitor_Example_Class import *
from Graph_Window_Main_Class import *

from gi.repository import Gtk, Gdk, GdkPixbuf, GObject, Pango
import numpy as np
from numpy.random import random
import sys

class Graph():

    g = Graph()
    g.set_directed(False)

    #Property for name and surname
    vpropSurname = g.new_vertex_property("string")
    g.vertex_properties["Surname"] = vpropSurname

    vpropNeighbours = g.new_vertex_property("float")
    g.vertex_properties["Neighbours"] = vpropNeighbours

    vpropSpecializations = g.new_vertex_property("object")
    # g.vertex_properties["Specializations"] = vpropSpecializations

    #Mail
    vpropMail = g.new_vertex_property("string")
    g.vertex_properties["Section"] = vpropMail

    #Property for counter of cooperations
    epropCounter = g.new_edge_property("float")
    g.edge_properties["Counter"] = epropCounter

    #Proprty maps for magazines
    epropMagazines = g.new_edge_property("object")

    edgeCounter = g.new_edge_property("int")
    # g.edge_properties["Counter2"] = edgeCounter

    #Filter property
    epropFilter = g.new_edge_property("bool")
    vpropFilter = g.new_vertex_property("bool")

    #Property for vertex colour
    vcolor = g.new_vertex_property("vector<double>")

    #Property for edge colour
    ecolor = g.new_edge_property("vector<double>")
    orange = 1

    #Predefined colors, maroon, yellow,olive,lime,green,aqua,teal,blue, navy, fuchsia, purple, black, grey, less grey, more grey, strange, strange2
    colors = [[0.7, 0, 0, 0.9],[1,1,0,.9],[.5,.5,0,.9],
            [0,1,0,.9],[0,.5,0,.9],[0,1,1,.9],
            [0,.5,.5,.9],[0,0,1,.9],[0,0,.5,.9],
            [1,0,1,.9],[.5,0,.5,.9],[0,0,0,.9],
            [.5,.5,.5,.9],[.7,.7,.7,.9],[.2,.2,.2,.9],
            [.5,.7,.7,.9],[.7,.7,.2,.9]]


    #Mails to num
    colorNumList = []

    #FR positioning
    ebet = None
    GlobalPos = None
    GlobalPosFR = None
    deg = None

    #Specializations positioning
    GlobalPosSpecialities = None
    GlobalWidgetPosSpecialities = None

    #Arf positioning
    ebetWidget = None
    degWidget = None

    #Pos for specs/Mags
    GlobalWidgetPosSpecs = None

    #Pos for All
    GlobalWidgetPosAll = None
    ebetWidgetAll = None
    degWidgetAll = None

    #Adding a vertex to graph
    def addVertex(self):
        self.g.add_vertex()

    #Adding an edge to graph
    def addEdge(self, vertex1, vertex2):
        self.g.add_edge(self.g.vertex(vertex1), self.g.vertex(vertex2))

    #Arf Layout of drawing a graph
    def drawGraphArfLayout(self, imageName):

        if self.GlobalPos == None:
            self.createPos()

        graph_draw(self.g,
                pos=self.GlobalPos,
                #vertex_text=self.vpropSurname,
                #vertex_font_size = 10,
                vorder=self.deg,
                eorder=None,
                edge_pen_width=self.ebet,
                edge_color=self.ebet,
                vertex_size=self.deg,
                vertex_fill_color=self.vcolor,
                output_size=(1920, 1680),
                output=imageName+".png")

    #fruchterman Reingold of drawing a graph
    def drawGraphFruchtermanReingoldLayout(self, imageName):
        if self.GlobalPosFR == None:
            self.createPosFr()

        graph_draw(self.g,
                pos=self.GlobalPosFR,
                vorder=self.deg,
                eorder=None,
                edge_pen_width=self.ebet,
                edge_color=self.ebet,
                vertex_size=self.deg,
                vertex_fill_color=self.vcolor,
                output_size=(1920, 1680),
                output=imageName+".png")

    #Create Interactive Window
    def interactiveWindow(self):

        graph_tool.draw.interactive_window(self.g,
            pos=self.GlobalPos,
            vertex_text=self.vpropSurname,
            vertex_font_size=10,
            edge_text=self.edgeCounter,
            nodesfirst=True,
            geometry=(800,600),
            edge_pen_width=1,
            update_layout=False,
            async=False,
            no_main=False)

    #Create Widget
    def graphWidget(self, choose, specMag):

        #self.createPosWidget()
        #Magazines
        # self.createPosWidgetMags()

        #Specializations
        #self.createPosWidgetSpecs()

        g2 = self.g.copy()
        vNeighbours = None

        #All Graph
        if choose == 0:
            if self.GlobalWidgetPosAll == None:
                self.createPosWidgetAll(g2)
            self.widgetDef(g2, self.GlobalWidgetPosAll,self.degWidgetAll, self.ebetWidgetAll)

        #Specs Graph
        elif choose == 1:
            g2, vNeighbours = self.createPosWidgetSpecs(specMag,g2)
            self.createPosWidget(g2,vNeighbours)
            self.widgetDef(g2, self.GlobalWidgetPos,self.degWidget,self.ebetWidget)

        #Mags Graph
        elif choose == 2:
            g2 = self.createPosWidgetMags(specMag,g2)
            self.widgetDef(g2, self.GlobalWidgetPos,self.degWidget,self.ebetWidget)

    def widgetDef(self, graph,pos,deg,ebet):
        s = Gdk.Screen.get_default()
        win = GraphWindowMain(
            self,
            graph,
            pos,
            geometry=(s.get_width()-240, s.get_height()-200),
            vprops=None,
            eprops=None,
            vorder=deg,
            eorder=None,
            edge_pen_width=ebet,
            edge_color=ebet,
            vertex_size=deg,
            # #edge_pen_width=1,
            # #vertex_font_size = 10,
            vertex_fill_color=self.vcolor,
            display_props_size=16
            #edge_text=self.epropCounter
            )

        win.connect("delete_event", Gtk.main_quit)
        win.show_all()
        Gtk.main()

    def findPath(self,source,destination):

        q = Queue()
        sourceV = None
        destinationV = None
        parent = None
        paths = []
        pathsC = 0

        for v in self.g.vertices():
            if(self.vpropSurname[v] == source):
                sourceV = int(v)
            elif(self.vpropSurname[v] == destination):
                destinationV = int(v)

        if sourceV == None or destinationV == None:
            return False

        tempPath = [sourceV]
        q.add(tempPath)
        visited = []

        validPaths = []
        counter = 1
        try:
            while bool(q) == True:
                tmpPath = q.remove()
                lastNode = tmpPath[len(tmpPath)-1]
                if lastNode == destinationV and counter >= 0:
                    validPaths.append(tmpPath)
                    counter -= 1
                elif counter == 0:
                    return validPaths
                for n in self.g.vertex(lastNode).out_neighbours():
                    if int(n) not in tmpPath:
                        newPath = tmpPath + [int(n)]
                        q.add(newPath)
        except:
            if(bool(validPaths) == False):
                return False
            else:
                return validPaths

    #Find path with A* algorithm
    def findPathA(self,source,destination):

        if self.GlobalWidgetPosAll == None:
            self.createPosWidgetAll(self.g)

        sourceV = None
        destinationV = None
        for v in self.g.vertices():
            if(self.vpropSurname[v] == source):
                sourceV = int(v)
            elif(self.vpropSurname[v] == destination):
                destinationV = int(v)

        if sourceV == None or destinationV == None:
            return False

        # weight = self.g.new_edge_property("double")
        weight2 = self.epropCounter.copy()

        # weight2.a = 1/weight2.a*10
        for e in self.g.edges():
           weight2[e] = np.sqrt(sum((self.GlobalWidgetPosAll[e.source()].a - self.GlobalWidgetPosAll[e.target()].a) ** 2))

        touch_v = self.g.new_vertex_property("bool")
        touch_e = self.g.new_edge_property("bool")
        target = self.g.vertex(sourceV)

        dist, pred = astar_search(self.g, self.g.vertex(destinationV), weight2,
                                    VisitorExample(touch_v, touch_e, target),
                                    heuristic=lambda v: self.h(v, target, self.GlobalWidgetPosAll))

        return dist, pred, destinationV, touch_v, touch_e, target

    def createPos(self):
        if self.deg == None:
            self.deg = self.vpropNeighbours.copy()
            self.deg.a = 20 * (np.sqrt(self.deg.a) * 0.5 + 0.4)
        if self.ebet == None:
            self.ebet = self.epropCounter.copy()
            self.ebet.a = 4 * (np.sqrt(self.ebet.a) * 0.5 + 0.4)
        self.GlobalPos = arf_layout(self.g, weight=self.ebet, d=0.5, a=2, max_iter=2000)

    def createPosFr(self):
        if self.deg == None:
            self.deg = self.vpropNeighbours.copy()
            self.deg.a = 20 * (np.sqrt(self.deg.a) * 0.5 + 0.4)
        if self.ebet == None:
            self.ebet = self.epropCounter.copy()
            self.ebet.a = 4 * (np.sqrt(self.ebet.a) * 0.5 + 0.4)
        self.GlobalPosFR = fruchterman_reingold_layout(self.g,weight=self.ebet, n_iter=200,r=1900)

    def createPosWidget(self,graph,vNeighbours):
        #self.degWidget = self.vpropNeighbours.copy()
        self.degWidget = vNeighbours
        self.degWidget.a = 10 * (np.sqrt(self.degWidget.a) * 0.5 + 0.4)
        self.ebetWidget = self.epropCounter.copy()
        self.ebetWidget.a = 2 * (np.sqrt(self.ebetWidget.a) * 0.5 + 0.4)
        #self.GlobalWidgetPos = arf_layout(self.g, weight=self.ebetWidget, d=0.5, a=2, max_iter=10000)
        self.GlobalWidgetPos = arf_layout(graph, weight=self.ebetWidget, d=0.5, a=2, max_iter=2000)

    def createPosWidgetAll(self,graph):
        self.degWidgetAll = self.vpropNeighbours.copy()
        #self.degWidgetAll.a = self.degWidgetAll.a
        self.degWidgetAll.a = 5 * (np.sqrt(self.degWidgetAll.a) + 0.4)
        self.ebetWidgetAll = self.epropCounter.copy()
        self.ebetWidgetAll.a = 0.5 * (np.sqrt(self.ebetWidgetAll.a)*0.5 + 0.4)

        # self.GlobalWidgetPosAll = fruchterman_reingold_layout(self.g,weight=self.ebetWidgetAll, n_iter=500)
        self.GlobalWidgetPosAll = arf_layout(graph, weight=self.ebetWidgetAll, d = 0.5, a = 10, max_iter=1000)
        # self.GlobalWidgetPosAll = sfdp_layout(graph, eweight=self.ebetWidgetAll)
        #self.GlobalWidgetPosAll = arf_layout(graph, weight=self.ebetWidgetAll, d = 0.5, a = 50, max_iter=2000)

        #self.GlobalWidgetPosAll = fruchterman_reingold_layout(graph, weight=self.ebetWidget, n_iter=100, r = 1000  )

    def h(self, v, target, pos):
        return np.sqrt(sum((pos[v].a - pos[target].a) ** 2))

    def printVerticies(self):
        iterator = 0
        for v in self.g.vertices():
            print v
            print self.vpropSurname[self.g.vertex(iterator)]
            iterator+=1

    def printEdges(self):
        for e in self.g.edges():
            print e
            print self.epropCounter[self.g.edge( e.source(), e.target() )]

    def addEmp(self, cursorResult):
        iterator = 0
        for emp in cursorResult:
            #Add surnames
            self.addVertex()
            self.vpropSurname[self.g.vertex(iterator)] = cursorResult[iterator][1] + " " + cursorResult[iterator][2]

            #Add color
            for color in self.colorNumList:
                if cursorResult[iterator][4] == color[1]:
                    self.vcolor[self.g.vertex(iterator)] = self.colors[color[0]]
            #self.vcolor[self.g.vertex(iterator)] = self.colors[0]

            self.vpropMail[self.g.vertex(iterator)] = cursorResult[iterator][4]

            #Add specializations
            self.vpropSpecializations[self.g.vertex(iterator)] = []
            try:
                for i in cursorResult[iterator][3].split(" "):
                    self.vpropSpecializations[self.g.vertex(iterator)].append(i)
            except:
                pass
            iterator += 1

    def addCoauthors(self, cursorResult):
        iterator = 0
        for co in cursorResult:

            #Increment
            if self.g.edge(cursorResult[iterator][1]-1, cursorResult[iterator][2]-1) is not None:
                self.epropCounter[cursorResult[iterator][1]-1, cursorResult[iterator][2]-1 ] += 1
                self.edgeCounter[cursorResult[iterator][1]-1, cursorResult[iterator][2]-1 ] += 1
                #Add magazine

                #For magazines in actual edge
                magsSemafor = 0
                for enum, magazines in enumerate(self.epropMagazines[cursorResult[iterator][1]-1, cursorResult[iterator][2]-1]):
                    if magazines[0] == cursorResult[iterator][4]:
                        self.epropMagazines[cursorResult[iterator][1]-1, cursorResult[iterator][2]-1][enum][1] += 1
                        magsSemafor = 1
                        break
                if magsSemafor == 0:
                    self.epropMagazines[cursorResult[iterator][1]-1, cursorResult[iterator][2]-1].append([cursorResult[iterator][4],1])
            #Create new
            else:

                #Add edge counter
                self.addEdge(cursorResult[iterator][1]-1, cursorResult[iterator][2]-1)
                self.epropCounter[cursorResult[iterator][1]-1, cursorResult[iterator][2]-1] = 1
                self.edgeCounter[cursorResult[iterator][1]-1, cursorResult[iterator][2]-1 ] = 1
                #Add magazine to edge
                self.epropMagazines[cursorResult[iterator][1]-1, cursorResult[iterator][2]-1] = []
                self.epropMagazines[cursorResult[iterator][1]-1, cursorResult[iterator][2]-1].append([cursorResult[iterator][4],1])

            iterator += 1

        self.removeUnused()

    #remove unusede vertices
    def removeUnused(self):
        iterator = 0
        delList = []

        for v in self.g.vertices():
            if (self.vpropSurname[v] == "Agnieszka Rosa") or (self.vpropSurname[v] == "Maciej Grochowski") or (self.vpropSurname[v] == "Małgorzata Kowalska") or (self.vpropSurname[v] == "Karolina Zawada"):
                delList.append(v)
                continue
            iterator2 = 0

            for n in v.out_neighbours():
                if (self.vpropSurname[n] == "Agnieszka Rosa") or (self.vpropSurname[n] == "Maciej Grochowski") or (self.vpropSurname[n] == "Małgorzata Kowalska") or (self.vpropSurname[n] == "Karolina Zawada"):
                    continue
                iterator2 +=1

            else:
                self.vpropNeighbours[v] = iterator2
            iterator += 1

        for v in reversed(sorted(delList)):
            self.g.remove_vertex(v)

    def mailToColor(self,cursorResult):
        for i, cursor in enumerate(cursorResult):
            self.colorNumList.append([i,str(cursor[0])])

    def printMagazines(self):
        for e in self.g.edges():
            print e.source()
            print e.target()
            print self.epropMagazines[e]

    def createPosWidgetSpecs(self,spec,graph):
        eFilter = self.epropFilter.copy()
        vFilter = self.vpropFilter.copy()
        vNeighbours = graph.new_vertex_property("int")

        for v in graph.vertices():
            if spec in self.vpropSpecializations[v]:
                vFilter[v] = 1
            else:
                vFilter[v] = 0

        for e in graph.edges():
            specials = ""
            if (spec in self.vpropSpecializations[e.source()]) and (spec in self.vpropSpecializations[e.target()]):
                eFilter[e] = 1
            else:
                eFilter[e] = 0

        graph.set_edge_filter(eFilter)
        graph.set_vertex_filter(vFilter)

        for v in graph.vertices():
            neighboursCount = 0
            for neighbours in v.out_neighbours():
                neighboursCount += 1
            vNeighbours[v] = neighboursCount

        return graph, vNeighbours

    def createPosWidgetMags(self,mag, graph):
        eFilter = self.epropFilter.copy()
        vFilter = self.vpropFilter.copy()

        for v in vFilter:
            v = 0

        self.ebetWidget = self.epropCounter.copy()

        for e in eFilter:
            e = 0

        for e in graph.edges():
            for mags in self.epropMagazines[e]:
                if mags[0] == mag:
                    eFilter[e] = 1
                    vFilter[e.source()] = 1
                    vFilter[e.target()] = 1
                    self.ebetWidget[e] = 2 * (np.sqrt(mags[1]) * 0.5 + 0.4)

        self.GlobalWidgetPos = arf_layout(graph, weight=self.ebetWidget, d=0.5, a=2, max_iter=100)
        graph.set_edge_filter(eFilter)
        graph.set_vertex_filter(vFilter)

        vNeighbours = graph.new_vertex_property("int")
        for v in graph.vertices():
            neighboursCount = 0
            for neighbours in v.out_neighbours():
                neighboursCount += 1
            vNeighbours[v] = neighboursCount

        self.degWidget = vNeighbours.copy()
        self.degWidget.a = 10 * (np.sqrt(self.degWidget.a) * 0.5 + 0.4)

        return graph
