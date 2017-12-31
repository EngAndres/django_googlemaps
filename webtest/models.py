from django.db import models
from django.utils import timezone
from django.db import connection
from geoposition.fields import GeopositionField


############################# States #############################
class StatesManager(models.Manager):
    def get_states(self):
        cursor = connection.cursor()
        cursor.execute("SELECT id AS id_state, name AS state_name FROM webtest_states;")
        states = cursor.fetchall()
        return states

class States(models.Model):
    name = models.TextField(unique = True)
    states = StatesManager()
    objects = models.Manager()

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
        cursor = connection.cursor()
        cursor.execute("SELECT id AS id_client, name AS name_client FROM webtest_client;")
        clients = cursor.fetchall()
        return clients


class Client(models.Model):
    name = models.TextField()
    created_date = models.DateTimeField(default = timezone.now)
    clients = ClientManager()
    objects = models.Manager()

    



############################# Vendor #############################
class VendorManager(models.Manager):
    def create_vendor(self, name_, address_, latitude_, longitude_, created_):
        vendor = Vendor(name = name_, address = address_,  latitude = latitude_, longitude = longitude_, created_date = created_)
        return vendor
    
    def get_vendors(self):
        cursor = connection.cursor()
        cursor.execute("SELECT name, address, latitude, longitude, created_date FROM webtest_vendor;")
        vendors = cursor.fetchall()
        return vendors

    def get_vendors_location(self):
        cursor = connection.cursor()
        cursor.execute("SELECT id AS id_vendor, name, address, latitude, longitude FROM webtest_vendor;")
        vendors = cursor.fetchall()
        return vendors

    def add_vendor(self, name_, address_, latitude_, longitude_):
        cursor = connection.cursor()
        cursor.execute("INSERT INTO webtest_vendor(name, address, latitude, longitude) VALUES (%s, %s, %s, %s)", [name_, address_, latitude_, longitude_])
        vendors = cursor.fetchall()
        return vendors


class Vendor(models.Model):
    name = models.TextField(unique = True)
    address = models.TextField()
    latitude = models.DecimalField(max_digits=12,decimal_places=8)
    longitude = models.DecimalField(max_digits=12,decimal_places=8)
    created_date = models.DateTimeField(default = timezone.now)
    vendors = VendorManager()
    objects = models.Manager()

    def __str__(self):
        toString = self.name + ", " + self.address
        return toString





############################# Orders #############################
class OrdersManager():
    
    def get_orders_by_client(self, client_):
        cursor = connection.cursor()
        cursor.execute("SELECT webtest_orders.id AS id_, webtest_orders.order_number AS order_num, webtest_states.name AS state_, webtest_vendor.name AS vendor_, webtest_orders.shipping_address AS address_ FROM webtest_orders INNER JOIN webtest_states ON webtest_states.id = webtest_orders.state_fk_id INNER JOIN webtest_vendor ON webtest_orders.vendor_fk_id = webtest_vendor.id WHERE webtest_orders.client_fk_id = %s", [client_])
        orders = cursor.fetchall()
        return orders

    def get_orders_by_vendor(self, vendor_):
        cursor = connection.cursor()
        cursor.execute("SELECT webtest_orders.id, webtest_orders.order_number, webtest_states.name, webtest_client.name, webtest_orders.shipping_address FROM webtest_orders INNER JOIN webtest_states ON webtest_states.id = webtest_orders.state_fk_id INNER JOIN webtest_client ON webtest_orders.client_fk_id = webtest_client.id WHERE webtest_orders.vendor_fk_id = %s;", [vendor_])
        orders = cursor.fetchall()
        return orders

    def get_orders_by_client_vendor(self, client_, vendor_):
        cursor = connection.cursor()
        cursor.execute("SELECT webtest_orders.id, webtest_orders.order_number, webtest_states.name, webtest_orders.shipping_address FROM webtest_orders INNER JOIN webtest_states ON webtest_states.id = webtest_orders.state_fk_id WHERE webtest_orders.vendor_fk_id = %s AND webtest_orders.client_fk_id = %s;", [vendor_, client_])
        orders = cursor.fetchall()
        return orders

    def get_orders_by_clien_locationt(self, client_, location_):
        cursor = connection.cursor()
        cursor.execute("SELECT webtest_orders.id, webtest_orders.order_number, webtest_vendor.name, webtest_states.name FROM webtest_orders INNER JOIN webtest_states ON webtest_states.id = webtest_orders.state_fk_id INNER JOIN webtest_vendor ON webtest_vendor.id = webtest_orders.vendor_fk_id WHERE webtest_orders.client_fk_id = %s AND lower(webtest_orders.shipping_address) = lower(%s);", [client_, address_])
        orders = cursor.fetchall()
        return orders

    def get_orders_by_vendor_location(self, vendor_, latitude_, longitude_):
        cursor = connection.cursor()
        cursor.execute("SELECT webtest_orders.id, webtest_client.name, webtest_orders.shipping_address, webtest_orders.created_date, webtest_states.name FROM webtest_orders INNER JOIN webtest_client ON webtest_client.id = webtest_orders.client_fk_id INNER JOIN webtest_vendor ON webtest_vendor.id = webtest_orders.vendor_fk_id INNER JOIN webtest_states ON webtest_states.id = webtest_orders.state_fk_id WHERE webtest_vendor.id = %s AND round(webtest_orders.shipping_latitude, 2) = %s AND round(webtest_orders.shipping_longitude,2) = %s;", [vendor_, latitude_, longitude_])
        orders = cursor.fetchall()
        return orders

    def get_orders_delivered(self):
        state_ = 3
        cursor = connection.cursor()
        cursor.execute("SELECT webtest_orders.id AS id_, webtest_orders.order_number AS order_num, webtest_vendor.name AS vendor_, webtest_client.name AS client_, webtest_orders.shipping_address AS address_, webtest_orders.delivered_date AS delivered_ FROM webtest_orders INNER JOIN webtest_client ON webtest_client.id = webtest_orders.client_fk_id INNER JOIN webtest_vendor ON webtest_vendor.id = webtest_orders.vendor_fk_id WHERE webtest_orders.state_fk_id=%s  ;", [state_])
        orders = cursor.fetchall()
        return orders

    def get_orders_non_delivered(self):
        state_1 = 1
        state_2 = 2
        cursor = connection.cursor()
        cursor.execute("SELECT webtest_orders.id AS id_, webtest_orders.order_number AS order_num, webtest_vendor.name AS vendor_, webtest_client.name AS client_, webtest_orders.shipping_address AS address_, webtest_orders.created_date AS created_ FROM webtest_orders INNER JOIN webtest_client ON webtest_client.id = webtest_orders.client_fk_id INNER JOIN webtest_vendor ON webtest_vendor.id = webtest_orders.vendor_fk_id WHERE webtest_orders.state_fk_id = %s OR webtest_orders.state_fk_id = %s;", [state_1, state_2])
        orders = cursor.fetchall()
        return orders

    def get_orders_average_time(self, vendor_, state_, latitude_, longitude_):
        cursor = connection.cursor()
        cursor.execute("SELECT AVG(cast(( strftime('%s', delivered_date)-strftime('%s', created_date)) AS real)/60)FROM webtest_orders WHERE vendor_fk_id = %s AND state_fk_id = %s AND round(shipping_latitude, 2) = %s AND round(shipping_longitude,2) = %s;", [vendor_, state_, latitude_, longitude_]) 
        orders = cursor.fetchall()
        return orders

    def insert_order(self, order_number_, tracking_number_, vendor_, client_, shipping_address_, shipping_latitude_, shipping_longitude_, state_):
        order = Orders(order_number = order_number_, tracking_number = tracking_number_, vendor_fk = vendor_, client_fk = client_, shipping_address = shipping_address_, shipping_latitude = shipping_latitude_, shipping_longitude = shipping_longitude_, state_fk = state_)
        return order        


class Orders(models.Model):
    order_number = models.IntegerField()
    tracking_number = models.IntegerField()
    vendor_fk = models.ForeignKey(Vendor, on_delete = models.CASCADE)
    client_fk = models.ForeignKey(Client, on_delete = models.CASCADE)
    shipping_address = models.TextField()
    shipping_latitude = models.DecimalField(max_digits=12,decimal_places=8)
    shipping_longitude = models.DecimalField(max_digits=12,decimal_places=8)
    state_fk = models.ForeignKey(States, on_delete = models.CASCADE)
    created_date = models.DateTimeField(default = timezone.now)
    delivered_date = models.DateTimeField(null=True)
    orders = OrdersManager()

    


    




############################# Tracking #############################
class Tracking(models.Model):
    order_fk = models.ForeignKey(Orders, on_delete = models.CASCADE)
    date_time = models.DateTimeField(default = timezone.now)
    state_fk = models.ForeignKey(States, on_delete = models.CASCADE)
