
import unittest
import stackcollapse
import os
import subprocess
import json


class TestStackcollapse(unittest.TestCase):

    def read_data(self, filename):
        dir = os.path.dirname(__file__)
        file = os.path.join(dir, 'data', filename)
        with open(file, 'r') as f:
            return f.read()

    def test_parse_stacktrace_log(self):
        log = self.read_data('stacktrace1.log')
        trace = list(stackcollapse.parse_stacktrace_log(log))
        self.assertEqual(7, len(trace))
        self.assertEqual(
            ("/usr/local/bin/helloworld-tornado", "9", "<module>"),
            trace[0])
        self.assertEqual(
            ("/python2.7/dateutil/parser.py", "611", "parse"),
            trace[6])

    def test_flame_input_stream(self):
        log1 = self.read_data('stacktrace1.log')
        log2 = self.read_data('stacktrace2.log')
        log3 = self.read_data('stacktrace3.log')
        flame = list(stackcollapse.flame([log1, log3, log3, log3,
                                          log2, log3, log3]))
        self.assertEqual(4, len(flame))
        self.assertEqual("3", flame[1].split(" ")[1])
        self.assertEqual("1", flame[2].split(" ")[1])
        self.assertEqual("2", flame[3].split(" ")[1])

    def test_script(self):
        log1 = self.read_data('stacktrace1.log')
        log2 = self.read_data('stacktrace2.log')
        log3 = self.read_data('stacktrace3.log')

        dir = os.path.dirname(__file__)
        script = os.path.join(dir, '..', 'bin', 'stackcollapse-py')
        p = subprocess.Popen(script, shell=True,
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)

        input = "\n".join([json.dumps(log) for log in [log1, log3, log3,
                                                       "hello, ignore me",
                                                       log3, log2, log3,
                                                       log3, "\n"]])
        stdout, stderr = p.communicate(input)

        self.assertEqual("", stderr)
        self.assertEqual(
            '<module>:/usr/local/bin/helloworld-tornado:9;wrapper:/usr/local/lib/python2.7/dist-packages/tornado/gen.py:267;ioloop_start:/home/root/helloworld/helloworld/helloworld.py:70;start:/usr/local/lib/python2.7/dist-packages/tornado/ioloop.py:827;<lambda>:/usr/local/lib/python2.7/dist-packages/tornado/gen.py:1097;_to_epoch:/home/root/helloworld/helloworld/services/mappers/__init__.py:105;parse:/python2.7/dateutil/parser.py:611 1\n<module>:<stdin>:1;compile:/python/2.7.11/lib/python2.7/re.py:194;_compile:/python/2.7.11/lib/python2.7/re.py:251 2\n 1\n<module>:<stdin>:1;compile:/python/2.7.11/lib/python2.7/re.py:194;_compile:/python/2.7.11/lib/python2.7/re.py:251 1\n<module>:/usr/local/bin/helloworld-tornado:9;wrapper:/usr/local/lib/python2.7/dist-packages/tornado/gen.py:267;ioloop_start:/home/root/helloworld/helloworld/helloworld.py:70;start:/usr/local/lib/python2.7/dist-packages/tornado/ioloop.py:827;<lambda>:/usr/local/lib/python2.7/dist-packages/tornado/gen.py:1097;_to_epoch:/home/root/helloworld/helloworld/services/mappers/__init__.py:105;parse:/python2.7/dateutil/parser.py:911 1\n<module>:<stdin>:1;compile:/python/2.7.11/lib/python2.7/re.py:194;_compile:/python/2.7.11/lib/python2.7/re.py:251 2\n 1\n',
            stdout)
