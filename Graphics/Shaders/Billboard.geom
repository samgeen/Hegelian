#version 150
#extension GL_EXT_geometry_shader4 : enable

// From http://morgan.leborgne.free.fr/GLSL-Shaders.html

#uniform float sphere_radius;

//varying out vec3 vertex_light_position;
varying out vec4 eye_position;
void main()
{
	float sphere_radius = 1.0;
    float halfsize = sphere_radius * 0.5;

    gl_TexCoord[0] = gl_TexCoordIn[0][0];
    gl_FrontColor = gl_FrontColorIn[0];

    //vertex_light_position = normalize(gl_LightSource[0].position.xyz);
    eye_position = gl_PositionIn[0];

    // Vertex 1
    gl_TexCoord[0].st = vec2(-1.0,-1.0);
    gl_Position = gl_PositionIn[0];
    gl_Position.xy += vec2(-halfsize, -halfsize);
    gl_Position = gl_ProjectionMatrix  * gl_Position;
    EmitVertex();

    // Vertex 2
    gl_TexCoord[0].st = vec2(-1.0,1.0);
    gl_Position = gl_PositionIn[0];
    gl_Position.xy += vec2(-halfsize, halfsize);
    gl_Position = gl_ProjectionMatrix  * gl_Position;
    EmitVertex();

    // Vertex 3
    gl_TexCoord[0].st = vec2(1.0,-1.0);
    gl_Position = gl_PositionIn[0];
    gl_Position.xy += vec2(halfsize, -halfsize);
    gl_Position = gl_ProjectionMatrix  * gl_Position;
    EmitVertex();

    // Vertex 4
    gl_TexCoord[0].st = vec2(1.0,1.0);
    gl_Position = gl_PositionIn[0];
    gl_Position.xy += vec2(halfsize, halfsize);
    gl_Position = gl_ProjectionMatrix  * gl_Position;
    EmitVertex();

    EndPrimitive();
}
