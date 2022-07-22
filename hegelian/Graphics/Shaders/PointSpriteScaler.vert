varying vec4 vertex_color;
varying float wcoord;

uniform float pointSize;

void main() 
{
	gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
	wcoord = gl_Position.w;
	// I have no idea why sqrt works OK-ish; I don't pretend to understand the
	//  perspective matrix, but it's not a linear scaling in w, for sure
	gl_PointSize = 5.0 * pointSize / sqrt(wcoord);
	vertex_color = gl_Color;
}