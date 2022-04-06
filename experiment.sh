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

# Parametric solver, varying number of samples for instance medium with d = 2
for i in {1..15}
do
    for j in {1..100}
    do
        python main.py instances/medium --parametric --export -d 2 -s $i
    done
done

python main.py instances/large --backward --export -d 2 -s 0