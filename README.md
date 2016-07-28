# stackcollapse

Convert python stacktrace log into flamegraph

kafka-stack-trace.log:
  one line one stacktrace

cat kafka-stacktrace.log | ./bin/stackcollapse-py | ./flamegraph.pl > 1sec-flame.html

get flamegraph.pl from https://github.com/brendangregg/FlameGraph
