from fann2 import libfann

ann = libfann.neural_net()
ann.create_from_file("train01.net")




"""
0.76544419384 3.03697944287 3.53850010256 6.31235534103 -11.4459334614 -8.01446724593 11.3427959454
1
0.746725612844 3.12653924937 3.55505313253 5.08541817171 9.40949379154 -6.88782057986 -10.2837843499
1
0.759736075972 3.03764420714 3.53262310372 6.00753891237 -10.8540725912 -7.79414735222 11.0414066862
1
0.748380448545 3.00249510571 3.63144631703 5.30379654555 9.77226234444 -6.9053930508 10.9769514013
1
0.756685415256 2.98711135609 3.5086436297 6.13914684236 -10.9737283494 -8.80275821961 -11.6223273671
1
0.746837082005 3.0288256457 3.57493780763 5.22106673194 9.62897342 -6.84356666234 10.2944650594
1
0.759794083292 2.94664707818 3.59582295889 6.67240866149 13.3538186395 8.23982168084 -11.8066991909
1
0.746366669965 2.91929253769 3.59759176357 5.2373117279 9.66003532746 -6.79230082754 10.4647895456
1
0.76810843191 3.12863467064 3.65944212244 6.17811709412 11.4084504933 -7.74331821299 11.1559685051
1
0.73683476055 2.89775453677 3.48247910514 5.17205671376 9.52922594771 -6.7205784234 9.94463569755
"""
print ann.run([0.603922476234,4.69682946077,3.44511393099,4.49804164937,-8.88051163731,-8.44059355095,-8.50509795945])