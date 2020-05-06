from compressions import *
import matplotlib.pyplot as plt
import sys

num_tokens = 500
if(len(sys.argv) > 1):
    num_tokens = int(sys.argv[1])

#generate index diff data
print("generating data")
data = generateData(num_tokens)
print("generated data")
diffs = data[0]
CRs = data[1]
print("fitting data")
piecewiseFit = findPiecewiseFit(data)
print("fitted data")
diffs_predicted = np.linspace(0, 1, num_tokens*2)
CRs_predicted = piecewiseFit.predict(diffs_predicted)

#raw index diff vs compression ratio
plt.title('Index Diff vs Compression Ratio over 10 trials')
plt.ylabel('Average Compression Ratio')
plt.xlabel('Index Diff')
plt.plot(diffs*num_tokens,CRs,'.')
plt.show()

#normalized
plt.title('Index Diff vs Compression Ratio (normalized)')
plt.ylabel('Average Compression Ratio')
plt.xlabel('Index Diff / Num Tokens')
plt.plot(diffs,CRs,'.')
plt.show()

#data^-2
plt.title('Index Diff vs Compression Ratio (transformed)')
plt.ylabel('1 / Average Compression Ratio²')
plt.xlabel('Index Diff / Num Tokens')
plt.plot(diffs,CRs**(-2),'.')
plt.show()

#data^-2 with model
plt.title('Index Diff vs Compression Ratio (transformed)')
plt.ylabel('1 / Average Compression Ratio²')
plt.xlabel('Index Diff / Num Tokens')
plt.plot(diffs,CRs**(-2),'.')
plt.plot(diffs_predicted,CRs_predicted)
plt.show()


#normalized with model
plt.title('Index Diff vs Compression Ratio (normalized)')
plt.ylabel('Average Compression Ratio')
plt.xlabel('Index Diff / Num Tokens')
plt.plot(diffs,CRs,'.')
plt.plot(diffs_predicted,np.reciprocal(np.sqrt(CRs_predicted)))
plt.show()