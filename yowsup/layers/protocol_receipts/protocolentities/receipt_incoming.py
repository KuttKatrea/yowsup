from yowsup.structs import ProtocolEntity, ProtocolTreeNode
from .receipt import ReceiptProtocolEntity
class IncomingReceiptProtocolEntity(ReceiptProtocolEntity):

    '''
    delivered:
    <receipt to="xxxxxxxxxxx@s.whatsapp.net" id="1415389947-15"></receipt>

    read
    <receipt to="xxxxxxxxxxx@s.whatsapp.net" id="1415389947-15" type="read"></receipt>

    INCOMING
    <receipt offline="0" from="xxxxxxxxxx@s.whatsapp.net" id="1415577964-1" t="1415578027"></receipt>
    '''

    def __init__(self, _id, _from, timestamp, offline = None, retry = None, type = None, children = False):
        super(IncomingReceiptProtocolEntity, self).__init__(_id)
        self.setIncomingData(_from, timestamp, offline, retry, type, children)

    def getType(self):
        return self.type

    def getFrom(self):
        return self._from

    def setIncomingData(self, _from, timestamp, offline, retry = None, type = None, children = None):
        self._from = _from
        self.timestamp = timestamp
        self.type = type
        self.children = children
        if offline is not None:
            print("Offline is %s" % offline)
            print("Retry is %s" % retry)
            self.offline = True
            self.offline_count = offline
            self.retry =  retry
        else:
            self.offline = None

    def toProtocolTreeNode(self):
        node = super(IncomingReceiptProtocolEntity, self).toProtocolTreeNode()
        node.setAttribute("from", self._from)
        node.setAttribute("t", str(self.timestamp))
        if self.offline is not None:
            node.setAttribute("offline", "1" if self.offline else "0")
        if self.type is not None:
            node.setAttribute("type", self.type)
        return node

    def __str__(self):
        out = super(IncomingReceiptProtocolEntity, self).__str__()
        out += "From: %s\n" % self._from
        out += "Timestamp: %s\n" % self.timestamp
        if self.offline is not None:
            out += "Offline: %s\n" % ("1" if self.offline else "0")
        if self.type is not None:
            out += "Type: %s\n" % (self.type)
        if self.children is not None:
            out += "Children: %s\n" % (self.children)
        return out

    @staticmethod
    def fromProtocolTreeNode(node):
        children = None

        children_list = node.getChild('list')
        if children_list is not None:
            children = list()
            for child in children_list.children:
                children.append(child.getAttributeValue('id'))

        return IncomingReceiptProtocolEntity(
            node.getAttributeValue("id"),
            node.getAttributeValue("from"),
            node.getAttributeValue("t"),
            node.getAttributeValue("offline"),
            node.getAttributeValue("retry"),
            node.getAttributeValue("type"),
            children
            )
