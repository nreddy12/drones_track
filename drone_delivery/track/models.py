from django.db import models


class ParkingSpot(models.Model):
    PARKING_STATUS = (('AVAILABLE', 'Available'),
                      ('OCCUPIED', 'Occupied'),)

    slot_number = models.IntegerField()
    slot_status = models.CharField(max_length=255,
                                   choices=PARKING_STATUS,
                                   default='AVAILABLE')
    slot_details = models.CharField(max_length=255)

    class Meta:
        db_table = 'parking_spot'


class Command(models.Model):
    INSTRUCTION =  (('PICKUP', 'Pick Up'),
                    ('CANCEL', 'Cancel'),
                    ('REACHED', 'Reached'),
                    ('UNLOADED', 'Unloaded'),)

    INITIATOR = (('COMMAND_CENTER', 'Command Center'),
                 ('DRONE', 'Drone'),)

    initiator = models.CharField(max_length=255,
                                choices=INITIATOR,
                                default='COMMAND_CENTER')
    initiate_time = models.DateTimeField()
    instruction = models.CharField(max_length=255,
                               choices=INSTRUCTION,
                               default='PICKUP')
    comments = models.CharField(max_length=255)

    class Meta:
        db_table = 'command'


class Drone(models.Model):
    DRONE_STATUS = (('AVAILABLE', 'Available'),
                    ('INSTRUCTION_RECEIVED', 'Instruction Recieved'),
                    ('ITEM_PICKED', 'Item Picked'),
                    ('REACHED_ADDRESS', 'Reached Delivery Address'),
                    ('ITEM_DELIVERED', 'Delivered Item'),
                    ('REACHED_PARKING', 'Reached Packing Spot'),)

    name = models.CharField(max_length=255)
    status = models.CharField(max_length=255,
                              choices=DRONE_STATUS,
                              default='AVAILABLE')
    parking_spot = models.ForeignKey(ParkingSpot, db_column='slot', on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'drone'


class Item(models.Model):
    ITEM_STATUS = (('AVAILABLE', 'Available'),
                   ('ORDERED', 'Ordered'),
                   ('PACKED', 'Packed'),
                   ('SHIPPED', 'Shipped'),
                   ('DELIVERED', 'Delivered'),)

    name = models.CharField(max_length=255)
    item_spot = models.IntegerField()
    order_status = models.CharField(max_length=255,
                                    choices=ITEM_STATUS,
                                    default='AVAILABLE')
    order_date = models.DateTimeField()
    address = models.CharField(max_length=255)
    item_details = models.CharField(max_length=255)

    class Meta:
        db_table = 'item'


class ItemDroneHistory(models.Model):
    item = models.ForeignKey(Item, db_column='item', on_delete=models.DO_NOTHING)
    drone = models.ForeignKey(Drone, db_column='drone', on_delete=models.DO_NOTHING)
    time_stamp = models.DateTimeField()
    action = models.CharField(max_length=255)

    class Meta:
        db_table = 'item_drone_history'
