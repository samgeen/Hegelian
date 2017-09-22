
#extension GL_EXT_geometry_shader4 : enable

// From http://morgan.leborgne.free.fr/GLSL-Shaders.html

void main()
{

    gl_Position = gl_PositionIn[0];
    gl_Position = gl_ProjectionMatrix  * gl_Position;
    EmitVertex();
}
