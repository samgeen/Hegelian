// LogBuffer.frag

uniform sampler3D tex3d;

varying vec4 pos;

void main() 
{
	vec4 outcolour = vec4(0.0, 0.0, 0.0, 0.0);
	//vec4 extinction = vec4(0.0, 0.0, 0.0, 0.0);
	vec4 emission;// = vec4(0.0, 0.0, 0.0, 0.0);
	float ion;
	float neut;
	float nH2;
	float iz;
	//float dz = 1.0/256.0 * 2.0;
	float dz = 1.0/350.0 * 2.0; // HEURISTIC HACK - TODO, FIGURE THIS OUT BETTER
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
		neut = nH2*0.01;
		//emission = vec4(0.0,1.0,1.0,1.0)*colour.r*colour.r*colour.b + vec4(1.0,0.01,0.0,0.0)*colour.r*colour.r*0.01;
		emission = vec4(neut,ion+0.01*neut,ion,ion);
		//outcolour = outcolour/pow(vec4(2.73,2.73,2.73,2.73),extinction) + emission;
		// SIMPLE, NO EXTINCTION
		//emission = vec4(1.0,0.1,0.0,0.0)*colour.r*colour.r;
		outcolour = outcolour + emission;
	}
	gl_FragColor = outcolour;
}