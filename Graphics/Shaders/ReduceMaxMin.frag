
// Sample a texture and return the max of a square of values
// NOTE - USES RED VALUE TO CALCULATE MAX AND ALPHA VALUE TO CALCULATE MIN
uniform sampler2D    tex;
uniform float        dt;

float mincompare(float v1, float v2)
{
	if ((v1 <= 0.0) && (v2 <= 0.0)) return 1.0;
	if (v1 <= 0.0) return v2;
	if (v2 <= 0.0) return v1;
	return min(v1,v2);
}

void main(void)
{
    vec4 col0 = texture2D(tex, gl_TexCoord[0].st);
    vec4 col1 = texture2D(tex, gl_TexCoord[0].st - vec2(dt, 0.0));
    vec4 col2 = texture2D(tex, gl_TexCoord[0].st - vec2(0.0, dt));
    vec4 col3 = texture2D(tex, gl_TexCoord[0].st - vec2(dt, dt));
    // Find max in the RGB colours
    float r = max(max(col0.r, col1.r), max(col2.r, col3.r));
    float g = max(max(col0.g, col1.g), max(col2.g, col3.g));
    float b = max(max(col0.b, col1.b), max(col2.b, col3.b));
    r = max(max(r,g),b);
    // Min is a little trickier as we need to ignore zero values
    vec4 as = vec4(col0.a,col1.a,col2.a,col3.a);
    float a = mincompare(mincompare(as[0],as[1]),mincompare(as[2],as[3]));
    // Set the colour to be r = max, a = min
    gl_FragColor = vec4(r,0.0,0.0,a);
}