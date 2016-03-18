from fann2 import libfann

connection_rate = 1
learning_rate = 0.25
num_input = 7
num_hidden = 15
num_output = 1

desired_error = -1
max_iterations = 50000
iterations_between_reports = 10000

ann = libfann.neural_net()
ann.create_sparse_array(connection_rate, (num_input, num_hidden, num_output))
ann.set_learning_rate(learning_rate)
ann.set_activation_function_output(libfann.SIGMOID_SYMMETRIC_STEPWISE)
# ann.set_bit_fail_limit(400)
ann.train_on_file("train01.data", max_iterations, iterations_between_reports, desired_error)

ann.save("train01.net")	