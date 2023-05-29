# Vertex Color Stylizer
Several functions for modifying vertex colors. For Blender 2.3 and later.

![vertex_color_stylizer_banner](https://github.com/pixelbutterfly/vertex_color_stylizer/assets/61604905/2f497ecf-eaf7-4132-a483-4281e72cd23d)

![vertex_color_stylizer](https://github.com/pixelbutterfly/vertex_color_stylizer/assets/61604905/bab325c0-fe1a-40fa-adb8-6db10c88efcf)

## Randomize Vertex Colors (soft)
Randomizes color per vertex.

![vertex_color_randomize_soft](https://github.com/pixelbutterfly/vertex_color_stylizer/assets/61604905/c4dc9e59-c553-4253-9427-e559181eaff9)

## Randomize Vertex Colors (hard)
Randomizes color per face corner.

![vertex_color_randomize_hard](https://github.com/pixelbutterfly/vertex_color_stylizer/assets/61604905/80782ac4-12d0-4d1a-ba06-ee4638f6e0c0)

## Harden Vertex Colors
Averages out the vertex colors per face, giving a faceted look to your colors.

![vertex_color_harden](https://github.com/pixelbutterfly/vertex_color_stylizer/assets/61604905/f224b324-995a-4f8f-8c32-02b9923a1570)

## Stylize Vertex Colors
Same as 'Harden Colors' but also randomizes the colors of the faces.

![vertex_color_stylize](https://github.com/pixelbutterfly/vertex_color_stylizer/assets/61604905/62a6dce5-20b9-490f-8a02-0ffbae7eeda6)

## Invert Vertex Colors
Similar to Blender's "invert color" function, but lets you mask by channel including the alpha channel.

![vertex_color_invert](https://github.com/pixelbutterfly/vertex_color_stylizer/assets/61604905/9ac8305d-a1af-4587-b602-ca24644d45e4)

## Blend Vertex Colors
Add, subtract, multiply, mix, or overlay the selected color over the selected faces. Different options for working on selected faces and on selected verts (when in edit mode).

![vertex_color_blend](https://github.com/pixelbutterfly/vertex_color_stylizer/assets/61604905/520705c4-9d7f-4992-89f4-28aeda7ec3aa)

## Notes
* All functions work in any viewport mode on the selected objects or (in edit mode) on the selected faces. 
* Stylize, Harden, and Randomize Colors (hard) require face corner vertex colors to work.
* Operations work on the currently selected color attribute. If it looks like nothing's happening, check that you're rendering the right color attribute.
* Blend modes respect the alpha value. Use an alpha of 1 to get full intensity blend strength.

## Installation
* Get the latest vertexColorStylizer.py release in: https://github.com/pixelbutterfly/vertex_color_stylizer
* start Blender and open the user preferences
* switch to the Add-ons tab and click the Install Add-on from file... button at the bottom
* locate the downloaded vertexColorStylizer.py file and double-click it
* search for the addon "Vertex Color Stylizer"
* activate the addon by ticking the checkbox (hit the Save User Settings button at the bottom if your blender is setup that way)

