# this may take a while.
echo 'this may take a while'

mpiexec -n 100 -f ../machinefiles/machinefile-3x4 ./trace_my_trace.py find ./find_path.py > cluster_3x4_my_trace_date_find.txt

echo 'one done'

mpiexec -n 100 -f ../machinefiles/machinefile-3x4 ./trace_my_trace.py fix_prev ./find_path.py > cluster_3x4_my_trace_date_fix_prev.txt

echo 'two done'

mpiexec -n 100 -f ../machinefiles/machinefile-3x4 ./trace_my_trace.py fix_dist ./find_path.py > cluster_3x4_my_trace_date_fix_dist.txt

echo 'three done'
