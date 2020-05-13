from compressions import *
import matplotlib.pyplot as plt
import sys

#generate compressions for skew graph
string_size=2000
if(len(sys.argv) > 1):
    string_size = int(sys.argv[1])


points = 2000
# strings = [random_string(string_size) for i in range(points)]
comps = [random_compression(1,string_size) for i in range(points)]
crs = list(map(compressionRatio,comps))
plt.hist(crs)
plt.show()















# iters = 50
# print("generating skew graph for {} chars".format(string_size))
# CRs_to_predict = np.linspace(1, 20, 100)
# generated = []
# for i in range(iters):
# 	print("{} / {}".format(i,iters))
# 	generated.extend([(CR,compressionRatio(random_compression(CR,string_size))) for CR in CRs_to_predict])
# predicted = [p[0] for p in generated]
# actual = [p[1] for p in generated]

# #skew plot
# plt.title('Predicted vs. Resulting Compression Ratio ({} letters)'.format(string_size))
# plt.ylabel('Actual Compression Ratio')
# plt.xlabel('Predicted Compression Ratio')
# plt.xlim((1,20))
# plt.ylim((1,20))
# plt.axes().set_aspect('equal')
# plt.plot(predicted,actual,'.')
# plt.show()