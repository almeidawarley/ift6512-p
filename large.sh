# Backward solver, varying rationality decay for instance large with s = 0
for i in {2..10}
do
    python main.py instances/large --backward --export -d $i -s 100
done

# Backward solver, varying number of samples for instance large with d = 2
for i in {1..512}
do
    for j in {1..10}
    do
        python main.py instances/large --backward --export -d 2 -s $i
    done
done

# Parametric solver, varying number of samples for instance large with d = 2
for i in {1..15}
do
    for j in {1..100}
    do
        python main.py instances/large --parametric --export -d 2 -s $i
    done
done