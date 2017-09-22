#version 120

varying vec4 vertex_color;
varying float wcoord;

uniform sampler2D texture;

void main()
{
	gl_FragColor = texture2D(texture, gl_TexCoord[0].st/wcoord) * vertex_color;
    //gl_FragColor = texture2D(texture, gl_PointCoord) * vertex_color;
}