from Core.Config.ConfigGetter import get_config_value
from Core.DTO.ItemDTO import ItemDTO
from TelegramBundle.Api import TelegramApi


def compare(stocks, items):
    blacklist = get_config_value("blacklist")
    for item in items:
        try:
            old_stock = [stock.amount for stock in stocks if stock.id == item.id][0]
        except IndexError:
            old_stock = 0

        new_stock = item.amount

        # Send only when stock has changed
        if new_stock != old_stock:

            # New item returned from API
            if old_stock == 0 and new_stock > 0:
                if not any(x in item.name for x in blacklist):
                    TelegramApi.send(get_item_message(item, new_stock))

            # Items stock decreased by customers
            elif old_stock > new_stock != 0:
                pass

            # Item sold out
            elif old_stock > new_stock == 0:
                if not any(x in item.name for x in blacklist):
                    TelegramApi.send(get_sold_out_message(item))

            # Other stock changes
            else:
                if not any(x in item.name for x in blacklist):
                    TelegramApi.send(get_stock_change_message(item, old_stock, new_stock))


def get_item_message(item: ItemDTO, new_stock):
    message = f"🍽 [{item.name}]({item.url})\n"
    message += f"📍 {item.address}\n"
    message += f"💰 {item.current_price}PLN/{item.old_price}PLN\n"
    message += f"🫱 {new_stock}\n"
    if item.ratings is not None:
        message += f"⭐️ {item.ratings}/5\n"
    if item.pick_up_from is not None and item.pick_up_to is not None:
        message += f"⏰ {item.pick_up_from}-{item.pick_up_to}\n"
    message += f"💡 {item.other_details}\n"
    message += "ℹ️ TooGoodToGo"
    return message


def get_sold_out_message(item: ItemDTO):
    return f" ⭕ Sold out: {item.name}."


def get_stock_change_message(item: ItemDTO, old_stock, new_stock):
    return f"There was a change of number of goodie bags in stock from {old_stock} to {new_stock} at {item.name}."
