
// All this does is pass through a texture coordinate and position vector
// Designed to run in parallel with reduction shaders
void main(void)
{
    gl_TexCoord[0] = gl_MultiTexCoord0;
    gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
}