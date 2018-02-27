from datetime import datetime
import time
from track.models import ParkingSpot, Item, Command, Drone, ItemDroneHistory


class DroneDelivery(object):
    """docstring for ClassName"""
    def __init__(self, instruction, item, drone):
        super(object, self).__init__()
        self.instruction = instruction
        self.item = item
        self.drone = drone

    def pickup_item(self):
        if self.drone.status == 'AVAILABLE':
            # update drone status
            self.set_status('INSTRUCTION_RECEIVED')
            self.add_history('Received pickup instruction from Command Center')

            # Update parking slot as available after drone left the place
            slot = ParkingSlot()
            slot.set_status(self.drone.parking_spot.slot_number, 'AVAILABLE')

            # pickup item from item from werehouse
            time.sleep(10)
            self.set_status('ITEM_PICKED')
            self.add_history('Item picked from Werehouse and started')
            self.item.order_status = 'SHIPPED'
            self.item.save()

            delivery_status = self.start_delivery()

            # Parking slot is occupied by drone
            slot.set_status(self.drone.parking_spot.slot_number, 'OCCUPIED')
            return delivery_status
        else:
            return False

    def start_delivery(self):
        # send message to command center
        time.sleep(10)
        self.set_status('REACHED_ADDRESS')
        self.send_instruction('REACHED_ADDRESS', 'Drone reached delivery address')
        self.add_history('Drone reached delivery address')

        time.sleep(5)
        self.set_status('ITEM_DELIVERED')
        self.send_instruction('ITEM_DELIVERED', 'Drone unloaded item at given delivering address')
        self.add_history('Drone unloaded item at given delivering address and returned')
        self.item.order_status = 'DELIVERED'
        self.item.save()

        # Drone returning from address
        time.sleep(10)
        self.set_status('REACHED_PARKING')
        self.send_instruction('REACHED_PARKING', "Drone is reached parking spot. Now it's ready for next instruction")
        self.set_status('AVAILABLE')
        self.add_history("Drone is reached parking spot. Now it's ready for next instruction")
        return True

    def get_status(self):
        return self.drone.status

    def set_status(self, status):
        self.drone.status = status
        self.drone.save()

    def add_history(self, action):
        try:
            history = ItemDroneHistory.objects.create(item=self.item,
                                                      drone=self.drone,
                                                      time_stamp=datetime.now(),
                                                      action=action)
        except:
            pass


    def send_instruction(self, instruction, comments=''):
        try:
            command = Command.objects.create(initiator='DRONE',
                                             initiate_time=datetime.now(),
                                             instruction=instruction,
                                             comments=comments)
        except:
            pass

    @staticmethod
    def get_all_drones(self, status=None):
        # filter all drones with statuses
        drones = None
        try:
            if status == None:
                drones = Drone.objects.all()
            else:
                drones = Drone.objects.filter(status=status)
        except:
            pass

        return drones


class CommandCenter(object):
    """docstring for CommandCenter"""
    def __init__(self, instruction, item):
        super(CommandCenter, self).__init__()
        self.instruction = instruction
        self.item = item

    def send_instruction(self):
        try:
            command = Command.objects.create(initiate_time=datetime.now(), 
                                             instruction=self.instruction)
            # Get drone and item objects before starting delivery
            drone = Drone.objects.filter(status='AVAILABLE')[0]
            item = Item.objects.get(id=self.item)
            # Drone starts pickup item
            drone_obj = DroneDelivery(self.instruction, item, drone)
            delivery_status = drone_obj.pickup_item()
            return delivery_status
        except Exception as e:
            return False


class ParkingSlot(object):
    """docstring for ParkingSlot"""
    def __init__(self):
        super(ParkingSlot, self).__init__()

    def set_status(self, slot, status):
        try:
            slot = ParkingSlot.objects.filter(slot_number=slot).update(slot_status=status)
            slot.save()
        except:
            pass

    def get_status(self, slot):
        try:
            slot = ParkingSpot.objects.get(slot_number=slot)
            status = slot.slot_status
        except:
            status = 'Invalid'
        return status
        
        