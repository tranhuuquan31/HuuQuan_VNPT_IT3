from datetime import datetime

def sample_response(input):
    user_message= str(input).lower()
    if user_message in ("/hello", "/hi","/xin chào", "/chào"):
        return "Chào anh đẹp trai <3 <3 "
    if user_message in ("/bạn là ai", "/who are you", "/tên của bạn", '/bạn tên gì'):
        return "Dạ, em là bot của Quân, em có thể cho biết ngày giờ nè"
    if user_message in ("/time", "/time?"):
        now = "Hôm nay là: " + datetime.now().strftime("%d-%m-%y, %H:%M:%S")
        return str(now) 
    return "Em còn non lắm, đừng làm khó em hổng hiểu đâuuuu" 

    
    