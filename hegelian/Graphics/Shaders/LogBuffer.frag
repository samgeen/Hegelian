
// LogBuffer.frag

// From http://aras-p.info/blog/2008/06/20/encoding-floats-to-rgba-again/
// NOTE: -0.5/255.0 IS DEPENDENT ON GRAPHICS CARD - SEE LINK ABOVE
vec4 EncodeFloatRGBA( float v ) 
{
	return fract( vec4(1.0, 255.0, 65025.0, 160581375.0) * v ) - 0.5/255.0;
}
float DecodeFloatRGBA( vec4 colour ) 
{
	return dot( colour, vec4(1.0, 1.0/255.0, 1.0/65025.0, 1.0/160581375.0) );
}

uniform sampler2D tex;
varying vec4 vertex_color;
uniform float texmin;
uniform float texinvrng;
void main() 
{
	vec4 colour = texture2D(tex,gl_TexCoord[0].st);
	//float intensity = (log(colour.r) - texmin) * texinvrng;
	//gl_FragColor = vec4(intensity,intensity,intensity,1.0);
	gl_FragColor = (log(colour) - texmin) * texinvrng;
}