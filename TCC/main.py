import fitness as fit
import setup
from setup import chrom as chrom

print(fit.getFitness("x5", chrom))

print(fit.getFitness("x1 + x2 + x5", chrom))

print(fit.getFitness("x5**x4 - sqrt(x1)", chrom))

print(fit.getFitness("x1/x2 - x3*x4**2 + 10*(x1+x5)", chrom))

print(fit.getFitness("sqrt(x1 + x2) - x3*ln(exp(x5))", chrom))
