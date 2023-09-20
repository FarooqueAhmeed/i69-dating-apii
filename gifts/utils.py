from gifts.models import RealGift, VirtualGift


def get_gift(self, info):
    try:
        if self.type == "real":
            return RealGift.objects.filter(allgift__id=self.id).first()
        elif self.type == "virtual":
            return VirtualGift.objects.filter(allgift__id=self.id).first()
        else:
            return None
    except Exception as e:
        print(e)
        return None
