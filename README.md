# Vertex Color Stylizer
Several functions for modifying vertex colors. For Blender 2.3 and later.

[![vertex_color_stylizer_banner](https://user-images.githubusercontent.com/61604905/234193874-39b382bf-df69-4e2e-acc6-1d360e0f0be9.png)](https://www.youtube.com/watch?v=CAhyvyByPFE)

## Randomize Vertex Colors (soft)
Randomizes color per vertex.

![vertex_color_add_soft_noise](https://github.com/pixelbutterfly/vertex_color_stylizer/assets/61604905/aca37b55-dab1-45c7-888b-c31703defc0b)

## Randomize Vertex Colors (hard)
Randomizes color per face corner.

![vertex_color_add_hard_noise](https://github.com/pixelbutterfly/vertex_color_stylizer/assets/61604905/22fd8573-e5c4-427a-be99-e85596338975)

## Harden Vertex Colors
Averages out the vertex colors per face, giving a faceted look to your colors.

![vertex_color_harden](https://github.com/pixelbutterfly/vertex_color_stylizer/assets/61604905/48b636ae-df77-4f17-ba59-b8dccaece3d6)

## Stylize Vertex Colors
Same as 'Harden Colors' but also randomizes the colors of the faces.

![vertex_color_stylize](https://github.com/pixelbutterfly/vertex_color_stylizer/assets/61604905/6d6935e5-f925-4429-bcaf-795e072738a4)

## Invert Vertex Colors
Similar to Blender's "invert color" function, but lets you mask by channel including the alpha channel.

![vertex_color_stylizer_invert](https://github.com/pixelbutterfly/vertex_color_stylizer/assets/61604905/fdb337ef-d9b3-44d3-b8ba-9951bb567ddd)

## Blend Vertex Colors
Add, subtract, multiply, mix, or overlay the selected color over the selected faces.

![vertex_color_blend](https://github.com/pixelbutterfly/vertex_color_stylizer/assets/61604905/27f435da-e476-42e6-b384-42bb25cbcdd5)

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

