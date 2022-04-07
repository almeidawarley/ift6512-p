# List of experiments ran for the results in the report

# Compute (full) backward policy for instance medium
python main.py instances/medium --backward --export -d 2
# Compute (sampled) backward policy for instance large
python main.py instances/large --backward --export -d 2 -s 512

# Compute (full) parametric policy for instance large
python main.py instances/medium --parametric --export -d 2
# Compute (sampled) parametric policy for instance large
python main.py instances/large --parametric --export -d 2 -s 512

# Compute (sampled) backward solver for parameter d = 2
# Varying number of samples for graphs of question #3
for i in {1..15}
do
    for j in {1..100}
    do
        python main.py instances/medium --backward --export -d 2 -s $i
    done
done

# Compute (sampled) backward solver for parameter d = 2
# Varying number of samples for graphs of question #3
for i in 10 20 30 40 50 60 70 80 90 100 120 140 160 180 200
do
    for j in {1..100}
    do
        python main.py instances/large --backward --export -d 2 -s $i
    done
done

# Compute graphs shown in the computational experiments
# For instance medium, use full enumeration as reference
python sample_graph.py instances/medium -d 2
python bar_graph.py instances/medium -d 2
python decay_graph.py instances/medium 50
# For instance large, use s= 512 samples as reference
python sample_graph.py instances/large -d 2 -s 512
python boxplot_graph.py instances/large -d 2 -s 512
python decay_graph.py instances/large 50 -s 512