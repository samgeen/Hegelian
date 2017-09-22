
// Sample a texture and return the max of a square of values
uniform sampler2D    tex;
uniform float        dt;

void main(void)
{
    vec4 col0 = texture2D(tex, gl_TexCoord[0].st);
    vec4 col1 = texture2D(tex, gl_TexCoord[0].st - vec2(dt, 0.0));
    vec4 col2 = texture2D(tex, gl_TexCoord[0].st - vec2(0.0, dt));
    vec4 col3 = texture2D(tex, gl_TexCoord[0].st - vec2(dt, dt));
    float r = max(max(col0.r, col1.r), max(col2.r, col3.r));
    gl_FragColor = vec4(r,r,r,1.0);
}