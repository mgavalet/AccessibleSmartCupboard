import pymongo 
from datetime import datetime

date_format = "%d/%m/%y"
today = datetime.today()#.strftime(date_format)

class myDatabase:

    clientDB = pymongo.MongoClient("mongodb://localhost:27017/") # connect to DB
    cupboardDB = clientDB.cupboardDBtest # create database -- needs to add content to be created 
    
    #Create collections - tables
    Users_collection = cupboardDB.Users # create Users table
    Manager_controller_collection = cupboardDB.Manager_controller # create Manager_controller table
    Well_known_items_collection = cupboardDB.Well_known_items
    Well_known_theme_collection = cupboardDB.Well_known_theme
    Cupboard_controller_collection = cupboardDB.Cupboard_controller

    Cupboard_collection = cupboardDB.Cupboard
    Shelf_collection = cupboardDB.Shelf
    Slot_collection = cupboardDB.Slot
    Users_permissions_collection = cupboardDB.Users_permissions
    Current_item_collection = cupboardDB.Current_item


    def getShelfObjIdByCupIdandVerOrder(self,cupboardId,verticalOrder): 
        myquery = { "cupboard_id" : cupboardId , "vertical_order" : verticalOrder}
        shelfObjId = self.Shelf_collection.find_one(myquery,{"_id" : 1})["_id"]
        return shelfObjId

    # INSERT
    def insertShelf(self,verticalOrder,length,height,cupboardId):
        ShelfObjId=self.Shelf_collection.insert_one({"vertical_order" : verticalOrder,"height": height , "length" : length , "cupboard_id" : cupboardId}).inserted_id
        return ShelfObjId

    def insertSlot(self,startPos,endPos,shelfObjId, currentItemId = "tempUnknown"):
        slot_id = self.Slot_collection.insert_one({"start" : startPos , "end" : endPos ,"shelf_id" : shelfObjId , "current_item_id" : currentItemId}).inserted_id
        return slot_id


    def insertCurrentItem(self,slotStartPos,slotEndPos,quantity,shelfId,expiringDate,lastUser,itemName,cupId):
        # create a Slot
        slot_id  = self.insertSlot(startPos=slotStartPos, endPos=slotEndPos , shelfObjId=shelfId)
        #Then create a Current item which is located in the Slot
        currentItemObjId = self.Current_item_collection.insert_one({"slot_id" : slot_id ,"Well_known_item_id" : itemName ,"quantity" : quantity , "expiring_date" : expiringDate , "last_user_id" : lastUser , "cupboard_id" : cupId}).inserted_id
        # update the field 'storedItemId' in Slot collection
        self.Slot_collection.update_one({"_id" : slot_id} , {"$set" : {"current_item_id" : currentItemObjId}})
    
    def insertUser(self,username,name,surname,age, permissionsData):
        self.Users_collection.insert_one({"_id" : username , "name" : name , "surname" : surname , "age" : age})
        self.insertUserAccess(username,permissionsData)


    def insertCupboard(self,cupboardId,doorStatus,knownTheme,defaultTime,repEvery,lastLearn, shelfData,cupCtrolData):
        # create a Cupboard
        self.Cupboard_collection.insert_one({"_id" : cupboardId , "door_status" : doorStatus, "known_theme" : knownTheme , "default_time" : defaultTime , "rep_every" : repEvery , "last_leran" : lastLearn})
        # now create and the shelves of the cupboard
        for shelf in shelfData:
            vertical_order = shelf["vertical_order"]
            height = shelf["height"]
            length = shelf["length"]
            ShelfObjId = self.insertShelf(verticalOrder=vertical_order,length=length,height=height,cupboardId=cupboardId)
            
            # now create an empty Slot with start=0 and length = length of Shelf
            self.insertSlot(startPos=0,endPos=length,shelfObjId=ShelfObjId, currentItemId="empty") 
        
        # now create a cupboard controller for the cupboard 
        self.insertCupboard_controller(cupboardId,cupCtrolData["IP"],cupCtrolData["server_port"],cupCtrolData["camera_IP"],cupCtrolData["arduino1Port"],cupCtrolData["arduino2Port"])


    def insertCupboard_controller(self,id,IP,server_port,camera_IP,arduino1Port,arduino2Port):
        self.Cupboard_controller_collection.insert_one({"_id" : id, "IP" : IP, "server_port" : server_port, "camera_IP" : camera_IP , "arduino1Port" : arduino1Port, "arduino2Port" : arduino2Port})

    def insertKnownItem(self,categ,name,original_weight,imagePath,expectedExpiring):
        self.Well_known_items_collection.insert_one({"categ" : categ , "name" : name , "orig_weight" : original_weight , "image" : imagePath , "exp_expiring_days" : expectedExpiring})
        
    def insertKnownTheme(self,name,icon):
        self.Well_known_theme_collection.insert_one({"_id" : name , "icon" : icon })

    def insertUserAccess(self,username,cupIdsList):
        self.Users_permissions_collection.insert_one({"_id" : username , "permission" : cupIdsList})


    def setAccess(self,username,cupboardId):
        self.Users_permissions_collection.find_one_and_update({"_id" : username} , {'$push' : {'permission' : cupboardId}})

    def removeAccess(self,username,cupboardId):
        self.Users_permissions_collection.find_one_and_update({"_id" : username} , {'$pull' : {'permission' : cupboardId}})

    def getAllcupboardsIPs(self):
        return list(self.Cupboard_controller_collection.find({} , {"_id" : 0 , "IP" : 1}))

    def storeItemsAfterTrain(self,trainData):

        cupboard_id = trainData["Cupboard"]        
    
        # delete all items of cupboard with id = cupboard_id
        self.Current_item_collection.delete_many({"cupboard_id" : cupboard_id})
        
        # delete - reset all empty slots of cupboard with id = cupboard_id
        self.Slot_collection.delete_many({"cupboard_id" : cupboard_id})

        for shelf in trainData["Shelf"]:
            vertical_order = shelf["vertical_order"]
            shelfObjId = self.getShelfObjIdByCupIdandVerOrder(cupboard_id,vertical_order)

            # delete all documents Slots of a Shelf to insert the updated ones
            self.Slot_collection.delete_many({"shelf_id" : shelfObjId})

            for slot in shelf["Slots"]:
                if slot["item"] == "empty" : # if it is an empty slot
                    self.insertSlot(slot["start"] , slot["end"] , shelfObjId, "empty")
                else:
                    # inserting Item will insert the corresponding Slot
                    self.insertCurrentItem(slot["start"],slot["end"],slot["item"]["quantity"],shelfObjId,slot["item"]["expiring_date"],slot["item"]["last_user_id"],slot["item"]["name"],cupboard_id) 

    def updateCupboardTheme(self,cupboardId,themeToSet):
        self.Cupboard_collection.find_one_and_update({"_id" : cupboardId} , {"$set" : {"known_theme" : themeToSet}})

    def getCupboardAllItems(self,cupboardId):
        
        allItems =  list(self.Current_item_collection.find({"cupboard_id" : cupboardId}))
        allItemsAugemented = []

        for item in allItems:
            item["original_weight"] = self.getOriginalWeight(item["Well_known_item_id"])
            item["vertical_order"] = self.getShelfVerOrderBySlotObjId(item["slot_id"])
            item["daysToExpire"] = self.getDaysToExpire(cupboardId,item["_id"]) # fixed bug
            
            item.pop("slot_id") # remove the field slot_id
            item.pop("_id") # remove the field _id
            
            allItemsAugemented.append(item)

        return allItemsAugemented

    def getItemsQuantityOfCupboardByItemName(self,cupboardId,itemToSearch):
        return list(self.Current_item_collection.find({"cupboard_id" : cupboardId , "Well_known_item_id" : itemToSearch} , {"quantity" : 1 }))

    def getCupboardItemsByShelfId(self,cupboardId,verticalOrder):
        shelfObjId = self.getShelfObjIdByCupIdandVerOrder(cupboardId,verticalOrder)

        cupboardItemsByShelf = [] # initialize

        cupboardItems = self.getCupboardAllItems(cupboardId)    
        
        for item in cupboardItems:
            SlotObjId = item["slot_id"]    
            slot_json = self.Slot_collection.find_one({"_id" :SlotObjId})
            if slot_json["shelf_id"] == shelfObjId:
                cupboardItemsByShelf.append(item)

        return cupboardItemsByShelf

    def getItemsQuantityOfInventoryByItemName(self,itemToSearch):
        return list(self.Current_item_collection.find({"Well_known_item_id" : itemToSearch} , {"quantity" : 1 }))

    def getInventoryAllItems(self):
        return list(self.Current_item_collection.find({}))
    
    def getCupsWithIngredient(self,itemToSearch):
        cupboardsWithIngredient = []
        items = self.Current_item_collection.find({"Well_known_item_id" : itemToSearch} , {"cupboard_id" : 1}) # cursor

        for item in items:
            cupboardsWithIngredient.append(item["cupboard_id"])

        return list(set(cupboardsWithIngredient))

    def getOriginalWeight(self,item):
        return  self.Well_known_items_collection.find_one({"name" : item} , {"_id" : 0 ,"orig_weight" : 1})["orig_weight"]

    def getControllerIPByCupId(self,cupId):
        return self.Cupboard_controller_collection.find_one({"_id" : cupId} )["IP"]

    def getEmptySlotsOfShelf(self,shelfObjId):
        emptySlotsPositions = list(self.Slot_collection.find({"shelf_id" : shelfObjId , "current_item_id" : "empty"} , {"start" : 1 , "end" : 1 , "_id" : 0}))
        return emptySlotsPositions # list

    def getAvailableCupboards(self , specificCupId = None):
        availableCupboardsList = []
        availableShelvesList = []
        availableCupsData = {}
        availableShelvesData = {}        
        
        if specificCupId == None : # inventory
            cupboards = self.Cupboard_collection.find({})
        else:
            cupboards = self.Cupboard_collection.find({"_id" : specificCupId})

        for cupboard in cupboards:
            cupId = cupboard["_id"]
            shelves = self.Shelf_collection.find({"cupboard_id" : cupId})

            for shelf in shelves :
                verticalOrder = shelf["vertical_order"]

                shelfObjId = self.getShelfObjIdByCupIdandVerOrder(cupId,verticalOrder)
                emptySlotsPositions = self.getEmptySlotsOfShelf(shelfObjId) #list

                if emptySlotsPositions : # if there are empty slots
                    availableShelvesData["vertical_order"] = verticalOrder
                    availableShelvesData["Slots"] = emptySlotsPositions

                    availableShelvesList.append(availableShelvesData)
                    availableShelvesData = {} # reset
            
            if availableShelvesList: # if there is at least one available shelf
                availableCupsData["id"] = cupId 
                availableCupsData["Shelves"] = availableShelvesList
                availableCupboardsList.append(availableCupsData)
                availableCupsData = {} # reset
            
            availableShelvesList = [] # reset 

        return availableCupboardsList
    
    def getCupboardsThemes(self):

        return list(self.Cupboard_collection.find({},{"_id" : 1 , "known_theme" : 1 }))

    def getItemInfoInCupboard(self,cupboardId,item):
        
        augmentedItemInfo = []
        itemInfo = list(self.Current_item_collection.find({"cupboard_id" : cupboardId , "Well_known_item_id" : item}))
        for item in itemInfo:
            item["slot_start"] = self.getSlotStart(item["slot_id"])
            item["slot_end"] = self.getSlotEnd(item["slot_id"])
            item["daysToExpire"] = self.getDaysToExpire(cupboardId,item["_id"]) # fixed bug
            item["original_weight"] = self.getOriginalWeight(item["Well_known_item_id"])
            augmentedItemInfo.append(item)

        return augmentedItemInfo 

    # get the vertical order of a shelf by the obj id of the slot
    def getShelfVerOrderBySlotObjId(self,slotObjId):
        shelfObjId = self.Slot_collection.find_one({"_id" : slotObjId} , {"shelf_id" : 1})["shelf_id"]
        return self.Shelf_collection.find_one({"_id" : shelfObjId} , {"vertical_order" : 1})["vertical_order"]

    # get daysToExpire of an item in a cupboard
    def getDaysToExpire(self,cupboardId,itemID):
        expiringDate = self.Current_item_collection.find_one({"cupboard_id" : cupboardId , "_id" : itemID} , {"expiring_date" : 1})["expiring_date"]
        expiringDate = datetime.strptime(expiringDate, '%d/%m/%y')
        
        return (expiringDate - datetime.today()).days + 1
    
    def getSlotStart(self,slotObjId):
        return self.Slot_collection.find_one({"_id" : slotObjId} , {"start" : 1})["start"]
    
    def getSlotEnd(self,slotObjId):
        return self.Slot_collection.find_one({"_id" : slotObjId} , {"end" : 1})["end"]

    