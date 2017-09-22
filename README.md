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

BRIEF STYLE GUIDE
This is not exhaustive and I probably break these myself, but I guess it's useful to have.
If you don't know how to do some of this stuff feel free to ask!
- This is a more or less Object Oriented project (insofar as Python allows/needs OO).
- Most functionality is provided by objects containing other objects
- Variables are camel case
- Objects and methods begin with an upper case letter (MyObject.Method), variables a lower case letter (myVariable)
- Try to avoid inheritance (Python doesn't really need inheritance for abstract types, but if it helps use that)
- Try to use composition rather than inheritance to extend functionality wherever possible
- Stuff like multiple inheritance, inheritance of concrete classes is bad
- All data in classes is private, and all methods that don't need to be public should be private.
- A leading underscore means private (e.g. self._camera, self._DoInternalStuffICanBreakLater)
- Try not to make huge .py files, break them up into separate modules if possible (few objects in 1 module at most)
- If you have any opinions on documentation and unit tests please let me know, otherwise try to comment every few lines