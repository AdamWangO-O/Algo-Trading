# Assignment_1

* Part 1

```
class OrderBook:
    def __init__(self):
        self.list_asks = []
        self.list_bids = []
        # the list of bids and offers is self explanatory. 
        # the orders attribute keeps a record of all the orders where they key is the order id and the
        # value is the order. If used correctly, this should help you implement the handle methods below.
        self.orders = {}
    def handle_order(self,o):
        if o['action']=='new':
            self.handle_new(o)
        elif o['action']=='modify':
            self.handle_modify(o)
        elif o['action']=='delete':
            self.handle_delete(o)
        else:
            print('Error-Cannot handle this action')

    def handle_new(self,o):
        if o["side"] == "bid":
            self.list_bids.append(o)
            self.list_bids.sort(key=lambda x:x["price"],reverse=True)
            self.orders[o["id"]] = o
        elif o["side"] == "ask":
            self.list_asks.append(o)
            self.list_asks.sort(key=lambda x:x["price"])
            self.orders[o["id"]] = o
        

    def handle_modify(self,o):
        for i in (self.list_bids):
            if i["id"] == o["id"]:
                i["quantity"] = o["quantity"]
                break
        for i in (self.list_asks):
            if i["id"] == o["id"]:
                i["quantity"] = o["quantity"]
                break

    def handle_delete(self,o):
        for i in range(len(self.list_bids)):
            if self.list_bids[i]["id"] == o["id"]:
                self.list_bids.pop(i)
                del self.orders[o["id"]]
                break
        for i in range(len(self.list_asks)):
            if self.list_asks[i]["id"] == o["id"]:
                self.list_asks.pop(i)
                del self.orders[o["id"]]
                break
```

* Part 2
```
def return_num_vowels(string):
    count = {"a":0,"e":0,"i":0,"o":0,"u":0}
    for i in string:
        if i.lower() in ["a","e","i","o","u"]:
            count[i.lower()] = count[i.lower()] + 1
    return count    

def return_num_characters(string):
    count = 0
    for i in string:
        if i.lower() in ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']:
            count = count + 1
    return count

def bar_plot(l):
    for i in l:
        if i == int(i) and i>0:
            for j in range(i):
                print("+",end="")
            print()
```

* Part 3

```
class Message:
    def __init__(self,st,sn):
        self.__sending_time = st
        self.__sequence_number = sn
        
    @property
    def sequence_number(self):
        return self.__sequence_number

    @sequence_number.setter
    def sequence_number(self, value):
        self.__sequence_number = value

    @property
    def sending_time(self):
        return self.__sending_time

    @sending_time.setter
    def sending_time(self, value):
        self.__sending_time = value

class AddModifyOrderMessage(Message):
    def __init__(self,st,sn,p,q,s,o_id):
        Message.__init__(self,st,sn)
        self.__price = p
        self.__quantity = q
        self.__side = s
        self.__order_id = o_id
        
    @property
    def order_id(self):
        return self.__order_id

    @order_id.setter
    def order_id(self, value):
        self.__order_id = value

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, value):
        self.__price = value

    @property
    def quantity(self):
        return self.__quantity

    @quantity.setter
    def quantity(self, value):
        self.__quantity = value

    @property
    def side(self):
        return self.__side

    @side.setter
    def side(self, value):
        self.__side = value
        
class DeleteOrderMessage(Message):
    def __init__(self,st,sn,s,o_id):
        Message.__init__(self,st,sn)
        self.__side = s
        self.__order_id = o_id
        
    @property
    def order_id(self):
        return self.__order_id

    @order_id.setter
    def order_id(self, value):
        self.__order_id = value

    @property
    def side(self):
        return self.__side

    @side.setter
    def side(self, value):
        self.__side = value

class TradeMessage(Message):
    def __init__(self,st,sn,s,t_id,tq):
        Message.__init__(self,st,sn)
        self.__side = s
        self.__trade_id = t_id
        self.__trade_quantity = tq
        
    @property
    def trade_quantity(self):
        return self.__trade_quantity

    @trade_quantity.setter
    def trade_quantity(self, value):
        self.__trade_quantity = value

    @property
    def side(self):
        return self.__side

    @side.setter
    def side(self, value):
        self.__side = value

    @property
    def trade_id(self):
        return self.__trade_id

    @trade_id.setter
    def trade_id(self, value):
        self.__trade_id = value
```