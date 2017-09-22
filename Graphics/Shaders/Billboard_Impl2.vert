#version 330
// From mpan3, http://blenderartists.org/forum/showthread.php?204645-1-Million-particles-using-geometry-shader

uniform mat4 viewMatrix, projMatrix;

in vec4 vertex;
in vec4 gl_Color;
uniform float pointSizeMin, pointSizeMax,densScale;
out float pointSize;

void main() 
{
	vec4 v = vertex;
	pointSize = (gl_Color.r * (pointSizeMax-pointSizeMin) + pointSizeMin);
	//v.z = sin(timer+v.y+v.x)*0.5+v.z;
	//v.x = sin(timer*10.0+v.y+v.y)*0.2+v.x;
	//gl_Position = gl_ModelViewProjectionMatrix * v;
}
