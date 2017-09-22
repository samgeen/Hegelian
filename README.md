HEGELIAN
=====

"Helping Everyone Graph Emitted Light from Interactive Artificial Nebulae"

Making the abstract concrete

3D real-time astrophysics simulation visualisation

Sam Geen (samgeen@gmail.com)

=====

See LICENSE.md for license info

This is a severely work-in-progress architecture for visualising RAMSES outputs in 3D. 

The current entry point for testing is Examples/example.py

Current functionality:
- displays uniform cubes with OpenGL + a shader that can ray-trace through 3 channel texture cubes
- has a rotating camera
- finds the max/min of the image with a shader and displays the log of the image in float precision
- a placeholder shader that shows neutral/ionised gas channels
- a routine that converts RAMSES files into uniform cubes with Pymses

It has some dead/non-functional code that
- billboards particles to screen (slow / possibly broken)

TODO:
- Make a much nicer interface to the code
- Tidy up a lot
- Add emission/extinction tables for nebulae / galaxies
- Merge particle / grid output
- Octree or non-uniform structures (mini-ramses format might help?)
- In-situ snapshot reading / caching
- Reference physical units rather than arbitrary code units
- Optimise heavily
- 3D stereoscopic images / planetarium view matrix output
- More camera types (fly-through)
- Video recording capability
- Cosmology view / synthetic observations / telescope simulations
- Optimise camera input controls (e.g. add flag/dt to keyboard controls rather than relying on refresh rate of keyboard)