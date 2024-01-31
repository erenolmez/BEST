import struct

MESSAGE_HEAD = "55"
ACTIVE_REPORT = "04"
FALL_REPORT = "06"

REPORT_RADAR = "03"
REPORT_OTHER = "05"

HEARTBEAT = "01"
ABNORMAL = "02"
ENVIRONMENT = "05"
BODYSIGN = "06"
CLOSE_AWAY = "07"

CA_BE = "01"
CA_CLOSE = "02"
CA_AWAY = "03"
SOMEBODY_BE = "01"
SOMEBODY_MOVE = "01"
SOMEBODY_STOP = "00"
NOBODY = "00"


class RADAR:
    def Bodysign_val(ad1, ad2, ad3, ad4, ad5):
        if ad1 == BODYSIGN:
            byte_array = bytearray([int(ad2), int(ad3), int(ad4), int(ad5)])
            float_value = struct.unpack('f', byte_array)[0]
            return float_value
        else:
            return 0


    def Situation_judgment(ad1, ad2, ad3, ad4, ad5):
        result = 0
        if ad1 == REPORT_RADAR or ad1 == REPORT_OTHER:
            if ad2 == ENVIRONMENT or ad2 == HEARTBEAT:
                if ad3 == NOBODY:
                    result = 1
                elif ad3 == SOMEBODY_BE and ad4 == SOMEBODY_MOVE:
                    result = 2
                elif ad3 == SOMEBODY_BE and ad4 == SOMEBODY_STOP:
                    result = 3
                    
            elif ad2 == CLOSE_AWAY:
                if ad3 == CA_BE and ad4 == CA_BE:
                    if ad5 == CA_BE:
                        result = 4
                    elif ad5 == CA_CLOSE:
                        result = 5
                    elif ad5 == CA_AWAY:
                        result = 6
                        
        return result
    
    def Fall_judgment(ad1, ad2, ad3, ad4):
        result = 0
        if ad1 == FALL_REPORT and ad2 == "01":
            if ad3 == "01":
                if ad4 == "00":
                    result = 1
                elif ad4 == "01":
                    result = 2
                elif ad4 == "02":
                    result = 3
                    
            elif ad3 == "02":
                if ad4 == "00":
                    result = 4
                elif ad4 == "01":
                    result = 5
                elif ad4 == "02":
                    result = 6
                elif ad4 == "03":
                    result = 7
                elif ad4 == "04":
                    result = 8

        return result