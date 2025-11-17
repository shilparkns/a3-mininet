from mininet.net import Mininet
from mininet.node import OVSKernelSwitch
from mininet.link import TCLink
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.topo import Topo

class NetworkTopo( Topo ):
    def build( self, **_opts ):

        info('*** Adding hosts\n')
        h1 = self.addHost('h1', ip='10.0.0.1/24')
        h2 = self.addHost('h2', ip='10.0.3.2/24')
        h3 = self.addHost('h3', ip='10.0.2.2/24')

        info('*** Adding switches\n')
        s1 = self.addSwitch('s1', cls=OVSKernelSwitch, failMode='standalone')
        s2 = self.addSwitch('s2', cls=OVSKernelSwitch, failMode='standalone')

        info('*** Creating links\n')
        self.addLink(h1, s1)
        self.addLink(h2, s1)
        self.addLink(s1, s2)
        self.addLink(h3, s2)

def exp2():

    networkTopo = NetworkTopo()
    net = Mininet(topo = networkTopo, link=TCLink, switch=OVSKernelSwitch, autoSetMacs = True)

    info('*** Starting network\n')
    net.start()

    h1, h2, h3 = net.get('h1', 'h2', 'h3')
    result_file = open('result1.txt', 'w')

    info('*** Running pings\n')

    def log_ping(src, dst):
        result = src.cmd('ping -c 1 %s' % dst)
        result_file.write('Ping from %s to %s:\n%s\n' % (src.name, dst.name, result))

    log_ping(h1, h3)
    log_ping(h2, h3)

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    exp2()