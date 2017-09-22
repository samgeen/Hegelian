#version 120

varying vec4 vertex_color;
uniform sampler2D texture;

void main()
{   
	vec4 tex = texture2D(texture, gl_TexCoord[0].xy)*vertex_color;
	// TODO: Figure out the empty pixel discard better
	if (tex.r < 1e-7)
	{
		discard;
	}
    gl_FragColor = tex;
}