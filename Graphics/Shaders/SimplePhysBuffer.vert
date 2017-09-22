
varying vec4 pos;

void main() 
{
	pos = gl_ModelViewProjectionMatrix * gl_Vertex;
	gl_Position = pos;
    gl_TexCoord[0] = gl_TextureMatrix[0] * gl_Vertex; //gl_MultiTexCoord0;
	//gl_Position = gl_TextureMatrix[0] * gl_Vertex;
}
