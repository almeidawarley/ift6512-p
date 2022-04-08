# List of experiments ran for the results in the report

# Compute (full) backward policy for instance small
python main.py instances/small --backward -d 1 --verbose
python main.py instances/small --backward -d 10 --verbose
python main.py instances/small --backward -d 100 --verbose
python main.py instances/small --backward -d 1000 --verbose
python main.py instances/small --backward -d 10000 --verbose

# Compute (full) parametric policy for instance small
python main.py instances/small --parametric -d 1 --verbose

# Compute (full) backward policy for instance medium
python main.py instances/medium --backward --export -d 2
# Compute (sampled) backward policy for instance large
python main.py instances/large --backward --export -d 2 -s 512

# Compute (full) parametric policy for instance large
python main.py instances/medium --parametric --export -d 2
# Compute (sampled) parametric policy for instance large
python main.py instances/large --parametric --export -d 2 -s 512

# Compute graphs shown in the computational experiments
# For instance medium, use full enumeration as reference
python sample_graph.py instances/medium -d 2
python bar_graph.py instances/medium -d 2
python decay_graph.py instances/medium 50
# For instance large, use s= 512 samples as reference
python sample_graph.py instances/large -d 2 -s 512
python boxplot_graph.py instances/large -d 2 -s 512
python decay_graph.py instances/large 50 -s 512