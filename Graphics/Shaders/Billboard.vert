#version 120

uniform vec3 cornerX;
uniform vec3 cornerY;
attribute float size;
attribute float mass;
attribute float cornerIndex;
varying vec4 vertex_color;

void main()
{
	int index = int(cornerIndex);
	gl_Position = gl_ProjectionMatrix 
		* (gl_ModelViewMatrix * vec4(0.0, 0.0, 0.0, 1.0) 
		+ vec4(gl_Vertex.x, gl_Vertex.y, gl_Vertex.z, 0.0));
	gl_Position = gl_ProjectionMatrix * (gl_Vertex + vec4(gl_ModelViewMatrix[3].xyz, 0));
	gl_Position = gl_ProjectionMatrix * gl_ModelViewMatrix * gl_Vertex;
	gl_Position += vec4(cornerX[index]*size,cornerY[index]*size,0.0,0.0);
	//gl_Position = gl_Vertex;
	vertex_color = mass*vec4(1.0,1.0,1.0,1.0);
    //vertex_color = vec4(1.0,1.0,1.0,1.0);
    gl_TexCoord[0].xy = gl_MultiTexCoord0.xy;
}