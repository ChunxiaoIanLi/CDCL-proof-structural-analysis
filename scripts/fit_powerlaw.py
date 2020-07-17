import sys
import os
import glob
from scipy import optimize
import matplotlib.pyplot as plt


def f(x, x0, alpha):
    return x0*(x**-alpha)


def fit_powerlaw(filename):
    file = open(filename)
    lines = file.readlines()
    y_data = list(map(lambda x: int(x.split(' ')[1]), lines))
    x_data = list(range(1, len(y_data) + 1))
    plt.plot(x_data, y_data, label='Data Points')

    fit = optimize.curve_fit(f, x_data, y_data)
    x0, alpha = fit[0]
    plt.plot(x_data, f(x_data, x0, alpha), label='Fitted Equation')

    plt.legend(loc="upper right")
    plt.xlabel('Index of variable')
    plt.ylabel('# of Appearances')
    plt.title('Heterogeneity of instance ' + filename.split('\\')[-1].split('/')[-1])
    plt.savefig(filename + '_fitted.png')
    # plt.show()

    fitted_file = open(filename + '_fitted.log', 'w+')
    fitted_file.write(str(x0) + " " + str(alpha) + "\n" + str(fit[1]))

    plt.clf()


def main(argv):
    if len(sys.argv) == 1:
        for filename in ["fit_powerlaw_ex1.dv", "fit_powerlaw_ex2.dv"]:
            fit_powerlaw(filename)
    elif os.path.isfile(argv[1]):
        fit_powerlaw(argv[1])
    else:
        path = argv[1]
        for filename in os.listdir(path):
            if filename.endswith('.dv'):
                fit_powerlaw(os.path.join(path, filename))


if __name__ == "__main__":
    main(sys.argv)
