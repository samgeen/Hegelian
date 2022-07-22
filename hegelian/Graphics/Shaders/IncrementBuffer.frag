
// IncrementBuffer.frag

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

varying vec4 vertex_color;
void main() 
{
	//gl_FragColor = EncodeFloatRGBA(vertex_color.a);
	gl_FragColor = vec4(1.0,1.0,1.0,1.0)*1e-7;
}
