
import os
import server_info

from mysql.utilities.exception import MUTLibError
from symbol import except_clause


class test(server_info.test):
    """check errors for serverinfo
    This test executes a series of error tests using a variety of
    parameters. It uses the server_info test as a parent for setup and teardown
    methods.
    """

    def check_prerequisites(self):
        if os.name == "nt":
            raise MUTLibError("Test does not execute correctly on Windows.")
        return server_info.test.check_prerequisites(self)

    def setup(self):
        self.server3 = None
        return server_info.test.setup(self)

    def run(self):
        self.server1 = self.servers.get_server(0)
        self.res_fname = "result.txt"

        from_conn2 = "--server=" + self.build_connection_string(self.server2)
        cmd_str = "mysqlserverinfo.py "

        test_num = 1
        comment = "Test case %d - no server" % test_num
        res = self.run_test_case(2, cmd_str, comment)
        if not res:
            raise MUTLibError("%s: failed" % comment)
        self.results.append("\n")

        test_num += 1
        cmd_opts = " --server=xewkjsdd:21"
        comment = "Test case %d - bad server" % test_num
        res = self.run_test_case(1, cmd_str + cmd_opts, comment)
        if not res:
            raise MUTLibError("%s: failed" % comment)
        self.results.append("\n")

        cmd_str = "mysqlserverinfo.py %s " % from_conn2

        test_num += 1
        cmd_opts = " --format=ASDASDASD"
        comment = "Test case %d - bad format" % test_num
        res = self.run_test_case(2, cmd_str + cmd_opts, comment)
        if not res:
            raise MUTLibError("%s: failed" % comment)
        self.results.append("\n")

        test_num += 1
        cmd_opts = " --format=grid"
        cmd_str_wrong = cmd_str.replace(":root", ":wrong")
        comment = "Test case %d - wrong password" % test_num
        res = self.run_test_case(1, cmd_str_wrong + cmd_opts, comment)
        if not res:
            raise MUTLibError("%s: failed" % comment)
        self.results.append("\n")

        test_num += 1
        cmd_opts = " --format=grid"
        cmd_str_wrong = cmd_str.replace(":root", ":")
        comment = "Test case %d - no password" % test_num
        res = self.run_test_case(1, cmd_str_wrong + cmd_opts, comment)
        if not res:
            raise MUTLibError("%s: failed" % comment)
        self.results.append("\n")

        cmd_str = self.start_stop_newserver()

        test_num += 1
        cmd_opts = " --format=vertical "
        comment = ("Test case %d - offline server without %s option" %
                   (test_num, "start, basedir, datadir"))
        res = self.run_test_case(1, cmd_str + cmd_opts, comment)
        if not res:
            raise MUTLibError("%s: failed" % comment)        
        self.results.append("\n")

        test_num += 1
        cmd_opts = " --format=vertical --basedir=."
        comment = ("Test case %d - offline server without %s option" %
                   (test_num, "start, datadir"))
        res = self.run_test_case(1, cmd_str + cmd_opts, comment)
        if not res:
            raise MUTLibError("%s: failed" % comment)
        self.results.append("\n")

        test_num += 1
        cmd_opts = " --format=vertical --basedir=. --datadir=."
        comment = ("Test case %d - offline server without %s option" % 
                   (test_num, "start"))
        res = self.run_test_case(1, cmd_str + cmd_opts, comment)
        if not res:
            raise MUTLibError("%s: failed" % comment)

        server_info.test.do_replacements(self)

        self.replace_result("ERROR: No login credentials",
                            "ERROR: Unable to get login-path\n")
        self.replace_result("ERROR: .mylogin.cnf",
                            "ERROR: Unable to get login-path\n")
        self.replace_result("ERROR: the used my_print_defaults",
                            "ERROR: Unable to get login-path\n")
        self.replace_result("ERROR: error: <the used my_print_defaults",
                            "ERROR: Unable to get login-path\n")

        return True

    def get_result(self):
        return self.compare(__name__, self.results)

    def record(self):
        return self.save_result_file(__name__, self.results)

    def cleanup(self):
        from mysql.utilities.common.tools import delete_directory
        if self.server3:
            delete_directory(self.datadir3)
            self.server3 = None
        return server_info.test.cleanup(self)
