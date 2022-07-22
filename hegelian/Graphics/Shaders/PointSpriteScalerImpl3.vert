varying vec4 vertex_color;
varying float wcoord;

uniform float pointSizeMin, pointSizeMax,densScale;

void main() 
{
	gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
	wcoord = gl_Position.w;
	// I have no idea why sqrt works OK-ish; I don't pretend to understand the
	//  perspective matrix, but it's not a linear scaling in w, for sure
	float pointRad = (gl_Color.r * (pointSizeMax-pointSizeMin) + pointSizeMin);
	gl_PointSize = 2000.0 * pointRad	/ sqrt(wcoord);
	vertex_color = vec4(1.0,1.0,1.0,1.0)/pointRad;
}