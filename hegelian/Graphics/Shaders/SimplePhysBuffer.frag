// LogBuffer.frag

uniform sampler3D tex3d;

varying vec4 pos;

void main() 
{
	vec4 outdata = vec4(0.0, 0.0, 0.0, 0.0);
	vec4 outcolour = vec4(0.0, 0.0, 0.0, 0.0);
	//vec4 extinction = vec4(0.0, 0.0, 0.0, 0.0);
	vec4 emission;// = vec4(0.0, 0.0, 0.0, 0.0);
	vec4 newcol1 = vec4(0.398, 0.757, 0.644, 1.0);
	vec4 newcol2 = vec4(0.984, 0.550, 0.382, 1.0);
	vec4 newcol3 = vec4(0.550, 0.625, 0.792, 1.0);
	float ion;
	float neut;
	float nH2;
	float hot;
	float iz;
	float dz = 1.0/256.0;
	//float dz = 1.0/350.0 * 2.0; // HEURISTIC HACK - TODO, FIGURE THIS OUT BETTER
	vec4 colour = vec4(0.0, 0.0, 0.0, 0.0);
	vec4 coord = vec4(0.0, 0.0, 0.0, 0.0);
	for (iz=-1.0; iz < 1.0; iz += dz)
	{
		// r = rho, g = T, b = xHII
		coord = gl_TextureMatrix[0] * vec4(pos.x,pos.y,iz,1.0);
		colour = texture3D(tex3d, coord.xyz);
		// Do a very simple model of extinction / emission
		// HACK - set distance between planes as 0.1 pc
		// 1 cm^-3 * 0.1 pc = 3e17 cm^-2
		//extinction = vec4(1.76e-5,1.76e-4,1.76e-3,0.0)*colour.r;
		nH2 = colour.r*colour.r; 
		ion = nH2*colour.b;
		neut = 1e-6;
		if (colour.g < 1e3)
		{
			neut = nH2*nH2;
		}
		hot = 1e-6;
		if (colour.g > 3e4)
		{
			hot = nH2*nH2;
		}
		emission = vec4(neut,ion,hot,1.0);
		//outcolour = outcolour/pow(vec4(2.73,2.73,2.73,2.73),extinction) + emission;
		// SIMPLE, NO EXTINCTION
		outdata = outdata + emission;
	}
	// Remap colours from RGB to nicer colour scheme
	// TODO: Fix remapping to not normalise out colours
	outcolour.r = newcol1.r * outdata.r + newcol2.r * outdata.g + newcol3.r * outdata.b;
	outcolour.g = newcol1.g * outdata.r + newcol2.g * outdata.g + newcol3.g * outdata.b;
	outcolour.b = newcol1.b * outdata.r + newcol2.b * outdata.g + newcol3.b * outdata.b;
	outcolour.a = 1.0;
	gl_FragColor = outcolour;
}