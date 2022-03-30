import instance as it
import backward as bd

a = it.Instance('instances/test')

'''
summ = .0
for w in a._W[0]:
    p = a.p(0, w, ['1'])
    print('p(w = {}): {}'.format(w, p))
    summ += p
print('Sum of probabilities: {}'.format(summ))
'''

s = bd.Backward(a)
s.run_solver()
s.print_policy()