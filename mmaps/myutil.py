
# ========================================================================================
def getRoundDigit(val):
    if not isinstance(val, float):
        return 0

    integer, dicimal = str(val).split('.')
    if not integer == '0':
        return 1
    else:
        round_digit = 1
        for i in range(len(dicimal)):
            if dicimal[i] == '0':
                round_digit += 1
            else:
                return round_digit
