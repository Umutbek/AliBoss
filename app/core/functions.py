from core import models, firestore


def create_order_in_firebase(saved_data):

    item_list =[]

    for i in saved_data.items.all():
        item_list.append(
            {
                'item': {
                    'name': i.item.name, 'description': i.item.description,
                    'category': str(i.item.category), 'subcategory': str(i.item.subcategory),
                    'subsubcategory': str(i.item.subsubcategory), 'cost': i.item.cost,
                    'costSale': i.item.costSale, 'issale': i.item.issale,
                    'supplier': i.item.supplier.id, 'uniqueid': i.item.uniqueid,
                    'imagelink': i.item.imagelink, 'image': str(i.item.image),
                    'phone': i.item.phone, 'instagram': i.item.instagram,
                    'facebook': i.item.facebook,'whatsapp': i.item.whatsapp,
                    'web': i.item.web,
                },
                'quantity': i.quantity
            }
        )

    data = {
        u'id': saved_data.id, u'store': saved_data.store, u'totalCost': saved_data.totalCost,
        u'user': saved_data.user, u'address': saved_data.address, u'phone': saved_data.phone, u'items': item_list,
        u'lat': saved_data.lat, u'lon': saved_data.lon, u'comment': saved_data.comment, u'storeName': saved_data.storeName,
        u'storeLogo': saved_data.storeLogo, u'status': saved_data.status, u'date': saved_data.date,
        u'bonus': saved_data.bonus, u'pay_status': saved_data.pay_status, u'isoptovik': saved_data.isoptovik
    }

    firestore.db.collection(u'orders').document(
        str(saved_data.id)).set(data)


def create_notification_in_fire_base(saved_data):
    data = {
        u'id': saved_data.id, u'title': saved_data.title, u'desc': saved_data.desc, u'itemId': saved_data.itemId
    }
    firestore.db.collection(u'notification').document(saved_data.id).set(data)


