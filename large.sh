# Backward solver, varying rationality decay for instance large with s = 0
#for i in {2..10}
#do
#    python main.py instances/large --backward --export -d $i -s 100
#done

# Backward solver, varying number of samples for instance large with d = 2
for i in 10 20 30 40 50 60 70 80 90 100 120 140 160 180 200
do
    for j in {1..10}
    do
        python main.py instances/large --backward --export -d 2 -s $i
    done
done

# Parametric solver, varying number of samples for instance large with d = 2
for i in 10 20 30 40 50 60 70 80 90 100 120 140 160 180 200
do
    for j in {1..100}
    do
        python main.py instances/large --parametric --export -d 2 -s $i
    done
done