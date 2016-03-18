from fann2 import libfann

ann = libfann.neural_net()
ann.create_from_file("redOrBlack.net")

print ann.run([0.535915943213, 2.80578521309 ,2.10856436755, 3.25266536956, 6.0806720787, 4.6799151241, -6.08696396883])