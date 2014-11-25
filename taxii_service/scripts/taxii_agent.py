from optparse import OptionParser

from crits.core.basescript import CRITsBaseScript
from taxii_service.handlers import execute_taxii_agent

class CRITsScript(CRITsBaseScript):
    def __init__(self, username=None):
        self.username = username

    def run(self, argv):
        parser = OptionParser()
        parser.add_option("-H", "--host", dest="host", action="store",
                          type="string", default='', help="Host to connect to.")
        parser.add_option("-k", "--keyfile", dest="keyfile", action="store",
                          type="string", default='', help="Key file.")
        parser.add_option("-c", "--certfile", dest="certfile", action="store",
                          type="string", default='', help="Certificate file.")
        parser.add_option("-s", "--start", dest="start", action="store",
                          default=None, help="Start time.")
        parser.add_option("-S", "--https", dest="https", action="store_true",
                          default=False, help="Connect over HTTPS.")
        parser.add_option("-e", "--end", dest="end", action="store",
                          default=None, help="End time.")
        parser.add_option("-v", "--verbose", dest="verbose", action="store_true",
                          default=False, help="Print saved objects.")
        parser.add_option("-f", "--feed", dest="feed", action="store",
                          default=None, help="Data feed.")

        (opts, args) = parser.parse_args(argv)

        if opts.verbose:
            if not opts.host:
                print "[+] Using host from service configuration."
            if not opts.keyfile:
                print "[+] Using keyfile from service configuration."
            if not opts.certfile:
                print "[+] Using certfile from service configuration."
            if not opts.feed:
                print "[+] Using feed from service configuration."
            if opts.https:
                print "[+] Connecting over HTTPS."

        objs = execute_taxii_agent(opts.host, opts.https, opts.feed,
                                   opts.keyfile, opts.certfile, opts.start,
                                   opts.end, analyst="Command Line",
                                   method="TAXII Agent")
        if opts.verbose:
            if not objs['status']:
                print "Failure: %s" % objs['reason']
            else:
                print "Failed content blocks: %i" % len(objs["failures"])
                print "Successful content blocks: %i" % objs["successes"]

                if  objs["successes"] > 0:
                    for k in ["Event", "Sample", "Email", "Indicator"]:
                        print "%s (%i)" % (k, len(objs[k]))
                        for i in objs[k]:
                            print i
