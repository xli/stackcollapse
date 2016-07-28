# stackcollapse

Convert python stacktrace log into flamegraph


### Example

suppose you have python stacktrace log in format: one line one stacktrace, stored in py-stacktrace.log, use the following command to transform it into flamegraph:

cat py-stacktrace.log | ./bin/stackcollapse-py | ./flamegraph.pl > flame.html

Note: get flamegraph.pl from https://github.com/brendangregg/FlameGraph
