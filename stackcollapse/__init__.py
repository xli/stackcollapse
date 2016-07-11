
import re


TRACE_LOG_PATTERN = r'^  File "([^"]+)", line (\d+), in (.+)$'
TRACE_LOG_REGEX = re.compile(TRACE_LOG_PATTERN)


def flame(input):
    ff = None
    count = 1
    for log in input:
        next_ff = flame_format(log)
        if ff is None:
            ff = next_ff
            count = 1
        elif ff == next_ff:
            count += 1
        elif next_ff is not None:
            yield "%s %d" % (ff, count)
            ff = next_ff
            count = 1
    if ff is not None:
        yield "%s %d" % (ff, count)


def flame_format(log):
    stack = parse_stacktrace_log(log)
    funcs = map("{0[2]}:{0[0]}:{0[1]}".format, stack)
    return ";".join(funcs)


def parse_stacktrace_log(log):
    for line in log.splitlines():
        m = TRACE_LOG_REGEX.match(line)
        if m:
            yield (m.group(1), m.group(2), m.group(3))
