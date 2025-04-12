# -*- coding: utf-8 -*-

import arcpy
import os


class changeSourceGDB:
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Change Source GDB"
        self.alias = "changeSourceGDB"

        # List of tool classes associated with this toolbox
        self.tools = [updateGDBSource]


class updateGDBSource:
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Update GDB Source"
        self.description = "This toolbox contains a tool that can change the source GDB of multiple layers in a map document"

    def getParameterInfo(self):
        """Define the tool parameters."""
        p0 = arcpy.Parameter(
                displayName = "Old Source GDB",
                name = "old_gdb",
                datatype = "DEWorkspace",
                parameterType = "Required",
                direction = "Input"
                )
        p1 = arcpy.Parameter(
                displayName = "New Source GDB",
                name = "new_gdb",
                datatype = "DEWorkspace",
                parameterType = "Required",
                direction = "Input"
                )
        params = [p0,p1]
        return params

    def isLicensed(self):
        """Set whether the tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter. This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        old_gdb = parameters[0].valueAsText
        new_gdb = parameters[1].valueAsText
        aprx = arcpy.mp.ArcGISProject("CURRENT")
        map_name = aprx.activeMap.name
        m = aprx.listMaps(f"{map_name}")[0]
        for lyr in m.listLayers():
            if lyr.supports("DATASOURCE") and os.path.dirname(lyr.dataSource) == old_gdb:
                lyr.updateConnectionProperties(old_gdb, new_gdb, validate=False)
                arcpy.AddMessage(f"New Data Source for {lyr}: {lyr.dataSource}")
        return

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""
        return

