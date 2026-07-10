CUISINE_IMAGES = {
    "North Indian": "https://images.unsplash.com/photo-1585937421612-70a008356fbe",
    "South Indian": "https://images.unsplash.com/photo-1631452180519-c014fe946bc7",
    "Chinese": "https://images.unsplash.com/photo-1563245372-f21724e3856d",
    "Italian": "https://images.unsplash.com/photo-1513104890138-7c749659a591",
    "Pizza": "https://images.unsplash.com/photo-1513104890138-7c749659a591",
    "Burger": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd",
    "Cafe": "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085",
    "Desserts": "https://images.unsplash.com/photo-1563805042-7684c019e1cb",
    "Biryani": "https://images.unsplash.com/photo-1563379091339-03246963d29a",
    "Seafood": "https://images.unsplash.com/photo-1559847844-5315695dadae"
}

DEFAULT_IMAGE = "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4"


def get_restaurant_image(cuisine):

    cuisine = cuisine.lower()

    for key, url in CUISINE_IMAGES.items():
        if key.lower() in cuisine:
            return url

    return DEFAULT_IMAGE