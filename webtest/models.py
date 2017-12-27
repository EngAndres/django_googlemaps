from django.db import models
from django.utils import timezone

############################# States #############################
class StatesManager(models.Manager):
    def get_states(self):
        query = "SELECT id, name FROM webtest_states;"

class States(models.Model):
    name = models.TextField(unique = True)

    def getName(self):
        self.name

    def insertName(self, name_):
        self.name = name_
        self.save()

    def __str__(self):
        return self.name




############################# Clients #############################
class ClientManager(models.Manager):
    def get_clients(self):
        query = "SELECT id, name FROM webtest_client;"
        clients = self.raw(query)


class Client(models.Model):
    name = models.TextField()
    created_date = models.DateTimeField(default = timezone.now)
    objects = ClientManager()

    def __str__(self):
        toString = self.name + ", created on " + self.created_date
        return toString



############################# Vendor #############################
class VendorManager(models.Manager):
    def get_vendors(self):
        query = "SELECT id, name, created_date FROM webtest_vendor;"
        vendors = self.raw(query)

    def get_vendors_location(self):
        query = "SELECT id, name, address, latitude, longitude FROM webtest_vendor;"
        vendors = self.raw(query)

    def add_vendor(self, name_, address_, latitude_, longitude_):
        query = ("INSERT INTO webtest_vendor(name, address, latitude, longitude) VALUES ('%s', '%s', '%f', '%f')", [name_, address_, latitude_, longitude_])
        self.raw(query)


class Vendor(models.Model):
    name = models.TextField(unique = True)
    address = models.TextField()
    latitude = models.IntegerField()
    longitude = models.IntegerField()
    created_date = models.DateTimeField(default = timezone.now)
    objects = VendorManager()

    def __str__(self):
        toString = self.name + ", " + self.address
        return toString





############################# Orders #############################
class OrdersManager():
    def get_orders_by_client(self, client_):
        query = ("SELECT webtest_orders.id, webtest_orders.order_number, webtest_states.name, webtest_vendor.name, webtest_orders.shipping_address FROM webtest_orders INNER JOIN webtest_states ON webtest_states.id = webtest_orders.state_fk_id INNER JOIN webtest_vendor ON webtest_orders.vendor_fk_id = webtest_vendor.id WHERE webtest_orders.client_fk_id = %d", [client_])
        orders = self.raw(query)

    def get_orders_by_vendor(self, vendor_):
        query = ("SELECT webtest_orders.id, webtest_orders.order_number, webtest_states.name, webtest_client.name, webtest_orders.shipping_address FROM webtest_orders INNER JOIN webtest_states ON webtest_states.id = webtest_orders.state_fk_id INNER JOIN webtest_client ON webtest_orders.client_fk_id = webtest_client.id WHERE webtest_orders.vendor_fk_id = %d;", [vendor_])
        orders = self.raw(query)

    def get_orders_by_client_vendor(self, client_, vendor_):
        query = ("SELECT webtest_orders.id, webtest_orders.order_number, webtest_states.name, webtest_orders.shipping_address FROM webtest_orders INNER JOIN webtest_states ON webtest_states.id = webtest_orders.state_fk_id WHERE webtest_orders.vendor_fk_id = %d AND webtest_orders.client_fk_id = %d;", [vendor_, client_])
        orders = self.raw(query)

    def get_orders_by_clien_locationt(self, client_, location_):
        query = ("SELECT webtest_orders.id, webtest_orders.order_number, webtest_vendor.name, webtest_states.name FROM webtest_orders INNER JOIN webtest_states ON webtest_states.id = webtest_orders.state_fk_id INNER JOIN webtest_vendor ON webtest_vendor.id = webtest_orders.vendor_fk_id WHERE webtest_orders.client_fk_id = %d AND lower(webtest_orders.shipping_address) = lower(%s);", [client_, address_])
        orders = self.raw(query)

    def get_orders_by_vendor_location(self, vendor_, latitude_, longitude_):
        query = ("SELECT webtest_orders.id, webtest_client.name, webtest_orders.shipping_address, webtest_orders.created_date, webtest_states.name FROM webtest_orders INNER JOIN webtest_client ON webtest_client.id = webtest_orders.client_fk_id INNER JOIN webtest_vendor ON webtest_vendor.id = webtest_orders.vendor_fk_id INNER JOIN webtest_states ON webtest_states.id = webtest_orders.state_fk_id WHERE webtest_vendor.id = %d AND round(webtest_orders.shipping_latitude, 2) = %f AND round(webtest_orders.shipping_longitude,2) = %f;", [vendor_, latitude_, longitude_])
        orders = self.raw(query)

    def get_orders_delivered(self):
        state_ = 3
        query = ("SELECT webtest_orders.id, webtest_orders.order_number, webtest_vendor.name, webtest_client.name, webtest_orders.shipping_address FROM webtest_orders INNER JOIN webtest_client ON webtest_client.id = webtest_orders.client_fk_id INNER JOIN webtest_vendor ON webtest_vendor.id = webtest_orders.vendor_fk_id WHERE webtest_orders.state_fk_id = %d;", [state_])
        orders = self.raw(query)

    def get_orders_by_non_delivered(self,):
        state_1 = 1
        state_2 = 2
        query = ("SELECT webtest_orders.id, webtest_orders.order_number, webtest_vendor.name, webtest_client.name, webtest_orders.shipping_address FROM webtest_orders INNER JOIN webtest_client ON webtest_client.id = webtest_orders.client_fk_id INNER JOIN webtest_vendor ON webtest_vendor.id = webtest_orders.vendor_fk_id WHERE webtest_orders.state_fk_id = %d OR webtest_orders.state_fk_id = %d;", [state_1, state_2])
        orders = self.raw(query)

    def get_orders_average_time(self, vendor_, state_, latitude_, longitude_):
        query = ("SELECT AVG(cast(( strftime('%s', delivered_date)-strftime('%s', created_date)) AS real)/60)FROM webtest_orders WHERE vendor_fk_id = %d AND state_fk_id = %d AND round(shipping_latitude, 2) = %f AND round(shipping_longitude,2) = %f;", [vendor_, state_, latitude_, longitude_]) 
        orders = self.raw(query)
	

class Orders(models.Model):
    order_number = models.IntegerField()
    vendor_fk = models.ForeignKey(Vendor, on_delete = models.CASCADE)
    client_fk = models.ForeignKey(Client, on_delete = models.CASCADE)
    shipping_address = models.TextField()
    shipping_latitude = models.IntegerField()
    shipping_longitude = models.IntegerField()
    state_fk = models.ForeignKey(States, on_delete = models.CASCADE)
    created_date = models.DateTimeField(default = timezone.now)
    delivered_date = models.DateTimeField()

    def insert_order(self, order_number_, vendor_, client_, shipping_address_, shipping_latitute_, shipping_longitude_, state_):
        self.order_number = order_number_
        self.vendor_fk = vendor_
        self.client_fk = client_
        self.shipping_address = shipping_address_
        self.shipping_latitude = shipping_latitude_
        self.shipping_longitude = shipping_longitude_
        self.state_fk = state_
        self.save()

    def __str__(self):
        toString = self.order_number + ", " + self.shipping_address
        return toString




############################# Tracking #############################
class Tracking(models.Model):
    order_fk = models.ForeignKey(Orders, on_delete = models.CASCADE)
    date_time = models.DateTimeField(default = timezone.now)
    state_fk = models.ForeignKey(States, on_delete = models.CASCADE)
