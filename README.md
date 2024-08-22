![](/docs/Clean_thumb.png)

Blender add-on for exporting mesh (.buffer) files for use in the Defold game engines mesh components. Options allow the user to choose what attribute streams they wish to export, keeping their game asset files lean.

How to install:

Go to Edit menu > preferences > Get Extensions , With internet enabled search filter "Add-ons" and Repositories set to "extensions.blender.org" search for "Clean Exporter" now should show up as available with a convenient install button.

![](/docs/Addon_search.png)

Alternatively you can download a github release and install in blender from disk option. There is a legacy release version that may work in older versions of blender pre 4.2. The current legacy version was tested using blender 3.1.2

## How to use:

After successful install you can find the add-on in 3Dview > N-panel. While in 3d view press the N key to bring up property panels then choose the CLEAN panel. 

![](/docs/Clean_Panel.png)

Next select one or more mesh objects for export. Note: each selected mesh object will be exported into it's own .buffer file and all non-mesh objects will be ignored. Select which attribute streams you would like to export (each stream can be accessed as needed in shader's ).  Choose an output directory to your project. Now ready to export!

## Streams:

∙ Vertex position - exports stream by default.

∙ Normals stream

∙ UV coordinates - exports as named in blender ( Properties > Data > UV Maps ). In Defold built-ins shader's use “texcoord0” as UV attribute name.

∙ Tangents stream

∙ Vertex Colors - Can be accessed in shader's as "color" attribute.

Y-UP: Rotates object(s) and applies transform to match Defold's right hand Cartesian coordinate system.

Output Directory: file path for export.

## Defold project: 

After exporting from blender you should now be ready to add the mesh .buffer files to mesh components in Defold.

![](/docs/Defold_Mesh_component.png)

![](/docs/Defold_build.png)