# Backward solver, varying rationality decay for instance medium with s = 0
for i in {2..20}
do
    python main.py instances/medium --backward --export -d $i -s 0
done

# Backward solver, varying number of samples for instance medium with d = 2
for i in {1..15}
do
    for j in {1..100}
    do
        python main.py instances/medium --backward --export -d 2 -s $i
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
