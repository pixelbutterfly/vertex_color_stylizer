# Vertex Color Stylizer
Several functions for modifying vertex colors. For Blender 2.3 and later.

[![vertex_color_stylizer_banner](https://user-images.githubusercontent.com/61604905/234193874-39b382bf-df69-4e2e-acc6-1d360e0f0be9.png)](https://www.youtube.com/watch?v=CAhyvyByPFE)

## Randomize Vertex Colors (soft)
Randomizes color per vertex.

![vertex_color_add_soft_noise](https://user-images.githubusercontent.com/61604905/234193903-e89caadc-70bc-475d-8a41-6e281d2fa68e.png)

## Randomize Vertex Colors (hard)
Randomizes color per face corner.

![vertex_color_add_hard_noise](https://user-images.githubusercontent.com/61604905/234194003-42364227-53e9-4b1a-9e36-42e4dd2d22ca.png)

## Harden Vertex Colors
Averages out the vertex colors per face, giving a faceted look to your colors.

![vertex_color_harden](https://user-images.githubusercontent.com/61604905/234193962-3e2924e7-a172-4915-a649-8bc792f573a3.png)

## Stylize Vertex Colors
Same as 'Harden Colors' but also randomizes the colors of the faces.

![vertex_color_stylize](https://user-images.githubusercontent.com/61604905/234194033-3234ee7d-8f75-4b38-819c-625d73ab3873.png)

## Invert Vertex Colors
Similar to Blender's "invert color" function, but lets you mask by channel including the alpha channel.

![vertex_color_stylizer_invert](https://user-images.githubusercontent.com/61604905/234194279-fb23a8e3-6411-4ab6-b295-edb577a2b8c5.png)

## Blend Vertex Colors
Add, subtract, multiply, mix, or overlay the selected color over the selected faces.

![vertex_color_blend](https://user-images.githubusercontent.com/61604905/234195912-6f64820d-5912-41c4-b864-cbaeccf0676e.png)


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

