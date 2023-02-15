import shortuuid

def get_referral_code():
    code = shortuuid.ShortUUID().random(length=6)
    invite_code = 'HM-' + code
    return invite_code
