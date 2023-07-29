class Users_permissions:
    def __init__(self,idUser,cupboardId):
        self.idUser = idUser 
        self.cupboardId = cupboardId

class User:
    def __init__(self,id,name,surname,age) -> None:
        self.id = id
        self.name = name 
        self.surname = surname
        self.age = age
    
class Manager_controller:
    def __init__(self,id,IP,port,redisChScale,redisChTouch,redisChProx) -> None:
        self.id = id
        self.IP = IP
        self.port = port
        self.redisChScale = redisChScale
        self.redisChTouch = redisChTouch
        self.redisChProx = redisChProx

class Well_known_theme:
    def __init__(self,id,icon,name):
        self.id = id
        self.icon = icon
        self.name = name 
    
    def pr(self):
        print("hi")

class Well_known_items:
    def __init__(self,id,categ,name,orig_weight,image,exp_expiring_days):
        self.id = id
        self.categ = categ
        self.name = name 
        self.orig_weight = orig_weight
        self.image = image
        self.exp_expiring_days = exp_expiring_days

class Cupboard_controller:
    def __init__(self,id,IP,server_port,camera_IP,arduino_1_port,arduino_2_port) -> None:
        self.id = id
        self.IP = IP
        self.server_port = server_port
        self.camera_IP = camera_IP
        self.arduino_1_port = arduino_1_port
        self.arduino_2_port = arduino_2_port


class Current_item:
    def __init__(self,id,quantity,expiring_date,cupboard_id,well_known_item_id,slot_id,last_user_id) -> None:
        self.id = id
        self.quantity = quantity
        self.expiring_date = expiring_date
        self.cupboard_id = cupboard_id
        self.well_known_item_id = well_known_item_id
        self.slot_id = slot_id
        self.last_user_id = last_user_id

    
class Shelf:
    def __init__(self,id,height,length,cupboard_id) -> None:
        self.id = id
        self.height = height
        self.length = length
        self.cupboard_id = cupboard_id

class Slot:
    def __init__(self,id,start,end,shelf_id) -> None:
        self.id = id 
        self.start = start
        self.end = end
        self.shelf_id = shelf_id


class Cupboard:
    def __init__(self,id,door_status,well_known_themes_id,default_time,rep_every,last_learn) -> None:
        self.id = id
        self.door_status = door_status
        self.well_known_themes_id = well_known_themes_id
        self.default_time = default_time
        self.rep_every = rep_every
        self.last_learn = last_learn