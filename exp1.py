from mininet.net import Mininet
from mininet.node import Node
from mininet.link import TCLink
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.topo import Topo


class LinuxRouter(Node):
    """A Node with IP forwarding enabled."""
    def config(self, **params):
        super(LinuxRouter, self).config(**params)
        self.cmd('sysctl net.ipv4.ip_forward=1')

    def terminate(self):
        self.cmd('sysctl net.ipv4.ip_forward=0')
        super(LinuxRouter, self).terminate()

class NetworkTopo( Topo ):
    def build( self, **_opts ):
        info('*** Adding routers\n')
        r1 = self.addHost('r1', cls=LinuxRouter, ip='10.0.0.3/24')
        r2 = self.addHost('r2', cls=LinuxRouter, ip='10.0.1.2/24')

        info('*** Adding hosts\n')
        h1 = self.addHost('h1', ip='10.0.0.1/24', defaultRoute='via 10.0.0.3')
        h2 = self.addHost('h2', ip='10.0.3.2/24', defaultRoute='via 10.0.3.4')
        h3 = self.addHost('h3', ip='10.0.2.2/24', defaultRoute='via 10.0.2.1')

        info('*** Creating links\n')
        self.addLink(h1, r1, intfName1='h1-eth0', intfName2='r1-eth0')

        self.addLink(r1, r2, intfName1='r1-eth1', intfName2='r2-eth0')

        self.addLink(r2, h3, intfName1='r2-eth1', intfName2='h3-eth0')

        self.addLink(r1, h2, intfName1='r1-eth2', intfName2='h2-eth0')

        


def exp1():

    networkTopo = NetworkTopo()
    net = Mininet(topo = networkTopo, link=TCLink)
    r1, r2 = net.get('r1', 'r2')
    h1, h2, h3 = net.get('h1', 'h2', 'h3')

    info('*** Starting network\n')
    net.start()

    info('*** Setting routes\n')
    # Routes for r1
    r1.cmd('ip route add 10.0.1.0/24 dev r1-eth1')
    r1.cmd('ip route add 10.0.2.0/24 via 10.0.1.2')
    r1.cmd('ip route add 10.0.3.0/24 dev r1-eth2')

    # Routes for r2
    r2.cmd('ip route add 10.0.0.0/24 via 10.0.1.1')
    r2.cmd('ip route add 10.0.3.0/24 via 10.0.1.1')

    info('*** Running pings\n')
    result_file = open('result1.txt', 'w')

    def log_ping(src, dst_ip):
        info(f'*** {src.name} pinging {dst_ip}\n')
        output = src.cmd(f'ping -c 1 {dst_ip}')
        result_file.write(f'\nPing from {src.name} to {dst_ip}:\n{output}\n')

    log_ping(h1, '10.0.2.2')  # h1 -> h3
    log_ping(h2, '10.0.2.2')  # h2 -> h3
    log_ping(h3, '10.0.0.1')  # h3 -> h1
    log_ping(h3, '10.0.3.2')  # h3 -> h2

    result_file.close()

    info('*** Done. Results saved in result1.txt\n')

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    exp1()
