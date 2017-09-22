#version 330
// From mpan3, http://blenderartists.org/forum/showthread.php?204645-1-Million-particles-using-geometry-shader

layout(triangles) in;
layout(triangle_strip, max_vertices = 4) out;
out vec2 texCoord;

in float pointSize;

//#define radius 1.0
//#define layer 1

void main() {
for(int i = 0; i < gl_in.length(); i++) {

float radius = pointSize+0.01;

vec4 p = gl_in[0].gl_Position;
texCoord = vec2(1.0,1.0);
//gl_Position = vec4(p.r+radius, p.g+radius+j*0.05, p.b, p.a);
gl_Position = vec4(p.r+radius, p.g+radius, p.b, p.a);
EmitVertex();

texCoord = vec2(0.0,1.0);
//gl_Position = vec4(p.r-radius, p.g+radius+j*0.05, p.b, p.a);
gl_Position = vec4(p.r-radius, p.g+radius, p.b, p.a);
EmitVertex();

texCoord = vec2(1.0,0.0);
//gl_Position = vec4(p.r+radius, p.g-radius+j*0.05, p.b, p.a);
gl_Position = vec4(p.r+radius, p.g-radius, p.b, p.a);
EmitVertex();

texCoord = vec2(0.0,0.0);
//gl_Position = vec4(p.r-radius, p.g-radius+j*0.05, p.b, p.a);
gl_Position = vec4(p.r-radius, p.g-radius, p.b, p.a);
EmitVertex();


EndPrimitive();
}
//}
}