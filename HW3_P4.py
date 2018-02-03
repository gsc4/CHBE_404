# Gregory Campo
# CHBE 404

import numpy as np
import matplotlib.pyplot as plt

# [ Stream_name, Ts, Tt, mCp ]
H1 = ['H1', 480., 250., 2.*1e-4]
H2 = ['H2', 430., 180., 3.*1e-4]
C1 = ['C1', 100., 400., 2.5*1e-4]
C2 = ['C2', 150., 360., 2.5*1e-4]
C3 = ['C3', 200., 400., 2.5*1e-4]

stream_info = np.array([H1, H2, C1, C2, C3])

delta_t_thres = 0
solved = False
Q_hot = []
Q_cold = []

while delta_t_thres <= 200:

	temps_to_consider = []

	for i in range(len(stream_info)):
		if stream_info[i][0].startswith('H'):
			temp_adjust = delta_t_thres
		else:
			temp_adjust = 0
		for j in range(1,3):
			temps_to_consider.append( float(stream_info[i][j]) - temp_adjust )

	temps_to_consider = list(set(temps_to_consider))
	temps_to_consider.sort(reverse = True)

	Q = []
	for i in range(len(temps_to_consider)-1):
		T_top = temps_to_consider[i]
		T_bot = temps_to_consider[i+1]
		Q_segment = 0
		for j in range(len(stream_info)):

			C = float(stream_info[j][-1])

			if stream_info[j][0].startswith('H'):
				Ts = float(stream_info[j][1]) - delta_t_thres
				Tt = float(stream_info[j][2]) - delta_t_thres
				
				if Ts > T_bot and Tt < T_top:
					Q_segment += C*( min(Ts,T_top) - max(T_bot, Tt) ) 
			
			else:
				Ts = float(stream_info[j][1])
				Tt = float(stream_info[j][2])
			
				if Ts < T_top and Tt > T_bot:
					Q_segment -= C*(min(T_top, Tt) - max(T_bot, Ts))
					
		Q.append(Q_segment)
		
	Q_total = sum(Q)
	Q_cum_sum = np.cumsum(Q)
	
	Q_adjusted = [x - min(Q_cum_sum) for x in Q_cum_sum]
		
	Q_cold.append(Q_adjusted[-1])
	Q_hot.append(-min(Q_cum_sum))
	
	if any( [Q_adjusted[x] == 0 for x in range(1,len(Q_adjusted)-1) ] ) and not solved :
		delta_t_thres_solved = delta_t_thres
		solved = True
	delta_t_thres += .01
	
print 'Threshold Delta T = ', delta_t_thres_solved
cold = plt.plot(np.arange(0,200.01,.01), Q_cold )
hot = plt.plot(np.arange(0,200.01,.01), Q_hot )
plt.legend(['Cold Utility','Hot Utility'], loc=2)
plt.show()